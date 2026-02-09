from datetime import datetime
import praw
import time

def scrub_content(reddit: praw.Reddit):
    user_posts = reddit.user.me().submissions.new(limit=1000)
    user_comments = reddit.user.me().comments.new(limit=1000)
        
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

    
    
