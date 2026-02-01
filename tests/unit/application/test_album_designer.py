"""Unit tests for AlbumDesigner service."""

import pytest
from unittest.mock import Mock, AsyncMock

from src.application.services.album_designer import AlbumDesigner
from src.application.dto.album_dto import AlbumDTO
from src.ports.output.llm_client_port import ILLMClient
from src.ports.output.context_loader_port import IContextLoader
from src.domain.models.album import Archetype, Genre


class TestAlbumDesigner:
    """Test AlbumDesigner service."""
    
    @pytest.fixture
    def mock_llm(self):
        """Create mock LLM client."""
        return AsyncMock(spec=ILLMClient)
    
    @pytest.fixture
    def mock_context(self):
        """Create mock context loader."""
        mock = Mock(spec=IContextLoader)
        mock.get_full_context.return_value = {
            "archetype": "cosmic_horror",
            "characteristics": {
                "sonic_elements": ["atmospheric", "heavy", "progressive"]
            }
        }
        return mock
    
    @pytest.fixture
    def service(self, mock_llm, mock_context):
        """Create service instance."""
        return AlbumDesigner(mock_llm, mock_context)
    
    @pytest.mark.asyncio
    async def test_design_album_calls_llm_and_context(self, service, mock_llm, mock_context):
        """Should call LLM and context loader."""
        # Setup mocks
        mock_llm.generate.return_value = '{"title": "Test Album", "concept": "Dark themes"}'
        
        # Execute
        album_dto = await service.design_album("cosmic_horror", ["metal"], num_tracks=2)
        
        # Verify
        mock_context.get_full_context.assert_called_once_with("cosmic_horror", ["metal"])
        assert mock_llm.generate.call_count >= 1  # At least album concept
        assert album_dto.title == "Test Album"
        assert album_dto.archetype == "cosmic_horror"
        assert len(album_dto.tracks) == 2
    
    @pytest.mark.asyncio
    async def test_design_album_generates_tracks(self, service, mock_llm, mock_context):
        """Should generate specified number of tracks."""
        mock_llm.generate.side_effect = [
            '{"title": "Void Album"}',  # Album
            '{"title": "Track 1", "lyrics": "Lyrics 1", "duration": 180}',
            '{"title": "Track 2", "lyrics": "Lyrics 2", "duration": 200}',
            '{"title": "Track 3", "lyrics": "Lyrics 3", "duration": 220}'
        ]
        
        album_dto = await service.design_album("cosmic_horror", ["metal"], num_tracks=3)
        
        assert len(album_dto.tracks) == 3
        assert album_dto.tracks[0].title == "Track 1"
        assert album_dto.tracks[1].title == "Track 2"
        assert album_dto.tracks[2].title == "Track 3"
    
    @pytest.mark.asyncio
    async def test_design_album_handles_invalid_json_response(self, service, mock_llm, mock_context):
        """Should handle non-JSON LLM responses."""
        mock_llm.generate.return_value = "Just some text, not JSON"
        
        album_dto = await service.design_album("cosmic_horror", ["metal"], num_tracks=1)
        
        # Should not crash, uses fallback parsing
        assert album_dto.title is not None
        assert len(album_dto.tracks) == 1
    
    @pytest.mark.asyncio
    async def test_build_style_tags(self, service, mock_context):
        """Should build style tags from genres and context."""
        context_data = {
            "characteristics": {
                "sonic_elements": ["atmospheric", "heavy", "progressive"]
            }
        }
        
        tags = service._build_style_tags(["metal", "jazz"], context_data)
        
        assert "metal" in tags
        assert "jazz" in tags
        assert len(tags) <= 5
    
    def test_to_domain_album_conversion(self, service):
        """Should convert DTO to domain model."""
        from src.application.dto.album_dto import TrackDTO
        
        album_dto = AlbumDTO(
            title="Test Album",
            archetype="cosmic_horror",
            genres=["metal", "jazz"]
        )
        album_dto.tracks.append(TrackDTO(
            title="Track 1",
            lyrics="Lyrics",
            style_tags=["metal"],
            track_number=1
        ))
        
        domain_album = service.to_domain_album(album_dto)
        
        assert domain_album.title == "Test Album"
        assert domain_album.archetype == Archetype.COSMIC_HORROR
        assert Genre.METAL in domain_album.genres
        assert len(domain_album.tracks) == 1
        assert domain_album.tracks[0].title == "Track 1"
