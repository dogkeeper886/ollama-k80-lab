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

### 📦 Version History

#### v1.3.0 (2025-07-01)

This release expands model support while maintaining full Tesla K80 compatibility:

**New Model Support:**
- **Qwen2.5-VL**: Multi-modal vision-language model for image understanding
- **Qwen3 Dense & Sparse**: Enhanced Qwen3 model variants
- **Improved MLLama**: Better support for Meta's LLaMA models

**Documentation Updates:**
- Updated installation guides for Tesla K80 compatibility
- Enhanced Docker Hub documentation with latest model information

#### v1.2.0 (2025-05-06)

This release introduces support for Qwen3 models, marking a significant step in our commitment to staying Tesla K80 with leading open-source language models. Testing includes successful execution of Gemma 3 12B, Phi-4 Reasoning 14B, and Qwen3 14B, ensuring compatibility with models expected to be widely used in May 2025.

## LLM-Powered Workflow Exploration

Beyond simply running Ollama, this project explores integrating LLMs into practical workflows. Here's a breakdown of the tools and techniques being investigated:

* **Dify Integration:** Leveraging Dify's platform for building LLM applications (chatbots, agents, workflows) and integrating them with Ollama.
* **VS Code 'Continue' Plugin & Model Context Protocol (MCP):**  Investigating filesystem operations and data manipulation within LLM workflows using the 'Continue' plugin and the Model Context Protocol.
* **N8N Integration:**  Exploring the use of N8N, a visual automation platform, to orchestrate LLM-powered quality assurance tasks.
* **auto-webui Usage:** Investigating the integration of LLMs into automated web UI testing and analysis pipelines.

## Setup and Running

**Prerequisites:**

* NVIDIA K80 GPU
* NVIDIA Tesla K80 driver installed and configured.
* NVIDIA Container Runtime installed and configured.
* Docker installed and running.

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

1. **How to Build an AI Home Lab with a Tesla Graphic Card**
   - [Watch here](https://youtu.be/-5gMpGI49PA)
   Description: Want to dive into the exciting world of AI development at home? In this video, I'm walking you through the entire process of building an AI lab using a Tesla graphic card – from setup to running models! This isn's your typical gaming build; we're tackling the unique challenges these cards present.

2. **We Fixed Our LLM Test!**
   - [Watch here](https://youtu.be/TUwjZ20rr-U)
   Description: We messed up! In our last video, we tested big AI models (called LLMs), but we found some mistakes in how we did it. So, we’re back with a new test! This time, we're checking out smaller, but still powerful, AI models: Ollama 3.2 Vision 11B, Gemma 3 12B, and Phi-4 14B. These models are easier to run on regular computers.

3. **How to Set Up Ollama for Tesla K80**
   - [Watch here](https://youtu.be/nJ0W6xCdp_c)
   Description: 🚀 Set up Ollama with a Tesla K80 – Full Guide for CUDA 11.4 + GCC 10 + Go + CMake 💻 In this video, I’ll walk you step-by-step through setting up Ollama to run on an NVIDIA Tesla K80 GPU using CUDA 11.4. We will handle all the heavy lifting — from installing the correct NVIDIA CUDA Toolkit suitable for a K80 Building GCC 10 from source (to meet compatibility needs) Compiling CMake manually, and Go installation Prepping your system with everything needed for Ollama development workflows 🔧 Whether you're setting up an dev box using similar hardware or just want to explore LLMs on Tesla K80, this guide has got you covered.

4. **LLM-Powered Text Refinement with Dify Studio**
   - [Watch here](https://youtu.be/FcAjriKB74M)
   Description: This video showcases how to use a Large Language Model (LLM) integrated with Dify Studio for text refinement tasks. We'll walk through the setup, demonstrate real-time processing of text for quality improvement, and evaluate response accuracy and coherence. Whether you're an AI enthusiast or looking to enhance your writing workflow, this tutorial will provide valuable insights.

5. **DeepSeek-R1:32B on Intel i3-14100 CPU - Real-Time Performance Analysis**
   - [Watch here](https://youtu.be/aCqV4hmMxtM)
   Description: In this video, we dive into the real-time performance of DeepSeek-R1:32B running on an Intel i3-14100 CPU. Following our previous showcase on a Tesla K80 GPU, we now evaluate its capabilities on a more accessible platform.

6. **DeepSeek-R1:32b in Action on Tesla K80 GPU - Real-Time Performance Showcase**
   - [Watch here](https://youtu.be/k8jHMa_cHCI)
   Description: Whether you’re a developer looking to optimize AI models on similar hardware, or just curious about high-performance computing setups, this video offers valuable insights. From technical setup tips to performance benchmarks, we cover it all. What You'll See: - NVIDIA-SMI Status - Ollama Log Insights - Real-Time Response Time Analysis

## License

This project is licensed under the [MIT License](LICENSE).

