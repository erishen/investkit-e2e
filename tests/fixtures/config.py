import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
SCREENSHOT_DIR = Path("test-results/screenshots")
VIDEO_DIR = Path("test-results/videos")
TRACE_DIR = Path("test-results/traces")

DEFAULT_TIMEOUT = 15000
DEFAULT_NAVIGATION_TIMEOUT = 30000
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720
MAX_PAGE_LOAD_SECONDS = 10
MAX_API_RESPONSE_SECONDS = 3
HEALTH_CHECK_TIMEOUT = 3
MIN_PAGE_CONTENT_LENGTH = 100
ERROR_STATUS_THRESHOLD = 400

SERVICES = {
    "asset_lens": {
        "url": os.getenv("ASSET_LENS_URL", "http://localhost:8000"),
        "health_endpoint": "/",
    },
    "ts_demo": {
        "url": os.getenv("TS_DEMO_URL", "http://localhost:3000"),
        "health_endpoint": "/",
    },
    "solo_chat": {
        "url": os.getenv("SOLO_CHAT_URL", "http://localhost:5173"),
        "health_endpoint": "/",
    },
    "stock_analyzer": {
        "url": os.getenv("STOCK_ANALYZER_URL", "http://localhost:8001"),
        "health_endpoint": "/",
    },
    "lobster": {
        "url": os.getenv("LOBSTER_URL", "http://localhost:8501"),
        "health_endpoint": "/",
    },
}
