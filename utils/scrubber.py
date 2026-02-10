from datetime import datetime
from praw import exceptions, Reddit
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import time

@retry(stop=stop_after_attempt(5), 
        wait=wait_exponential(multiplier=1, min=4, max=60), 
        retry=retry_if_exception_type(exceptions.APIException))
def scrub_content(reddit: Reddit):
    try:
        user_posts = reddit.user.me().submissions.new(limit=1000)
    except Exception as e:
        print(f"Failed to retrieve user's posts: {e}. Continuing on without them...")
        user_posts = []
    
    try:
        user_comments = reddit.user.me().comments.new(limit=1000)
    except Exception as e:
        print(f"Failed to retrieve user's comments: {e}. Continuing on without them...")
        user_comments = []
        
    print("\nStarting retrieval, editing and then deleting user submitted posts...\n")
    for post in user_posts:
        if post.is_self:
            # Update the text of the post to conceal its original contents prior to deletion.
            post.edit(f"[deleted] {datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(1)
            
        # Delete the post so that it no longer exists.
        post.delete()
        time.sleep(1)

    print("\nFinished editing then deleting user submitted posts...\n")
    
    print("\nStarting editing and then deleting user submitted comments...\n")

    for comment in user_comments:
        # Update the text of the post to conceal its original contents prior to deletion.
        comment.edit("[deleted] " + datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(1)

        # Delete the post so that it no longer exists.
        comment.delete()
        time.sleep(1)
    
    print("\nFinished retrieving, editing then deleting user submitted comments...")

    
    
