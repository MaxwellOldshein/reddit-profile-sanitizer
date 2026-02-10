from config.settings import Settings
from datetime import datetime
from praw import exceptions, Reddit
from prawcore.exceptions import TooManyRequests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import time

@retry(stop=stop_after_attempt(5), 
        wait=wait_exponential(multiplier=1, min=4, max=60), 
        retry=retry_if_exception_type(exceptions.RedditAPIException, TooManyRequests))
def export_content(reddit: Reddit, settings: Settings):
    try:
        user_posts = list(reddit.user.me().submissions.new(limit=1000))
    except exceptions.RedditAPIException:
        print(f"Failed to retrieve user's posts due to API-related exception. Retrying...")
        raise # Trigger the back off retry logic above for any API-related PRAW exception.
    except TooManyRequests as e:
        print(f"Failed to retrieve user's posts due to rate-limiting. Retrying...")
        raise # Trigger the back off retry logic above any rate-limiting related exception.
    except Exception as e:
        print(f"Failed to retrieve user's posts due to fatal exception: {e}. Continuing on without them...")
        user_posts = []

    try:
        user_comments = list(reddit.user.me().comments.new(limit=1000))
    except exceptions.RedditAPIException:
        print(f"Failed to retrieve user's comments due to API-related exception. Retrying...")
        raise # Trigger the back off retry logic above for any API-related PRAW exception.
    except TooManyRequests as e:
        print(f"Failed to retrieve user's comments due to rate-limiting. Retrying...")
        raise # Trigger the back off retry logic above any rate-limiting related exception.
    except Exception as e:
        print(f"Failed to retrieve user's comments due to fatal exception: {e}. Continuing on without them...")
        user_comments = []

    # Create text file to store a backup of the most recent version of the user's submitted posts/comments for later review potentially or local storage.
    with open(settings.history_file, "w") as user_submitted_content_file:   
        # Debug user submitted posts.
        print("\nRetrieving and saving user submitted posts...\n")
        user_submitted_content_file.write(f"Generated For /u/{reddit.user.me()} On: {datetime.fromtimestamp(time.time()).strftime('%A, %B %d, %Y at %H:%M:%S')}")
        user_submitted_content_file.write(f"\n\nAudit Summary: {len(user_posts)} posts and {len(user_comments)} comments exported to file.")
        user_submitted_content_file.write("\n\n\nUSER SUBMITTED POSTS:\n")
        user_submitted_content_file.write("\n---------------------------------------------------------------------------------------------------------------------------------------------------")

        if (user_posts):
            for post in user_posts:
                # Save the relevent information about the post to a local file for later viewing, if needed.
                user_submitted_content_file.write(f"\nID: {post.id}")
                user_submitted_content_file.write(f"\nTitle: {post.title}")
                user_submitted_content_file.write(f"\nContent: {post.selftext if post.is_self else post.url}")
                user_submitted_content_file.write(f"\nURL: https://www.reddit.com{post.permalink}")
                user_submitted_content_file.write(f"\nScore: {post.score}")
                user_submitted_content_file.write(f"\nNumber of Comments: {post.num_comments}")
                user_submitted_content_file.write(f"\nSubreddit Name: {post.subreddit}")
                user_submitted_content_file.write(f"\nCreated At: {datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')}")
                user_submitted_content_file.write(f"\nEdited At: {datetime.fromtimestamp(post.edited).strftime('%Y-%m-%d %H:%M:%S') if type(post.edited) == float else 'N/A'}")
                user_submitted_content_file.write("\n---------------------------------------------------------------------------------------------------------------------------------------------------")
        else:
            user_submitted_content_file.write("\nNo user submitted posts found on Reddit to export.")
            user_submitted_content_file.write("\n---------------------------------------------------------------------------------------------------------------------------------------------------")


        print("\nFinished retrieving and saving user submitted posts...\n")

        # Debug user submitted comments.
        print("\nStarting retrieving and saving user submitted comments...\n")
        user_submitted_content_file.write("\n\n\nUSER SUBMITTED COMMENTS:\n")
        user_submitted_content_file.write("\n---------------------------------------------------------------------------------------------------------------------------------------------------")

        if (user_comments):
            for comment in user_comments:
                # Save the relevent information about the comment to a local file for later viewing, if needed.
                user_submitted_content_file.write(f"\nID: {comment.id}")
                user_submitted_content_file.write(f"\nBody: {comment.body}")
                user_submitted_content_file.write(f"\nURL: https://www.reddit.com{comment.permalink}")
                user_submitted_content_file.write(f"\nScore: {comment.score}")
                user_submitted_content_file.write(f"\nSubreddit Name: {comment.subreddit}")
                user_submitted_content_file.write("\n---------------------------------------------------------------------------------------------------------------------------------------------------")
        else:
            user_submitted_content_file.write("\nNo user submitted comments found on Reddit to export.")
            user_submitted_content_file.write("\n---------------------------------------------------------------------------------------------------------------------------------------------------")
            
        print("\nFinished retrieving and saving user submitted comments...")