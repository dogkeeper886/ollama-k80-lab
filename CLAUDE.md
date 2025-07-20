# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a laboratory for running Ollama (local LLM runner) on NVIDIA K80 GPUs with custom Docker builds optimized for CUDA 11.4 compatibility. The project focuses on LLM-powered workflow automation for software quality assurance, integrating with tools like Dify, VS Code Continue plugin, N8N, and auto-webui.

## Docker Commands

### Running Ollama
```bash
# Pull and run the custom K80-optimized Ollama image
docker pull dogkeeper886/ollama37
docker run --runtime=nvidia --gpus all -p 11434:11434 dogkeeper886/ollama37

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

## Architecture

### Core Components

1. **ollama37-builder/**: Multi-stage Docker build environment
   - Rocky Linux 8 base with NVIDIA drivers 470
   - CUDA 11.4 toolkit for K80 GPU compatibility
   - Custom-compiled GCC 10, CMake 4.0, Go 1.24.2
   - Environment setup scripts for proper library paths

2. **ollama37/**: Runtime Docker image
   - Compiled Ollama binary optimized for K80
   - Minimal runtime environment with required CUDA libraries
   - Exposes Ollama API on port 11434
   - Persistent volume support for model storage

3. **dify/**: Workflow automation configurations
   - YAML workflow definitions for LLM-powered QA tasks
   - Python utilities for Atlassian/Jira integration (`format_jira_ticket.py`)
   - Workflow templates: BugBlitz, QualityQuest, ER2Test, etc.
   - Knowledge base with PDF documentation for various systems

4. **mcp-servers/**: Model Context Protocol integrations
   - Web browser MCP server for enhanced LLM capabilities

### Key Environment Variables
- `OLLAMA_HOST=0.0.0.0:11434` - API endpoint
- `LD_LIBRARY_PATH="/usr/local/lib64:/usr/local/cuda-11.4/lib64"` - CUDA libraries
- `NVIDIA_DRIVER_CAPABILITIES=compute,utility` - GPU capabilities
- `NVIDIA_VISIBLE_DEVICES=all` - GPU visibility

### Hardware Requirements
- NVIDIA K80 GPU
- NVIDIA Tesla K80 driver installed
- NVIDIA Container Runtime for Docker
- Sufficient storage for model downloads (models stored in `./volume/` when using docker-compose)

## Development Workflow

### Model Testing
The project supports running various LLM models optimized for K80:
- Qwen2.5-VL (multi-modal vision-language model)
- Qwen3 Dense & Sparse variants
- Improved MLLama models
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