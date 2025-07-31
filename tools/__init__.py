"""
Tools package for the Streamlit PDF Analysis application.

This package contains custom tools for the smol agents framework:
- PDF analysis tool
- AI PDF analysis tool (with OpenRouter API integration)
- Excel document generation tool
- Word document generation tool
"""

from .excel_generator import ExcelGeneratorTool
from .ai_pdf_tool import AIPDFTool

__all__ = [
    'ExcelGeneratorTool',
    'AIPDFTool',
]