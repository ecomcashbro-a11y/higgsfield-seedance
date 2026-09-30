# Higgsfield Seedance 2.5

Python example using the official Higgsfield SDK and `subscribe`.

Configuration:

- model: `bytedance/seedance-2.5/text-to-video`
- prompt: `A cinematic scene at sunset`
- duration: `5`
- resolution: `720p`
- aspect ratio: `16:9`

## Setup

1. Create `.env.local` from `.env.example`.
2. Put the credential in `.env.local` as:

   `HF_KEY=key-id:key-secret`

3. Install dependencies:

   `python -m pip install -r requirements.txt`

4. Run:

   `python main.py`

The credential is loaded only at runtime. `.env.local` is ignored by Git and must never be committed.
