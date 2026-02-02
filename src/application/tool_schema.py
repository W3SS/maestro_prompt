from typing import List, Optional
from pydantic import BaseModel, Field

class DesignAlbumInput(BaseModel):
    """Input for designing an album."""
    archetype: str = Field(..., description="Album archetype (e.g., 'concept_album', 'compilation')")
    genres: List[str] = Field(..., description="List of musical genres")
    theme: Optional[str] = Field(None, description="Optional album theme")

class DesignAlbumOutput(BaseModel):
    """Output from designing an album."""
    album_id: Optional[str] = Field(None, description="Generated Album ID (internal)")
    title: str = Field(..., description="Album title")
    tracks: List[dict] = Field(..., description="List of generated tracks")
    # We can expand this with more fields from AlbumDTO

class CreateBatchInput(BaseModel):
    """Input for creating a batch."""
    name: str = Field(..., description="Batch name")

class CreateBatchOutput(BaseModel):
    """Output from creating a batch."""
    batch_id: str = Field(..., description="Batch ID")
    status: str = Field(..., description="Initial status")

class AddItemsInput(BaseModel):
    """Input for adding items to batch."""
    batch_id: str = Field(..., description="Batch ID")
    items: List[dict] = Field(..., description="List of items (prompt, style_tags, title)")

class StartBatchInput(BaseModel):
    """Input for starting a batch."""
    batch_id: str = Field(..., description="Batch ID")

class AddItemsOutput(BaseModel):
    """Output from adding items to batch."""
    batch_id: str = Field(..., description="Batch ID")
    items_count: int = Field(..., description="Total number of items in batch")
    status: str = Field(..., description="Batch status")

class GetBatchInput(BaseModel):
    """Input for getting a batch."""
    batch_id: str = Field(..., description="Batch ID")

class GetBatchOutput(BaseModel):
    """Output from getting a batch."""
    batch_id: str = Field(..., description="Batch ID")
    name: str = Field(..., description="Batch name")
    status: str = Field(..., description="Batch status")
    items_count: int = Field(..., description="Number of items")
    created_at: str = Field(..., description="Creation timestamp")

class ListBatchesInput(BaseModel):
    """Input for listing batches."""
    status: Optional[str] = Field(None, description="Filter by status (pending/processing/completed)")

class ListBatchesOutput(BaseModel):
    """Output from listing batches."""
    batches: List[dict] = Field(..., description="List of batch summaries")
    total: int = Field(..., description="Total number of batches")

class CompleteBatchInput(BaseModel):
    """Input for completing a batch."""
    batch_id: str = Field(..., description="Batch ID")

class CompleteBatchOutput(BaseModel):
    """Output from completing a batch."""
    batch_id: str = Field(..., description="Batch ID")
    status: str = Field(..., description="Updated status")
    completed_at: str = Field(..., description="Completion timestamp")

class CancelBatchInput(BaseModel):
    """Input for canceling a batch."""
    batch_id: str = Field(..., description="Batch ID")

class CancelBatchOutput(BaseModel):
    """Output from canceling a batch."""
    batch_id: str = Field(..., description="Batch ID")
    status: str = Field(..., description="Updated status (cancelled)")
