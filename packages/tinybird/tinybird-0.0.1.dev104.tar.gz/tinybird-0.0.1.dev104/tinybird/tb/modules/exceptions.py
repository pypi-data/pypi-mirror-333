from typing import Any, Dict, Optional

import click

from tinybird.tb.modules.telemetry import add_telemetry_event


class CLIException(click.exceptions.ClickException):
    """Default exception for all exceptions raised in the CLI.

    Allows to specift a custom telemetry event to be sent before
    raising the exception (if not specified, it sends a generic
    `error` beacon with the error message)
    """

    def __init__(self, message: str, telemetry_event: Optional[str] = None, **kw_telemetry_event_data: Any) -> None:
        telemetry_event = telemetry_event or "error"
        data: Dict[str, Any] = {"error": message}
        data.update(kw_telemetry_event_data)
        add_telemetry_event(telemetry_event, **data)
        super().__init__(message)


class CLIAuthException(CLIException):
    """Exceptions generated by the auth commands"""

    def __init__(self, message: str, **kw_telemetry_event_data: Any) -> None:
        super().__init__(message, "auth_error", **kw_telemetry_event_data)


class CLIReleaseException(CLIException):
    """Exceptions generated by the release commands"""

    def __init__(self, message: str, **kw_telemetry_event_data: Any) -> None:
        super().__init__(message, "release_error", **kw_telemetry_event_data)


class CLIBranchException(CLIException):
    """Exceptions generated by the branch commands"""

    def __init__(self, message: str, **kw_telemetry_event_data: Any) -> None:
        super().__init__(message, "branch_error", **kw_telemetry_event_data)


class CLIGitReleaseException(CLIException):
    """Exceptions generated by the git release related commands"""

    def __init__(self, message: str, **kw_telemetry_event_data: Any) -> None:
        super().__init__(message, "git_release_error", **kw_telemetry_event_data)


class CLIConnectionException(CLIException):
    """Exceptions generated by the connection commands"""

    def __init__(self, message: str, **kw_telemetry_event_data: Any) -> None:
        super().__init__(message, "connection_error", **kw_telemetry_event_data)


class CLIDatasourceException(CLIException):
    """Exceptions generated by the datasource commands"""

    def __init__(self, message: str, **kw_telemetry_event_data: Any) -> None:
        super().__init__(message, "datasource_error", **kw_telemetry_event_data)


class CLIPipeException(CLIException):
    """Exceptions generated by the pipe commands"""

    def __init__(self, message: str, **kw_telemetry_event_data: Any) -> None:
        super().__init__(message, "pipe_error", **kw_telemetry_event_data)


class CLIWorkspaceMembersException(CLIException):
    """Exceptions generated by the workspace members commands"""

    def __init__(self, message: str, **kw_telemetry_event_data: Any) -> None:
        super().__init__(message, "workspace_members_error", **kw_telemetry_event_data)


class CLIWorkspaceException(CLIException):
    """Exceptions generated by the workspace commands"""

    def __init__(self, message: str, **kw_telemetry_event_data: Any) -> None:
        super().__init__(message, "workspace_error", **kw_telemetry_event_data)


class CLITokenException(CLIException):
    """Exceptions generated by the token commands"""

    def __init__(self, message: str, **kw_telemetry_event_data: Any) -> None:
        super().__init__(message, "token_error", **kw_telemetry_event_data)
