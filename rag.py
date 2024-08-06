import streamlit as st
from config.globals import SPEAKER_TYPES, initial_prompt
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json
import os

# Load environment variables
load_dotenv()

# Retrieve API key from environment variable
google_api_key = os.getenv("GOOGLE_API_KEY")

# Function to load text from JSON file
def load_text_from_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    text = "\n\n".join([item['titre'] + "\n" + "\n".join(item['paragraphes']) for item in data])
    return text

# Function to initialize vector index from text
def initialize_vector_index(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)
    texts = text_splitter.split_text(text)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_index = Chroma.from_texts(texts, embeddings).as_retriever()
    return vector_index

# Function to get response from the model
def get_response(question):
    vector_index = st.session_state.vector_index
    docs = vector_index.get_relevant_documents(question)
    
    prompt_template = """
    Answer the question as detailed as possible from the provided context,
    make sure to provide all the details. If the answer is not in
    the provided context, just say, "The answer is not available in the context."
    Don't provide incorrect information.\n\n
    Context:\n {context}?\n
    Question:\n{question}\n
    Answer:
    """
    
    prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, api_key=google_api_key)
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
    return response['output_text']

# Set up the Streamlit app configuration
st.set_page_config(
    page_title="DATA 354 RAG App",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state for chat history and JSON context
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [initial_prompt]
if 'json_context' not in st.session_state:
    st.session_state.json_context = None

# Load JSON file and initialize vector index
json_path = 'articles.json'  # Remplacez par le chemin de votre fichier JSON
text = load_text_from_json(json_path)
vector_index = initialize_vector_index(text)
st.session_state.vector_index = vector_index
st.session_state.json_context = text

# Function to clear chat history
def clear_chat_history():
    st.session_state.chat_history = [initial_prompt]

# Sidebar configuration
with st.sidebar:
    st.title('🔍 DATA 354 Chatbot')
    st.write('This chatbot uses the Gemini Pro API with RAG capabilities.')
    st.button('Clear Chat History', on_click=clear_chat_history, type='primary')

# Main interface
st.header('Data354 RAG Chatbot')
st.subheader('Ask questions about articles from Ecofin!')

# Display the welcome prompt if chat history is only the initial prompt
if len(st.session_state.chat_history) == 1:
    with st.chat_message(SPEAKER_TYPES.BOT, avatar="🔍"):
        st.write(initial_prompt['content'])

# Get user input
prompt = st.chat_input("Ask a question about articles", key="user_input")

# Handle the user prompt and generate response
if prompt:
    # Add user prompt to chat history
    st.session_state.chat_history.append({'role': SPEAKER_TYPES.USER, 'content': prompt})
    
    # Display chat messages from the chat history
    for message in st.session_state.chat_history[1:]:
        with st.chat_message(message["role"], avatar="👤" if message['role'] == SPEAKER_TYPES.USER else "🔍"):
            st.write(message["content"])
    
    # Get the response using the QA pipeline
    with st.spinner(text='Generating response...'):
        response_text = get_response(prompt)
        st.session_state.chat_history.append({'role': SPEAKER_TYPES.BOT, 'content': response_text})
    
    # Display the bot response
    with st.chat_message(SPEAKER_TYPES.BOT, avatar="🔍"):
        st.write(response_text)

# Add footer for additional information or credits
st.markdown("""
<hr>
<div style="text-align: center;">
    <small>Powered by Gemini Pro API | Developed by Ahoulou Assemien Jean-Eudes</small>
</div>
""", unsafe_allow_html=True)


def get_response(question):
    # Liste de questions et réponses générales
    general_responses = {
        "bonjour": "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
        "comment ça va": "Je suis un bot, donc je n'ai pas de sentiments, mais je suis là pour vous aider !",
        "merci": "De rien ! N'hésitez pas à poser d'autres questions.",
    }
    
    # Vérifier si la question est dans les questions générales
    question_lower = question.lower()
    for key in general_responses:
        if key in question_lower:
            return general_responses[key]
    
    # Récupérer les documents pertinents pour la question
    vector_index = st.session_state.vector_index
    docs = vector_index.get_relevant_documents(question)
    
    prompt_template = """
    Answer the question as detailed as possible from the provided context,
    make sure to provide all the details. If the answer is not in
    the provided context, just say, "The answer is not available in the context."
    Don't provide incorrect information.\n\n
    Context:\n {context}\n
    Question:\n{question}\n
    Answer:
    """
    
    prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, api_key=google_api_key)
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
    return response['output_text']

