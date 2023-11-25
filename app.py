import openai
import pyodbc  # or another SQL connection library

# Set up OpenAI credentials
openai.api_type = "azure"
openai.api_key = "3a669b6667bf46bca2cb1f3d2e0d467e"
openai.api_base = "https://gptopenai0.openai.azure.com/"
openai.api_version = "2023-07-01-preview"

# Connect to your Azure SQL database
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=blog0.database.windows.net;DATABASE=bloguser;'
                      'UID=saroot;PWD=766587La')

def get_embeddings(text):
    # Truncate the text to 8000 characters
    truncated_text = text[:8000]

    response = openai.Embedding.create(input=truncated_text, engine="embeddings")
    embeddings = response['data'][0]['embedding']
    return embeddings


def update_database(article_id, title_vector, content_vector):
    cursor = conn.cursor()

    # Convert vectors to strings
    title_vector_str = str(title_vector)
    content_vector_str = str(content_vector)

    # Update the SQL query to use the string representations
    cursor.execute("""
        UPDATE news
        SET title_vector = ?, content_vector = ?
        WHERE article_id = ?
    """, (title_vector_str, content_vector_str, article_id))
    conn.commit()


def embed_and_update():
    cursor = conn.cursor()
    cursor.execute("SELECT top 20000 article_id, title, full_content FROM news where title_vector is null and full_content is not null and title is not null order by published desc")
    
    title_vector = ""
    content_vector = ""
    
    for row in cursor.fetchall():
        article_id, title, full_content = row
        
        print(f"Embedding article {article_id} - {title}")
        
        title_vector = get_embeddings(title)
        content_vector = get_embeddings(full_content)
        
        update_database(article_id, title_vector, content_vector)

embed_and_update()