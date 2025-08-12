from datetime import datetime
from typing import Dict, List, Any, Optional


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def _create_empty_session(session_id: str) -> Dict[str, Any]:
        """Create a new empty session with default fields."""
        return {
            "session_id": session_id,
            "timestamp": "",
            "messages": [],
            "parameters": {},
        }

    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Retrieve session by ID. If it doesn't exist, create and return an empty session."""
        if session_id not in self.sessions:
            self.sessions[session_id] = self._create_empty_session(session_id)
        return self.sessions[session_id]

    def delete_session(self, session_id: str) -> bool:
        """Delete a session. Returns True if successful, False if session not found."""
        return self.sessions.pop(session_id, None) is not None

    def append_message(self, session_id: str, message: str, role: str):
        """Append a message to the session's message list."""
        session = self.get_session(session_id)
        session["messages"].append({"content": message, "role": role})

    @staticmethod
    def apply_changes(self, session_id: str):
        pass
