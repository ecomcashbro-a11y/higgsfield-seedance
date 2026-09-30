import "dotenv/config";
import { HiggsfieldClient } from "@higgsfield/client";

const credentials = process.env.HF_CREDENTIALS;
if (!credentials) {
  throw new Error("Missing HF_CREDENTIALS in .env.local");
}

const client = new HiggsfieldClient({ credentials });

async function main() {
  try {
    const result = await client.subscribe("bytedance/seedance-2.5/text-to-video", {
      input: {
        prompt: "A cinematic scene at sunset",
        duration: 5,
        resolution: "720p",
        aspect_ratio: "16:9",
      },
    });

    const status = (result as any)?.status;
    if (status && ["failed", "canceled", "cancelled", "moderated"].includes(String(status).toLowerCase())) {
      throw new Error(`Generation ended with status: ${status}`);
    }

    const videoUrl =
      (result as any)?.video?.url ??
      (result as any)?.output?.url ??
      (result as any)?.url ??
      (result as any)?.data?.url;

    if (!videoUrl) {
      throw new Error("Generation completed without a video URL.");
    }

    console.log(videoUrl);
  } catch (error) {
    console.error(error instanceof Error ? error.message : error);
    process.exitCode = 1;
  }
}

main();
