# ollama-k80-lab: Exploring Local LLMs & Workflow Automation

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This project is a laboratory for experimenting with running Ollama, a local Large Language Model (LLM) runner, on NVIDIA K80 GPUs. While the K80 is an older card, this project aims to overcome its hardware limitations through custom compilation, demonstrating the potential for accessible and cost-effective LLM experimentation. Beyond basic execution, this project explores leveraging LLMs to significantly improve software quality assurance workflows, integrating with tools like Dify, VS Code's 'Continue' plugin, N8N, and auto-webui.  This is more than just getting Ollama running; it's about integrating LLMs into practical development workflows.

## Motivation

* **Democratizing Local LLM Access:** Ollama simplifies running LLMs locally, but compatibility can be a barrier. This project aims to remove those barriers, making LLM experimentation more accessible, even with older hardware.
* **K80 Hardware Utilization:** The NVIDIA K80 offers a viable option for LLM inference, especially for smaller to medium-sized models. This project seeks to maximize its utility.
* **LLM-Powered Software Quality Assurance:** This project investigates how LLMs can revolutionize software quality assurance, automating tedious tasks and improving overall efficiency.
* **Cost-Effective Experimentation:** Local LLM execution avoids the costs associated with cloud-based APIs, enabling wider access and experimentation for developers and researchers.
* **Career Development:** This project serves as a practical platform for exploring and developing skills in prompt engineering, LLM application development, and workflow automation within a software quality assurance context.

## Customized Ollama Build

This repository includes a customized version of Ollama, specifically optimized for running on an NVIDIA K80 GPU. This involves compiling from source with specific configurations to address potential compatibility issues.  For detailed build instructions, contributions, and the full build process, please visit: [ollama37](https://github.com/dogkeeper886/ollama37)

**Key Build Considerations:**

* **CUDA 11.4 Support:** The build is configured to work with CUDA Toolkit 11.4, a common and well-supported version for the K80.
* **GCC 10 Compatibility:** Built from source to ensure compatibility with the Ollama build process.
* **Manual CMake Compilation:** Compiled manually to avoid potential issues with pre-built binaries.
* **Go Installation:** Includes instructions for installing Go, a key component of the Ollama build.

## LLM-Powered Workflow Exploration

Beyond simply running Ollama, this project explores integrating LLMs into practical workflows. Here's a breakdown of the tools and techniques being investigated:

* **Dify Integration:** Leveraging Dify's platform for building LLM applications (chatbots, agents, workflows) and integrating them with Ollama.
* **VS Code 'Continue' Plugin & Model Context Protocol (MCP):**  Investigating filesystem operations and data manipulation within LLM workflows using the 'Continue' plugin and the Model Context Protocol.
* **N8N Integration:**  Exploring the use of N8N, a visual automation platform, to orchestrate LLM-powered quality assurance tasks.
* **auto-webui Usage:** Investigating the integration of LLMs into automated web UI testing and analysis pipelines.

## Setup and Running

**Prerequisites:**

* NVIDIA K80 GPU
* CUDA Toolkit 11.4
* GCC 10 (or later)
* Go (version compatible with Ollama - check Ollama documentation)
* CMake
* Git

**Steps:**

1.  **Pull the Docker Image:**  To get the pre-built Ollama environment, pull the image from Docker Hub using this command:

    ```bash
    docker pull dogkeeper886/ollama37
    ```

2.  **Run the Docker Container:** Start the Ollama container with GPU support using the following command.  This command also exposes Ollama on port 11434, which you'll need to interact with it.

    ```bash
    docker run --runtime=nvidia --gpus all -p 11434:11434 dogkeeper886/ollama37
    ```

    *   `--runtime=nvidia`:  Specifies that the container should use the NVIDIA runtime for GPU acceleration.
    *   `--gpus all`:  Makes all available GPUs accessible to the container.
    *   `-p 11434:11434`: Maps port 11434 on the host machine to port 11434 inside the container.

For detailed build instructions and further customization, refer to the [GitHub repository](ollama37/README.md).

## Video Showcase

Check out these videos showcasing different aspects of running Ollama on a Tesla K80 GPU:

1. **DeepSeek-R1:32b Performance Showcasing**
   - [Watch here](https://youtu.be/k8jHMa_cHCI)
   Description: Whether you’re a developer looking to optimize AI models on similar hardware, or just curious about high-performance computing setups, this video offers valuable insights. From technical setup tips to performance benchmarks, we cover it all.

2. **How to Set Up Ollama for Tesla K80**
   - [Watch here](https://youtu.be/nJ0W6xCdp_c)
   Description: 🚀 Set up Ollama with a Tesla K80 – Full Guide for CUDA 11.4 + GCC 10 + Go + CMake 💻 In this video, I’ll walk you step-by-step through setting up Ollama to run on an NVIDIA Tesla K80 GPU using CUDA 11.4. We will handle all the heavy lifting — from installing the correct NVIDIA CUDA Toolkit suitable for a K80 Building GCC 10 from source (to meet compatibility needs) Compiling CMake manually, and Go installation Prepping your system with everything needed for Ollama development workflows 🔧 Whether you're setting up an dev box using similar hardware or just want to explore LLMs on Tesla K80, this guide has got you covered.

3. **LLM-Powered Text Refinement with Dify Studio**
   - [Watch here](https://youtu.be/FcAjriKB74M)
   Description: This video showcases how to use a Large Language Model (LLM) integrated with Dify Studio for text refinement tasks. We'll walk through the setup, demonstrate real-time processing of text for quality improvement, and evaluate response accuracy and coherence. Whether you're an AI enthusiast or looking to enhance your writing workflow, this tutorial will provide valuable insights.

## License

This project is licensed under the [MIT License](LICENSE).

