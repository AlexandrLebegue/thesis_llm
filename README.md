# PDF Analysis & Document Generator

A powerful Streamlit application that combines PDF analysis with document generation capabilities using the smol agents framework and OpenAI integration.

## 🌟 Features

### 📖 PDF Analysis
- Upload PDF files through the web interface
- Ask questions about PDF content
- Extract key information and data points
- Summarize documents automatically
- Quote relevant sections from PDFs

### 📊 Excel Generation
- Create structured spreadsheets with data and charts
- Professional formatting with headers and styling
- Support for multiple worksheets
- Automatic chart generation (bar, line, pie charts)
- Data visualization capabilities

### 📝 Word Document Creation
- Generate formatted Word documents
- Professional styling and layout
- Tables, lists, and structured content
- Multiple sections and headings
- Document properties and metadata

### 🤖 AI-Powered Intelligence
- Uses OpenAI models (GPT-4, GPT-3.5-turbo) via smol agents
- Specialized prompts for document tasks
- Intelligent tool selection based on user requests
- Conversational interface for complex tasks

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
streamlit run streamlit_app.py
```

3. **Configure the application:**
   - Enter your OpenAI API key in the sidebar
   - Select your preferred model (GPT-4 recommended)
   - Click "Initialize Agent"

## 📋 Usage Guide

### Basic Workflow

1. **Initialize the Agent**
   - Enter your OpenAI API key in the sidebar
   - Choose your preferred model
   - Click "🚀 Initialize Agent"

2. **Upload PDF (Optional)**
   - Use the file uploader to select a PDF
   - The system will confirm successful upload

3. **Make Requests**
   - Type your request in the text area
   - Click "🚀 Submit Request"
   - View the AI response and any generated files

4. **Download Generated Files**
   - Generated Excel and Word files appear in the sidebar
   - Click "Download" to save files locally

### Example Requests

#### PDF Analysis
```
- "What are the main topics discussed in this PDF?"
- "Extract all financial data from the document"
- "Summarize the key findings and recommendations"
- "What dates and numbers are mentioned in the document?"
```

#### Document Generation
```
- "Create an Excel file with monthly sales data for 2024"
- "Generate a Word report summarizing the PDF content"
- "Create a comparison table in Excel format"
- "Make a professional report with charts and tables"
```

#### Combined Tasks
```
- "Analyze this PDF and create an Excel summary with key data points"
- "Extract the financial information and generate a Word report"
- "Create both Excel and Word versions of the data analysis"
```

## 🛠️ Technical Architecture

### Core Components

1. **Streamlit Interface** (`streamlit_app.py`)
   - Web-based user interface
   - File upload handling
   - Chat interface
   - Download management

2. **Custom Tools** (`tools/`)
   - `PDFAnalysisTool`: PDF content extraction and analysis
   - `ExcelGeneratorTool`: Advanced Excel file creation
   - `WordGeneratorTool`: Professional Word document generation
   - `SimpleExcelGeneratorTool`: Basic Excel export
   - `SimpleWordGeneratorTool`: Basic Word document creation

3. **Specialized Prompts** (`prompts.yaml`)
   - Document analysis prompts
   - Excel generation guidelines
   - Word formatting instructions
   - Error handling prompts

4. **Smol Agents Integration**
   - OpenAI model integration
   - Tool orchestration
   - Reasoning and planning capabilities

### File Structure
```
├── streamlit_app.py              # Main Streamlit application
├── prompts.yaml                  # Specialized AI prompts
├── requirements.txt              # Python dependencies
├── tools/                        # Custom tools directory
│   ├── __init__.py
│   ├── pdf_analysis_tool.py      # PDF analysis capabilities
│   ├── excel_generator.py        # Excel file generation
│   └── word_generator.py         # Word document generation
├── temp/                         # Generated files storage
├── project_plan.md               # Development plan
└── README_streamlit_app.md       # This documentation
```

## 🔧 Configuration Options

### Model Selection
- **GPT-4**: Best quality, higher cost
- **GPT-4-turbo**: Faster processing, good quality
- **GPT-3.5-turbo**: Fastest, most economical

### Agent Parameters
- **Max Reasoning Steps**: 5-20 (default: 10)
- **Verbosity Level**: Controls output detail
- **Tool Selection**: Automatic based on request type

## 📊 Supported File Formats

### Input
- **PDF**: Any text-based PDF file
- **Text**: Direct text input for document generation

### Output
- **Excel (.xlsx)**: Structured data, charts, multiple sheets
- **Word (.docx)**: Formatted documents, tables, professional styling

## 🎯 Use Cases

### Business & Professional
- **Report Generation**: Convert PDFs to structured reports
- **Data Analysis**: Extract and visualize data from documents
- **Document Conversion**: Transform content between formats
- **Executive Summaries**: Create concise summaries from lengthy documents

### Academic & Research
- **Literature Review**: Analyze research papers and create summaries
- **Data Extraction**: Pull key information from academic documents
- **Citation Analysis**: Extract references and create bibliographies
- **Research Reports**: Generate formatted research documentation

### Personal & Administrative
- **Document Organization**: Structure and format personal documents
- **Financial Analysis**: Extract and analyze financial information
- **Meeting Notes**: Convert meeting transcripts to structured formats
- **Project Documentation**: Create professional project reports

## 🔍 Troubleshooting

### Common Issues

1. **Agent Initialization Failed**
   - Verify OpenAI API key is correct
   - Check internet connection
   - Ensure sufficient API credits

2. **PDF Upload Issues**
   - Confirm file is in PDF format
   - Check file size (large files may take longer)
   - Ensure PDF contains extractable text

3. **File Generation Errors**
   - Check temp directory permissions
   - Verify sufficient disk space
   - Review error messages in the interface

4. **Performance Issues**
   - Reduce max reasoning steps for faster processing
   - Use GPT-3.5-turbo for quicker responses
   - Break complex requests into smaller tasks

### Error Messages

- **"No text could be extracted"**: PDF may be image-based or corrupted
- **"API request failed"**: Check API key and internet connection
- **"Tool execution failed"**: Review request format and try again

## 🔐 Security & Privacy

### Data Handling
- PDF content is processed temporarily and not stored permanently
- Generated files are stored locally in the temp directory
- API communications are encrypted via HTTPS

### API Key Security
- API keys are handled securely through Streamlit's session state
- Keys are not logged or stored permanently
- Use environment variables for production deployments

### File Management
- Temporary files are created in the local temp directory
- Users should regularly clean up generated files
- No data is sent to external services except OpenAI API

## 🚀 Advanced Usage

### Custom Prompts
Modify `prompts.yaml` to customize AI behavior:
- Adjust analysis depth and focus
- Change document formatting preferences
- Add domain-specific instructions

### Tool Customization
Extend functionality by modifying tools:
- Add new document formats
- Implement custom data processing
- Create specialized analysis tools

### Integration Options
- Deploy on cloud platforms (Streamlit Cloud, Heroku, AWS)
- Integrate with existing document workflows
- Connect to enterprise document management systems

## 📈 Performance Tips

### Optimization Strategies
1. **Request Optimization**
   - Be specific about requirements
   - Break complex tasks into steps
   - Use simple tools for basic tasks

2. **Model Selection**
   - Use GPT-4 for complex analysis
   - Use GPT-3.5-turbo for simple tasks
   - Adjust max steps based on complexity

3. **File Management**
   - Regularly clean temp directory
   - Monitor disk space usage
   - Optimize PDF file sizes before upload

## 🤝 Contributing

### Development Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `python -m pytest` (if tests are added)
4. Start development server: `streamlit run streamlit_app.py`

### Adding New Features
- Create new tools in the `tools/` directory
- Update prompts in `prompts.yaml`
- Modify the main interface in `streamlit_app.py`
- Update documentation

## 📄 License

This project is provided as-is for educational and development purposes.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review error messages carefully
3. Verify configuration settings
4. Test with simpler requests first

---

**Built with ❤️ using Streamlit, smol agents, and OpenAI**