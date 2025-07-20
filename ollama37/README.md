# Docker Image for Ollama on NVIDIA K80 GPU

## Description

This Docker image provides a ready-to-use environment for running Ollama, a local Large Language Model (LLM) runner, specifically optimized to leverage the capabilities of an NVIDIA K80 GPU. This setup is ideal for AI researchers and developers looking to experiment with models in a controlled home lab setting.

The project repository, [dogkeeper886/ollama-k80-lab](https://github.com/dogkeeper886/ollama-k80-lab), offers insights into configuring and using the image effectively. The Dockerfile included in this image is designed for ease of use and efficiency:

- **Build Stage**: Compiles Ollama from source using GCC and CMake.
- **Runtime Environment**: Utilizes Rocky Linux 8 with necessary GPU drivers and libraries pre-configured.

This setup ensures that users can start experimenting with AI models without the hassle of manual environment configuration, making it a perfect playground for innovation in AI research.

## Features

- **GPU Acceleration**: Fully supports NVIDIA K80 GPUs to accelerate model computations.
- **Multi-Modal AI**: Supports vision-language models like Qwen2.5-VL for image understanding.
- **Advanced Reasoning**: Built-in thinking support for enhanced AI reasoning capabilities.
- **Pre-built Binary**: Contains the compiled Ollama binary for immediate use.
- **CUDA Libraries**: Includes necessary CUDA libraries and drivers for GPU operations.
- **Enhanced Tool Support**: Improved tool calling and WebP image input support.
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

## Ollama37 Docker Compose

This `docker-compose.yml` file sets up an Ollama 3.7 container for a more streamlined and persistent environment. It utilizes volumes to persist data and ensures the container automatically restarts if it fails.

### Prerequisites

*   Docker
*   Docker Compose

### Usage

1.  **Save the `docker-compose.yml` file:** Save the content provided below into a file named `docker-compose.yml` in a convenient directory.

2.  **Run the container:** Open a terminal in the directory where you saved the file and run the following command:

    ```bash
    docker-compose up -d
    ```

    This command downloads the `dogkeeper886/ollama37` image (if not already present) and starts the Ollama container in detached mode.

    ```yml
    services:
      ollama37:
        image: dogkeeper886/ollama37
        container_name: ollama37
        ports:
          - "11434:11434"
        restart: unless-stopped # Automatically restart the container
        runtime: nvidia # Utilize NVIDIA GPU runtime
        volumes:
          - ./volume:/root/.ollama # Persist Ollama data
    ```

    **Explanation of key `docker-compose.yml` directives:**

    *   `version: '3.8'`: Specifies the Docker Compose file version.
    *   `services.ollama.image: dogkeeper886/ollama37`: Defines the Docker image to use.
    *   `ports: - "11434:11434"`: Maps port 11434 on the host machine to port 11434 inside the container, making Ollama accessible.
    *   `volumes: - ./.ollama:/root/.ollama`:  **Important:**  This mounts a directory named `.ollama` in the same directory as the `docker-compose.yml` file to the `/root/.ollama` directory inside the container.  This ensures that downloaded models and Ollama configuration data are persisted even if the container is stopped or removed.  Create a `.ollama` directory if it does not already exist.
    *   `restart: unless-stopped`:  This ensures the container automatically restarts if it crashes or is stopped (but not if you explicitly stop it with `docker-compose down`).
    *   `runtime: nvidia`: Explicitly instructs Docker to use the NVIDIA runtime, ensuring GPU acceleration.

3.  **Accessing Ollama:** After running the container, you can interact with Ollama using its API.  Refer to the Ollama documentation for usage details.

### Stopping the Container

To stop the container, run:

```bash
docker-compose down
```

This will stop and remove the container, but the data stored in the `.ollama` directory will be preserved.

## 📦 Version History

### v1.3.0 (2025-07-01)

This release expands model support while maintaining full Tesla K80 compatibility:

**New Model Support:**
- **Qwen2.5-VL**: Multi-modal vision-language model for image understanding
- **Qwen3 Dense & Sparse**: Enhanced Qwen3 model variants
- **Improved MLLama**: Better support for Meta's LLaMA models

**Documentation Updates:**
- Updated installation guides for Tesla K80 compatibility
- Enhanced Docker Hub documentation with latest model information

### v1.2.0 (2025-05-06)

This release introduces support for Qwen3 models, marking a significant step in our commitment to staying Tesla K80 with leading open-source language models. Testing includes successful execution of Gemma 3 12B, Phi-4 Reasoning 14B, and Qwen3 14B, ensuring compatibility with models expected to be widely used in May 2025.

## 🎯 Contributing

We're thrilled to welcome your contributions! Should you encounter any issues or have ideas for improving this Docker image, please submit them as an issue on the GitHub repository: [https://github.com/dogkeeper886/ollama-k80-lab](https://github.com/dogkeeper886/ollama-k80-lab).

We are committed to continually enhancing our projects and appreciate all feedback. Thank you!
