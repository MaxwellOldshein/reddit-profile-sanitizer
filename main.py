import warnings

from config.settings import load_settings
from api.reddit_client import get_reddit_client
from utils.exporter import export_content
from utils.scrubber import scrub_content

def main():
    warnings.filterwarnings("ignore", "Reddit will check for validation*", DeprecationWarning)

    settings = load_settings()
    reddit = get_reddit_client(settings)

    export_content(reddit, settings)
    scrub_content(reddit)

    print("Process completed. All user content saved, edited, and then removed.")

if __name__ == "__main__":
    main()