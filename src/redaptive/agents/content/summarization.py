#!/usr/bin/env python3
"""
MCP Summarize Agent
Provides text summarization tools using Google Gemini and MCP protocol
"""

import asyncio
import logging
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import sys

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

from redaptive.agents.base import BaseMCPServer

class SummarizeAgent(BaseMCPServer):
    def __init__(self):
        super().__init__("summarize-agent", "1.0.0")
        self.model = None
        self.setup_model()
        self.setup_tools()
        
    def setup_model(self):
        """Setup Google Gemini model"""
        try:
            # Check for API key
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                logging.warning("GOOGLE_API_KEY not found. Some features may not work.")
                return
            
            logging.info(f"Found API key: {api_key[:20]}...")
            
            # Initialize the model
            genai.configure(api_key=api_key)
            logging.info("GenAI configured successfully")
            
            self.model = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.3,
                max_tokens=1000
            )
            logging.info("Google Gemini model initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Google Gemini model: {e}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
    
    def setup_tools(self):
        """Register summarization tools"""
        self.register_tool(
            "summarize_text",
            "Summarize text content using Google Gemini",
            self.summarize_text,
            {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text content to summarize"
                    },
                    "max_length": {
                        "type": "integer",
                        "description": "Maximum length of summary in words",
                        "default": 150
                    },
                    "style": {
                        "type": "string",
                        "description": "Summary style: 'concise', 'detailed', 'bullet_points'",
                        "default": "concise"
                    }
                },
                "required": ["text"]
            }
        )
        
        self.register_tool(
            "summarize_file",
            "Summarize text from a file using Google Gemini",
            self.summarize_file,
            {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the text file to summarize"
                    },
                    "max_length": {
                        "type": "integer",
                        "description": "Maximum length of summary in words",
                        "default": 150
                    },
                    "style": {
                        "type": "string",
                        "description": "Summary style: 'concise', 'detailed', 'bullet_points'",
                        "default": "concise"
                    }
                },
                "required": ["file_path"]
            }
        )
        
        self.register_tool(
            "extract_key_points",
            "Extract key points from text using Google Gemini",
            self.extract_key_points,
            {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text content to analyze"
                    },
                    "num_points": {
                        "type": "integer",
                        "description": "Number of key points to extract",
                        "default": 5
                    },
                    "categories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Categories to focus on (e.g., ['main ideas', 'action items', 'important dates'])",
                        "default": ["main ideas"]
                    }
                },
                "required": ["text"]
            }
        )
        
        self.register_tool(
            "analyze_sentiment",
            "Analyze sentiment and tone of text using Google Gemini",
            self.analyze_sentiment,
            {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text content to analyze"
                    },
                    "detailed": {
                        "type": "boolean",
                        "description": "Whether to provide detailed analysis",
                        "default": False
                    }
                },
                "required": ["text"]
            }
        )
    
    async def summarize_text(self, text: str, max_length: int = 150, style: str = "concise"):
        """Summarize text content"""
        if not self.model:
            return {"error": "Google Gemini model not initialized"}
        
        try:
            # Create prompt based on style
            if style == "concise":
                prompt = f"Summarize the following text in {max_length} words or less:\n\n{text}"
            elif style == "detailed":
                prompt = f"Provide a detailed summary of the following text in {max_length} words or less:\n\n{text}"
            elif style == "bullet_points":
                prompt = f"Summarize the following text as bullet points (max {max_length} words total):\n\n{text}"
            else:
                prompt = f"Summarize the following text in {max_length} words or less:\n\n{text}"
            
            # Generate summary
            response = self.model.invoke(prompt)
            summary = response.content if hasattr(response, 'content') else str(response)
            
            return {
                "original_length": len(text.split()),
                "summary_length": len(summary.split()),
                "summary": summary,
                "style": style,
                "max_length": max_length
            }
        except Exception as e:
            return {"error": f"Failed to summarize text: {str(e)}"}
    
    async def summarize_file(self, file_path: str, max_length: int = 150, style: str = "concise"):
        """Summarize text from a file"""
        try:
            # Check if file exists
            if not Path(file_path).exists():
                return {"error": f"File not found: {file_path}"}
            
            # Read file
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            if not text.strip():
                return {"error": "File is empty"}
            
            # Use the text summarization function
            return await self.summarize_text(text, max_length, style)
            
        except Exception as e:
            return {"error": f"Failed to summarize file: {str(e)}"}
    
    async def extract_key_points(self, text: str, num_points: int = 5, categories: list = None):
        """Extract key points from text"""
        if not self.model:
            return {"error": "Google Gemini model not initialized"}
        
        try:
            if categories is None:
                categories = ["main ideas"]
            
            categories_str = ", ".join(categories)
            prompt = f"""Extract {num_points} key points from the following text, focusing on: {categories_str}

Text:
{text}

Please format the response as a JSON object with the following structure:
{{
    "key_points": [
        {{"point": "point text", "category": "category name"}}
    ],
    "summary": "brief overall summary"
}}"""
            
            # Generate key points
            response = self.model.invoke(prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Try to parse JSON response
            try:
                result = json.loads(response_text)
                return result
            except json.JSONDecodeError:
                # If JSON parsing fails, return as text
                return {
                    "key_points": [{"point": response_text, "category": "extracted"}],
                    "summary": "Key points extracted",
                    "raw_response": response_text
                }
                
        except Exception as e:
            return {"error": f"Failed to extract key points: {str(e)}"}
    
    async def analyze_sentiment(self, text: str, detailed: bool = False):
        """Analyze sentiment and tone of text"""
        if not self.model:
            return {"error": "Google Gemini model not initialized"}
        
        try:
            if detailed:
                prompt = f"""Analyze the sentiment and tone of the following text in detail:

Text: {text}

Please provide a detailed analysis including:
- Overall sentiment (positive, negative, neutral)
- Tone (formal, informal, professional, casual, etc.)
- Emotional intensity (low, medium, high)
- Key emotional indicators
- Writing style analysis

Format as JSON:
{{
    "sentiment": "overall sentiment",
    "tone": "tone description",
    "intensity": "emotional intensity",
    "indicators": ["list", "of", "indicators"],
    "style": "writing style analysis"
}}"""
            else:
                prompt = f"""Analyze the sentiment of the following text:

Text: {text}

Provide a simple analysis with:
- Sentiment (positive, negative, neutral)
- Tone (brief description)

Format as JSON:
{{
    "sentiment": "sentiment",
    "tone": "tone description"
}}"""
            
            # Generate analysis
            response = self.model.invoke(prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Try to parse JSON response
            try:
                result = json.loads(response_text)
                return result
            except json.JSONDecodeError:
                # If JSON parsing fails, return as text
                return {
                    "analysis": response_text,
                    "raw_response": response_text
                }
                
        except Exception as e:
            return {"error": f"Failed to analyze sentiment: {str(e)}"}

async def main():
    """Start the Summarize Agent"""
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    
    logging.info("🚀 Starting summarize agent...")
    agent = SummarizeAgent()
    logging.info("✅ Summarize agent created successfully")
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main()) 