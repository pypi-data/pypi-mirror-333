from datetime import datetime, timezone
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
import logging
from talentwizer_commons.utils.db import mongo_database

logger = logging.getLogger(__name__)

def is_token_expired(token_data: dict) -> bool:
    """Check if the access token is expired or about to expire in next 5 minutes."""
    if not token_data.get('expires_at'):
        return True
        
    expires_at = token_data['expires_at']
    now = int(datetime.now(timezone.utc).timestamp())
    
    # Check if token expires in next 5 minutes
    return now >= (expires_at - 300)  # 300 seconds = 5 minutes

async def refresh_access_token(token_data: dict) -> dict:
    """Refresh the access token using refresh token."""
    try:
        creds = Credentials(
            token=token_data["accessToken"],
            refresh_token=token_data["refreshToken"],
            token_uri="https://oauth2.googleapis.com/token",
            client_id=token_data["clientId"],
            client_secret=token_data["clientSecret"],
            scopes=token_data["scope"].split()
        )
        
        # Force token refresh
        creds.refresh(Request())
        
        # Update token data with new tokens
        token_data.update({
            "accessToken": creds.token,
            "expires_at": int(creds.expiry.timestamp()) if creds.expiry else None,
            # Keep refresh token if the new one is None
            "refreshToken": creds.refresh_token or token_data["refreshToken"]
        })
        
        # Update token in database
        await update_stored_token(token_data)
        
        return token_data
        
    except RefreshError as e:
        logger.error(f"Failed to refresh token: {str(e)}")
        raise

async def update_stored_token(token_data: dict):
    """Update the stored token in the database."""
    try:
        # Update token in sessions collection
        result = mongo_database["sessions"].update_one(
            {"email": token_data["email"]},
            {"$set": {
                "integrationSession.accessToken": token_data["accessToken"],
                "integrationSession.refreshToken": token_data["refreshToken"],
                "integrationSession.expires_at": token_data["expires_at"]
            }}
        )
        
        if result.modified_count == 0:
            logger.warning(f"No token updated for email: {token_data['email']}")
            
    except Exception as e:
        logger.error(f"Failed to update stored token: {str(e)}")
        raise
