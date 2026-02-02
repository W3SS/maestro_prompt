from typing import Any, Dict
from src.infrastructure.di.container import get_container
from src.application.tool_schema import (
    DesignAlbumInput, DesignAlbumOutput, 
    CreateBatchInput, CreateBatchOutput,
    AddItemsInput, AddItemsOutput,
    StartBatchInput,
    GetBatchInput, GetBatchOutput,
    ListBatchesInput, ListBatchesOutput,
    CompleteBatchInput, CompleteBatchOutput,
    CancelBatchInput, CancelBatchOutput
)

class MaestroTools:
    """
    Universal Tool Registry.
    
    Acts as a Bridge between the raw Application Services and external interfaces (API, MCP, UTCP).
    Handles dependencies resolution via Container.
    """
    
    @staticmethod
    async def design_album(input_data: DesignAlbumInput) -> DesignAlbumOutput:
        """Use AI to design a concept album with tracks and lyrics."""
        container = get_container()
        designer = container.album_designer()
        
        # Run async method directly (propagating async)
        album = await designer.design_album(
            archetype=input_data.archetype,
            genres=input_data.genres,
            num_tracks=8
        )
        
        return DesignAlbumOutput(
            title=album.title,
            tracks=[
                {
                    "title": t.title,
                    "lyrics": t.lyrics,
                    "style_tags": t.style_tags,
                    "duration": t.duration_estimate
                }
                for t in album.tracks
            ]
        )


    @staticmethod
    async def create_batch(input_data: CreateBatchInput) -> CreateBatchOutput:
        """Create a new Suno generation batch."""
        container = get_container()
        manager = container.batch_manager()
        
        batch_dto = await manager.create_batch(name=input_data.name)
        
        return CreateBatchOutput(
            batch_id=batch_dto.id,
            status=batch_dto.status
        )
        
    @staticmethod
    async def start_batch(input_data: StartBatchInput) -> Dict[str, Any]:
        """Start processing a batch."""
        container = get_container()
        manager = container.batch_manager()
        
        batch_dto = await manager.start_batch(input_data.batch_id)
        
        return {
            "batch_id": batch_dto.id,
            "status": batch_dto.status,
            "message": "Batch started successfully"
        }

    @staticmethod
    async def add_items_to_batch(input_data: AddItemsInput) -> AddItemsOutput:
        """Add items to an existing batch."""
        container = get_container()
        manager = container.batch_manager()
        
        batch_dto = await manager.add_items(input_data.batch_id, input_data.items)
        
        return AddItemsOutput(
            batch_id=batch_dto.id,
            items_count=len(batch_dto.items),
            status=batch_dto.status
        )
    
    @staticmethod
    async def get_batch(input_data: GetBatchInput) -> GetBatchOutput:
        """Get batch details by ID."""
        container = get_container()
        manager = container.batch_manager()
        
        batch_dto = await manager.get_batch(input_data.batch_id)
        
        return GetBatchOutput(
            batch_id=batch_dto.id,
            name=batch_dto.name,
            status=batch_dto.status,
            items_count=len(batch_dto.items),
            created_at=batch_dto.created_at.isoformat()
        )
    
    @staticmethod
    async def list_batches(input_data: ListBatchesInput) -> ListBatchesOutput:
        """List all batches, optionally filtered by status."""
        container = get_container()
        manager = container.batch_manager()
        
        batches_dto = await manager.list_batches(status=input_data.status)
        
        batches = [
            {
                "batch_id": b.id,
                "name": b.name,
                "status": b.status,
                "items_count": len(b.items),
                "created_at": b.created_at.isoformat()
            }
            for b in batches_dto
        ]
        
        return ListBatchesOutput(
            batches=batches,
            total=len(batches)
        )
    
    @staticmethod
    async def complete_batch(input_data: CompleteBatchInput) -> CompleteBatchOutput:
        """Mark batch as completed."""
        container = get_container()
        manager = container.batch_manager()
        
        batch_dto = await manager.complete_batch(input_data.batch_id)
        
        return CompleteBatchOutput(
            batch_id=batch_dto.id,
            status=batch_dto.status,
            completed_at=batch_dto.completed_at.isoformat()
        )
    
    @staticmethod
    async def cancel_batch(input_data: CancelBatchInput) -> CancelBatchOutput:
        """Cancel a batch."""
        container = get_container()
        manager = container.batch_manager()
        
        batch_dto = await manager.cancel_batch(input_data.batch_id)
        
        return CancelBatchOutput(
            batch_id=batch_dto.id,
            status=batch_dto.status
        )
