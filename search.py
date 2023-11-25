import streamlit as st
import pandas as pd
import pyodbc
import openai

# Set up OpenAI credentials
openai.api_type = "azure"
openai.api_key = "3a669b6667bf46bca2cb1f3d2e0d467e"
openai.api_base = "https://gptopenai0.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
# or from sqlalchemy import create_engine

# Function to connect to the database
def get_connection():
    server = 'blog0.database.windows.net' 
    database = 'bloguser' 
    username = 'saroot' 
    password = '766587La' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    # or use sqlalchemy: engine = create_engine(f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server")
    return cnxn

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
        menu_items={
            'Get Help': 'https://www.gov.br/inpi/pt-br',
            'About': "This app is designed to guide you through the fundamental procedures of safeguarding your trademarks, patents, industrial designs, geographical indications, computer programs, circuit topographies, and technology contracts with the Brazilian Patent and Trademark Office (BRPTO)."
        }
    )


    with st.sidebar:
        st.image("https://i.pinimg.com/736x/b8/4b/3a/b84b3a2604e591c53777cd190576ba55--image-search.jpg")   
        ""
        "Vector Similarity Search with Azure SQL database and OpenAI"
        "Vector databases are gaining quite a lot of interest lately. Using text embeddings and vector operations makes extremely easy to find similar “things”. Things can be articles, photos, products…everything. As one can easily imagine, this ability is great to easily implement suggestions in applications. From providing suggestions on similar articles or other products that may be of interest, to quickly finding and grouping similar items, the applications are many."
        ""
        ""
        "Created by [Lawrence Teixeira](https://www.linkedin.com/in/lawrenceteixeira/)"
        ""
        ""
        "Please note that this is only an example to demonstrate the results of a vector similarity search."    
    
    st.title("Vector Similarity Search with Azure SQL")

    # Text input for search query
    search_query = st.text_input("Enter your search query:")

    if st.button("Search"):
        # Connection to the database
        cnxn = get_connection()
        
        #vector = get_embeddings(search_query)
        
        # Definir a stored procedure e a consulta SQL
        stored_procedure = f"EXEC dbo.SearchNews '{search_query}'"

        # Executar a stored procedure
        cnxn.execute(stored_procedure)
        
        query = "SELECT r.cosine_distance, r.published, r.category, r.author, r.title, r.full_content, r.url FROM result R order by r.cosine_distance DESC"

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