"""Album Designer Service - orchestrates album design using LLM and context."""

from typing import List, Dict, Any
import json

from src.ports.output.llm_client_port import ILLMClient
from src.ports.output.context_loader_port import IContextLoader
from src.domain.models.album import Album, Track, Archetype, Genre
from src.application.dto.album_dto import AlbumDTO, TrackDTO


class AlbumDesigner:
    """
    Application Service for designing albums.
    
    Orchestrates the album design process using:
    - LLM for creative generation
    - Context for genre/archetype knowledge
    - Domain models for validation
    """
    
    def __init__(self, llm_client: ILLMClient, context_loader: IContextLoader):
        """
        Initialize the service.
        
        Args:
            llm_client: LLM client for generation
            context_loader: Context loader for knowledge base
        """
        self.llm = llm_client
        self.context = context_loader
    
    async def design_album(
        self,
        archetype: str,
        genres: List[str],
        num_tracks: int = 8
    ) -> AlbumDTO:
        """
        Design a complete album.
        
        Args:
            archetype: Narrative archetype (e.g., "cosmic_horror")
            genres: Musical genres (e.g., ["metal", "jazz"])
            num_tracks: Number of tracks to generate
        
        Returns:
            AlbumDTO with complete album data
        """
        # Load context
        context_data = self.context.get_full_context(archetype, genres)
        
        # Build prompt for album concept
        album_prompt = self._build_album_prompt(archetype, genres, context_data)
        
        # Generate album concept
        album_response = await self.llm.generate(album_prompt)
        album_data = self._parse_album_response(album_response)
        
        # Create album DTO
        album_dto = AlbumDTO(
            title=album_data.get("title", f"{archetype.title()} Album"),
            archetype=archetype,
            genres=genres
        )
        
        # Generate tracks
        for i in range(1, num_tracks + 1):
            track_dto = await self._generate_track(
                album_dto.title,
                archetype,
                genres,
                i,
                context_data
            )
            album_dto.tracks.append(track_dto)
        
        return album_dto
    
    async def _generate_track(
        self,
        album_title: str,
        archetype: str,
        genres: List[str],
        track_number: int,
        context_data: Dict[str, Any]
    ) -> TrackDTO:
        """Generate a single track."""
        track_prompt = self._build_track_prompt(
            album_title,
            archetype,
            genres,
            track_number,
            context_data
        )
        
        track_response = await self.llm.generate(track_prompt)
        track_data = self._parse_track_response(track_response)
        
        return TrackDTO(
            title=track_data.get("title", f"Track {track_number}"),
            lyrics=track_data.get("lyrics", ""),
            style_tags=self._build_style_tags(genres, context_data),
            track_number=track_number,
            duration_estimate=track_data.get("duration", 240)  # Default 4 min
        )
    
    def _build_album_prompt(
        self,
        archetype: str,
        genres: List[str],
        context_data: Dict[str, Any]
    ) -> str:
        """Build prompt for album concept generation."""
        return f"""Design a music album with the following parameters:

Archetype: {archetype}
Genres: {', '.join(genres)}

Context: {json.dumps(context_data, indent=2)}

Generate:
1. Album title (creative and thematic)
2. Overall concept and narrative arc

Format your response as JSON with keys: title, concept"""
    
    def _build_track_prompt(
        self,
        album_title: str,
        archetype: str,
        genres: List[str],
        track_number: int,
        context_data: Dict[str, Any]
    ) -> str:
        """Build prompt for track generation."""
        return f"""Create track {track_number} for album "{album_title}":

Archetype: {archetype}
Genres: {', '.join(genres)}

Generate:
1. Track title
2. Complete lyrics (verse-chorus-verse-chorus-bridge-chorus structure)
3. Estimated duration in seconds

Format as JSON with keys: title, lyrics, duration"""
    
    def _build_style_tags(
        self,
        genres: List[str],
        context_data: Dict[str, Any]
    ) -> List[str]:
        """Build style tags from genres and context."""
        tags = genres.copy()
        
        # Add context-based tags
        if "characteristics" in context_data:
            chars = context_data["characteristics"]
            if isinstance(chars, dict):
                tags.extend(chars.get("sonic_elements", []))
        
        return tags[:5]  # Limit to 5 tags
    
    def _parse_album_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response for album data."""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback: extract title from text
            lines = response.strip().split('\n')
            return {
                "title": lines[0] if lines else "Untitled Album",
                "concept": response
            }
    
    def _parse_track_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response for track data."""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback: use raw response as lyrics
            return {
                "title": "Untitled",
                "lyrics": response,
                "duration": 240
            }
    
    def to_domain_album(self, album_dto: AlbumDTO) -> Album:
        """
        Convert DTO to domain model.
        
        Args:
            album_dto: Album DTO
        
        Returns:
            Album domain entity
        """
        album = Album(
            title=album_dto.title,
            archetype=Archetype(album_dto.archetype),
            genres=[Genre(g) for g in album_dto.genres]
        )
        
        for track_dto in album_dto.tracks:
            track = Track(
                title=track_dto.title,
                lyrics=track_dto.lyrics,
                style_tags=track_dto.style_tags,
                duration_estimate=track_dto.duration_estimate,
                track_number=track_dto.track_number
            )
            album.add_track(track)
        
        return album
