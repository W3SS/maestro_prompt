"""Unit tests for MaestroTools (TDD RED Phase)."""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from src.application.tools import MaestroTools
from src.application.tool_schema import (
    DesignAlbumInput, CreateBatchInput, StartBatchInput,
    AddItemsInput, GetBatchInput, ListBatchesInput,
    CompleteBatchInput, CancelBatchInput
)

pytestmark = pytest.mark.asyncio

class TestMaestroTools:
    """Test suite for MaestroTools (TDD approach)."""
    
    @patch("src.application.tools.get_container")
    async def test_design_album_success(self, mock_get_container):
        """Should design an album with AI."""
        # Setup mock container and designer
        mock_container = Mock()
        mock_designer = Mock()
        mock_get_container.return_value = mock_container
        mock_container.album_designer.return_value = mock_designer
        
        # Setup mock return value
        mock_track = Mock()
        mock_track.title = "Test Track"
        mock_track.lyrics = "Test Lyrics"
        mock_track.style_tags = ["test"]
        mock_track.duration_estimate = "3:30"
        
        mock_album = Mock()
        mock_album.title = "Test Album"
        mock_album.tracks = [mock_track]
        
        # Configure async method mock
        mock_designer.design_album = AsyncMock(return_value=mock_album)
        
        input_data = DesignAlbumInput(
            archetype="concept_album",
            genres=["metal", "progressive"],
            theme="cosmic horror"
        )
        
        result = await MaestroTools.design_album(input_data)
        
        assert result.title == "Test Album"
        assert len(result.tracks) == 1
        assert result.tracks[0]["title"] == "Test Track"
    
    async def test_create_batch_success(self):
        """Should create a new batch."""
        input_data = CreateBatchInput(name="Test Batch")
        
        result = await MaestroTools.create_batch(input_data)
        
        assert result.batch_id is not None
        assert result.status == "pending"
    
    async def test_add_items_to_batch(self):
        """Should add items to an existing batch."""
        # Create batch first
        batch = await MaestroTools.create_batch(CreateBatchInput(name="Test"))
        
        input_data = AddItemsInput(
            batch_id=batch.batch_id,
            items=[
                {"prompt": "Heavy metal track", "style_tags": ["metal"], "title": "Track 1"},
                {"prompt": "Jazz fusion", "style_tags": ["jazz"], "title": "Track 2"}
            ]
        )
        
        result = await MaestroTools.add_items_to_batch(input_data)
        
        assert result.batch_id == batch.batch_id
        assert result.items_count == 2
        assert result.status == "pending"
    
    async def test_get_batch_returns_dto(self):
        """Should retrieve batch details by ID."""
        # Create batch
        batch = await MaestroTools.create_batch(CreateBatchInput(name="Retrieve Test"))
        
        input_data = GetBatchInput(batch_id=batch.batch_id)
        
        result = await MaestroTools.get_batch(input_data)
        
        assert result.batch_id == batch.batch_id
        assert result.name == "Retrieve Test"
        assert result.status == "pending"
        assert result.items_count == 0
    
    async def test_get_batch_invalid_id_raises_error(self):
        """Should raise error for nonexistent batch."""
        input_data = GetBatchInput(batch_id="invalid-id")
        
        with pytest.raises(KeyError):
            await MaestroTools.get_batch(input_data)
    
    async def test_list_batches_without_filter(self):
        """Should list all batches."""
        # Create multiple batches
        await MaestroTools.create_batch(CreateBatchInput(name="Batch 1"))
        await MaestroTools.create_batch(CreateBatchInput(name="Batch 2"))
        
        input_data = ListBatchesInput()
        
        result = await MaestroTools.list_batches(input_data)
        
        assert result.total >= 2
        assert len(result.batches) >= 2
    
    async def test_list_batches_filters_by_status(self):
        """Should filter batches by status."""
        # Create and start a batch
        batch = await MaestroTools.create_batch(CreateBatchInput(name="Started Batch"))
        await MaestroTools.start_batch(StartBatchInput(batch_id=batch.batch_id))
        
        input_data = ListBatchesInput(status="processing")
        
        result = await MaestroTools.list_batches(input_data)
        
        assert all(b["status"] == "processing" for b in result.batches)
    
    async def test_start_batch_updates_status(self):
        """Should start a batch and update status."""
        batch = await MaestroTools.create_batch(CreateBatchInput(name="Start Test"))
        
        input_data = StartBatchInput(batch_id=batch.batch_id)
        
        result = await MaestroTools.start_batch(input_data)
        
        assert result["batch_id"] == batch.batch_id
        assert result["status"] == "processing"
    
    async def test_complete_batch_updates_status(self):
        """Should complete a batch."""
        batch = await MaestroTools.create_batch(CreateBatchInput(name="Complete Test"))
        await MaestroTools.start_batch(StartBatchInput(batch_id=batch.batch_id))
        
        input_data = CompleteBatchInput(batch_id=batch.batch_id)
        
        result = await MaestroTools.complete_batch(input_data)
        
        assert result.batch_id == batch.batch_id
        assert result.status == "completed"
        assert result.completed_at is not None
    
    async def test_cancel_batch_succeeds(self):
        """Should cancel a batch."""
        batch = await MaestroTools.create_batch(CreateBatchInput(name="Cancel Test"))
        
        input_data = CancelBatchInput(batch_id=batch.batch_id)
        
        result = await MaestroTools.cancel_batch(input_data)
        
        assert result.batch_id == batch.batch_id
        assert result.status == "cancelled"
