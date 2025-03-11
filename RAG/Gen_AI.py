import streamlit as st
#import fitz  # PyMuPDF
import os
import json
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_toolkits.conversational_retrieval.openai_functions import create_conversational_retrieval_agent
#from langchain.agents import create_conversational_retrieval_agent
from langchain.tools.retriever import create_retriever_tool
from langchain.llms import HuggingFaceEndpoint
from langdetect import detect

#
# 


# 📂 Répertoire contenant les PDF scrapés

PDF_DIR = "Data_articles/"

st.set_page_config(
    page_title="Tech News Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.header(" Bienvenue  ! ")

#  Modèle IA**
# Ton token Hugging Face

HF_TOKEN = os.getenv("TOKEN_key")
# Modèle IA
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(
    repo_id=MODEL_ID,
    task="text-generation",
    huggingfacehub_api_token=HF_TOKEN,
    max_new_tokens=1024,
    do_sample=True,
    temperature=0.95,
    top_p=0.95
)

#  Chargement et extraction des articles en PDF**
# Charger dynamiquement les PDF du répertoire**
pdf_files = [os.path.join(PDF_DIR, f) for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]

#pdf_files = ["articles_RAG1.pdf", "articles_RAG2.pdf","articles_RAG3.pdf", "articles_RAG4.pdf",
             # "articles_RAG5.pdf","articles_RAG6.pdf","articles_RAG7.pdf"]

# **Extraction du texte des PDF**
documents = []
for pdf_file in pdf_files:
    loader = PyPDFLoader(pdf_file)
    documents.extend(loader.load())

#  Découpage du texte pour optimiser la recherche**  ## découpage en chevauchant
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
split_documents = text_splitter.split_documents(documents)

#  Création de la base de données FAISS pour la recherche**
db = FAISS.from_documents(split_documents, HuggingFaceEmbeddings())

#  Outil de recherche dans les articles**
retriever_tool = create_retriever_tool(
    db.as_retriever(),
    "tech_news_retriever",
    "Recherche et retourne reponses basées sur des articles ."
)

tools = [retriever_tool]

#  Mémoire conversationnelle**
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

#  Création de l'agent conversationnel**
agent = create_conversational_retrieval_agent(llm, tools, memory_key='chat_history', verbose=True)

#  Barre de navigation**
st.sidebar.title(" Navigation")
page = st.sidebar.radio("Aller à", ["🏠 Accueil", "🤖 AI Assistant", "📚 Articles récents utilisés"])

#  Page Accueil**
if page == "🏠 Accueil":
    st.title("📢 Bienvenue sur mon agent conversationel !")

    st.write("Utilisez le menu à gauche pour explorer les actualités tech et poser vos questions.")
    
    st.image("Capture.png", caption="Votre assistant IA pour l'actualité sur agence ECOFIN 📡")

#  Page AI Assistant**
elif page == "🤖 AI Assistant":
    st.title("🧠 Assistant IA")
    st.write("Posez votre question et obtenez une réponse basée sur les derniers articles de agence ECOFIN !")

    # **Zone de saisie de l'utilisateur**
    user_query = st.text_input("💬 Posez votre question  :", placeholder="posez moi une question")

    # **Gestion de la conversation**
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Comment puis-je vous aider ?"}]
    if "memory" not in st.session_state:
        st.session_state['memory'] = memory

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.chat_message("user").write(user_query)
        
        with st.chat_message("assistant"):
            try:
                detected_lang = detect(user_query)  # Détection de la langue
            except:
                detected_lang = "fr"  # Défaut : français si la détection échoue

            #  Ajout du prompt selon la langue détectée
            if detected_lang == "fr":
                user_query = "Réponds uniquement en français : " + user_query
            elif detected_lang == "en":
                user_query = "Answer only in English: " + user_query
            else:
                user_query = "Réponds uniquement en français : " + user_query  # Défaut

            #user_query = "Réponds uniquement en français : " + user_query
            response = agent(user_query)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response['output'])
    st.image("IA_agents.png", caption="Votre assistant IA pour l'actualité sur agence ECOFIN 📡")
#  Page Articles Récents**
elif page == "📚 Articles récents utilisés":
    #st.title("📰 Articles Tech Récents")

    #  **Affichage des extraits des articles PDF**
   # for pdf_file in pdf_files:
    #    doc = fitz.open(pdf_file)
     #   first_page_text = doc[0].get_text("text")[:500]  # Extrait des 500 premiers caractères
      #  st.subheader(f"📄 {pdf_file}")
       # st.write(first_page_text + "...")  # Affiche un extrait du contenu

# **Lecture des liens sauvegardés et affichage dans Streamlit**
#if st.button("Afficher les articles récents"):
    # Charger les liens sauvegardés depuis le fichier JSON
    try:
        with open("article_links.json", "r") as f:
            saved_links = json.load(f)

         #**Afficher les liens dans Streamlit**
        st.title("📰 Articles utilisés")
        st.write("Cliquez sur les liens ci-dessous pour accéder aux articles :")

        for link in saved_links:
            #st.markdown(f"[Lire l'article]({link})")
            st.markdown(f"📄[{link}]({link})")

    except FileNotFoundError:
        st.error("Le fichier contenant les liens des articles est introuvable.")
    #st.image("Capture.png", caption="Votre assistant IA pour l'actualité sur agence ECOFIN 📡")