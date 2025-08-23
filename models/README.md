# Local LLM Models

This directory contains the local language model used by EduPlannerBotAI for offline operation.

## Required Model

**Model**: TinyLlama 1.1B Chat v1.0  
**Format**: GGUF (quantized)  
**Size**: ~1.1GB  
**Quantization**: Q4_K_M (4-bit, optimized for memory and speed)

## Download Instructions

### Option 1: Direct Download from Hugging Face

1. Visit the model page: [TinyLlama-1.1B-Chat-v1.0-GGUF](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF)
2. Download the file: `tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf`
3. Place it in this `models/` directory
4. Ensure the filename matches exactly: `tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf`

### Option 2: Using Hugging Face CLI

```bash
# Install huggingface-hub if not already installed
pip install huggingface-hub

# Download the model
huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF \
    tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
    --local-dir models/
```

### Option 3: Using wget/curl

```bash
# Using wget
wget -O models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
    "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

# Using curl
curl -L -o models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
    "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
```

## File Structure

After downloading, your directory should look like this:

```
models/
├── README.md
└── tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf  # ~1.1GB
```

## Verification

Verify the model is correctly downloaded:

```bash
# Check file exists and size
ls -lh models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf

# Expected output:
# -rw-r--r-- 1 user user 1.1G Jan 1 12:00 tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf

# Check file integrity (optional)
file models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
```

## Model Specifications

- **Architecture**: TinyLlama 1.1B (Llama architecture)
- **Training Data**: Chat/instruction fine-tuned
- **Context Length**: 2048 tokens
- **Quantization**: Q4_K_M (4-bit, optimized)
- **Memory Usage**: ~2GB RAM during inference
- **Performance**: Good quality for study plan generation

## Troubleshooting

### Model Not Found Error
```
[Local LLM error: Model not loaded]
```
**Solution**: Ensure the model file is in the correct location with the exact filename.

### Memory Issues
```
[Local LLM error: Out of memory]
```
**Solution**: 
- Ensure you have at least 2GB RAM available
- Close other memory-intensive applications
- Consider using a smaller model variant

### Slow Performance
**Solutions**:
- Ensure you have a multi-core CPU
- Close unnecessary background processes
- The first request may be slower due to model loading

## Alternative Models

If you prefer a different model, you can use any GGUF format model:

1. **Llama 2 7B**: Better quality, larger size (~4GB)
2. **Mistral 7B**: Excellent performance, medium size (~4GB)
3. **Phi-2**: Good quality, smaller size (~1.4GB)

**Note**: Update the model path in `services/local_llm.py` if using a different model.

## Performance Tips

- **First Run**: The first request will be slower as the model loads into memory
- **Subsequent Requests**: Much faster after initial loading
- **Memory**: Keep at least 2GB RAM free for optimal performance
- **CPU**: Multi-core processors will improve inference speed

## Support

If you encounter issues with the local LLM:

1. Check the bot logs for detailed error messages
2. Verify the model file is correctly placed
3. Ensure sufficient system resources
4. Open an issue on GitHub with error details

## License

The TinyLlama model is licensed under Apache 2.0. See the [Hugging Face page](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF) for full license details.
