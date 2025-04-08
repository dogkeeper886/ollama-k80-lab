# ollama-k80-lab

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This project explores running Ollama, a local LLM runner, with a NVIDIA K80 GPU and investigates its integration with Dify, a powerful framework for building LLM-powered applications. The goal is to assess performance, explore limitations, and demonstrate the potential of this combination for local LLM experimentation and deployment.

## Motivation

* **Local LLM Exploration:** Ollama makes it incredibly easy to run Large Language Models locally. This project aims to leverage that ease with the power of a GPU.
* **K80 Utilization:** The NVIDIA K80, while older, remains a viable GPU for LLM inference. This project aims to demonstrate its capability for running smaller to medium sized LLMs.
* **Dify Integration:** Dify provides a robust framework for building LLM applications (chatbots, agents, etc.). We want to see how seamlessly Ollama and Dify can work together, allowing us to rapidly prototype and deploy LLM-powered solutions.
* **Cost-Effective Experimentation:** Running LLMs locally avoids the costs associated with cloud-based APIs, enabling broader access and experimentation.

## Modified Version

This repository includes a modified version of Ollama, specifically customized for running on a Tesla K80 GPU. For more details and contributions, visit our GitHub page:

[ollama37](https://github.com/dogkeeper886/ollama37)

This custom build aims to optimize performance and compatibility with the Tesla K80 hardware, ensuring smoother integration and enhanced efficiency in LLM applications.

## Video Showcase

Check out this video showcasing "DeepSeek-R1:32b in Action on Tesla K80 GPU - Real-Time Performance Showcase":

https://youtu.be/k8jHMa_cHCI

**Description:** Whether you’re a developer looking to optimize AI models on similar hardware, or just curious about high-performance computing setups, this video offers valuable insights. From technical setup tips to performance benchmarks, we cover it all.

**What You'll See:**
- NVIDIA-SMI Status
- Ollama Log Insights
- Real-Time Response Time Analysis

## License

This project is licensed under the [MIT License](LICENSE).
