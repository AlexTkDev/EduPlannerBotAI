# Local LLM Models

This directory stores the local language model used by EduPlannerBotAI for offline mode.

## Default model (updated)

**Model family**: Google Gemma 4 (instruction-tuned, GGUF)  
**Recommended file name**: `google-gemma-4b-it-Q4_K_M.gguf`  
**Expected path**: `models/google-gemma-4b-it-Q4_K_M.gguf`

> If your GGUF file has a different name, set `LOCAL_LLM_MODEL_PATH` in `.env`.

## Quick setup

1. Download a Gemma 4 GGUF file from your preferred source.
2. Put it into the `models/` folder.
3. Set `.env`:

```env
LOCAL_LLM_MODEL_PATH=models/google-gemma-4b-it-Q4_K_M.gguf
LOCAL_LLM_CONTEXT=4096
LOCAL_LLM_THREADS=4
LOCAL_LLM_MAX_TOKENS=512
```

## File structure

```text
models/
├── README.md
└── google-gemma-4b-it-Q4_K_M.gguf
```

## Verification

```bash
ls -lh models/google-gemma-4b-it-Q4_K_M.gguf
file models/google-gemma-4b-it-Q4_K_M.gguf
```

## Troubleshooting

### Model not loaded

If you see:

```text
[Local LLM error: Model not loaded]
```

Check:
- file path in `LOCAL_LLM_MODEL_PATH`
- read permissions for the model file
- available RAM/CPU resources

### Out-of-memory or slow responses

- Reduce context: `LOCAL_LLM_CONTEXT=2048`
- Use lower-bit quantization if available
- Close other heavy processes
