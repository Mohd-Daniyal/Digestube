from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq

app = Flask(__name__)
CORS(app)  # allow the chrome-extension:// origin to call this server

GROQ_API_KEY = "gsk_YOUR_API_KEY_HERE"  # replace with your Groq API key

client = Groq(api_key=GROQ_API_KEY)

MODEL = "openai/gpt-oss-20b"
MAX_TRANSCRIPT_CHARS = 12000  # keeps well under the free-tier TPM cap in one call

SUMMARY_SYSTEM_PROMPT = """You summarize YouTube video transcripts for someone deciding whether they
need to watch the full video. Write 1-2 short paragraphs (roughly 80-150
words total) in plain prose — no bullet points, no headers, no markdown,
no asterisks. Cover what the video is actually about and its main points,
and always state the outcome: if it's a tutorial, what the end result or
solution is; if it's a story, review, or anything building toward a
reveal, twist, verdict, or answer, state that resolution plainly rather
than teasing it. The summary should let someone skip the video and still
know how it ends. Be direct and specific — avoid vague filler like
'the video covers various topics.'"""

@app.get("/summary")
def summary_api():
    video_id = request.args.get("id", "")
    if not video_id:
        return jsonify(error="Missing video id"), 400

    try:
        transcript = get_transcript(video_id)
    except Exception as e:
        app.logger.error(f"Transcript fetch failed for {video_id}: {e}")
        return jsonify(error="Couldn't get the transcript for this video."), 500

    try:
        summary = get_summary(transcript)
    except Exception as e:
        app.logger.error(f"Summary generation failed for {video_id}: {e}")
        return jsonify(error="Couldn't generate a summary right now."), 500

    return jsonify(summary=summary), 200


def get_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()
    fetched = ytt_api.fetch(video_id)
    return " ".join(snippet.text for snippet in fetched)


def get_summary(transcript):
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Summarize this transcript:\n\n{transcript[:MAX_TRANSCRIPT_CHARS]}",
            },
        ],
        max_tokens=600,
        temperature=0.4,
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    app.run(port=5000)