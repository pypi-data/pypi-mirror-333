import uuid

from django.utils import timezone

from dj_waanverse_auth.models import UserSession
from dj_waanverse_auth.security.utils import get_ip_address


def create_session(user, request, login_method) -> str:
    """
    Create a new session for a user and return the session ID.

    Args:
        user: The user object associated with the session.
        request: The request object.
        login_method: The login method used for the session.
    Returns:
        A string representing the newly created session ID.
    """
    session_id = str(uuid.uuid4())
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    UserSession.objects.create(
        account=user,
        session_id=session_id,
        ip_address=get_ip_address(request),
        user_agent=user_agent,
        login_method=login_method,
    )

    return session_id


def validate_session(session_id: str) -> bool:
    """
    Validate a session by checking its existence and updating the last_used timestamp.

    Args:
        session_id: The ID of the session to validate.

    Returns:
        True if the session is valid, False otherwise.
    """
    try:
        session = UserSession.objects.get(session_id=session_id, is_active=True)
        session.last_used = timezone.now()
        session.save(update_fields=["last_used"])
        return True
    except UserSession.DoesNotExist:
        return False


def revoke_session(session_id: str) -> None:
    """
    Revoke a specific session by marking it as inactive.

    Args:
        session_id: The ID of the session to revoke.
    """
    UserSession.objects.filter(session_id=session_id).update(is_active=False)


def revoke_other_sessions(user, current_session_id: str) -> None:
    """
    Revoke all active sessions for a user except the current session.

    Args:
        user: The user object whose other sessions should be revoked.
        current_session_id: The ID of the current session to exclude.
    """
    UserSession.objects.filter(user=user, is_active=True).exclude(
        session_id=current_session_id
    ).update(is_active=False)
