"""Unit tests for BatchManager service."""

import pytest

from src.application.services.batch_manager import BatchManager
from src.domain.exceptions.domain_errors import InvalidBatchError


class TestBatchManager:
    """Test BatchManager service."""
    
    @pytest.fixture
    def service(self):
        """Create service instance."""
        return BatchManager()
    
    def test_create_batch(self, service):
        """Should create a new batch."""
        batch_dto = service.create_batch("Test Batch")
        
        assert batch_dto.name == "Test Batch"
        assert batch_dto.status == "pending"
        assert batch_dto.id is not None
        assert len(batch_dto.items) == 0
    
    def test_add_items_to_batch(self, service):
        """Should add items to batch."""
        batch_dto = service.create_batch("Test")
        
        items = [
            {"prompt": "Song 1", "style_tags": "metal", "title": "Track 1"},
            {"prompt": "Song 2", "style_tags": "jazz", "title": "Track 2"}
        ]
        
        updated_dto = service.add_items(batch_dto.id, items)
        
        assert len(updated_dto.items) == 2
        assert updated_dto.items[0].title == "Track 1"
        assert updated_dto.items[1].title == "Track 2"
    
    def test_cannot_add_items_to_nonexistent_batch(self, service):
        """Should raise error for invalid batch ID."""
        with pytest.raises(KeyError):
            service.add_items("nonexistent-id", [{"prompt": "Test", "style_tags": "metal"}])
    
    def test_start_batch(self, service):
        """Should transition batch to processing."""
        batch_dto = service.create_batch("Test")
        
        updated_dto = service.start_batch(batch_dto.id)
        
        assert updated_dto.status == "processing"
    
    def test_complete_batch(self, service):
        """Should mark batch as completed."""
        batch_dto = service.create_batch("Test")
        service.start_batch(batch_dto.id)
        
        updated_dto = service.complete_batch(batch_dto.id)
        
        assert updated_dto.status == "completed"
        assert updated_dto.completed_at is not None
    
    def test_fail_batch(self, service):
        """Should mark batch as failed."""
        batch_dto = service.create_batch("Test")
        service.start_batch(batch_dto.id)
        
        updated_dto = service.fail_batch(batch_dto.id)
        
        assert updated_dto.status == "failed"
        assert updated_dto.completed_at is not None
    
    def test_cancel_batch(self, service):
        """Should cancel batch."""
        batch_dto = service.create_batch("Test")
        service.start_batch(batch_dto.id)
        
        updated_dto = service.cancel_batch(batch_dto.id)
        
        assert updated_dto.status == "cancelled"
        assert updated_dto.completed_at is not None
    
    def test_get_batch(self, service):
        """Should retrieve batch by ID."""
        batch_dto = service.create_batch("Test")
        
        retrieved_dto = service.get_batch(batch_dto.id)
        
        assert retrieved_dto.id == batch_dto.id
        assert retrieved_dto.name == "Test"
    
    def test_get_nonexistent_batch_raises_error(self, service):
        """Should raise error for invalid batch ID."""
        with pytest.raises(KeyError):
            service.get_batch("nonexistent-id")
    
    def test_list_all_batches(self, service):
        """Should list all batches."""
        service.create_batch("Batch 1")
        service.create_batch("Batch 2")
        service.create_batch("Batch 3")
        
        batches = service.list_batches()
        
        assert len(batches) == 3
    
    def test_list_batches_filtered_by_status(self, service):
        """Should filter batches by status."""
        batch1_dto = service.create_batch("Batch 1")
        batch2_dto = service.create_batch("Batch 2")
        service.create_batch("Batch 3")
        
        service.start_batch(batch1_dto.id)
        service.start_batch(batch2_dto.id)
        
        processing_batches = service.list_batches(status="processing")
        
        assert len(processing_batches) == 2
        assert all(b.status == "processing" for b in processing_batches)
    
    def test_update_item_status(self, service):
        """Should update item status."""
        batch_dto = service.create_batch("Test")
        items = [{"prompt": "Song 1", "style_tags": "metal"}]
        service.add_items(batch_dto.id, items)
        
        updated_dto = service.update_item_status(
            batch_dto.id,
            0,
            "completed",
            suno_id="suno-123",
            audio_url="https://example.com/audio.mp3"
        )
        
        assert updated_dto.items[0].status == "completed"
        assert updated_dto.items[0].suno_id == "suno-123"
        assert updated_dto.items[0].audio_url == "https://example.com/audio.mp3"
    
    def test_update_item_with_invalid_index_raises_error(self, service):
        """Should raise error for invalid item index."""
        batch_dto = service.create_batch("Test")
        
        with pytest.raises(IndexError):
            service.update_item_status(batch_dto.id, 99, "completed")
    
    def test_cannot_add_items_to_processing_batch(self, service):
        """Should enforce domain rules via exceptions."""
        batch_dto = service.create_batch("Test")
        service.start_batch(batch_dto.id)
        
        with pytest.raises(InvalidBatchError):
            service.add_items(batch_dto.id, [{"prompt": "Test", "style_tags": "metal"}])
