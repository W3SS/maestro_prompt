import json
import os
from typing import List, Optional, Dict, Any
from src.ports.output.batch_repository import IBatchRepository
from src.domain.models.batch import Batch


class JsonFileRepository(IBatchRepository):
    """
    Implementation of IBatchRepository that persists data to a JSON file.
    This is simple and effective for local deployment.
    """

    def __init__(self, data_file: str = "data/batches.json"):
        self.data_file = data_file
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Ensure the data file and directory exist."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def _load_data(self) -> Dict[str, Any]:
        """Load data from JSON file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_data(self, data: Dict[str, Any]) -> None:
        """Save data to JSON file."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, default=str)

    async def save(self, batch: Batch) -> None:
        """Save or update a batch."""
        import asyncio
        data = await asyncio.to_thread(self._load_data)
        
        # Convert to dataclass dict
        from dataclasses import asdict
        batch_dict = asdict(batch)
        # Handle Enum and datetime
        if batch.created_at: 
            batch_dict['created_at'] = batch.created_at.isoformat()
        if batch.completed_at:
            batch_dict['completed_at'] = batch.completed_at.isoformat()
        if batch.status:
            batch_dict['status'] = batch.status.value
        
        # Items handling
        items_data = []
        for item in batch.items:
             items_data.append(asdict(item))
        batch_dict['items'] = items_data

        data[batch.id] = batch_dict
        await asyncio.to_thread(self._save_data, data)

    async def get(self, batch_id: str) -> Optional[Batch]:
        """Get a batch by ID."""
        import asyncio
        data = await asyncio.to_thread(self._load_data)
        batch_data = data.get(batch_id)
        if batch_data:
            return self._reconstruct_batch(batch_data)
        return None

    async def list_all(self) -> List[Batch]:
        """List all batches."""
        import asyncio
        data = await asyncio.to_thread(self._load_data)
        return [self._reconstruct_batch(batch_data) for batch_data in data.values()]

    async def update(self, batch: Batch) -> None:
        """Update a batch (same as save)."""
        await self.save(batch)

    async def delete(self, batch_id: str) -> None:
        """Delete a batch by ID."""
        import asyncio
        data = await asyncio.to_thread(self._load_data)
        if batch_id in data:
            del data[batch_id]
            await asyncio.to_thread(self._save_data, data)

    def _reconstruct_batch(self, data: Dict[str, Any]) -> Batch:
        from src.domain.models.batch import BatchItem, BatchStatus
        from datetime import datetime
        
        items = [BatchItem(**i) for i in data.get('items', [])]
        
        # Parse datetimes
        created_at = data.get('created_at')
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
            
        completed_at = data.get('completed_at')
        if isinstance(completed_at, str):
            completed_at = datetime.fromisoformat(completed_at)
            
        return Batch(
            name=data['name'],
            id=data['id'],
            items=items,
            status=data['status'],
            created_at=created_at,
            completed_at=completed_at,
            metadata=data.get('metadata', {})
        )
