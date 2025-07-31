"""
Streamlit PDF Analysis and Document Generation Application

This application provides a web interface for PDF analysis and document generation
using the smol agents framework with OpenAI integration.
"""

import streamlit as st
import os
import sys
import yaml
import tempfile
import json
from typing import Optional, Dict, Any
from pathlib import Path

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import smol agents components
from smolagents import CodeAgent
from smolagents.models import OpenAIServerModel

# Import custom tools
from tools import AIPDFTool, ExcelGeneratorTool
from tools.excel_generator import SimpleExcelGeneratorTool
from tools.word_generator import SimpleWordGeneratorTool
import traceback

# Configure Streamlit page
st.set_page_config(
    page_title="Analyse PDF & Générateur de Documents 📄",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def initialize_agent(model_name: str = None, max_steps: int = 10) -> Optional[CodeAgent]:
    """
    Initialize the smol agent with OpenRouter integration and custom tools.
    
    Args:
        model_name (str): OpenRouter model to use (defaults to secrets config)
        max_steps (int): Maximum reasoning steps for the agent
        
    Returns:
        CodeAgent: Initialized agent instance or None if failed
    """
    try:
        # Get API key and default model from secrets
        api_key = st.secrets["openrouter"]["api_key"]
        if model_name is None:
            model_name = st.secrets["openrouter"]["default_model"]
        
        # Initialize OpenRouter model (OpenAI-compatible API)
        model = OpenAIServerModel(
            api_base="https://openrouter.ai/api/v1",
            model_id=model_name,
            api_key=api_key,
            max_tokens=32768
        )
        
        
        # Create agent with custom tools
        agent = CodeAgent(
            model=model,
            tools=[
                AIPDFTool(),
                ExcelGeneratorTool(),
                SimpleExcelGeneratorTool(),
                SimpleWordGeneratorTool(),

            ],
            max_steps=max_steps,
            verbosity_level=1,
            additional_authorized_imports=[
                "pandas", "numpy", "json", "os", "tempfile"
            ]
        )
        
        return agent
        
    except Exception as e:
        tb = traceback.format_exc()
        st.error(f"Erreur lors de l'initialisation de l'agent : {str(e)}\n\nTraceback:\n{tb}")
        return None

def load_prompts() -> Optional[Dict[str, Any]]:
    """Load custom prompt templates from YAML file."""
    try:
        with open("prompts.yaml", 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        st.warning(f"Impossible de charger les prompts personnalisés : {str(e)}. Utilisation des prompts par défaut.")
        return None

def create_temp_directory() -> str:
    """Create and return the temporary directory path."""
    temp_dir = os.path.join(os.getcwd(), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

def handle_multiple_pdf_uploads(uploaded_files) -> list:
    """Handle multiple PDF file uploads and return list of file paths with metadata."""
    processed_files = []
    
    if uploaded_files is not None:
        # Create temp directory if it doesn't exist
        temp_dir = create_temp_directory()
        
        for uploaded_file in uploaded_files:
            if uploaded_file.type == "application/pdf":
                # Save uploaded file to temporary location
                temp_file_path = os.path.join(temp_dir, f"uploaded_{uploaded_file.name}")
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.read())
                
                processed_files.append({
                    'path': temp_file_path,
                    'name': uploaded_file.name,
                    'size': uploaded_file.size if hasattr(uploaded_file, 'size') else 0
                })
            else:
                st.error(f"Le fichier '{uploaded_file.name}' n'est pas un fichier PDF et sera ignoré.")
    
    return processed_files

def process_user_input(agent: CodeAgent, user_input: str, pdf_path: Optional[str] = None, pdf_files: Optional[list] = None) -> str:
    """
    Process user input with the agent and return the response.
    
    Args:
        agent: The initialized smol agent
        user_input: User's query or instruction
        pdf_path: Optional single PDF file path (for backward compatibility)
        pdf_files: Optional list of PDF file info dictionaries
        
    Returns:
        str: Agent's response
    """
    try:
        # Prepare the input context
        context = {"user_input": user_input}
        
        # Handle multiple files or single file
        if pdf_files and len(pdf_files) > 0:
            context["pdf_available"] = True
            context["pdf_files"] = pdf_files
            
            # For multiple PDF analysis tasks
            if len(pdf_files) > 1:
                file_list = "\n".join([f"- {file_info['name']}: {file_info['path']}" for file_info in pdf_files])
                formatted_input = f"""
J'ai plusieurs documents PDF téléchargés :
{file_list}

Demande de l'utilisateur : "{user_input}"

Veuillez utiliser l'outil d'analyse PDF pour analyser le contenu de chaque PDF individuellement et répondre à la demande de l'utilisateur. Si la demande implique de comparer des fichiers ou de créer des documents (Excel ou Word), utilisez les outils appropriés pour les générer.

Plusieurs PDF sont disponibles pour l'analyse. Traitez chaque fichier selon les besoins de la demande de l'utilisateur.
"""
            else:
                # Single file from the list
                file_info = pdf_files[0]
                formatted_input = f"""
J'ai un document PDF téléchargé au chemin : {file_info['path']}

Demande de l'utilisateur : "{user_input}"

Veuillez utiliser l'outil d'analyse PDF pour analyser le contenu du PDF et répondre à la demande de l'utilisateur. Si la demande implique de créer des documents (Excel ou Word), utilisez les outils appropriés pour les générer.

PDF disponible pour l'analyse à : {file_info['path']}
"""
        elif pdf_path:
            # Backward compatibility for single file
            context["pdf_available"] = True
            context["pdf_path"] = pdf_path
            formatted_input = f"""
J'ai un document PDF téléchargé au chemin : {pdf_path}

Demande de l'utilisateur : "{user_input}"

Veuillez utiliser l'outil d'analyse PDF pour analyser le contenu du PDF et répondre à la demande de l'utilisateur. Si la demande implique de créer des documents (Excel ou Word), utilisez les outils appropriés pour les générer.

PDF disponible pour l'analyse à : {pdf_path}
"""
        else:
            # For general document generation tasks
            formatted_input = f"""
Demande de l'utilisateur : "{user_input}"

Veuillez aider l'utilisateur avec sa demande liée aux documents. Utilisez les outils appropriés pour créer des documents Excel ou Word selon les besoins.
"""
        
        # Execute the agent
        response = agent.run(formatted_input)
        
        return str(response)
        
    except Exception as e:
        return f"Erreur lors du traitement de la demande : {str(e)}"

def display_file_downloads():
    """Display available files for download."""
    temp_dir = create_temp_directory()
    
    if os.path.exists(temp_dir):
        files = [f for f in os.listdir(temp_dir) if f.endswith(('.xlsx', '.docx'))]
        
        if files:
            st.subheader("📥 Fichiers Générés")
            
            for file in files:
                file_path = os.path.join(temp_dir, file)
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        file_data = f.read()
                    
                    # Determine file type for proper MIME type
                    if file.endswith('.xlsx'):
                        mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        icon = "📊"
                    else:
                        mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                        icon = "📄"
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"{icon} {file}")
                    with col2:
                        st.download_button(
                            label="Télécharger",
                            data=file_data,
                            file_name=file,
                            mime=mime_type,
                            key=f"download_ooo_{file}"
                        )

def main():
    """Main application function."""
    if 'first_run' not in st.session_state:
        st.session_state.first_run = True
        # Clean up temp directory on app start
        temp_dir = create_temp_directory()
        if os.path.exists(temp_dir):
            for f in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, f)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception:
                    pass
        agent = initialize_agent("qwen/qwen3-coder:free", 10)
        if agent:
            st.session_state.agent = agent
            # st.success("✅ Agent initialized successfully!")
        else:
            st.error("❌ Échec de l'initialisation de l'agent...")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Model selection
        model_name = st.selectbox(
            "Modèle OpenRouter",
            ["qwen/qwen3-coder:free", "google/gemini-2.0-flash-exp:free", "meta-llama/llama-3.1-8b-instruct:free"],
            index=0,
            help="Sélectionnez le modèle OpenRouter à utiliser"
        )
        
        # Max steps configuration
        max_steps = st.slider(
            "Étapes de Raisonnement Max",
            min_value=5,
            max_value=20,
            value=10,
            help="Nombre maximum d'étapes de raisonnement pour l'agent"
        )
        
        # Initialize agent button
        if st.button("🚀 Mettre à Jour l'Agent"):
            with st.spinner("Initialisation de l'agent..."):
                agent = initialize_agent(model_name, max_steps)
                if agent:
                    st.session_state.agent = agent
                    st.success("✅ Agent initialisé avec succès !")
                else:
                    st.error("❌ Échec de l'initialisation de l'agent")
        
        # Display agent status
        if 'agent' in st.session_state:
            st.success("🤖 Agent Prêt")
        else:
            st.warning("⚠️ Agent non initialisé")
    
    # Main interface
    if 'agent' not in st.session_state:
        st.info("👈 Veuillez configurer et initialiser l'agent dans la barre latérale pour commencer.")
        return
    
    with st.container(border=True):
        # Initialize chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": "👋 Bienvenue ! Je suis là pour vous aider à analyser des PDF et générer des documents. Veuillez télécharger un fichier PDF ou poser une question.",
                    })
        # Display chat history using st.chat_message
        if st.session_state.chat_history:
            # Application header
            st.title("📄 Analyse de PDF & Générateur de Documents")
            st.markdown("""
            Bienvenue ! Cette application vous permet de :
            - 📖 **Analyser des documents PDF** et poser des questions sur leur contenu
            - 📊 **Générer des fichiers Excel** avec des données, des tableaux et des graphiques
            - 📝 **Créer des documents Word** avec une mise en forme professionnelle
            - 🔄 **Convertir entre différents formats de documents**
            """)
            st.divider()
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    if message["role"] == "user" and message.get("has_pdfs"):
                        pdf_files = message.get("pdf_files", [])
                        if len(pdf_files) == 1:
                            st.caption(f"📎 Fichier PDF joint: {pdf_files[0]['name']}")
                        elif len(pdf_files) > 1:
                            st.caption(f"📎 {len(pdf_files)} fichiers PDF joints:")
                            for file_info in pdf_files:
                                st.caption(f"  • {file_info['name']}")
                    # Legacy support for old messages with single PDF
                    elif message["role"] == "user" and message.get("has_pdf"):
                        st.caption("📎 Fichier PDF joint")
        
        # Chat input with file acceptance
        user_input = st.chat_input(
            "Écrivez un message et/ou joignez un fichier PDF",
            accept_file="multiple",
            file_type=["pdf"]
        )
        
        # Process chat input
        if user_input:

            # Handle both text and file input
            message_text = user_input.get("text", "")
            uploaded_files = user_input.get("files", None)
            
            processed_files = []
            if uploaded_files:
                processed_files = handle_multiple_pdf_uploads(uploaded_files)
            
            if message_text.strip() or processed_files:
                # Add user message to chat history immediately
                user_message = {
                    "role": "user",
                    "content": message_text if message_text.strip() else f"{len(processed_files)} fichier(s) PDF téléchargé(s) pour analyse",
                    "has_pdfs": len(processed_files) > 0,
                    "pdf_files": processed_files
                }
                st.session_state.chat_history.append(user_message)
                
                # Display the user message immediately
                with st.chat_message("user"):
                    st.markdown(user_message["content"])
                    if user_message.get("has_pdfs"):
                        if len(processed_files) == 1:
                            st.caption(f"📎 Fichier PDF joint : {processed_files[0]['name']}")
                        else:
                            st.caption(f"📎 {len(processed_files)} fichiers PDF joints :")
                            for file_info in processed_files:
                                st.caption(f"  • {file_info['name']}")
                
                # Process with agent and show response for each PDF
                with st.chat_message("assistant"):
                    if processed_files:
                        # Check if user wants to compare multiple files or process them individually
                        if len(processed_files) > 1 and any(keyword in message_text.lower() for keyword in ['compare', 'difference', 'différence', 'comparer', 'vs', 'versus']):
                            # Process all files together for comparison
                            with st.spinner(f"Comparaison de {len(processed_files)} fichiers..."):
                                combined_response = process_user_input(
                                    st.session_state.agent,
                                    message_text if message_text.strip() else "Veuillez comparer ces fichiers PDF",
                                    pdf_files=processed_files
                                )
                                st.markdown(combined_response)
                        else:
                            # Process each PDF individually
                            all_responses = []
                            for i, file_info in enumerate(processed_files):
                                with st.spinner(f"Traitement de {file_info['name']}..."):
                                    file_response = process_user_input(
                                        st.session_state.agent,
                                        message_text if message_text.strip() else "Veuillez analyser ce fichier PDF",
                                        pdf_files=[file_info]
                                    )
                                    
                                    # Display response with file identification
                                    st.markdown(f"### 📄 Analyse pour : {file_info['name']}")
                                    st.markdown(file_response)
                                    all_responses.append(f"**{file_info['name']}:**\n{file_response}")
                                    
                                    if i < len(processed_files) - 1:
                                        st.divider()
                            
                            # Combine all responses for chat history
                            combined_response = "\n\n---\n\n".join(all_responses)
                    else:
                        # No files, just process the text
                        with st.spinner("Traitement de votre demande..."):
                            combined_response = process_user_input(
                                st.session_state.agent,
                                message_text,
                                None
                            )
                            st.markdown(combined_response)
                            # After processing, check for new generated files and display download buttons
                            temp_dir = create_temp_directory()
                            existing_files = set([msg.get("file_name") for msg in st.session_state.chat_history if msg.get("file_name")])
                            current_files = set([f for f in os.listdir(temp_dir) if f.endswith(('.xlsx', '.docx'))])

                            new_files = current_files - existing_files
                            for file in new_files:
                                file_path = os.path.join(temp_dir, file)
                                with open(file_path, 'rb') as f:
                                    file_data = f.read()
                                if file.endswith('.xlsx'):
                                    mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                                    icon = "📊"
                                else:
                                    mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                                    icon = "📄"
                                st.download_button(
                                    label=f"{icon} Télécharger {file}",
                                    data=file_data,
                                    file_name=file,
                                    mime=mime_type,
                                    key=f"download_{file}"
                                )
                                # Optionally, add to chat history to avoid duplicate download buttons
                                st.session_state.chat_history.append({
                                    "role": "system",
                                    "content": f"Fichier généré disponible : {file}",
                                    "file_name": file
                                })
                    
                    # Add agent response to chat history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": combined_response
                    })
                    st.rerun()

        
        # Clear chat button
        if st.session_state.chat_history:
            if st.button("🗑️ Effacer l'Historique du Chat"):
                st.session_state.chat_history = []
                st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": "👋 Bienvenue ! Je suis là pour vous aider à analyser des PDF et générer des documents. Veuillez télécharger un fichier PDF ou poser une question.",
                    })
                
                st.rerun()
    with st.expander("📂 Fichiers Générés", expanded=False):
        
        # Generated files section (below chat)
        display_file_downloads()
    
if __name__ == "__main__":
    main()