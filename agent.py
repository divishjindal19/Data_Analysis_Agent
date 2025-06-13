import os
import json
import tempfile
import re
import streamlit as st
import pandas as pd
import pytesseract
import docx
import pandasql as ps
from PIL import Image
from pdfplumber import open as pdf_open
from together import Together

# --- Streamlit UI ---
st.title("📊 Data Analyst Agent")

with st.sidebar:
    st.header("Together API Key")
    together_key = st.text_input("Enter your Together API key:", type="password")
    if together_key:
        os.environ["TOGETHER_API_KEY"] = together_key
        st.success("API key saved!")
    else:
        st.warning("Please enter your Together API key to proceed.")

uploaded_file = st.file_uploader("Upload a data file (.csv, .xlsx, .pdf, .docx, .txt, .jpg, .png)", 
                                 type=["csv", "xlsx", "pdf", "docx", "txt", "jpg", "png"])

# --- Processing different types of files ---
def preprocess_and_save(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()
    df = None
    try:
        if file_type == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_type == 'xlsx':
            df = pd.read_excel(uploaded_file)
        elif file_type == 'pdf':
            text = ""
            with pdf_open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            df = pd.DataFrame({'Text': text.split("\n")})
        elif file_type == 'docx':
            doc = docx.Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
            df = pd.DataFrame({'Text': text.split("\n")})
        elif file_type == 'txt':
            text = uploaded_file.read().decode("utf-8")
            df = pd.DataFrame({'Text': text.split("\n")})
        elif file_type in ['jpg', 'png']:
            img = Image.open(uploaded_file)
            text = pytesseract.image_to_string(img)
            df = pd.DataFrame({'Text': text.split("\n")})
        else:
            st.error("Unsupported file format")
            return None, None, None

        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "temp_uploaded.csv")
        df.to_csv(temp_path, index=False)
        return temp_path, df.columns.tolist(), df

    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None, None, None

# -------AGENT's ROLE--------
if uploaded_file and "TOGETHER_API_KEY" in os.environ:
    temp_path, columns, df = preprocess_and_save(uploaded_file)

    if temp_path and columns and df is not None:
        st.write("Uploaded Data Preview:")
        st.dataframe(df)
        st.write("Detected Columns:", columns)

        user_query = st.text_area("Ask a question about the data:")

        if st.button("Submit Query"):
            if not user_query.strip():
                st.warning("Please enter a query.")
            else:
                try:
                    st.info("🧠 Querying Together.ai...")
                    client = Together(api_key=os.environ["TOGETHER_API_KEY"])

                    
                    prompt = f"""
You are a data analyst assistant. Analyze the DataFrame `df` (provided separately) and respond to the user's query below.
- If SQL is useful, generate a query using SQLite-style SQL and explain it.
- If visualization is requested, return valid Python code using seaborn or matplotlib, enclosed in triple backticks.

User Query: {user_query}
DataFrame preview:
{df.head(5).to_markdown()}
                    """

                    response = client.chat.completions.create(
                        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
                        messages=[{"role": "user", "content": prompt}],
                    )

                    reply = response.choices[0].message.content
                    st.markdown("### Response")
                    st.markdown(reply)

                    # --- Execute any Python code (visualization) returned ---
                    code_blocks = re.findall(r"```python(.*?)```", reply, re.DOTALL)
                    if code_blocks:
                        st.markdown("### Executing Visualization")
                        try:
                            exec(code_blocks[0], {"df": df, "plt": __import__('matplotlib.pyplot'), "sns": __import__('seaborn')})
                            st.pyplot()
                        except Exception as e:
                            st.error(f"Visualization error: {e}")

                except Exception as e:
                    st.error(f"Together API error: {e}")
else:
    st.info("⬅️ Upload a file and enter your Together API key to get started.")
