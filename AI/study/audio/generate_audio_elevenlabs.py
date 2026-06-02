"""
ElevenLabs TTS generator for the AI Exam Prep study package.

Produces a higher-quality MP3 for the master index and every lecture chapter
using the ElevenLabs `eleven_multilingual_v2` model — chosen over the existing
edge-tts version because the listener has dyslexia and wants the cleanest,
most natural narration we can get.

The Markdown -> spoken-English cleaning pipeline is REUSED verbatim from
`generate_audio.py` (LaTeX-math prose conversion, table flattening, code-block
stand-ins, pronunciation overrides, etc.). This script only swaps the TTS
backend and adds chunk-size + cost accounting appropriate for the ElevenLabs
HTTP API (~5,000 character per-request soft cap).

Voice / model choice
--------------------
- VOICE_ID = Rachel (`21m00Tcm4TlvDq8ikWAM`)
    Clear, calm, well-paced American female; recommended on the ElevenLabs
    voice library for narration / education. Dyslexia-friendly because the
    prosody is steady and the consonants are crisply enunciated.
- MODEL_ID = `eleven_multilingual_v2`
    Highest-quality production model for English narration.
    Alternative: `eleven_turbo_v2_5` is roughly 2-3x faster and ~50% cheaper
    but slightly less natural. We pay the latency premium for the full
    package.

Voice alternatives (drop-in by editing VOICE_ID below):
    - Rachel   21m00Tcm4TlvDq8ikWAM   American female, clear (default)
    - Domi     AZnzlk1XvdvUeBnXmlld   American female, strong
    - Antoni   ErXwobaYiN019PkySvjV   American male, warm
    - Elli     MF3mGyEYCl7XYWbV9V6O   American female, young
    - Josh     TxGEqnHWrfWFTfGW9XjX   American male, deep
    - Arnold   VR6AewLTigWG4xSOukaG   American male, crisp
    - Adam     pNInz6obpgDQGcFmaJgB   American male, deep narration

Usage:
    py -3.12 study\\audio\\generate_audio_elevenlabs.py

Requires `study/audio/.env` containing `ELEVENLABS_API_KEY=...`.
"""

from __future__ import annotations

import io
import os
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import Iterable

# Re-use the cleaner from the existing edge-tts script (sibling module).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_audio import (  # noqa: E402  (intentional after sys.path tweak)
    SOURCES,
    clean_markdown_for_tts,
    fmt_duration,
    fmt_size,
    mp3_duration_seconds,
)

from dotenv import load_dotenv  # noqa: E402
from elevenlabs.client import ElevenLabs  # noqa: E402
from pydub import AudioSegment  # noqa: E402


# -------------------------- configuration ----------------------------------

# Default voice — Rachel. See header for alternatives.
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
MODEL_ID = "eleven_multilingual_v2"
OUTPUT_FORMAT = "mp3_44100_128"  # 128 kbps stereo, the API's standard quality

# ElevenLabs HTTP synthesis is best-behaved at ~5,000 chars per request.
# We split on paragraph boundaries to keep prosody clean.
MAX_CHARS_PER_CHUNK = 4500

# Voice tuning (dyslexia-friendly: stable prosody, natural similarity, no
# stylistic exaggeration).
VOICE_STABILITY = 0.5
VOICE_SIMILARITY_BOOST = 0.75
VOICE_STYLE = 0.0
VOICE_SPEAKER_BOOST = True

# Retry/backoff for transient API errors.
ATTEMPTS_PER_CHUNK = 4
BACKOFF_BASE_SECONDS = 4.0  # 4, 8, 16, 32 ...

AUDIO_DIR = Path(__file__).resolve().parent
LOG_FILE = AUDIO_DIR / "_run_elevenlabs.log"


# -------------------------- chunking ---------------------------------------

