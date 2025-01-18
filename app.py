import streamlit as st
from rag import RAGProcessor
import os
from dotenv import load_dotenv
import tempfile

# Load environment variables
load_dotenv()

# Check for API key
if not os.getenv('GOOGLE_API_KEY'):
    st.error("Please set the GOOGLE_API_KEY in your .env file.")
    st.stop()

def initialize_session_state():
    """Initialize session state variables."""
    if "rag_processor" not in st.session_state:
        st.session_state.rag_processor = RAGProcessor()
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None

def save_uploaded_files(uploaded_files):
    """Save uploaded files to a temporary directory and return file paths."""
    try:
        temp_dir = tempfile.mkdtemp()
        file_paths = []

        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            file_paths.append(file_path)

        return file_paths
    except Exception as e:
        st.error(f"Error saving uploaded files: {e}")
        return []

def main():
    st.set_page_config(
        page_title="Finance Buddy",
        page_icon="💰",
        layout="wide"
    )

    initialize_session_state()

    # Main header with emoji
    st.markdown("<div class='main-header'>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align: center;'>💰 Finance Buddy</h1>", 
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("PL_image-removebg-preview.png", use_column_width=True)
        st.title("📄 Document Analysis")
        uploaded_files = st.file_uploader(
            "Upload P&L Documents (PDF)",
            accept_multiple_files=True,
            type=['pdf']
        )

        if uploaded_files and st.button("Process Documents", key="process_docs"):
            with st.spinner("Processing documents..."):
                try:
                    # Save uploaded files and process them
                    file_paths = save_uploaded_files(uploaded_files)
                    if file_paths:
                        st.session_state.vector_store = st.session_state.rag_processor.process_documents(file_paths)
                        st.success("✅ Documents processed successfully!")
                except Exception as e:
                    st.error(f"Error processing documents: {e}")

    # Main content
    st.markdown("""
    💡 **Ask questions about your P&L statements and financial data.**  
    """)

    # Query input
    query = st.text_input("🔍 Ask your question:", key="query")

    if query:
        if not st.session_state.vector_store:
            st.warning("Please upload and process documents first!")
        else:
            with st.spinner("Analyzing..."):
                try:
                    response = st.session_state.rag_processor.generate_response(
                        query,
                        st.session_state.vector_store
                    )
                    st.markdown("### 📋 Response:")
                    st.markdown(f">{response}")
                except Exception as e:
                    st.error(f"Error generating response: {e}")

    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center;'>💼 Built with Streamlit & Google Generative AI</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
