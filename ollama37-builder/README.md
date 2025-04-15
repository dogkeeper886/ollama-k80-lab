# Ollama CUDA 11.4 Builder Image for Tesla K80 (Compute Capability 3.7)

This Docker image provides a development environment tailored specifically to build [Ollama37](https://github.com/dogkeeper886/ollama37) on older NVIDIA GPUs, with an emphasis on devices like the **Tesla K80** which have compute capability of `3.7`. It comes equipped with essential tools and software including CUDA toolkit 11.4 support.

## 🔧 Key Features

- **Base Image:** Rocky Linux v8
- **CUDA Toolkit Version:** 11.4 - For high-performance GPU acceleration.
- **NVIDIA Driver (v470):** `nvidia-driver:470-dkms` to ensure compatibility with Tesla K80 GPUs and beyond, specifically targeting compute capability of version 3.7.
- **GCC v10:** A versatile compiler that will be necessary for building C/C++ projects in this Docker image environment is compiled from source within the container itself; thus ensuring up-to-date features are available during builds.
- **CMake (v4.0.0):** This build system generator, also built directly into our custom Rocky Linux 8 image version v10 ensures a comprehensive and flexible C/C++ project building process that can be tailored to your needs within this environment; again compiled from source for the latest features right in your container.
- **Go (v1.24.2):** This lightweight programming language is essential when compiling Go projects, especially those utilizing cgo.

This Docker image strikes a balance between supporting legacy hardware such as Tesla K80 and meeting modern software build requirements like CUDA 11.4 for cutting-edge development needs including but not limited to Ollama37.


## 🚀 How To Use

Designed with builders in mind; this container is perfect when you're aiming to compile projects that leverage the power of NVIDIA GPUs, particularly those compatible with compute capability `3.7`.

### Quick Example Usage:

```bash
docker run --rm -it dogkeeper886/ollama37-builder bash
```

When you have access inside your newly instantiated Docker environment (`dogkeeper886/ollama37-builder`):

1. Navigate to the source directory:
    ```sh
    cd /usr/local/src \
        && git clone https://github.com/dogkeeper886/ollama37 \
        && cd ollama37 
    ```
2. Set up your build and compile it using CMake along with GCC (as our custom compiled version):
    ```bash
    CC=/usr/local/bin/gcc CXX=/usr/local/bin/g++ cmake -B build \
        && cmake --build build
    ```
3. Lastly, go ahead and compile the project using Go (also utilizing our custom-built version), ensuring you have enabled modules for compatibility:
    ```bash
    go build -o ollama .
    ```

## 🎯 Contributing

We're thrilled to welcome your contributions! Should you encounter any issues or have ideas for improving this Docker image, please submit them as an issue on the GitHub repository.

We are committed to continually enhancing our projects and appreciate all feedback. Thank you!