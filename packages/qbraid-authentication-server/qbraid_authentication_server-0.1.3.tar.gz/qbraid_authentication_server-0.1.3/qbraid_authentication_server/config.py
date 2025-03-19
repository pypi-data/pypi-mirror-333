import json
import sys
from typing import Optional

import tornado
from jupyter_server.base.handlers import APIHandler
from qbraid_core import QbraidSession


class UserConfigHandler(APIHandler):
    """Handler for managing user configurations and other local data."""

    @tornado.web.authenticated
    def get(self):
        """Get user's qBraid credentials."""
        config = self.get_config()

        self.finish(json.dumps(config))

    @staticmethod
    def get_config() -> dict[str, Optional[str]]:
        """
        Retrieve the user's qBraid credentials.

        Returns:
            A dictionary containing user configuration details.
        """
        try:
            session = QbraidSession()
            config = {
                "email": session.get_config("email"),
                "refreshToken": session.get_config("refresh-token"),
                "apiKey": session.get_config("api-key"),
                "url": session.get_config("url"),
            }
            return config
        except Exception as e:
            print(f"Error while retrieving user configuration: {str(e)}", file=sys.stderr)
            return {key: None for key in ["email", "refreshToken", "apiKey", "url"]}
