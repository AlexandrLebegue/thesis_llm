"""
AI PDF Tool for Smol Agents

This tool converts the original tool_ai_pdf.py functionality to work with the smol agents framework.
It allows the agent to extract text from PDF files and query it using AI through OpenRouter API.
"""

import pymupdf as fitz  # PyMuPDF - newer versions use pymupdf import
import requests
import os
from typing import Optional
from smolagents import Tool
import streamlit as st


class AIPDFTool(Tool):
    """
    A tool that allows the agent to extract text from PDF files and query it using AI through OpenRouter API.
    
    This tool combines PDF text extraction with AI analysis to answer questions about PDF content.
    It preserves all the original functionality from tool_ai_pdf.py while adapting it to the smol agents framework.
    """
    
    name = "ai_pdf_analysis"
    description = """
    Extract text from a PDF file and query it using AI through OpenRouter API.
    
    This tool can:
    - Extract text content from PDF files using PyMuPDF
    - Send the extracted content along with a user query to OpenRouter AI
    - Get intelligent responses about the PDF content using Gemini 2.0 Flash model
    - Handle API authentication and error management
    
    Use this tool when you need to analyze PDF documents with AI assistance,
    ask questions about PDF content, or get intelligent summaries and insights.
    """
    
    inputs = {
        "pdf_path": {
            "type": "string",
            "description": "Path to the PDF file to analyze"
        },
        "query": {
            "type": "string", 
            "description": "Question or request about the PDF content"
        }
    }
    
    output_type = "string"
    
    def forward(self, pdf_path: str, query: str) -> str:
        """
        Extract text from a PDF file and query it using AI through OpenRouter API.
        
        Args:
            pdf_path (str): Path to the PDF file
            query (str): Question or request about the PDF content
            api_key (str, optional): OpenRouter API key. If not provided, will use OPENROUTER_API_KEY env var
            
        Returns:
            str: AI response based on the PDF content and query
        """
        
        try:
            # Get API key from Streamlit secrets
            try:
                api_key = st.secrets["openrouter"]["api_key"]
            except (KeyError, AttributeError):
                # Fallback to environment variable if secrets not available
                api_key = os.getenv("OPENROUTER_API_KEY")
            
            if not api_key:
                return "Error: OpenRouter API key is required. Configure it in Streamlit secrets or set OPENROUTER_API_KEY environment variable."
            
            # Check if PDF file exists
            if not os.path.exists(pdf_path):
                return f"Error: PDF file not found: {pdf_path}"
            
            # Extract text from PDF
            pdf_text = self._extract_pdf_text(pdf_path)
            
            if not pdf_text.strip():
                return "Error: No text could be extracted from the PDF file."
            
            # Prepare AI prompt
            prompt = self._create_ai_prompt(pdf_text, query)
            
            # Query the AI
            response = self._query_openrouter_ai(prompt, api_key)
            
            return response
            
        except FileNotFoundError as e:
            return f"Error: {str(e)}"
        except ValueError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Error processing request: {str(e)}"

    def _extract_pdf_text(self, pdf_path: str) -> str:
        """
        Extract text content from a PDF file using PyMuPDF.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text content
        """
        try:
            doc = fitz.open(pdf_path)
            text_content = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_content += f"\n--- Page {page_num + 1} ---\n"
                text_content += page.get_text()
            
            doc.close()
            return text_content
            
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")

    def _create_ai_prompt(self, pdf_text: str, user_query: str) -> str:
        """
        Create an optimized prompt for the AI to analyze PDF content.
        
        Args:
            pdf_text (str): Extracted text from the PDF
            user_query (str): User's question or request
            
        Returns:
            str: Formatted prompt for the AI
        """
        
        preprompt = """You are an expert document analyst with exceptional reading comprehension skills. Your task is to carefully analyze the provided PDF document content and answer questions about it with precision and clarity.

INSTRUCTIONS:
- Read and understand the entire document content thoroughly
- Provide accurate, evidence-based answers using only information from the document
- If information is not available in the document, clearly state this
- Quote relevant sections when appropriate to support your answers
- Maintain objectivity and avoid making assumptions beyond what's written
- Structure your response clearly and concisely

DOCUMENT CONTENT:
"""
        
        user_prompt = f"\n\nUSER QUESTION: {user_query}\n\nPlease provide a comprehensive answer based on the document content above."
        
        return preprompt + pdf_text + user_prompt

    def _query_openrouter_ai(self, prompt: str, api_key: str) -> str:
        """
        Send query to OpenRouter API using Gemini 2.0 Flash model.
        
        Args:
            prompt (str): The complete prompt to send to the AI
            api_key (str): OpenRouter API key
            
        Returns:
            str: AI response
        """
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "google/gemini-2.5-pro",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1000000,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                return "Error: No response received from AI service."
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except KeyError as e:
            raise Exception(f"Unexpected API response format: {str(e)}")

