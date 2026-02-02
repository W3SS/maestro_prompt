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

    def save(self, batch: Batch) -> None:
        """Save or update a batch."""
        data = self._load_data()
        # Convert to dataclass dict
        # Assuming Batch is a dataclass, we can use asdict or verify if pydantic is used (it is @dataclass)
        # But wait, in domain/models/batch.py it uses @dataclass but imports field. 
        # Using dataclasses.asdict would be safer if not pydantic.
        # But previous code used batch.model_dump(). Let's check if it inherits from BaseModel.
        # It is just @dataclass. So model_dump is not available unless pydantic.dataclasses is used.
        # The file showed: `from dataclasses import dataclass, field`
        # So `model_dump` WILL FAIL. I need to fix this too.
        
        # FIX: Manual serialization helper since it's a standard dataclass
        # Or better: make domain models Pydantic dataclasses or BaseModels. 
        # Given the project uses Pydantic elsewhere, I should probably upgrade the domain model to Pydantic
        # OR implementation a manual to_dict.
        
        # For now, I'll assume I should implementation to_dict here or use dataclasses.asdict
        
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
        self._save_data(data)

    def get(self, batch_id: str) -> Optional[Batch]:
        """Get a batch by ID."""
        data = self._load_data()
        batch_data = data.get(batch_id)
        if batch_data:
            # We need to reconstruct objects from dict. 
            # This logic mimics what Pydantic does.
            return self._reconstruct_batch(batch_data)
        return None

    def list_all(self) -> List[Batch]:
        """List all batches."""
        data = self._load_data()
        return [self._reconstruct_batch(batch_data) for batch_data in data.values()]

    def update(self, batch: Batch) -> None:
        """Update a batch (same as save)."""
        self.save(batch)

    def delete(self, batch_id: str) -> None:
        """Delete a batch by ID."""
        data = self._load_data()
        if batch_id in data:
            del data[batch_id]
            self._save_data(data)

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
            status=data['status'], # Enum handles string in post_init? No, post_init validates.
            # But the constructor expects Enum.
            # Batch post_init handles string conversion? yes
            created_at=created_at,
            completed_at=completed_at,
            metadata=data.get('metadata', {})
        )
