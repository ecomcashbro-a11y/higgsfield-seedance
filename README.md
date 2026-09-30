# Higgsfield Seedance 2.5

TypeScript example using the official Higgsfield SDK and `subscribe` with:

- model: `bytedance/seedance-2.5/text-to-video`
- prompt: `A cinematic scene at sunset`
- duration: 5
- resolution: 720p
- aspect ratio: 16:9

## Setup

1. Copy `.env.example` to `.env.local`.
2. Put your credential in `.env.local`:

   `HF_CREDENTIALS=key-id:key-secret`

3. Install dependencies:

   `npm install`

4. Run:

   `npm start`

`.env.local` is gitignored and must never be committed.
