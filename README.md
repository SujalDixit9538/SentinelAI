---
title: SentinelAI SOC Dashboard
emoji: 🛡️
colorFrom: gray
colorTo: red
sdk: gradio
app_file: app.py
python_version: "3.11"
pinned: false
---
# SentinelAI
Network Intrusion Detection System with watsonx.ai integration.


# 🛡️ SentinelAI: Hybrid Network Intrusion Detection System

## 📌 Project Overview
SentinelAI is an enterprise-grade, high-speed Network Intrusion Detection System (NIDS) designed to process streaming network packets with minimal latency. It utilizes a hybrid AI architecture, combining an O(F) Machine Learning model for real-time anomaly detection with IBM watsonx.ai Generative AI for human-readable SOC mitigation reporting.

## 🚀 Technical Architecture
* **Real-Time Threat Detection:** Utilizes a memory-safe `SGDClassifier` optimized for streaming environments with O(F) inference time.
* **Hybrid LLM Integration:** Connects mathematical threat telemetry directly to **IBM Granite (watsonx.ai)** to automatically generate human-in-the-loop incident mitigation reports.
* **Cloud-Resilient Storage:** Integrates `ibm-boto3` for IBM Cloud Object Storage, featuring a graceful local-fallback mechanism to ensure the system never crashes during cloud outages.
* **Human-in-the-Loop (HITL) Online Learning:** Allows security analysts to correct false positives in the Gradio dashboard, triggering instantaneous matrix weight recalibrations via partial-fit algorithms.

## 🛠️ Tech Stack
* **Machine Learning:** `scikit-learn`, `numpy`, `pandas`
* **Generative AI:** `ibm-watsonx-ai` (IBM Granite Foundation Models)
* **Cloud Infrastructure:** IBM Cloud Code Engine, IBM Cloud Object Storage
* **Interface:** `gradio`

## ⚙️ How to Run Locally
1. Clone the repository and install dependencies: `pip install -r requirements.txt`
2. Duplicate `.env.example` and rename it to `.env`. Insert your IBM Cloud credentials.
3. Launch the SOC Dashboard: `python dashboard/gradio_app.py`
