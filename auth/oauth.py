from urllib.parse import urlparse, parse_qs
import praw

from config.settings import Settings

def authorize_new_reddit_user(settings: Settings) -> str:
    # Unauthenticated Reddit client to authenticate the user.
    reddit = praw.Reddit(
        client_id=settings.client_id,
        client_secret=None,
        redirect_uri=settings.redirect_uri,
        user_agent=settings.user_agent
    )

    scopes = ["identity", "read", "edit", "history"]
    auth_url = reddit.auth.url(scopes=scopes, state="randomstring123", duration="permanent")

    print(f"Open this URL in your browser to finalize authentication: \n{auth_url}")

    redirect_response_url = input("\nPaste the full URL from your browser here to continue:\n")
    redirect_response_code = parse_qs(urlparse(redirect_response_url).query)["code"][0]
    refresh_token = reddit.auth.authorize(redirect_response_code)

    # Save Reddit authorization token to the .env file for future usage
    with(".env", "a") as env_file:
        env_file.write(f"\nREFRESH_TOKEN={refresh_token}")

    return refresh_token