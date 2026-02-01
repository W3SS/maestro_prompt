"""Domain exceptions for Maestro AI."""

class MaestroDomainError(Exception):
    """Base exception for all domain errors."""
    pass


class InvalidAlbumError(MaestroDomainError):
    """Raised when album data is invalid."""
    pass


class InvalidTrackError(MaestroDomainError):
    """Raised when track data is invalid."""
    pass


class InvalidBatchError(MaestroDomainError):
    """Raised when batch data is invalid."""
    pass


class InvalidArchetypeError(MaestroDomainError):
    """Raised when archetype is not recognized."""
    pass


class InvalidGenreError(MaestroDomainError):
    """Raised when genre is not recognized."""
    pass
