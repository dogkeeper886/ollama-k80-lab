# Docker Image for Ollama on NVIDIA K80 GPU

## Description

This Docker image provides a ready-to-use environment for running Ollama, a local Large Language Model (LLM) runner, specifically optimized to leverage the capabilities of an NVIDIA K80 GPU. This setup is ideal for AI researchers and developers looking to experiment with models in a controlled home lab setting.

The project repository, [dogkeeper886/ollama-k80-lab](https://github.com/dogkeeper886/ollama-k80-lab), offers insights into configuring and using the image effectively. The Dockerfile included in this image is designed for ease of use and efficiency:

- **Build Stage**: Compiles Ollama from source using GCC and CMake.
- **Runtime Environment**: Utilizes Rocky Linux 8 with necessary GPU drivers and libraries pre-configured.

This setup ensures that users can start experimenting with AI models without the hassle of manual environment configuration, making it a perfect playground for innovation in AI research.

## Features

- **GPU Acceleration**: Fully supports NVIDIA K80 GPUs to accelerate model computations.
- **Pre-built Binary**: Contains the compiled Ollama binary for immediate use.
- **CUDA Libraries**: Includes necessary CUDA libraries and drivers for GPU operations.
- **Environment Variables**: Configured to facilitate seamless interaction with the GPU and network settings.

## Usage

### Prerequisites

Ensure you have Docker installed on your system and that your NVIDIA K80 GPU is properly set up. You may need the NVIDIA Container Toolkit to enable GPU support in Docker containers.

### Pulling the Image

To pull the image from Docker Hub, use:

```bash
docker pull dogkeeper886/ollama37
```

### Running the Container

To run the container with GPU support, execute:

```bash
docker run --runtime=nvidia --gpus all -p 11434:11434 dogkeeper886/ollama37
```

This command will start Ollama and expose it on port `11434`, allowing you to interact with the service.

## 📦 Version History

### v1.2.0 (2025-05-06)

This release introduces support for Qwen3 models, marking a significant step in our commitment to staying Tesla K80 with leading open-source language models. Testing includes successful execution of Gemma 3 12B, Phi-4 Reasoning 14B, and Qwen3 14B, ensuring compatibility with models expected to be widely used in May 2025.

## 🎯 Contributing

We're thrilled to welcome your contributions! Should you encounter any issues or have ideas for improving this Docker image, please submit them as an issue on the GitHub repository: [https://github.com/dogkeeper886/ollama-k80-lab](https://github.com/dogkeeper886/ollama-k80-lab).

We are committed to continually enhancing our projects and appreciate all feedback. Thank you!
