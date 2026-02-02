"""Unit tests for Batch domain model."""

import pytest
from datetime import datetime

from src.domain.models.batch import Batch, BatchItem, BatchStatus
from src.domain.exceptions.domain_errors import InvalidBatchError


class TestBatchItem:
    """Test BatchItem entity."""
    
    def test_batch_item_creation_valid(self):
        """Should create a valid batch item."""
        item = BatchItem(
            prompt="Cosmic horror metal song",
            style_tags=["heavy metal", "atmospheric"],
            title="Void Song"
        )
        
        assert item.prompt == "Cosmic horror metal song"
        assert item.style_tags == ["heavy metal", "atmospheric"]
        assert item.title == "Void Song"
        assert item.status == "pending"
        assert item.suno_id is None
    
    def test_batch_item_empty_prompt_raises_error(self):
        """Should raise error for empty prompt."""
        with pytest.raises(InvalidBatchError, match="prompt cannot be empty"):
            BatchItem(
                prompt="",
                style_tags=["metal"]
            )
    
    def test_batch_item_empty_style_tags_raises_error(self):
        """Should raise error for empty style_tags."""
        with pytest.raises(InvalidBatchError, match="style_tags cannot be empty"):
            BatchItem(
                prompt="Test prompt",
                style_tags=[]
            )


class TestBatch:
    """Test Batch entity."""
    
    def test_batch_creation_valid(self):
        """Should create a valid batch."""
        batch = Batch(name="Album Batch 1")
        
        assert batch.name == "Album Batch 1"
        assert batch.status == BatchStatus.PENDING
        assert len(batch.items) == 0
        assert isinstance(batch.created_at, datetime)
        assert batch.completed_at is None
    
    def test_batch_empty_name_raises_error(self):
        """Should raise error for empty name."""
        with pytest.raises(InvalidBatchError, match="name cannot be empty"):
            Batch(name="")
    
    def test_batch_invalid_status_raises_error(self):
        """Should raise error for invalid status."""
        with pytest.raises(InvalidBatchError, match="Invalid batch status"):
            Batch(name="Test", status="invalid_status")
    
    def test_batch_add_item(self):
        """Should add item to pending batch."""
        batch = Batch(name="Test")
        item = BatchItem(prompt="Test", style_tags=["metal"])
        
        batch.add_item(item)
        
        assert batch.get_item_count() == 1
        assert batch.items[0] == item
    
    def test_batch_add_invalid_item_raises_error(self):
        """Should raise error when adding non-BatchItem."""
        batch = Batch(name="Test")
        
        with pytest.raises(InvalidBatchError, match="valid BatchItem"):
            batch.add_item("not a batch item")
    
    def test_batch_cannot_add_item_when_processing(self):
        """Should not allow adding items to processing batch."""
        batch = Batch(name="Test")
        batch.start_processing()
        
        item = BatchItem(prompt="Test", style_tags=["metal"])
        
        with pytest.raises(InvalidBatchError, match="Cannot add items"):
            batch.add_item(item)

# ... validation tests already fixed ...
    
    def test_batch_get_completed_count(self):
        """Should count completed items."""
        batch = Batch(name="Test")
        
        item1 = BatchItem(prompt="Test 1", style_tags=["metal"], status="completed")
        item2 = BatchItem(prompt="Test 2", style_tags=["metal"], status="pending")
        item3 = BatchItem(prompt="Test 3", style_tags=["metal"], status="completed")
        
        batch.items = [item1, item2, item3]
        
        assert batch.get_completed_count() == 2
    
    def test_batch_get_progress_percentage(self):
        """Should calculate progress percentage."""
        batch = Batch(name="Test")
        
        item1 = BatchItem(prompt="Test 1", style_tags=["metal"], status="completed")
        item2 = BatchItem(prompt="Test 2", style_tags=["metal"], status="pending")
        item3 = BatchItem(prompt="Test 3", style_tags=["metal"], status="completed")
        item4 = BatchItem(prompt="Test 4", style_tags=["metal"], status="completed")
        
        batch.items = [item1, item2, item3, item4]
        
        assert batch.get_progress_percentage() == 75.0

    def test_batch_string_representation(self):
        """Should have meaningful string representation."""
        batch = Batch(name="Test Batch")
        batch.items = [
            BatchItem(prompt="Test1", style_tags=["metal"], status="completed"),
            BatchItem(prompt="Test2", style_tags=["metal"])
        ]
        
        batch_str = str(batch)
        
        assert "Test Batch" in batch_str
        assert "pending" in batch_str
        assert "2 items" in batch_str
        assert "50.0%" in batch_str


class TestBatchStatus:
    """Test BatchStatus enum."""
    
    def test_batch_status_values(self):
        """Should have expected status values."""
        assert BatchStatus.PENDING.value == "pending"
        assert BatchStatus.PROCESSING.value == "processing"
        assert BatchStatus.COMPLETED.value == "completed"
        assert BatchStatus.FAILED.value == "failed"
        assert BatchStatus.CANCELLED.value == "cancelled"
    
    def test_batch_status_from_string(self):
        """Should create status from string."""
        status = BatchStatus("processing")
        assert status == BatchStatus.PROCESSING
