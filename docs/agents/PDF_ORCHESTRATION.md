# PDF Processing with Intelligent Orchestration

## Overview

The PDF processing agents (Textract and Summarize) have been integrated with the intelligent orchestration system, enabling sophisticated document analysis workflows using AWS Textract and Google Gemini.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Intelligent Orchestration                │
├─────────────────────────────────────────────────────────────┤
│  User Request → Pattern Matching → Workflow Planning →     │
│  Agent Coordination → MCP Communication → Results           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    MCP Agents                              │
├─────────────────┬─────────────────┬─────────────────────────┤
│  Textract Agent │ Summarize Agent │   Other Agents         │
│   (MCP Server)  │   (MCP Server)  │   (MCP Servers)        │
├─────────────────┼─────────────────┼─────────────────────────┤
│ • extract_text  │ • summarize_text│ • time                 │
│ • extract_tables│ • analyze_sent. │ • energy               │
│ • extract_forms │ • extract_key_  │ • db-admin             │
│ • analyze_doc.  │   points        │                        │
└─────────────────┴─────────────────┴─────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Services                        │
├─────────────────────────────────────────────────────────────┤
│  AWS Textract (Document Analysis) + Google Gemini (AI)     │
└─────────────────────────────────────────────────────────────┘
```

## Features

### ✅ **Integrated PDF Processing**
- **AWS Textract Integration**: Document text extraction, table extraction, form analysis
- **Google Gemini Integration**: AI-powered summarization and sentiment analysis
- **Pattern Matching**: PDF workflows are automatically recognized
- **Multi-Agent Coordination**: Works with textract and summarize agents

### ✅ **Intelligent Workflow Patterns**
- **PDF Summarization**: `"summarize this PDF"` → `textract.extract_text` + `summarize.summarize_text`
- **Document Analysis**: `"analyze this document"` → `textract.analyze_document` + `summarize.analyze_sentiment`
- **Table Extraction**: `"extract tables from PDF"` → `textract.extract_tables`
- **Form Processing**: `"extract forms from PDF"` → `textract.extract_forms`

### ✅ **Natural Language Processing**
- **Keyword Recognition**: Automatically detects PDF-related requests
- **Context Understanding**: Extracts relevant parameters from requests
- **Workflow Composition**: Creates appropriate multi-step workflows

## Usage Examples

### 1. Simple PDF Summarization
```python
from orchestration.intelligent.intelligent_orchestrator import process_user_request

result = await process_user_request(
    "summarize this PDF",
    file_path="documents/report.pdf",
    max_length=200
)
```

### 2. Document Sentiment Analysis
```python
result = await process_user_request(
    "analyze the sentiment of this document",
    file_path="documents/feedback.pdf"
)
```

### 3. Table Extraction
```python
result = await process_user_request(
    "extract tables from this PDF",
    file_path="documents/financial_report.pdf"
)
```

### 4. Complex Document Analysis
```python
result = await process_user_request(
    "give me a complete analysis of this document",
    file_path="documents/research_paper.pdf",
    max_length=300,
    include_sentiment=True
)
```

## Workflow Patterns

### PDF Summarization Pattern
```json
{
  "goal": "summarize a PDF document",
  "keywords": ["pdf", "summarize", "summary", "document"],
  "steps": [
    {"agent": "textract", "tool": "extract_text"},
    {"agent": "summarize", "tool": "summarize_text"}
  ]
}
```

### Document Analysis Pattern
```json
{
  "goal": "analyze document content and sentiment",
  "keywords": ["analyze", "sentiment", "document", "content"],
  "steps": [
    {"agent": "textract", "tool": "extract_text"},
    {"agent": "summarize", "tool": "analyze_sentiment"}
  ]
}
```

### Table Extraction Pattern
```json
{
  "goal": "extract tables from a document",
  "keywords": ["table", "extract", "document", "pdf"],
  "steps": [
    {"agent": "textract", "tool": "extract_tables"}
  ]
}
```

## Setup and Configuration

### 1. Environment Variables
```bash
# AWS Configuration for Textract
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-west-2

