from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.batch import Batch


class IBatchRepository(ABC):
    """Interface for Batch Repository (Port)."""

    @abstractmethod
    async def save(self, batch: Batch) -> None:
        """Save or update a batch."""
        pass

    @abstractmethod
    async def get(self, batch_id: str) -> Optional[Batch]:
        """Get a batch by ID."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Batch]:
        """List all batches."""
        pass

    @abstractmethod
    async def update(self, batch: Batch) -> None:
        """Update a batch."""
        pass

    @abstractmethod
    async def delete(self, batch_id: str) -> None:
        """Delete a batch by ID."""
        pass
