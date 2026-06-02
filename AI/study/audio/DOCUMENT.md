# `study/audio/` — TTS Audio Versions of Every Study Document

Text-to-speech (MP3) renderings of the master index and all ten lecture chapters, intended for a dyslexic listener who prefers listening to reading. Audio is generated locally from the canonical Markdown sources (not the PDFs) so the spoken content stays in sync with any chapter revisions.

Two generators live side-by-side. Both share the same Markdown -> spoken-English cleaning pipeline (defined once in `generate_audio.py`) so the spoken content is identical; only the TTS backend differs.

| Generator | Backend | Voice | Notes |
|---|---|---|---|
| `generate_audio.py` | Microsoft `edge-tts` (free, no API key) | `en-US-JennyNeural`, rate `-10%` | Original version. Output now archived in `_edge-tts-backup/`. |
| `generate_audio_elevenlabs.py` | ElevenLabs (paid API) | `Rachel` (`21m00Tcm4TlvDq8ikWAM`), model `eleven_multilingual_v2` | Current canonical version — substantially more natural prosody, better for dyslexic listeners. |

## Files

- `generate_audio.py` — original edge-tts driver + the canonical `clean_markdown_for_tts()` cleaner that both scripts use.
- `generate_audio_elevenlabs.py` — ElevenLabs driver. Imports the cleaner from `generate_audio.py` (no duplication).
- `.env` — gitignored. Contains `ELEVENLABS_API_KEY=...`. Created locally; **never committed**.
- `_run.log` — last edge-tts run log.
- `_run_elevenlabs.log` — last ElevenLabs run log (chunk-level success/failure + summary, no secrets).
- `_edge-tts-backup/` — the previous edge-tts MP3s, preserved for A/B comparison and fallback.
- `*.mp3` (eleven outputs at the directory root) — current ElevenLabs renderings.

## Source Markdown -> MP3 mapping

| MP3 | Source |
|---|---|
| `00-master-index.mp3` | `../00-master-index.md` |
| `L02-Agents.mp3` | `../lectures/L02-Agents.md` |
| `L03-Uninformed-Search.mp3` | `../lectures/L03-Uninformed-Search.md` |
| `L05-Local-Search.mp3` | `../lectures/L05-Local-Search.md` |
| `L06-Adversarial-Search.mp3` | `../lectures/L06-Adversarial-Search.md` |
| `L07-CSP.mp3` | `../lectures/L07-CSP.md` |
| `L09a-Bayesian-Networks.mp3` | `../lectures/L09a-Bayesian-Networks.md` |
| `L09b-HMM.mp3` | `../lectures/L09b-HMM.md` |
| `L10-Intro-to-ML.mp3` | `../lectures/L10-Intro-to-ML.md` |
| `L11-Regression.mp3` | `../lectures/L11-Regression.md` |
| `L12-Clustering.mp3` | `../lectures/L12-Clustering.md` |

## Cleaning pipeline (shared by both generators)

`clean_markdown_for_tts()` in `generate_audio.py` is the single source of truth. It:

1. Reads each Markdown source verbatim.
2. Replaces fenced code blocks (` ```python `, ` ```mermaid `) with the spoken phrase "code example, see the PDF" or "diagram, see the PDF" so the listener is told to consult the printable when visual content is essential.
3. Rewrites inline math (`$...$`) and block math (`$$...$$`) into spoken English: Greek letters spelled out (`\alpha` -> "alpha"), operators verbalised (`\leq` -> "less than or equal to", `\to` -> "to"), subscripts/superscripts unpacked (`x_i` -> "x sub i", `x^2` -> "x squared"), fractions read as "(numerator) over (denominator)", summations as "sum from i equals 1 to N". Complex expressions that don't fully resolve fall back to "[math expression]".
4. Unrolls Markdown tables row-by-row in prose ("Row 1: column A is X, column B is Y").
5. Reduces image references (`![caption](path)`) to "Figure: caption.".
6. Strips anchor IDs (`{#some-id}`), HTML comments, blockquote markers, list bullets, bold/italic markers, and `§` prefixes.
7. Emits "Section: {title}." with extra silence around H2 headings so the listener hears the structural break.
8. Applies pronunciation overrides for acronyms (e.g. `BFS` -> "B F S", `K-means` -> "K means", `A*` -> "A-star").

