
"""
Created on Tue Feb 20 23:23:10 2024

@author: M.BALASAI
"""

from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
import os
import google.generativeai as genai
import streamlit as st

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
prompt='You are given a question asked by the user and the text taken from a source. Your job is to give a meaningful answer based on the text to the user and add some information if you definitely know about it, or else do not add anything. Give the answer in a user-friendly way.'

# fun for loading the directory
def load_pdf(data_dir):
    loader = DirectoryLoader(data_dir, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

#fun for extracting the text
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=90)
    text_chunks = text_splitter.split_documents(extracted_data)
    return [chunk.page_content for chunk in text_chunks]

#creating chromadb collection
def create_or_get_collection(client, collection_name):
    if collection_name in client.list_collections():
        # If collection exists, return it
        return client.get_collection(collection_name)
    else:
        # If collection does not exist, create it
        collection = client.create_collection(
            name=collection_name,
            embedding_function=embedding_func,
            metadata={"hnsw:space": "cosine"},
        )
        return collection

CHROMA_DATA_PATH = "chroma_data/"
#EMBED_MODEL = "all-MiniLM-L6-v2"

#for generating unique chromadb instance
import datetime
import random
import string

def generate_unique_collection_name(base_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_string = ''.join(random.choices(string.ascii_lowercase, k=4))
    return f"{base_name}_{timestamp}_{random_string}"

# Usage:
COLLECTION_NAME = generate_unique_collection_name("demo_docs6002")
print(COLLECTION_NAME)



client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
embedding_func = embedding_functions.DefaultEmbeddingFunction()



data_dir = "C:/Users/M.SAI/Desktop/fit_bot_ast/books"  # Replace with the directory containing PDF files
extracted_data = load_pdf(data_dir)
text_chunks = text_split(extracted_data)

# Create or get the collection
collection = create_or_get_collection(client, COLLECTION_NAME)

# Add documents to the collection
collection.add(
    documents=text_chunks,
    ids=[f"id{i}" for i in range(len(text_chunks))],
    metadatas=[{"set": g} for g in range(len(text_chunks))]
)




def get_gemini_response(input_text):
    global prompt, collection

    # Query the collection for similar documents based on user input
    query_results = collection.query(
        query_texts=[input_text],
        n_results=1,
    )
    print('enterer')
    if query_results:
        text1 = query_results["documents"][0][0]
        text = text1.replace('\n', ' ').lower()

        # Generate response using Gemini
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt, text, input_text])
        response_text = response.text
        print('res got')

        return response_text
    else:
        return "No results found."
    
    
st.title('Fitness Chatbot')

user_input1 = st.text_input('Enter what workout:')
button_clicked = st.button('Submit')

if button_clicked:
    respo2 = get_gemini_response(user_input1)
    st.write(respo2)

st.header('personalised plans')
body_types = ['Ectomorph', 'Mesomorph', 'Endomorph']
fitness_goals = ['Build Muscle', 'Lose Weight', 'Improve Endurance']
dietary_restrictions = ['Vegetarian', 'Vegan', 'Gluten-Free']

# Creating dropdowns for body type, fitness goals, and dietary restrictions
selected_body_type = st.selectbox('Select Body Type:', body_types)
selected_fitness_goals = st.multiselect('Select Fitness Goals:', fitness_goals)
selected_dietary_restrictions = st.multiselect('Select Dietary Restrictions:', dietary_restrictions)


button_ = st.button('generate response')

if button_:
    text2 = f"Body Type: {selected_body_type}, Fitness Goals: {', '.join(selected_fitness_goals)}, Dietary Restrictions: {', '.join(selected_dietary_restrictions)}"
    response  = get_gemini_response(text2)
    response_text = response.text
    st.write(response_text)