# Google AI Configuration for Summarization
GOOGLE_API_KEY=your_google_api_key
```

### 2. Agent Startup
```bash
# Start individual agents
python start_agents.py textract
python start_agents.py summarize

# List all available agents
python start_agents.py --list

# Start all agents (for testing)
python start_agents.py --all
```

## Testing

### Integration Tests
```bash
# Test PDF processing workflow
python tests/integration/test_pdf_summary.py

# Test individual agents
python tests/integration/test_textract_agent.py
python tests/integration/test_summarize_agent.py
```

### Example Usage
```bash
# Run the comprehensive PDF example
python examples/pdf_orchestration_example.py
```

## Agent Tools

### Textract Agent Tools
- **`extract_text`**: Extract text content from PDF documents
- **`extract_tables`**: Extract table data from PDF documents
- **`extract_forms`**: Extract form fields from PDF documents
- **`analyze_document`**: Comprehensive document analysis

### Summarize Agent Tools
- **`summarize_text`**: Generate AI-powered text summaries
- **`analyze_sentiment`**: Analyze text sentiment and tone
- **`extract_key_points`**: Extract key points from text
- **`summarize_file`**: Summarize entire files

## Benefits of Integration

### 🎯 **Intelligent Workflow Composition**
- Automatically determines which agents and tools to use
- Creates optimal workflows based on user requests
- Handles complex multi-step processes

### 🔄 **Multi-Agent Coordination**
- Coordinates between textract and summarize agents
- Manages agent lifecycle (start/stop/communication)
- Handles MCP protocol communication

### 🧠 **Pattern-Based Planning**
- Recognizes common PDF processing patterns
- Maps natural language to specific workflows
- Provides fallback to dynamic planning

### 📊 **Comprehensive Tool Discovery**
- Automatically discovers all available tools
- Validates tool schemas and requirements
- Provides tool documentation and examples

## Current Status

### ✅ **Working Features**
- Textract agent MCP server integration
- Summarize agent MCP server integration
- Workflow pattern recognition
- Multi-agent coordination
- Tool discovery and validation
- Natural language request processing
- AWS Textract integration
- Google Gemini integration

### 🔧 **Areas for Improvement**
- Error handling for large PDF files
- Progress tracking for long-running operations
- Caching of extracted text for efficiency
- Support for more document formats

## Next Steps

1. **Performance Optimization**: Implement caching and progress tracking
2. **Error Recovery**: Robust error handling for large files
3. **Additional Formats**: Support for more document types
4. **Advanced Analysis**: More sophisticated document analysis features
5. **Batch Processing**: Handle multiple documents efficiently
6. **Documentation**: Add more examples and use cases

## Related Documentation

### **System Overview**
- **[README.md](README.md)** - Complete system architecture and technical overview
- **[MCP_LEARNING_GUIDE.md](MCP_LEARNING_GUIDE.md)** - Learn about the MCP protocol used by agents

### **Other Application Guides**
- **[ENERGY_ORCHESTRATION.md](ENERGY_ORCHESTRATION.md)** - Energy analysis workflows
- **[DATABASE_ORCHESTRATION.md](DATABASE_ORCHESTRATION.md)** - Database operations and management

### **Quick References**
- **System Setup**: See [README.md](README.md#quick-start) for environment setup
- **Agent Management**: See [README.md](README.md#available-agents--tools) for all available agents
- **Testing**: See [README.md](README.md#testing) for comprehensive testing guide

## Conclusion

The PDF processing agents are fully integrated with the intelligent orchestration system, providing a sophisticated platform for document analysis and processing. The integration enables natural language processing, intelligent workflow composition, and multi-agent coordination, making it easy to build complex document processing applications.

The system is ready for production use with proper AWS and Google API configuration and can be extended with additional agents and workflow patterns as needed. 