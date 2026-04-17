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

#### v2.0.3 (2026-04-13)

This release marks a major milestone — not just for new model support, but for the maturity of the project's CI/CD pipeline. Over thousands of lines of test infrastructure now guard every upstream port, powered by a dual-judge system where an Ollama instance itself serves as the LLM Judge.

**Why an LLM Judge?** Model responses are naturally non-deterministic — the same prompt can produce different but equally valid answers. Traditional pattern matching is too brittle for this. The LLM Judge evaluates whether model output is *semantically reasonable*, catching genuine regressions (broken templates, garbled output, missing capabilities) without false-flagging normal variation. This has been critical for maintaining stability across multiple upstream ports.

**New Model Support:**
- **Gemma 4** — Full parser, renderer, and model architecture port
- **FunctionGemma** — Template and tool-calling support
- **Qwen3.5 Ollama Engine** — Ported with DeltaNet recurrent state

**Bug Fixes:**
- Fixed Qwen3.5 attn_gate shape mismatch for 27b variant
- Fixed ghost GPU allocations — llama engine was leaking VRAM on model unload
- Reduced vision image reservation for non-flash GPUs (K80)
- Fixed Ministral-3 template function and YaRN RoPE parameters

**CI/CD & Testing:**
- Throughput benchmark tool with standalone tok/s measurement and CI workflow
- Debug logging framework with `OLLAMA_DEBUG` toggle
- GPU count validation and nvidia-smi memory profiling in tests
- `num_predict` guard to prevent infinite generation in test runs

**Throughput Benchmark (Tesla K80, measured by GitHub Actions CI on v2.0.3):**

| Model | GPUs | Prompt tok/s | Gen tok/s | VRAM |
|-------|------|-------------|-----------|------|
| ministral-3:3b | 1 | 1155.91 | 17.29 | 3466 MiB |
| gemma3:4b | 1 | 68.48 | 15.24 | 4785 MiB |
| gpt-oss:20b | 2 | 128.96 | 14.80 | 14938 MiB |
| qwen3-vl:30b | 2 | 28.04 | 13.33 | 20864 MiB |
| gemma4:e4b | 1 | 64.88 | 13.12 | 9796 MiB |
| **gemma4:26b** | **2** | **42.64** | **12.09** | **18583 MiB** |
| qwen3-vl:8b | 1 | 32.48 | 9.74 | 7617 MiB |
| qwen3.5:9b | 1 | 31.17 | 7.66 | 7529 MiB |
| deepseek-r1:14b | 2 | 12.56 | 5.41 | 12803 MiB |
| **gemma3:27b** | **2** | **8.62** | **3.02** | **19916 MiB** |
| deepseek-r1:32b | 3 | 5.74 | 2.66 | 24581 MiB |
| qwen3.5:27b | 2 | 8.59 | 2.61 | 21150 MiB |

Gemma 4 at 26B generates **4× faster** than Gemma 3 at 27B on identical hardware — the headline story of v2.0.3.

#### v1.4.0 (2025-08-10)

This release introduces GPT-OSS support and delivers critical stability improvements for Tesla K80 GPUs:

**New Model Support:**
- **GPT-OSS**: Open-source GPT implementation with optimized context management for smaller VRAM GPUs

**Tesla K80 Improvements:**
- Fixed VMM pool crashes through proper memory alignment granularity
- Resolved multi-GPU model switching deadlocks and silent failures
- Enhanced BF16 compatibility for Compute Capability 3.7 devices
- Optimized Docker build performance with parallel compilation

This release ensures reliable operation across single and multi-GPU Tesla K80 configurations while expanding model support with the latest open-source innovations.

#### v1.3.0 (2025-07-01)

This release expands model support while maintaining full Tesla K80 compatibility:

**New Model Support:**
- **Qwen2.5-VL**: Multi-modal vision-language model for image understanding
- **Gemma 3n**: Efficient models designed for execution on everyday devices such as laptops, tablets or phones

**Documentation Updates:**
- Updated installation guides for Tesla K80 compatibility

#### v1.2.0 (2025-05-06)

This release introduces support for Qwen3 models, marking a significant step in our commitment to staying Tesla K80 with leading open-source language models. Testing includes successful execution of Gemma 3 12B, Phi-4 Reasoning 14B, and Qwen3 14B, ensuring compatibility with models expected to be widely used in May 2025.

## LLM-Powered Workflow Exploration

Beyond simply running Ollama, this project explores integrating LLMs into practical workflows. The `dify/` directory contains ready-to-use Dify workflow definitions (BugBlitz, QualityQuest, ER2Test, etc.) and the `prompts/` directory provides prompt templates — both are designed for users who interact with Ollama through a web UI rather than an AI coding agent.

* **Dify Integration:** Leveraging Dify's platform for building LLM applications (chatbots, agents, workflows) and integrating them with Ollama.
* **VS Code 'Continue' Plugin & Model Context Protocol (MCP):**  Investigating filesystem operations and data manipulation within LLM workflows using the 'Continue' plugin and the Model Context Protocol.
* **N8N Integration:**  Exploring the use of N8N, a visual automation platform, to orchestrate LLM-powered quality assurance tasks.
* **auto-webui Usage:** Investigating the integration of LLMs into automated web UI testing and analysis pipelines.

