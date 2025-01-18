from typing import List
import google.generativeai as genai
from langchain.embeddings.base import Embeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
import pandas as pd
import os

class CustomGoogleEmbeddings(Embeddings):
    """Custom Embedding Class for Google Generative AI"""
    def __init__(self, model='models/embedding-001'):
        self.client = genai
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            text = text[:2048] if len(text) > 2048 else text
            try:
                embedding = self.client.embed_content(
                    model=self.model,
                    content=text,
                    task_type="retrieval_document"
                )['embedding']
                embeddings.append(embedding)
            except Exception as e:
                print(f"Embedding error: {e}")
                embeddings.append([0.0] * 768)
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        text = text[:2048] if len(text) > 2048 else text
        try:
            return self.client.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_query"
            )['embedding']
        except Exception as e:
            print(f"Query embedding error: {e}")
            return [0.0] * 768

class RAGProcessor:
    def __init__(self):
        self.embeddings = CustomGoogleEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", ",", " ", ""]
        )
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')
        
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from PDF with focus on structured content"""
        try:
            pdf_reader = PdfReader(pdf_file)
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n\n"
                
            # Basic structure preservation
            # Look for common P&L statement patterns
            lines = text.split('\n')
            structured_text = ""
            for line in lines:
                # Identify potential financial entries (e.g., "Revenue: $1000")
                if any(keyword in line.lower() for keyword in ['revenue', 'profit', 'loss', 'expenses', 'income', 'cost', 'margin', 'ebitda', 'tax']):
                    structured_text += f"FINANCIAL_ENTRY: {line}\n"
                else:
                    structured_text += line + "\n"
                    
            return structured_text
            
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def process_documents(self, pdf_files: List[str]) -> FAISS:
        """Process multiple PDF documents and create vector store"""
        combined_text = ""
        for pdf in pdf_files:
            combined_text += self.extract_text_from_pdf(pdf)
            
        # Create more focused chunks
        text_chunks = self.text_splitter.split_text(combined_text)
        
        # Create vector store
        try:
            vector_store = FAISS.from_texts(text_chunks, embedding=self.embeddings)
            return vector_store
        except Exception as e:
            print(f"Error creating vector store: {e}")
            raise

    def generate_response(self, question: str, vector_store: FAISS) -> str:
        """Generate response using RAG approach"""
        # Retrieve relevant context
        docs = vector_store.similarity_search(question, k=4)
        context = "\n".join([doc.page_content for doc in docs])
        
        prompt = f"""
        You are a financial analyst assistant. Using the following financial data context, 
        answer the question accurately and professionally. Include specific numbers and 
        calculations when relevant.
        
        Context: {context}
        
        Question: {question}
        
        If the context doesn't contain enough information to answer accurately, 
        please state that clearly. Focus on P&L related information and financial metrics.
        When providing financial figures, please format them clearly with appropriate units 
        (e.g., "$1,234,567" or "1.2M" for millions).
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {e}"