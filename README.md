# ollama-k80-lab

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This project explores running Ollama, a local LLM runner, with an NVIDIA K80 GPU. The goal is to assess performance, explore limitations, and demonstrate the potential of this combination for local LLM experimentation and deployment. We also investigate the usage of Dify for building LLM applications and the Model Context Protocol (MCP) with VS Code's Continue plugin for filesystem operations.

## Motivation

* **Local LLM Exploration:** Ollama simplifies running Large Language Models locally. This project leverages Ollama's ease of use with the power of a GPU.
* **K80 Utilization:** The NVIDIA K80, while an older GPU, remains a viable option for LLM inference, particularly for smaller to medium-sized models.
* **Dify Integration:** Dify provides a robust framework for building LLM applications (chatbots, agents, etc.). We aim to demonstrate seamless integration between Ollama and Dify for rapid prototyping and deployment.
* **Cost-Effective Experimentation:** Running LLMs locally avoids the costs associated with cloud-based APIs, enabling broader access and experimentation.

## Modified Version

This repository includes a customized version of Ollama, specifically optimized for running on an NVIDIA K80 GPU. This build incorporates specific configurations to address potential compatibility issues with the K80 architecture. For more details, contributions, and the full build process, visit our GitHub page:
[ollama37](https://github.com/dogkeeper886/ollama37)

**Key Features of the Custom Build:**

*  **CUDA 11.4 Support:** The build is configured to work with CUDA Toolkit 11.4, which is a common and well-supported version for the K80.
*  **GCC 10 Compatibility:** We built GCC 10 from source to ensure compatibility with the Ollama build process.
*  **CMake Manual Compilation:** CMake was compiled manually to avoid potential issues with pre-built binaries.
*  **Go Installation:** The project includes instructions for installing Go, a key component of the Ollama build.

## Setup and Running

**Prerquisites:**

*  NVIDIA K80 GPU
*  CUDA Toolkit 11.4
*  GCC 10 (or later)
*  Go (version compatible with Ollama - check Ollama documentation)
*  CMake
*  Git

**Steps:**

1. Clone the repository: `git clone https://github.com/dogkeeper886/ollama37`
2. Follow the instructions in the `ollama37` repository for building and installing Ollama.

## Video Showcase

Check out these videos showcasing different aspects of running Ollama on a Tesla K80 GPU:

1. **DeepSeek-R1:32b Performance Showcasing**
   - [Watch here](https://youtu.be/k8jHMa_cHCI)
   Description: Whether you’re a developer looking to optimize AI models on similar hardware, or just curious about high-performance computing setups, this video offers valuable insights. From technical setup tips to performance benchmarks, we cover it all.

2. **How to Set Up Ollama for Tesla K80**
   - [Watch here](https://youtu.be/nJ0W6xCdp_c)
   Description: 🚀 Set up Ollama with a Tesla K80 – Full Guide for CUDA 11.4 + GCC 10 + Go + CMake 💻 In this video, I’ll walk you step-by-step through setting up Ollama to run on an NVIDIA Tesla K80 GPU using CUDA 11.4. We will handle all the heavy lifting — from installing the correct NVIDIA CUDA Toolkit suitable for a K80 Building GCC 10 from source (to meet compatibility needs) Compiling CMake manually, and Go installation Prepping your system with everything needed for Ollama development workflows 🔧 Whether you're setting up an dev box using similar hardware or just want to explore LLMs on Tesla K80, this guide has got you covered.

## License

This project is licensed under the [MIT License](LICENSE).
