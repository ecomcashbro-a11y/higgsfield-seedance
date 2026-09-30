import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import higgsfield_client

load_dotenv(Path(__file__).with_name(".env.local"))

if not os.getenv("HF_KEY"):
    raise RuntimeError("Missing HF_KEY in .env.local")

MODEL = "bytedance/seedance-2.5/text-to-video"
ARGUMENTS = {
    "prompt": "A cinematic scene at sunset",
    "duration": 5,
    "resolution": "720p",
    "aspect_ratio": "16:9",
}

TERMINAL_FAILURE_STATUSES = {
    "failed",
    "failure",
    "canceled",
    "cancelled",
    "moderated",
    "nsfw",
    "ip_detected",
}


def find_video_url(value):
    if isinstance(value, dict):
        for key in ("status", "state"):
            status = value.get(key)
            if isinstance(status, str) and status.lower() in TERMINAL_FAILURE_STATUSES:
                raise RuntimeError(f"Generation ended with status: {status}")

        for key in ("url", "video_url", "rawUrl", "raw_url"):
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate.startswith(("http://", "https://")):
                return candidate

        for child in value.values():
            found = find_video_url(child)
            if found:
                return found

    elif isinstance(value, (list, tuple)):
        for child in value:
            found = find_video_url(child)
            if found:
                return found

    return None


def main():
    try:
        result = higgsfield_client.subscribe(
            MODEL,
            arguments=ARGUMENTS,
        )
        video_url = find_video_url(result)
        if not video_url:
            raise RuntimeError("Generation completed without a video URL.")
        print(video_url)
    except Exception as exc:
        print(f"Generation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
