from langchain.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
import pathlib
import requests
import sqlite3 

url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
local_path = pathlib.Path('chinook.db')
DB_FILE = 'chinook.db'
def file_download():
    if local_path.exists():
        print(f"{local_path} already exist in the local path")
    else:
        response = requests.get(url,timeout=60)
        if response.status_code == 200:
            local_path.write_bytes(response.content)
            print(f"Saved the file and saved as {local_path}")
        else:
            print(f"failed with status code: {response.status_code}")
@tool
def sql_table():
    """function is used to define the schema of the tables"""
    conn = sqlite3.connect(DB_FILE)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table = [row[0] for row in cursor.fetchall() if row[0].startswith("sqlite_") ]
        print(f"availables table {table}")
        cursor.execute("SELECT * from Artist limit 5;")
        print(f"{cursor.fetchall()}")

    finally:
        conn.close()
@tool 
def sql_query(query):
    """function which is used to provide the correct query from the table"""
    conn = sqlite3.connect(query)
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return str(result)
    finally:
        conn.close()
if __name__ == '__main__':
    file_download()
    SYSTEM_PROMPT = "You are a useful AI agent whose main purpose is to dealing with the local sqlite."
    MODEL = ChatOllama(model= "gemma4:e4b")
    tools = [sql_table,sql_query]
    agent = create_agent(
        model = MODEL,
        tools = tools,
        system_prompt = SYSTEM_PROMPT
    )
    result = agent.invoke({"messages": [{"role": "user", "content": "Show me the tables in the database"}]})
    print(result["messages"][-1].content)

