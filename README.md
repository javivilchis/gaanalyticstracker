# Google Analytics 4 (GA4) Data Extraction Script

![Python Version](https://img.shields.io/badge/logo-python-blue?logo=python&logoColor=f5f5f5) [![Build Status](https://img.shields.io/badge/logo-github-green?logo=github&logoColor=f5f5f5)](https://github.com)

This project contains a Python script to programmatically extract data from Google Analytics 4 using the [Google Analytics Data API (v1beta)](https://developers.google.com/analytics/devguides/reporting/data/v1).

---

## 🛠️ Prerequisites

Before running the script, you must set up your Google Cloud and Analytics credentials:

1.  **Create a Google Cloud Project**: Visit the [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
2.  **Enable the API**: Search for and enable the **Google Analytics Data API**.
3.  **Create a Service Account**:
    - Navigate to **IAM & Admin > Service Accounts** and click **Create Service Account**.
    - Once created, go to the **Keys** tab, click **Add Key > Create new key**, and select **JSON**.
    - Save this file in your project directory as `credentials.json`.
4.  **Grant Access in GA4**:
    - Open your [Google Analytics Admin](https://analytics.google.com/) panel.
    - Go to **Property Settings > Property Access Management**.
    - Add the service account email (found in your JSON file) with **Viewer** or **Editor** access.
5.  **Get your Property ID**: Find your **Property ID** in GA4 under **Property Settings > Property Details** (top right corner).

---

## 🚀 Getting Started

### 1. Set Up a Python Virtual Environment

It is recommended to use a virtual environment to manage your dependencies.

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**\*MACos/Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Required Libraries

Install the official Google Analytics client library:

```bash
pip install google-analytics-data pandas matplotlib python-dotenv
```

### 3. Configure the Script

Update the following variables in your main.py (or equivalent) script:
**PROPERTY_ID:** Your 9-digit GA4 Property ID.
**credentials.json:** Ensure the path to your JSON key file is correct.

### 🏃 Running the Code

Execute the script from your terminal:

```bash
python main.py
```
