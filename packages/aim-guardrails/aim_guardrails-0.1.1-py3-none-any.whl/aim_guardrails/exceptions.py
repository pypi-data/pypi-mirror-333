class AimGuardrailMissingSecrets(Exception):
    """Raised when required Aim API credentials are missing."""

    pass


class AimGuardrailAPIError(Exception):
    """Raised when there's an error with the Aim API."""

    pass
