# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a laboratory for running Ollama (local LLM runner) on NVIDIA K80 GPUs with custom Docker builds optimized for CUDA 11.4 compatibility. The project serves as the foundation for a broader ecosystem — the K80-optimized Ollama build (ollama37) powers an LLM Judge in CI that guards upstream ports, and provides the local LLM runtime for QA workflow automation. Legacy Dify workflows and prompt templates are included for web UI users; for AI coding agent workflows, see [ai-qa-workflow](https://github.com/dogkeeper886/ai-qa-workflow).

## Docker Commands

### Running Ollama
```bash
# Pull and run the custom K80-optimized Ollama image
docker pull dogkeeper886/ollama37:v2.03
docker run --runtime=nvidia --gpus all -p 11434:11434 dogkeeper886/ollama37:v2.03

# Using docker-compose (recommended for persistent data)
cd ollama37/
docker-compose up -d

# Stop the service
docker-compose down
```

### Building Custom Images
```bash
# Build the builder image (contains CUDA 11.4, GCC 10, CMake, Go)
cd ollama37-builder/
docker build -t dogkeeper886/ollama37-builder .

# Build the runtime image
cd ollama37/
docker build -t dogkeeper886/ollama37 .
```

## Key Environment Variables
- `OLLAMA_HOST=0.0.0.0:11434` - API endpoint
- `LD_LIBRARY_PATH="/usr/local/lib64:/usr/local/cuda-11.4/lib64"` - CUDA libraries
- `NVIDIA_DRIVER_CAPABILITIES=compute,utility` - GPU capabilities
- `NVIDIA_VISIBLE_DEVICES=all` - GPU visibility

## Hardware Requirements
- NVIDIA K80 GPU
- NVIDIA Tesla K80 driver installed
- NVIDIA Container Runtime for Docker
- Sufficient storage for model downloads (models stored in `./volume/` when using docker-compose)

## Development Workflow

### Model Testing
The project supports running various LLM models optimized for K80:
- Gemma 4 (parser, renderer, architecture port)
- FunctionGemma (tool-calling support)
- Qwen3.5 Ollama Engine (DeltaNet recurrent state)
- Qwen2.5-VL (multi-modal vision-language model)
- Gemma 3 12B
- Phi-4 Reasoning 14B
- DeepSeek-R1:32B

### Quality Assurance Integration
The Dify workflows enable automated processing of:
- Jira tickets to Markdown conversion
- Requirements analysis and test generation
- Documentation refinement
- Bug report processing

### Persistent Data
When using docker-compose, model data persists in `./volume/` directory, mapped to `/root/.ollama` inside the container.