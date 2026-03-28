# 💸 PhonePe Pulse Data Analytics Dashboard

### 📊 Project Overview
This project is an end-to-end Data Engineering and Analytics capstone. It extracts unstructured data from the official PhonePe Pulse GitHub repository, transforms it using Python and Pandas, and loads it into a robust local SQLite Database. Finally, it visualizes the geographical and temporal metrics of India's digital payment ecosystem via a live Streamlit web dashboard.

### 🛠️ Technologies Used
* **Python** (Data Extraction, Transformation, and Scripting)
* **Pandas** (Data Manipulation)
* **SQLite3** (Relational Database Management)
* **Streamlit** (Web Dashboard UI)
* **Plotly** (Interactive Geo-Visualizations & Charts)

### 🚀 How to Run Locally
1. Clone this repository.
2. Run `data_extraction.py` to pull the raw JSON data.
3. Run `sql_setup.py` to build and populate the `phonepe_pulse.db` database.
4. Run `streamlit run app.py` to launch the dashboard in your browser.