For users of Claude Code and AI coding agents, see [ai-qa-workflow](https://github.com/dogkeeper886/ai-qa-workflow) — the actively maintained evolution of these workflows, with full test lifecycle automation from Jira to TestLink.

## Setup and Running

**Prerequisites:**

* NVIDIA K80 GPU
* NVIDIA Tesla K80 driver installed and configured.
* NVIDIA Container Runtime installed and configured.
* Docker installed and running.

**Steps:**

1.  **Pull the Docker Image:**  To get the pre-built Ollama environment, pull the image from Docker Hub using this command:

    ```bash
    docker pull dogkeeper886/ollama37:v2.0.3
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

1. **Ollama37 v2.0.3: Running Gemma 4 & Qwen 3.5 on Tesla K80 GPUs**
   - [Watch here](https://youtu.be/B1PbLr3rUhc)
   Description: Walkthrough of the v2.0.3 release — new model support for Gemma 4, Qwen 3.5, FunctionGemma, and Ministral-3, with benchmarks measured on K80 hardware via the new GitHub Actions throughput tool. Live demo runs Gemma 4 26B through a Dify chat interface while a Grafana dashboard tracks VRAM and temperature across both GPUs in real time. Headline finding: Gemma 4 at 26B generates 4× faster than Gemma 3 at 27B on the same hardware.

2. **Why I Run AI on 10-Year-Old GPUs: Ollama K80 Docker Build System & CI/CD Pipeline**
   - [Watch here](https://youtu.be/iYxgGsPu5rM)
   Description: A deep dive into our modern AI CI/CD pipeline built entirely on legacy Nvidia K80 GPUs. Covers the two-stage Docker build system (Rocky Linux 8, CUDA 11.4, GCC 10, CMake 4.0, Go 1.25.3), self-hosted GitHub Actions runner with a custom test framework featuring Simple Judge (exit code/pattern matching) and LLM Judge (Gemma3 12B for test validation), creating a full AI-powered pipeline from build to model compatibility testing.

3. **GPT-OSS 20B on a Tesla K80 – Real Time Performance Analysis**
   - [Watch here](https://youtu.be/58azOBe_tGM)
   Description: Experience the power of GPT-OSS 20B running on a Tesla K80 GPU with real-time performance analysis. This video demonstrates the latest open-source GPT implementation with optimized context management, showcasing its capabilities on K80 hardware.

4. **How to Build an AI Home Lab with a Tesla Graphic Card**
   - [Watch here](https://youtu.be/-5gMpGI49PA)
   Description: Want to dive into the exciting world of AI development at home? In this video, I'm walking you through the entire process of building an AI lab using a Tesla graphic card – from setup to running models! This isn's your typical gaming build; we're tackling the unique challenges these cards present.

5. **We Fixed Our LLM Test!**
   - [Watch here](https://youtu.be/TUwjZ20rr-U)
   Description: We messed up! In our last video, we tested big AI models (called LLMs), but we found some mistakes in how we did it. So, we're back with a new test! This time, we're checking out smaller, but still powerful, AI models: Ollama 3.2 Vision 11B, Gemma 3 12B, and Phi-4 14B. These models are easier to run on regular computers.

6. **How to Set Up Ollama for Tesla K80**
   - [Watch here](https://youtu.be/nJ0W6xCdp_c)
   Description: 🚀 Set up Ollama with a Tesla K80 – Full Guide for CUDA 11.4 + GCC 10 + Go + CMake 💻 In this video, I'll walk you step-by-step through setting up Ollama to run on an NVIDIA Tesla K80 GPU using CUDA 11.4. We will handle all the heavy lifting — from installing the correct NVIDIA CUDA Toolkit suitable for a K80 Building GCC 10 from source (to meet compatibility needs) Compiling CMake manually, and Go installation Prepping your system with everything needed for Ollama development workflows 🔧 Whether you're setting up an dev box using similar hardware or just want to explore LLMs on Tesla K80, this guide has got you covered.

7. **LLM-Powered Text Refinement with Dify Studio**
   - [Watch here](https://youtu.be/FcAjriKB74M)
   Description: This video showcases how to use a Large Language Model (LLM) integrated with Dify Studio for text refinement tasks. We'll walk through the setup, demonstrate real-time processing of text for quality improvement, and evaluate response accuracy and coherence. Whether you're an AI enthusiast or looking to enhance your writing workflow, this tutorial will provide valuable insights.

8. **DeepSeek-R1:32B on Intel i3-14100 CPU - Real-Time Performance Analysis**
   - [Watch here](https://youtu.be/aCqV4hmMxtM)
   Description: In this video, we dive into the real-time performance of DeepSeek-R1:32B running on an Intel i3-14100 CPU. Following our previous showcase on a Tesla K80 GPU, we now evaluate its capabilities on a more accessible platform.

9. **DeepSeek-R1:32b in Action on Tesla K80 GPU - Real-Time Performance Showcase**
   - [Watch here](https://youtu.be/k8jHMa_cHCI)
   Description: Whether you're a developer looking to optimize AI models on similar hardware, or just curious about high-performance computing setups, this video offers valuable insights. From technical setup tips to performance benchmarks, we cover it all. What You'll See: - NVIDIA-SMI Status - Ollama Log Insights - Real-Time Response Time Analysis

## License

This project is licensed under the [MIT License](LICENSE).

