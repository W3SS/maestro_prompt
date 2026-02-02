"""Unit tests for BatchManager service."""

import pytest
import asyncio
from unittest.mock import AsyncMock

from src.application.services.batch_manager import BatchManager
from src.domain.exceptions.domain_errors import InvalidBatchError

pytestmark = pytest.mark.asyncio

class TestBatchManager:
    """Test BatchManager service."""
    
    @pytest.fixture
    def service(self):
        """Create service instance."""
        return BatchManager()
    
    async def test_create_batch(self, service):
        """Should create a new batch."""
        batch_dto = await service.create_batch("Test Batch")
        
        assert batch_dto.name == "Test Batch"
        assert batch_dto.status == "pending"
        assert batch_dto.id is not None
        assert len(batch_dto.items) == 0
    
    async def test_add_items_to_batch(self, service):
        """Should add items to batch."""
        batch_dto = await service.create_batch("Test")
        
        items = [
            {"prompt": "Song 1", "style_tags": ["metal"], "title": "Track 1"},
            {"prompt": "Song 2", "style_tags": ["jazz"], "title": "Track 2"}
        ]
        
        updated_dto = await service.add_items(batch_dto.id, items)
        
        assert len(updated_dto.items) == 2
        assert updated_dto.items[0].title == "Track 1"
        assert updated_dto.items[1].title == "Track 2"
    
    async def test_cannot_add_items_to_nonexistent_batch(self, service):
        """Should raise error for invalid batch ID."""
        with pytest.raises(KeyError):
            await service.add_items("nonexistent-id", [{"prompt": "Test", "style_tags": ["metal"]}])
    
    async def test_start_batch(self, service):
        """Should transition batch to processing."""
        batch_dto = await service.create_batch("Test")
        
        updated_dto = await service.start_batch(batch_dto.id)
        
        assert updated_dto.status == "processing"
    
    async def test_complete_batch(self, service):
        """Should mark batch as completed."""
        batch_dto = await service.create_batch("Test")
        await service.start_batch(batch_dto.id)
        
        updated_dto = await service.complete_batch(batch_dto.id)
        
        assert updated_dto.status == "completed"
        assert updated_dto.completed_at is not None
    
    async def test_fail_batch(self, service):
        """Should mark batch as failed."""
        batch_dto = await service.create_batch("Test")
        await service.start_batch(batch_dto.id)
        
        updated_dto = await service.fail_batch(batch_dto.id)
        
        assert updated_dto.status == "failed"
        assert updated_dto.completed_at is not None
    
    async def test_cancel_batch(self, service):
        """Should cancel batch."""
        batch_dto = await service.create_batch("Test")
        await service.start_batch(batch_dto.id)
        
        updated_dto = await service.cancel_batch(batch_dto.id)
        
        assert updated_dto.status == "cancelled"
        assert updated_dto.completed_at is not None
    
    async def test_get_batch(self, service):
        """Should retrieve batch by ID."""
        batch_dto = await service.create_batch("Test")
        
        retrieved_dto = await service.get_batch(batch_dto.id)
        
        assert retrieved_dto.id == batch_dto.id
        assert retrieved_dto.name == "Test"
    
    async def test_get_nonexistent_batch_raises_error(self, service):
        """Should raise error for invalid batch ID."""
        with pytest.raises(KeyError):
            await service.get_batch("nonexistent-id")
    
    async def test_list_all_batches(self, service):
        """Should list all batches."""
        await service.create_batch("Batch 1")
        await service.create_batch("Batch 2")
        await service.create_batch("Batch 3")
        
        batches = await service.list_batches()
        
        assert len(batches) == 3
    
    async def test_list_batches_filtered_by_status(self, service):
        """Should filter batches by status."""
        batch1_dto = await service.create_batch("Batch 1")
        batch2_dto = await service.create_batch("Batch 2")
        await service.create_batch("Batch 3")
        
        await service.start_batch(batch1_dto.id)
        await service.start_batch(batch2_dto.id)
        
        processing_batches = await service.list_batches(status="processing")
        
        assert len(processing_batches) == 2
        assert all(b.status == "processing" for b in processing_batches)
    
    async def test_update_item_status(self, service):
        """Should update item status."""
        batch_dto = await service.create_batch("Test")
        items = [{"prompt": "Song 1", "style_tags": ["metal"]}]
        await service.add_items(batch_dto.id, items)
        
        updated_dto = await service.update_item_status(
            batch_dto.id,
            0,
            "completed",
            suno_id="suno-123",
            audio_url="https://example.com/audio.mp3"
        )
        
        assert updated_dto.items[0].status == "completed"
        assert updated_dto.items[0].suno_id == "suno-123"
        assert updated_dto.items[0].audio_url == "https://example.com/audio.mp3"
    
    async def test_update_item_with_invalid_index_raises_error(self, service):
        """Should raise error for invalid item index."""
        batch_dto = await service.create_batch("Test")
        
        with pytest.raises(IndexError):
            await service.update_item_status(batch_dto.id, 99, "completed")
    
    async def test_cannot_add_items_to_processing_batch(self, service):
        """Should enforce domain rules via exceptions."""
        batch_dto = await service.create_batch("Test")
        await service.start_batch(batch_dto.id)
        
        with pytest.raises(InvalidBatchError):
            await service.add_items(batch_dto.id, [{"prompt": "Test", "style_tags": ["metal"]}])
