# 📊 Data Analyst Agent (Powered by Together AI)

An AI-powered Streamlit application that acts as your personal **data analyst**. It allows you to upload various data files (like `.csv`, `.xlsx`, `.pdf`, `.docx`, `.txt`, `.jpg`, and `.png`) and ask questions about your data using natural language.

This agent leverages the **Together AI API** with advanced open-source LLMs like `Llama-4-Maverick-17B` to:
- Answer data-related queries
- Generate SQL queries
- Create visualizations with `matplotlib` or `seaborn`
- Provide analysis of structured or extracted data

---

## 🚀 Features

- 🧠 **Natural Language Interface**  
  Ask questions like _"What is the average sales by region?"_ or _"Plot a bar chart of monthly revenue."_

- 📂 **Multiformat File Support**  
  Supports `.csv`, `.xlsx`, `.pdf`, `.docx`, `.txt`, and images (`.jpg`, `.png`) with OCR.

- 🧼 **Automatic Preprocessing**  
  Extracts data into a pandas DataFrame for analysis regardless of the original file type.

- 📈 **Visualization Execution**  
  Detects and runs Python visualization code returned by the model inside the app.

---

## 🧑‍💻 Tech Stack

- **Streamlit** – for the user interface  
- **Together API** – to access LLMs like `Llama-4-Maverick-17B`  
- **Pandas / PandasQL** – for tabular data processing  
- **Matplotlib / Seaborn** – for chart generation  
- **Tesseract OCR** – to extract text from images  
- **PDFPlumber / python-docx** – for reading `.pdf` and `.docx` files

---

## 📦 Installation

```bash
git clone https://github.com/your-username/data-analyst-agent.git
cd data-analyst-agent

# Install dependencies
pip install -r requirements.txt

