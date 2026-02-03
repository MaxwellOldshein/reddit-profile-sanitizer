import praw
from auth.oauth import authorize_new_reddit_user
from config.settings import Settings

def get_reddit_client(settings: Settings) -> praw.reddit:
    if settings.refresh_token:
        reddit = praw.Reddit(
            client_id=settings.client_id,
            client_secret=None,
            refresh_token=settings.refresh_token,
            redirect_uri=settings.redirect_uri,
            user_agent=settings.user_agent,
            validate_on_submit=True # Supress DeprecationWarning for validation checking when editing content.
        )
        
        shouldProceedInput = input(f"Located provided refresh token for /u/{reddit.user.me()}. Would you like to proceed with that that? (Y/N): ")

        if shouldProceedInput.upper() != "Y":
            print("Exiting process without proceeding. To clear this user, remove the REFRESH_TOKEN variable from your .env file before trying again for a new user.")
            exit(1)
        
        return reddit
    
    print("No refresh token found... Authorizing new user for the script via Reddit.")

    new_refresh_token = authorize_new_reddit_user(settings)

    return praw.Reddit(
        client_id=settings.client_id,
        client_secret=None,
        refresh_token=new_refresh_token,
        redirect_uri=settings.redirect_uri,
        user_agent=settings.user_agent,
        validate_on_submit=True # Supress DeprecationWarning for validation checking when editing content.
    )