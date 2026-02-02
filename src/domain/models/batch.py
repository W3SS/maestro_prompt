"""Domain model for Suno batch management."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

from src.domain.exceptions.domain_errors import InvalidBatchError


class BatchStatus(str, Enum):
    """Status of a Suno batch."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class BatchItem:
    """Individual item in a Suno batch."""
    prompt: str
    style_tags: List[str]
    title: str = ""
    status: str = "pending"
    suno_id: Optional[str] = None
    audio_url: Optional[str] = None
    
    def __post_init__(self):
        """Validate batch item."""
        if not self.prompt or not self.prompt.strip():
            raise InvalidBatchError("Batch item prompt cannot be empty")
        
        if not isinstance(self.style_tags, list):
             raise InvalidBatchError("Batch item style_tags must be a list of strings")
             
        if not self.style_tags:
             # It is allowed to be empty contextually? Maybe. 
             # But previous logic checked for 'not empty strip'.
             # Let's assume at least one tag is needed or relax it.
             # "Cannot be empty" suggests required.
             raise InvalidBatchError("Batch item style_tags cannot be empty")


@dataclass
class Batch:
    """Batch entity for Suno queue management."""
    name: str
    items: List[BatchItem] = field(default_factory=list)
    status: BatchStatus = BatchStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate batch data."""
        if not self.id:
            import uuid
            self.id = str(uuid.uuid4())

        if not self.name or not self.name.strip():
            raise InvalidBatchError("Batch name cannot be empty")
        
        if not isinstance(self.items, list):
            raise InvalidBatchError("Batch items must be a list")
        
        # Validate status
        if not isinstance(self.status, BatchStatus):
            try:
                self.status = BatchStatus(self.status)
            except ValueError:
                raise InvalidBatchError(
                    f"Invalid batch status: {self.status}. "
                    f"Must be one of {[s.value for s in BatchStatus]}"
                )
    
    def add_item(self, item: BatchItem) -> None:
        """Add an item to the batch."""
        if not isinstance(item, BatchItem):
            raise InvalidBatchError("Must provide a valid BatchItem object")
        
        if self.status != BatchStatus.PENDING:
            raise InvalidBatchError(
                f"Cannot add items to batch with status {self.status.value}"
            )
        
        self.items.append(item)
    
    def start_processing(self) -> None:
        """Mark batch as processing."""
        if self.status != BatchStatus.PENDING:
            raise InvalidBatchError(
                f"Cannot start batch with status {self.status.value}"
            )
        self.status = BatchStatus.PROCESSING
    
    def complete(self) -> None:
        """Mark batch as completed."""
        if self.status != BatchStatus.PROCESSING:
            raise InvalidBatchError(
                f"Cannot complete batch with status {self.status.value}"
            )
        self.status = BatchStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def fail(self) -> None:
        """Mark batch as failed."""
        if self.status == BatchStatus.COMPLETED:
            raise InvalidBatchError("Cannot fail an already completed batch")
        self.status = BatchStatus.FAILED
        self.completed_at = datetime.now()
    
    def cancel(self) -> None:
        """Cancel the batch."""
        if self.status in [BatchStatus.COMPLETED, BatchStatus.FAILED]:
            raise InvalidBatchError(
                f"Cannot cancel batch with status {self.status.value}"
            )
        self.status = BatchStatus.CANCELLED
        self.completed_at = datetime.now()
    
    def get_item_count(self) -> int:
        """Get the number of items in the batch."""
        return len(self.items)
    
    def get_completed_count(self) -> int:
        """Get number of completed items."""
        return sum(1 for item in self.items if item.status == "completed")
    
    def get_progress_percentage(self) -> float:
        """Get batch completion percentage."""
        if not self.items:
            return 0.0
        return (self.get_completed_count() / len(self.items)) * 100
    
    def __str__(self) -> str:
        """String representation."""
        return (
            f"Batch('{self.name}', {self.status.value}, "
            f"{len(self.items)} items, {self.get_progress_percentage():.1f}% done)"
        )
