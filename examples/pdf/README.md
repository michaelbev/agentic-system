# PDF Agent Examples

This directory contains examples demonstrating PDF processing and document analysis using intelligent orchestration.

## Files

- **`pdf_orchestration_example.py`** - Main orchestration example showing PDF processing workflows

## Features Demonstrated

- PDF text extraction using Textract
- Document summarization
- Multi-document processing
- Specific information extraction

## Running the Example

```bash
# From the project root
python examples/pdf/pdf_orchestration_example.py
```

## Prerequisites

1. PDF processing agents must be started:
   - `python start_agents.py textract`
   - `python start_agents.py summarize`
2. Environment variables configured in `.env`
3. Sample PDF files available for processing

## Expected Output

The example will demonstrate:
- PDF text extraction
- Document summarization
- Multi-document workflows
- Error handling for missing files

## Documentation

For detailed information about the PDF agents, see [PDF_ORCHESTRATION.md](../../docs/agents/PDF_ORCHESTRATION.md). 