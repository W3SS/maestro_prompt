"""Batch Manager Service - manages Suno batch operations."""

from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from src.domain.models.batch import Batch, BatchItem, BatchStatus
from src.application.dto.album_dto import BatchDTO, BatchItemDTO


class BatchManager:
    """
    Application Service for managing Suno batches.
    
    Handles:
    - Batch creation and lifecycle
    - Item management
    - Status transitions
    - Persistence (future: via repository port)
    """
    
    def __init__(self):
        """Initialize the service."""
        self._batches: Dict[str, Batch] = {}
    
    def create_batch(self, name: str) -> BatchDTO:
        """
        Create a new batch.
        
        Args:
            name: Batch name
        
        Returns:
            BatchDTO with generated ID
        """
        batch = Batch(
            name=name,
            id=str(uuid.uuid4())
        )
        
        self._batches[batch.id] = batch
        
        return self._to_dto(batch)
    
    def add_items(self, batch_id: str, items: List[Dict[str, Any]]) -> BatchDTO:
        """
        Add items to a batch.
        
        Args:
            batch_id: Batch ID
            items: List of item data (prompt, style_tags, title)
        
        Returns:
            Updated BatchDTO
        
        Raises:
            KeyError: If batch not found
        """
        batch = self._batches[batch_id]
        
        for item_data in items:
            item = BatchItem(
                prompt=item_data["prompt"],
                style_tags=item_data["style_tags"],
                title=item_data.get("title", "")
            )
            batch.add_item(item)
        
        return self._to_dto(batch)
    
    def start_batch(self, batch_id: str) -> BatchDTO:
        """
        Start processing a batch.
        
        Args:
            batch_id: Batch ID
        
        Returns:
            Updated BatchDTO
        """
        batch = self._batches[batch_id]
        batch.start_processing()
        return self._to_dto(batch)
    
    def complete_batch(self, batch_id: str) -> BatchDTO:
        """
        Mark batch as completed.
        
        Args:
            batch_id: Batch ID
        
        Returns:
            Updated BatchDTO
        """
        batch = self._batches[batch_id]
        batch.complete()
        return self._to_dto(batch)
    
    def fail_batch(self, batch_id: str) -> BatchDTO:
        """
        Mark batch as failed.
        
        Args:
            batch_id: Batch ID
        
        Returns:
            Updated BatchDTO
        """
        batch = self._batches[batch_id]
        batch.fail()
        return self._to_dto(batch)
    
    def cancel_batch(self, batch_id: str) -> BatchDTO:
        """
        Cancel a batch.
        
        Args:
            batch_id: Batch ID
        
        Returns:
            Updated BatchDTO
        """
        batch = self._batches[batch_id]
        batch.cancel()
        return self._to_dto(batch)
    
    def get_batch(self, batch_id: str) -> BatchDTO:
        """
        Get batch by ID.
        
        Args:
            batch_id: Batch ID
        
        Returns:
            BatchDTO
        
        Raises:
            KeyError: If batch not found
        """
        batch = self._batches[batch_id]
        return self._to_dto(batch)
    
    def list_batches(self, status: Optional[str] = None) -> List[BatchDTO]:
        """
        List all batches, optionally filtered by status.
        
        Args:
            status: Optional status filter
        
        Returns:
            List of BatchDTOs
        """
        batches = list(self._batches.values())
        
        if status:
            batches = [b for b in batches if b.status.value == status]
        
        return [self._to_dto(b) for b in batches]
    
    def update_item_status(
        self,
        batch_id: str,
        item_index: int,
        status: str,
        suno_id: Optional[str] = None,
        audio_url: Optional[str] = None
    ) -> BatchDTO:
        """
        Update individual item status.
        
        Args:
            batch_id: Batch ID
            item_index: Item index in batch
            status: New status
            suno_id: Optional Suno ID
            audio_url: Optional audio URL
        
        Returns:
            Updated BatchDTO
        """
        batch = self._batches[batch_id]
        
        if item_index >= len(batch.items):
            raise IndexError(f"Item index {item_index} out of range")
        
        item = batch.items[item_index]
        item.status = status
        
        if suno_id:
            item.suno_id = suno_id
        if audio_url:
            item.audio_url = audio_url
        
        return self._to_dto(batch)
    
    def _to_dto(self, batch: Batch) -> BatchDTO:
        """Convert domain Batch to DTO."""
        return BatchDTO(
            name=batch.name,
            status=batch.status.value,
            items=[
                BatchItemDTO(
                    prompt=item.prompt,
                    style_tags=item.style_tags,
                    title=item.title,
                    status=item.status,
                    suno_id=item.suno_id,
                    audio_url=item.audio_url
                )
                for item in batch.items
            ],
            created_at=batch.created_at,
            completed_at=batch.completed_at,
            id=batch.id,
            metadata=batch.metadata
        )
