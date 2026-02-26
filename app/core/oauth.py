from authlib.integrations.starlette_client import OAuth
from fastapi import Request
from app.core.config import settings

oauth = OAuth()

google = oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

async def get_google_user_info(request: Request, token):
    try:
        resp = await google.get('https://www.googleapis.com/oauth2/v2/userinfo', token=token)
        user_data = resp.json()
        return {
            'google_id': user_data['id'],
            'email': user_data['email'],
            'username': user_data['name'],
            'picture': user_data.get('picture')
        }
    except Exception as e:
        print(f"Error getting Google user info: {e}")
        raise