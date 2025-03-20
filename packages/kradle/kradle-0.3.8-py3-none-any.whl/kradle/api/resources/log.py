"""Run-specific API operations."""
from typing import Dict, List, TypedDict, NotRequired
from ..http import HTTPClient

class LogAPI:
    """Log management API endpoints."""
    
    def __init__(self, http: HTTPClient):
        self.http = http

    def create(self, run_id, participant_id, message, level="info"):
        if not isinstance(message, str):
            message = str(message)
        return self.http.post(
            f'runs/{run_id}/logs',
            {
                'level': level,
                'message': message,
                'participantId': participant_id
            },
        )