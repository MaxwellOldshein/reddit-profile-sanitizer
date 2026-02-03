import os
import time
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    client_id: str
    refresh_token: str | None
    redirect_uri: str = "http://localhost:8080"
    user_agent: str = "script:postscrubapp:v1.0"

    @property
    def data_directory(self) -> Path:
        return Path("data")

    @property
    def history_file(self) -> Path:
        return self.data_directory / f"user_submitted_content_{time.time()}.txt"

def load_settings() -> Settings:
    client_id = os.getenv("CLIENT_ID")

    if not client_id:
        raise ValueError("Missing critical CLIENT_ID value in .env file")
    
    return Settings(client_id=client_id, refresh_token=os.getenv("REFRESH_TOKEN"))