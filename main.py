import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import higgsfield_client

load_dotenv(Path(__file__).with_name(".env.local"))

if not os.getenv("HF_KEY"):
    raise RuntimeError("Missing HF_KEY in .env.local")

MODEL = "bytedance/seedance-2.5/text-to-video"

PROMPT = """
Create a 30-second vertical 9:16 photorealistic POV cooking video for TikTok, Instagram Reels and YouTube Shorts.

RECIPE: Creamy crispy chicken pasta.

STYLE AND CONTINUITY:
- First-person POV, hands only. Never show face, eyes, torso, full body, or a talking presenter.
- Same light-skinned male hands throughout, no jewelry, sleeves rolled to the forearms.
- Realistic modern kitchen.
- Matte charcoal-grey stone countertop, one light natural-oak cutting board, brushed stainless-steel pan, matte black utensils, one cream-white ceramic plate, one small white ceramic bowl.
- Soft warm directional daylight from the left around 4500K, shallow depth of field, warm natural color grading.
- Food fills 70-90% of frame.
- Vertical portrait only.
- Absolutely no on-screen text, subtitles, captions, ingredient labels, banners, usernames, watermarks, or recipe cards.

0-10 SECONDS — HOOK:
Close side-angle at countertop height. Start immediately with an appetizing hero shot of golden crispy chicken pieces sizzling in a stainless-steel pan beside glossy creamy pasta. Steam rises. Hands toss the chicken once and spoon creamy sauce over the pasta. Fast, satisfying food cinematography.
German off-screen voiceover, warm energetic male food-creator voice:
"Die meisten machen cremige Hähnchen-Pasta viel zu kompliziert. So wird sie richtig saftig, knusprig und unglaublich cremig."

10-20 SECONDS — INGREDIENTS:
Natural camera transition to top-down overhead. Hands quickly arrange and prep exact ingredients: 300 g chicken breast, 200 g pasta, 200 ml cooking cream, 80 g grated Parmesan, 1 tablespoon olive oil, 2 teaspoons paprika powder, 1 teaspoon garlic powder, 1/2 teaspoon salt, black pepper. Show cutting chicken into bite-size pieces and seasoning it. No written labels.
German voiceover:
"Du brauchst 300 Gramm Hähnchenbrust, 200 Gramm Pasta, 200 Milliliter Sahne, 80 Gramm Parmesan, einen Esslöffel Öl und Paprika, Knoblauch, Salz und Pfeffer."

20-30 SECONDS — PREPARATION + CTA:
Return to front three-quarter side angle. Add seasoned chicken to the hot pan, strong realistic sizzling, stir and sear until golden on the outside. Keep cooking action continuous while the CTA is spoken. End with the chicken mid-sear and the pan positioned so a second 30-second continuation can start seamlessly from the exact same cooking state.
German voiceover:
"Brate das Hähnchen jetzt kräftig an. Und bevor wir weitermachen: Aus welcher Stadt schaust du gerade zu? Schreib sie in die Kommentare, dann grüße ich jemanden im nächsten Video."

AUDIO:
Natural cooking sounds: sizzling, knife on board, light ingredient rustling, pan stirring. German male off-screen voice only, warm, natural, energetic, not robotic. No music overpowering the voice.

The final frame must preserve the exact kitchen, pan, hands, lighting, food state, and camera setup for seamless continuation in part 2.
""".strip()

ARGUMENTS = {
    "prompt": PROMPT,
    "duration": 30,
    "resolution": "1080p",
    "aspect_ratio": "9:16",
    "bitrate_mode": "high",
    "output_format": "mp4",
    "generate_audio": True,
}

FAILURE_STATUSES = {"failed", "canceled", "cancelled", "nsfw", "moderated"}


def main():
    try:
        result = higgsfield_client.subscribe(
            MODEL,
            arguments=ARGUMENTS,
        )

        status = str(result.get("status", "")).lower() if isinstance(result, dict) else ""
        if status in FAILURE_STATUSES:
            error = result.get("error") if isinstance(result, dict) else None
            raise RuntimeError(f"Generation ended with status: {status}. {error or ''}".strip())

        if not isinstance(result, dict) or result.get("status") != "completed":
            raise RuntimeError(f"Unexpected terminal response: {result}")

        video = result.get("video") or {}
        video_url = video.get("url")
        if not video_url:
            raise RuntimeError("Generation completed without a video URL.")

        print(video_url)

    except Exception as exc:
        print(f"Generation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