## ElevenLabs generator specifics

- **Model:** `eleven_multilingual_v2` (highest-quality English narration; ~3x more natural than the turbo model at the cost of latency).
- **Voice settings:** `stability=0.5`, `similarity_boost=0.75`, `style=0.0`, `use_speaker_boost=True` — chosen for steady, calm prosody (dyslexia-friendly) without exaggerated affect.
- **Output format:** `mp3_44100_128` (128 kbps, 44.1 kHz stereo).
- **Chunking:** ElevenLabs' HTTP synthesis is best-behaved at ~5,000 characters per request. The script chunks on paragraph boundaries with a 4,500-character soft cap, falling back to sentence-level splits for the rare oversized paragraph.
- **Concatenation:** per-chunk MP3s are merged with `pydub` (full decode + re-encode at 128 kbps), since ElevenLabs MP3s carry proper ID3v2 + LAME headers that would corrupt a naive byte-append.
- **Retry policy:** four attempts per chunk with exponential backoff (4s, 8s, 16s, 32s). Failures are logged to `_run_elevenlabs.log`, never to the printed transcript with the request payload, so the API key cannot leak via error messages.
- **Cost accounting:** the script tracks characters per chunk and prints a per-file + grand-total summary at the end.

### Switching voice

Edit `VOICE_ID` at the top of `generate_audio_elevenlabs.py`. Drop-in alternatives:

| Name | Voice ID | Profile |
|---|---|---|
| Rachel  | `21m00Tcm4TlvDq8ikWAM` | American female, clear (default) |
| Domi    | `AZnzlk1XvdvUeBnXmlld` | American female, strong |
| Antoni  | `ErXwobaYiN019PkySvjV` | American male, warm |
| Elli    | `MF3mGyEYCl7XYWbV9V6O` | American female, young |
| Josh    | `TxGEqnHWrfWFTfGW9XjX` | American male, deep |
| Arnold  | `VR6AewLTigWG4xSOukaG` | American male, crisp |
| Adam    | `pNInz6obpgDQGcFmaJgB` | American male, deep narration |

## Regenerating

```powershell
# Original edge-tts (free, faster, slightly less natural):
py -3.12 study\audio\generate_audio.py

# ElevenLabs (paid, slower, more natural — current canonical version):
py -3.12 study\audio\generate_audio_elevenlabs.py
```

Both generators are idempotent: a second run overwrites every MP3 with identical-quality output.

## Dependencies

- Python 3.12 (`py -3.12 --version`)
- `edge-tts` (Microsoft TTS, no API key)
- `elevenlabs` (paid API, key in `.env`)
- `python-dotenv` (loads `.env`)
- `pydub` + `ffmpeg` (decode+re-encode of ElevenLabs MP3s; also used for accurate duration reporting)

Install:

```powershell
py -3.12 -m pip install edge-tts elevenlabs python-dotenv pydub
```

## Secret handling

The ElevenLabs API key lives **only** in `study/audio/.env`. That path is gitignored at the repo root (see `../../../.gitignore`, line `.env`). The generator script:

- reads the key via `os.environ.get("ELEVENLABS_API_KEY")` after `load_dotenv()`,
- never hardcodes it,
- never prints it (chunk error messages log only the exception **type**, not the full message that some SDK versions include the request payload in).

## Recent changes

- **2026-05-31:** Added `generate_audio_elevenlabs.py` (ElevenLabs / Rachel / `eleven_multilingual_v2`) for higher-quality dyslexia-friendly narration. Edge-tts MP3s moved to `_edge-tts-backup/`. `.env` added at the repo root `.gitignore`.
- **2026-05-23:** Initial generation. `generate_audio.py` written; all 11 MP3s produced from current Markdown sources with `en-US-JennyNeural` at `rate=-10%`.
