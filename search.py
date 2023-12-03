import streamlit as st
import pandas as pd
import pyodbc
import openai
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI credentials from environment variables
openai.api_type = os.getenv('OPENAI_API_TYPE')
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_version = os.getenv('OPENAI_API_VERSION')
# or from sqlalchemy import create_engine

# Function to connect to the database
def get_connection():
    while True:
        try:
            cnxn = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={os.getenv("DB_SERVER")};'
                f'DATABASE={os.getenv("DB_DATABASE")};'
                f'UID={os.getenv("DB_UID")};'
                f'PWD={os.getenv("DB_PWD")}',
                timeout=5
            )
            return cnxn
        except pyodbc.OperationalError:
            print("Connection failed, retrying in 2 seconds...")
            time.sleep(2)

def get_embeddings(text):
    # Truncate the text to 8000 characters
    truncated_text = text[:8000]

    response = openai.Embedding.create(input=truncated_text, engine="embeddings")
    embeddings = response['data'][0]['embedding']
    return embeddings

# Streamlit app
def main():
    
    st.set_page_config(
        page_title="Navigating Vector Operations in Azure SQL for Better Data Insights",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )


    with st.sidebar:
        st.image("https://i.pinimg.com/736x/b8/4b/3a/b84b3a2604e591c53777cd190576ba55--image-search.jpg")   
        ""
        "[Navigating Vector Operations in Azure SQL for Better Data Insights](https://lawrence.eti.br/2023/11/25/navigating-vector-operations-in-azure-sql-for-better-data-insights-a-guide-how-to-use-generative-ai-to-prompt-queries-in-datasets/)"
        "Vector databases are gaining quite a lot of interest lately. Using text embeddings and vector operations makes extremely easy to find similar “things”. Things can be articles, photos, products…everything. As one can easily imagine, this ability is great to easily implement suggestions in applications. From providing suggestions on similar articles or other products that may be of interest, to quickly finding and grouping similar items, the applications are many."
        ""
        ""
        "Source: [Global News Dataset](https://www.kaggle.com/datasets/everydaycodings/global-news-dataset/)" 
        ""
        "Created by [Lawrence Teixeira](https://www.linkedin.com/in/lawrenceteixeira/)"
        ""
        "Please remember, this is merely a sample to illustrate the outcomes of a vector similarity search, as detailed in the preceding article."    
    
    st.title("Vector Similarity Search in Azure SQL")

    # Text input for search query
    search_query = st.text_input("Type here your search:", placeholder="e.g., 'Generative AI: The Future Unveiled'")

    if st.button("Search"):
        # Connection to the database
        cnxn = get_connection()
        
        #vector = get_embeddings(search_query)
        
        # Definir a stored procedure e a consulta SQL
        stored_procedure = f"EXEC dbo.SearchNews '{search_query}'"

        # Executar a stored procedure
        cnxn.execute(stored_procedure)
        
        query = "SELECT r.cosine_distance, r.published, r.category, r.title, r.author, r.full_content, r.url FROM result R order by r.cosine_distance DESC"

        # Executing the query
        df = pd.read_sql(query, cnxn)

        # Displaying results
        if not df.empty:
            st.write("Search Results:")
            st.dataframe(df)
        else:
            st.write("No results found.")

if __name__ == "__main__":
    main()
