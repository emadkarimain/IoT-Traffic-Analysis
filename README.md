# 📡 Global-Scale Public IoT Traffic Analysis

![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)
![Protocol](https://img.shields.io/badge/Protocol-MQTT-green.svg)
![Data](https://img.shields.io/badge/Data-286k_Messages-orange.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)

## 📖 Executive Summary
This project represents a bridge between **Network Engineering** and **Big Data Analytics**. Moving beyond theoretical simulations, I engineered a high-concurrency Python ingestion engine to analyze the "wild" behavior of the global IoT ecosystem.

We successfully monitored **6 major public MQTT brokers** simultaneously across Europe and Asia (including HiveMQ, Mosquitto, and EMQX), capturing and benchmarking over **286,253 real-time messages** in a single session.

> **Objective:** To empirically analyze the trade-offs between Reliability (QoS) and Latency in public IoT infrastructures.

---

## ⚙️ Technical Architecture

The core of this project is a **Multi-threaded Asynchronous Logger** capable of handling high-throughput message bursts without blocking.

### The Pipeline
1.  **Discovery Phase:** Scanned legacy datasets (`.pkl`) to identify "Active Topics" (e.g., `tele/#`, `zigbee2mqtt/#`) rather than listening blindly.
2.  **Ingestion Engine:** A Python script utilizing `paho-mqtt` client threads.
    * **Concurrency:** Spawns independent threads for each broker to ensure network latency on one connection does not affect others.
    * **Wildcard Strategy:** Subscribed to `root/#` trees based on the discovery phase to maximize capture rate.
3.  **Analytics Layer:** Processed raw CSV logs using `Pandas` for cleaning and `Seaborn` for visualization.

---

## 📊 Key Empirical Findings

### 1. Speed Over Reliability (The "Fire-and-Forget" Standard)
Analysis of the `QoS` (Quality of Service) flags revealed a unanimous industry preference:
* **100% of captured traffic utilized QoS 0.**
* **Implication:** Public IoT deployments prioritize battery life and bandwidth over guaranteed delivery.

### 2. Protocol Dominance
* **JSON (67%)** is the de facto standard for payloads, prioritizing interoperability.
* **Plain String (21%)** and **Numeric (12%)** legacy microcontrollers or educational kits mostly use formats.

### 3. Infrastructure Bottlenecks
Benchmarking revealed critical differences in broker architecture:
* **HiveMQ** demonstrated superior handling of anonymous wildcard traffic.
* **Mosquitto** implementations enforced strict Access Control Lists (ACLs), throttling connection attempts significantly compared to commercial counterparts.

*(For detailed charts and statistical breakdowns, see the [Full Technical Report](reports/Professional_Report.pdf))*

---

## 📂 Repository Structure

```text
├── data/
│   ├── mqtt_captured_data.csv       # Raw dataset (286k+ rows)
│   ├── clean_topics.txt             # List of targeted topic roots
│   └── *.pkl                        # Intermediate serialized objects
│
├── notebooks/                       # Jupyter Notebooks (The Analysis Pipeline)
│   ├── 01_Topic_Discovery.ipynb     # Step 1: Extracting topics from raw dumps
│   ├── 02_Topic_Selection.ipynb     # Step 2: Filtering top 50 active topic trees
│   ├── 03_Data_Acquisition_Engine.ipynb # Step 3: Main Multi-threaded Logger
│   └── 04_Traffic_Analysis.ipynb    # Step 4: Visualization & Statistical Analysis
│
├── reports/
│   ├── Professional_Report.pdf      # 📄 FINAL TECHNICAL REPORT
│   ├── generate_report.py           # Automated PDF generator script
│   └── *.png                        # Generated charts used in the report
│
├── .gitignore                       # System file configuration
└── requirements.txt                 # Project dependencies
```

## 🛠️ Installation & Usage
### Prerequisites
    Python 3.8+
    Pip package manager

### 1. Clone the Repository
    git clone [https://github.com/YOUR_USERNAME/IoT-Traffic-Analysis.git](https://github.com/YOUR_USERNAME/IoT-Traffic-Analysis.git)
    cd IoT-Traffic-Analysis

### 2. Install Dependencies
    pip install -r requirements.txt

### 3. Run the Analysis
    To reproduce the findings, run the notebooks in sequential order inside the notebooks/ folder.

## To generate the PDF report automatically:
    python reports/generate_report.py

## 👨‍💻 Author

Emad Karimian Shamsabadi

. M.Sc. Telecommunication Engineering - Politecnico di Milano

. Course: Lab Experience in Communication Networks

. Focus: IoT Protocols, Network Analysis, Data Engineering

   
