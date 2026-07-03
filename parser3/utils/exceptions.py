"""Custom exceptions for Parser 3.0."""


class Parser3Error(Exception):
    """Base exception for Parser 3.0."""


class ConfigurationError(Parser3Error):
    """Raised when configuration cannot be loaded or is invalid."""


class DocumentReadError(Parser3Error):
    """Raised when a Word document cannot be read."""


class ValidationError(Parser3Error):
    """Raised when parsed output fails validation."""
