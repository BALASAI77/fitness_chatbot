# fitness_chatbot
Overview
This project implements a Fitness Chatbot that provides personalized workout and diet plans based on user input. The chatbot utilizes the Gemini model from Google's Generative AI to generate responses based on user queries and input text from a collection of fitness-related documents stored in a ChromaDB database. Users can interact with the chatbot by entering workout queries and selecting options for personalized plans based on their body type, fitness goals, and dietary restrictions.

Requirements
Python 3.x
Streamlit
ChromaDB
Google Generative AI
PyPDF2 (for PDF text extraction)
Setup
Install the required Python libraries using pip:

code:
pip install streamlit chromadb google-generativeai PyPDF2
Obtain a Google API key for accessing the Generative AI services and set it as an environment variable named GOOGLE_API_KEY.

Usage
Run the Streamlit application by executing the following command in the terminal:


code:

streamlit run fitness_chatbot.py
Once the application is running, users can interact with the Fitness Chatbot through the provided text input fields and buttons.

Functionality
Workout Input:
Users can enter workout queries in the text input field labeled "Enter what workout."
After entering a workout query, they can click the "Submit" button to receive a response from the chatbot.
Personalized Plans:
Users can select their body type, fitness goals, and dietary restrictions using the dropdown and multiselect input fields provided.
Clicking the "Generate Response" button triggers the chatbot to generate personalized workout and diet plans based on the selected options.
The chatbot utilizes the Gemini model to generate responses by combining user input with text extracted from fitness-related documents stored in a ChromaDB database.
Files
fitness_chatbot.py: Main Python script implementing the Fitness Chatbot application.
README.md: Detailed readme file providing information about the project, requirements, setup instructions, usage guidelines, and functionality.
Additional Notes
Ensure that the directory containing PDF files for text extraction is correctly specified in the data_dir variable within the fitness_chatbot.py script.
The generate_unique_collection_name() function generates a unique name for the ChromaDB collection based on the current timestamp and a random string. This ensures that each run of the application creates a new collection to store extracted text data.
The get_gemini_response() function queries the ChromaDB collection for similar documents based on user input and generates responses using the Gemini model.
This README file provides an overview of the Fitness Chatbot project, including setup instructions, usage guidelines, and functionality details. Users can refer to this document for guidance on running the application and understanding its features.