def chunk_text(text: str, max_chars: int = MAX_CHARS_PER_CHUNK) -> list[str]:
    """Split cleaned text into chunks at paragraph boundaries.

    Mirrors the edge-tts script's strategy: prefer paragraph breaks so the TTS
    engine doesn't have to splice prosody across requests; fall back to
    sentence-level splits inside paragraphs that exceed `max_chars` (rare).
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    buf: list[str] = []
    buf_len = 0
    for para in paragraphs:
        if len(para) > max_chars:
            sentences = re.split(r"(?<=[.!?])\s+", para)
            for sent in sentences:
                if buf_len + len(sent) + 1 > max_chars and buf:
                    chunks.append("\n\n".join(buf))
                    buf, buf_len = [], 0
                buf.append(sent)
                buf_len += len(sent) + 1
            continue
        if buf_len + len(para) + 2 > max_chars and buf:
            chunks.append("\n\n".join(buf))
            buf, buf_len = [], 0
        buf.append(para)
        buf_len += len(para) + 2
    if buf:
        chunks.append("\n\n".join(buf))
    return chunks


# -------------------------- TTS calls --------------------------------------

def synth_chunk_bytes(client: ElevenLabs, text: str) -> bytes:
    """Call ElevenLabs text-to-speech for one chunk; return raw MP3 bytes.

    Uses the streaming convert() API and concatenates the chunks. We never
    keep more than one chunk in flight at a time.
    """
    audio_iter = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        model_id=MODEL_ID,
        output_format=OUTPUT_FORMAT,
        text=text,
        voice_settings={
            "stability": VOICE_STABILITY,
            "similarity_boost": VOICE_SIMILARITY_BOOST,
            "style": VOICE_STYLE,
            "use_speaker_boost": VOICE_SPEAKER_BOOST,
        },
    )
    buf = io.BytesIO()
    for piece in audio_iter:
        if piece:
            buf.write(piece)
    return buf.getvalue()


def synth_chunk_with_retry(
    client: ElevenLabs,
    text: str,
    attempts: int = ATTEMPTS_PER_CHUNK,
) -> bytes:
    last_err: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            data = synth_chunk_bytes(client, text)
            if not data:
                raise RuntimeError("ElevenLabs returned empty audio")
            return data
        except Exception as exc:                                  # noqa: BLE001
            last_err = exc
            wait = BACKOFF_BASE_SECONDS * (2 ** (attempt - 1))
            # Don't print the exception's full message — it can contain the
            # request payload which may include the API key in some SDK
            # versions. Just print the type + a short summary.
            etype = type(exc).__name__
            print(
                f"    chunk attempt {attempt}/{attempts} failed ({etype}); "
                f"sleeping {wait:.0f}s",
                flush=True,
            )
            time.sleep(wait)
    raise RuntimeError(
        f"ElevenLabs synthesis failed after {attempts} attempts "
        f"(last error type: {type(last_err).__name__})"
    )


# -------------------------- concat with pydub ------------------------------

def concat_mp3_with_pydub(parts: Iterable[Path], output: Path) -> None:
    """Decode each chunk with pydub/ffmpeg and re-encode to a single MP3.

    ElevenLabs MP3s use a proper file-level container (often with ID3v2 and
    LAME headers), so a naive byte append produces files whose duration meta
    is wrong even though most players still play them. Going through pydub
    yields a clean, seekable output.
    """
    parts = list(parts)
    combined = AudioSegment.empty()
    for part in parts:
        combined += AudioSegment.from_mp3(part)
    combined.export(output, format="mp3", bitrate="128k")


# -------------------------- per-file driver --------------------------------

def process_file(
    src: Path,
    out_dir: Path,
    client: ElevenLabs,
    log: io.TextIOBase,
) -> dict:
    basename = src.stem
    print(f"Generating {basename}.mp3 ...", flush=True)
    log.write(f"\n=== {basename} ===\n")
    t0 = time.time()

    md = src.read_text(encoding="utf-8")
    cleaned = clean_markdown_for_tts(md)
    chunks = chunk_text(cleaned)
    chars_this_file = sum(len(c) for c in chunks)
    final_path = out_dir / f"{basename}.mp3"

    print(
        f"  {len(chunks)} chunk(s), {chars_this_file:,} characters total",
        flush=True,
    )

    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix=f"el_tts_{basename}_") as tmp:
        tmp_dir = Path(tmp)
        part_paths: list[Path] = []
        for i, chunk in enumerate(chunks, 1):
            part = tmp_dir / f"part_{i:03d}.mp3"
            try:
                data = synth_chunk_with_retry(client, chunk)
                part.write_bytes(data)
                part_paths.append(part)
                print(
                    f"    chunk {i}/{len(chunks)} OK "
                    f"({len(chunk):,} chars -> {len(data):,} bytes)",
                    flush=True,
                )
                log.write(
                    f"chunk {i}/{len(chunks)}: {len(chunk)} chars, "
                    f"{len(data)} bytes\n"
                )
            except Exception as exc:                              # noqa: BLE001
                etype = type(exc).__name__
                print(
                    f"    [WARN] chunk {i}/{len(chunks)} failed ({etype})",
                    flush=True,
                )
                log.write(
                    f"chunk {i}/{len(chunks)} FAILED ({etype})\n"
                )
                failures.append(f"{basename} chunk {i}/{len(chunks)}")
        if not part_paths:
            raise RuntimeError(f"no chunks succeeded for {basename}")
        if len(part_paths) == 1:
            shutil.copyfile(part_paths[0], final_path)
        else:
            concat_mp3_with_pydub(part_paths, final_path)

    elapsed = time.time() - t0
    size_b = final_path.stat().st_size
    dur = mp3_duration_seconds(final_path)
    print(
        f"  done in {elapsed:.1f}s -> {final_path.name} "
        f"({fmt_size(size_b)}, {fmt_duration(dur)})",
        flush=True,
    )
    log.write(
        f"DONE {final_path.name} size={size_b} duration={dur} "
        f"chars={chars_this_file} elapsed={elapsed:.1f}s\n"
    )
    log.flush()

    return {
        "src": src,
        "out": final_path,
        "size_bytes": size_b,
        "duration_seconds": dur,
        "elapsed_seconds": elapsed,
        "chunks": len(chunks),
        "chars": chars_this_file,
        "failures": failures,
    }


# -------------------------- main -------------------------------------------

def main() -> int:
    # Load .env from THIS directory (don't fall back to repo root — the key
    # only ever lives next to this script).
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        print(
            f"[ERROR] missing {env_path}. Create it with one line:\n"
            f"        ELEVENLABS_API_KEY=...",
            file=sys.stderr,
        )
        return 2
    load_dotenv(env_path)

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("[ERROR] ELEVENLABS_API_KEY not set after loading .env",
              file=sys.stderr)
        return 2

    client = ElevenLabs(api_key=api_key)

    missing = [p for p in SOURCES if not p.exists()]
    if missing:
        for m in missing:
            print(f"[ERROR] source not found: {m}", file=sys.stderr)
        return 2

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    print(
        f"Voice ID: {VOICE_ID}\n"
        f"Model:    {MODEL_ID}\n"
        f"Format:   {OUTPUT_FORMAT}\n"
        f"Output:   {AUDIO_DIR}\n"
    )

    results: list[dict] = []
    total_failures: list[str] = []

    with LOG_FILE.open("w", encoding="utf-8") as log:
        log.write(
            f"ElevenLabs TTS run\nvoice={VOICE_ID} model={MODEL_ID} "
            f"format={OUTPUT_FORMAT}\n"
            f"started={time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        for src in SOURCES:
            try:
                res = process_file(src, AUDIO_DIR, client, log)
                results.append(res)
                total_failures.extend(res["failures"])
            except Exception as exc:                              # noqa: BLE001
                etype = type(exc).__name__
                print(f"[ERROR] {src.name} failed ({etype})",
                      file=sys.stderr, flush=True)
                log.write(f"{src.name} WHOLE-FILE FAILURE ({etype})\n")
                total_failures.append(f"{src.name} (whole file)")

        # ---- summary -----------------------------------------------------
        print("\n=== Summary ===")
        total_bytes = 0
        total_seconds = 0.0
        total_chars = 0
        for r in results:
            total_bytes += r["size_bytes"]
            total_chars += r["chars"]
            if r["duration_seconds"]:
                total_seconds += r["duration_seconds"]
            print(
                f"  {r['out'].name:35s}  {fmt_size(r['size_bytes']):>10s}  "
                f"{fmt_duration(r['duration_seconds']):>12s}  "
                f"({r['chunks']} chunks, {r['chars']:,} chars)"
            )
        print()
        print(f"Total characters sent to ElevenLabs: {total_chars:,}")
        print(f"Total files: {len(results)}")
        print(f"Total audio bytes: {fmt_size(total_bytes)}")
        print(f"Total audio duration: {fmt_duration(total_seconds)}")

        log.write(
            f"\nSUMMARY chars={total_chars} files={len(results)} "
            f"bytes={total_bytes} seconds={total_seconds:.1f}\n"
            f"finished={time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        if total_failures:
            print("\nFailures:")
            for f in total_failures:
                print(f"  - {f}")
            log.write("FAILURES:\n")
            for f in total_failures:
                log.write(f"  - {f}\n")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
