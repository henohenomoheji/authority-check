class ImageInterpretationError(Exception):
    """Base class for domain errors in image interpretation."""


class InvalidImageFormatError(ImageInterpretationError):
    """Raised when uploaded file extension is not supported."""


class ImageTooLargeError(ImageInterpretationError):
    """Raised when uploaded file exceeds the size limit."""


class EmptyImageError(ImageInterpretationError):
    """Raised when uploaded file is empty."""


class InvalidPromptError(ImageInterpretationError):
    """Raised when prompt is invalid (e.g., too long)."""


class MissingConfigurationError(ImageInterpretationError):
    """Raised when required environment variables are missing."""


class ModelTimeoutError(ImageInterpretationError):
    """Raised when model API times out."""


class ModelUnavailableError(ImageInterpretationError):
    """Raised when model API is unavailable or returns an error."""
