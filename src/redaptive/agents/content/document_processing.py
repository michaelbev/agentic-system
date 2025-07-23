#!/usr/bin/env python3
"""
MCP Document Processing Agent for Energy Documents
Provides specialized document extraction and analysis for energy industry documents
including utility bills, ESG reports, compliance documents, and energy audits
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

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from redaptive.agents.base import BaseMCPServer

class DocumentProcessingAgent(BaseMCPServer):
    def __init__(self):
        super().__init__("document-processing-agent", "1.0.0")
        self.textract_client = None
        self.s3_client = None
        self.setup_aws_clients()
        self.setup_tools()
        
    def setup_aws_clients(self):
        """Setup AWS clients for Textract and S3"""
        try:
            # Get region from environment variable or AWS config, fallback to us-west-2
            region = os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION') or 'us-west-2'
            
            # Initialize AWS clients
            self.textract_client = boto3.client('textract', region_name=region)
            self.s3_client = boto3.client('s3', region_name=region)
            logging.info(f"AWS clients initialized successfully in region: {region}")
        except NoCredentialsError:
            logging.warning("AWS credentials not found. Some features may not work.")
        except Exception as e:
            logging.error(f"Failed to initialize AWS clients: {e}")
    
    def setup_tools(self):
        """Register energy document processing tools"""
        self.register_tool(
            "process_utility_bill",
            "Extract key data from utility bills including usage, costs, and meter readings",
            self.process_utility_bill,
            {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the utility bill document (PDF, PNG, JPG, etc.)"
                    },
                    "utility_type": {
                        "type": "string",
                        "description": "Type of utility: electricity, gas, water, steam",
                        "enum": ["electricity", "gas", "water", "steam"]
                    },
                    "bucket_name": {
                        "type": "string",
                        "description": "S3 bucket name (optional, will use local file if not provided)"
                    }
                },
                "required": ["file_path", "utility_type"]
            }
        )
        
        self.register_tool(
            "extract_text",
            "Extract text from a document using AWS Textract",
            self.extract_text,
            {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the document file (PDF, PNG, JPG, etc.)"
                    },
                    "bucket_name": {
                        "type": "string",
                        "description": "S3 bucket name (optional, will use local file if not provided)"
                    }
                },
                "required": ["file_path"]
            }
        )
        
        self.register_tool(
            "extract_tables",
            "Extract tables from a document using AWS Textract",
            self.extract_tables,
            {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the document file"
                    },
                    "bucket_name": {
                        "type": "string",
                        "description": "S3 bucket name (optional)"
                    }
                },
                "required": ["file_path"]
            }
        )
        
        self.register_tool(
            "extract_forms",
            "Extract form data from a document using AWS Textract",
            self.extract_forms,
            {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the document file"
                    },
                    "bucket_name": {
                        "type": "string",
                        "description": "S3 bucket name (optional)"
                    }
                },
                "required": ["file_path"]
            }
        )
        
        self.register_tool(
            "process_esg_report",
            "Extract sustainability metrics and data from ESG reports",
            self.process_esg_report,
            {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the ESG report document"
                    },
                    "report_type": {
                        "type": "string",
                        "description": "Type of ESG report: sustainability, carbon, energy_audit, compliance",
                        "enum": ["sustainability", "carbon", "energy_audit", "compliance"]
                    },
                    "bucket_name": {
                        "type": "string",
                        "description": "S3 bucket name (optional)"
                    }
                },
                "required": ["file_path", "report_type"]
            }
        )
        
        self.register_tool(
            "extract_energy_certificates",
            "Extract data from energy certificates (Energy Star, LEED, etc.)",
            self.extract_energy_certificates,
            {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the energy certificate document"
                    },
                    "certificate_type": {
                        "type": "string",
                        "description": "Type of certificate: energy_star, leed, breeam, other",
                        "enum": ["energy_star", "leed", "breeam", "other"]
                    },
                    "bucket_name": {
                        "type": "string",
                        "description": "S3 bucket name (optional)"
                    }
                },
                "required": ["file_path", "certificate_type"]
            }
        )
        
        self.register_tool(
            "analyze_document",
            "Perform comprehensive document analysis using AWS Textract",
            self.analyze_document,
            {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the document file"
                    },
                    "bucket_name": {
                        "type": "string",
                        "description": "S3 bucket name (optional)"
                    },
                    "features": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Features to extract: ['TABLES', 'FORMS', 'LINES', 'WORDS']",
                        "default": ["TABLES", "FORMS"]
                    }
                },
                "required": ["file_path"]
            }
        )
    
    async def process_utility_bill(self, file_path: str, utility_type: str, bucket_name: Optional[str] = None):
        """Process utility bills to extract energy usage, costs, and billing data"""
        try:
            # First extract all document data
            features = ["TABLES", "FORMS"]
            if bucket_name:
                document_data = await self._extract_from_s3(file_path, bucket_name, features)
            else:
                document_data = await self._extract_from_local(file_path, features)
            
            if "error" in document_data:
                return document_data
            
            # Extract utility-specific data
            utility_data = self._parse_utility_data(document_data, utility_type)
            
            return {
                "utility_type": utility_type,
                "extracted_data": utility_data,
                "raw_document_data": document_data,
                "processing_status": "success"
            }
        except Exception as e:
            return {"error": f"Failed to process utility bill: {str(e)}"}
    
    async def process_esg_report(self, file_path: str, report_type: str, bucket_name: Optional[str] = None):
        """Process ESG reports to extract sustainability metrics and compliance data"""
        try:
            features = ["TABLES", "FORMS"]
            if bucket_name:
                document_data = await self._extract_from_s3(file_path, bucket_name, features)
            else:
                document_data = await self._extract_from_local(file_path, features)
            
            if "error" in document_data:
                return document_data
            
            # Extract ESG-specific metrics
            esg_data = self._parse_esg_data(document_data, report_type)
            
            return {
                "report_type": report_type,
                "sustainability_metrics": esg_data,
                "raw_document_data": document_data,
                "processing_status": "success"
            }
        except Exception as e:
            return {"error": f"Failed to process ESG report: {str(e)}"}
    
    async def extract_energy_certificates(self, file_path: str, certificate_type: str, bucket_name: Optional[str] = None):
        """Extract data from energy efficiency certificates"""
        try:
            features = ["TABLES", "FORMS"]
            if bucket_name:
                document_data = await self._extract_from_s3(file_path, bucket_name, features)
            else:
                document_data = await self._extract_from_local(file_path, features)
            
            if "error" in document_data:
                return document_data
            
            # Extract certificate-specific data
            certificate_data = self._parse_certificate_data(document_data, certificate_type)
            
            return {
                "certificate_type": certificate_type,
                "certification_data": certificate_data,
                "raw_document_data": document_data,
                "processing_status": "success"
            }
        except Exception as e:
            return {"error": f"Failed to process energy certificate: {str(e)}"}

    async def extract_text(self, file_path: str, bucket_name: Optional[str] = None):
        """Extract text from a document"""
        try:
            if bucket_name:
                # Extract from S3
                return await self._extract_from_s3(file_path, bucket_name, "TEXTS")
            else:
                # Extract from local file
                return await self._extract_from_local(file_path, "TEXTS")
        except Exception as e:
            return {"error": f"Failed to extract text: {str(e)}"}
    
    async def extract_tables(self, file_path: str, bucket_name: Optional[str] = None):
        """Extract tables from a document"""
        try:
            if bucket_name:
                return await self._extract_from_s3(file_path, bucket_name, "TABLES")
            else:
                return await self._extract_from_local(file_path, "TABLES")
        except Exception as e:
            return {"error": f"Failed to extract tables: {str(e)}"}
    
    async def extract_forms(self, file_path: str, bucket_name: Optional[str] = None):
        """Extract form data from a document"""
        try:
            if bucket_name:
                return await self._extract_from_s3(file_path, bucket_name, "FORMS")
            else:
                return await self._extract_from_local(file_path, "FORMS")
        except Exception as e:
            return {"error": f"Failed to extract forms: {str(e)}"}
    
    async def analyze_document(self, file_path: str, bucket_name: Optional[str] = None, features: list = None):
        """Perform comprehensive document analysis"""
        try:
            if features is None:
                features = ["TABLES", "FORMS"]
            
            if bucket_name:
                return await self._extract_from_s3(file_path, bucket_name, features)
            else:
                return await self._extract_from_local(file_path, features)
        except Exception as e:
            return {"error": f"Failed to analyze document: {str(e)}"}
    
    async def _extract_from_local(self, file_path: str, features: list):
        """Extract from local file"""
        if not self.textract_client:
            return {"error": "AWS Textract client not initialized"}
        
        # Check if file exists
        if not Path(file_path).exists():
            return {"error": f"File not found: {file_path}"}
        
        try:
            # Read file
            with open(file_path, 'rb') as file:
                document = {'Bytes': file.read()}
            
            # Call Textract
            if isinstance(features, str):
                features = [features]
            
            if len(features) == 1 and features[0] == "TEXTS":
                response = self.textract_client.detect_document_text(Document=document)
                return self._parse_text_response(response)
            else:
                response = self.textract_client.analyze_document(
                    Document=document,
                    FeatureTypes=features
                )
                return self._parse_analysis_response(response, features)
                
        except ClientError as e:
            return {"error": f"AWS Textract error: {e.response['Error']['Message']}"}
        except Exception as e:
            return {"error": f"Failed to process file: {str(e)}"}
    
    async def _extract_from_s3(self, file_path: str, bucket_name: str, features: list):
        """Extract from S3 file"""
        if not self.textract_client:
            return {"error": "AWS Textract client not initialized"}
        
        try:
            # Use S3 document
            document = {
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': file_path
                }
            }
            
            if isinstance(features, str):
                features = [features]
            
            if len(features) == 1 and features[0] == "TEXTS":
                response = self.textract_client.detect_document_text(Document=document)
                return self._parse_text_response(response)
            else:
                response = self.textract_client.analyze_document(
                    Document=document,
                    FeatureTypes=features
                )
                return self._parse_analysis_response(response, features)
                
        except ClientError as e:
            return {"error": f"AWS Textract error: {e.response['Error']['Message']}"}
        except Exception as e:
            return {"error": f"Failed to process S3 file: {str(e)}"}
    
    def _parse_text_response(self, response):
        """Parse text detection response"""
        text_blocks = []
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                text_blocks.append({
                    'text': block['Text'],
                    'confidence': block['Confidence'],
                    'geometry': block['Geometry']
                })
        
        return {
            'text_blocks': text_blocks,
            'full_text': ' '.join([block['text'] for block in text_blocks]),
            'total_blocks': len(text_blocks)
        }
    
    def _parse_analysis_response(self, response, features):
        """Parse document analysis response"""
        result = {
            'features': features,
            'blocks': len(response['Blocks'])
        }
        
        if 'TABLES' in features:
            result['tables'] = self._extract_tables_from_response(response)
        
        if 'FORMS' in features:
            result['forms'] = self._extract_forms_from_response(response)
        
        if 'TEXTS' in features or 'LINES' in features:
            result['text'] = self._parse_text_response(response)
        
        return result
    
    def _extract_tables_from_response(self, response):
        """Extract tables from Textract response"""
        tables = []
        table_blocks = [block for block in response['Blocks'] if block['BlockType'] == 'TABLE']
        
        for table_block in table_blocks:
            table = {
                'id': table_block['Id'],
                'confidence': table_block['Confidence'],
                'rows': [],
                'cells': []
            }
            
            # Extract cells
            for block in response['Blocks']:
                if block['BlockType'] == 'CELL' and block.get('Relationships'):
                    for relationship in block['Relationships']:
                        if relationship['Type'] == 'CHILD' and table_block['Id'] in relationship['Ids']:
                            cell = {
                                'id': block['Id'],
                                'row_index': block.get('RowIndex', 0),
                                'column_index': block.get('ColumnIndex', 0),
                                'text': self._get_cell_text(block, response['Blocks'])
                            }
                            table['cells'].append(cell)
            
            # Organize cells into rows
            if table['cells']:
                max_row = max(cell['row_index'] for cell in table['cells'])
                for row_idx in range(max_row + 1):
                    row_cells = [cell for cell in table['cells'] if cell['row_index'] == row_idx]
                    row_cells.sort(key=lambda x: x['column_index'])
                    table['rows'].append([cell['text'] for cell in row_cells])
            
            tables.append(table)
        
        return tables
    
    def _extract_forms_from_response(self, response):
        """Extract forms from Textract response"""
        forms = []
        key_value_blocks = [block for block in response['Blocks'] if block['BlockType'] == 'KEY_VALUE_SET']
        
        for block in key_value_blocks:
            if block.get('EntityTypes') and 'KEY' in block['EntityTypes']:
                key_text = self._get_block_text(block, response['Blocks'])
                value_text = ""
                
                # Find associated value
                if block.get('Relationships'):
                    for relationship in block['Relationships']:
                        if relationship['Type'] == 'VALUE':
                            for value_id in relationship['Ids']:
                                value_block = next((b for b in response['Blocks'] if b['Id'] == value_id), None)
                                if value_block:
                                    value_text = self._get_block_text(value_block, response['Blocks'])
                
                forms.append({
                    'key': key_text,
                    'value': value_text,
                    'confidence': block['Confidence']
                })
        
        return forms
    
    def _get_cell_text(self, cell_block, all_blocks):
        """Get text from a cell block"""
        text = ""
        if cell_block.get('Relationships'):
            for relationship in cell_block['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        child_block = next((b for b in all_blocks if b['Id'] == child_id), None)
                        if child_block and child_block['BlockType'] == 'WORD':
                            text += child_block['Text'] + " "
        return text.strip()
    
    def _get_block_text(self, block, all_blocks):
        """Get text from any block"""
        text = ""
        if block.get('Relationships'):
            for relationship in block['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        child_block = next((b for b in all_blocks if b['Id'] == child_id), None)
                        if child_block and child_block['BlockType'] == 'WORD':
                            text += child_block['Text'] + " "
        return text.strip()
    
    def _parse_utility_data(self, document_data, utility_type):
        """Parse utility bill data to extract energy-specific information"""
        utility_info = {
            "billing_period": None,
            "total_usage": None,
            "total_cost": None,
            "rate_schedule": None,
            "meter_readings": [],
            "demand_charges": None,
            "energy_charges": None,
            "taxes_and_fees": None
        }
        
        # Extract data from forms
        if "forms" in document_data:
            for form in document_data["forms"]:
                key = form["key"].lower()
                value = form["value"]
                
                # Billing period
                if any(term in key for term in ["billing period", "service period", "billing date"]):
                    utility_info["billing_period"] = value
                
                # Total usage patterns based on utility type
                if utility_type == "electricity":
                    if any(term in key for term in ["kwh", "kilowatt", "usage", "consumption"]):
                        utility_info["total_usage"] = value
                elif utility_type == "gas":
                    if any(term in key for term in ["therm", "ccf", "mcf", "gas usage"]):
                        utility_info["total_usage"] = value
                elif utility_type == "water":
                    if any(term in key for term in ["gallon", "ccf", "water usage"]):
                        utility_info["total_usage"] = value
                
                # Cost information
                if any(term in key for term in ["total amount", "amount due", "current charges"]):
                    utility_info["total_cost"] = value
                
                # Demand charges (electricity specific)
                if utility_type == "electricity" and any(term in key for term in ["demand", "kw"]):
                    utility_info["demand_charges"] = value
        
        # Extract data from tables
        if "tables" in document_data:
            for table in document_data["tables"]:
                utility_info["meter_readings"].extend(self._extract_meter_readings_from_table(table, utility_type))
        
        return utility_info
    
    def _parse_esg_data(self, document_data, report_type):
        """Parse ESG report data to extract sustainability metrics"""
        esg_info = {
            "carbon_emissions": {},
            "energy_consumption": {},
            "renewable_energy": {},
            "certifications": [],
            "sustainability_goals": [],
            "compliance_status": {}
        }
        
        # Extract sustainability metrics from forms and tables
        if "forms" in document_data:
            for form in document_data["forms"]:
                key = form["key"].lower()
                value = form["value"]
                
                # Carbon emissions
                if any(term in key for term in ["co2", "carbon", "emissions", "scope"]):
                    if "scope 1" in key:
                        esg_info["carbon_emissions"]["scope_1"] = value
                    elif "scope 2" in key:
                        esg_info["carbon_emissions"]["scope_2"] = value
                    elif "scope 3" in key:
                        esg_info["carbon_emissions"]["scope_3"] = value
                    else:
                        esg_info["carbon_emissions"]["total"] = value
                
                # Energy consumption
                if any(term in key for term in ["energy", "kwh", "mwh", "consumption"]):
                    esg_info["energy_consumption"]["total"] = value
                
                # Renewable energy
                if any(term in key for term in ["renewable", "solar", "wind", "green energy"]):
                    esg_info["renewable_energy"]["percentage"] = value
                
                # Certifications
                if any(term in key for term in ["leed", "energy star", "breeam", "certification"]):
                    esg_info["certifications"].append({"type": key, "value": value})
        
        return esg_info
    
    def _parse_certificate_data(self, document_data, certificate_type):
        """Parse energy certificate data"""
        certificate_info = {
            "certification_level": None,
            "score": None,
            "valid_until": None,
            "building_info": {},
            "energy_metrics": {},
            "recommendations": []
        }
        
        if "forms" in document_data:
            for form in document_data["forms"]:
                key = form["key"].lower()
                value = form["value"]
                
                if certificate_type == "energy_star":
                    if "score" in key:
                        certificate_info["score"] = value
                    elif "rating" in key:
                        certificate_info["certification_level"] = value
                
                elif certificate_type == "leed":
                    if any(term in key for term in ["platinum", "gold", "silver", "certified"]):
                        certificate_info["certification_level"] = value
                
                # Common fields
                if any(term in key for term in ["expir", "valid", "renewal"]):
                    certificate_info["valid_until"] = value
                
                if any(term in key for term in ["building", "property", "address"]):
                    certificate_info["building_info"][key] = value
                
                if any(term in key for term in ["eui", "energy use", "kwh", "efficiency"]):
                    certificate_info["energy_metrics"][key] = value
        
        return certificate_info
    
    def _extract_meter_readings_from_table(self, table, utility_type):
        """Extract meter readings from table data"""
        readings = []
        
        for row in table.get("rows", []):
            if len(row) >= 2:
                # Look for date and reading patterns
                potential_date = row[0]
                potential_reading = row[1] if len(row) > 1 else None
                
                # Basic pattern matching for meter readings
                if potential_reading and any(char.isdigit() for char in potential_reading):
                    readings.append({
                        "date": potential_date,
                        "reading": potential_reading,
                        "utility_type": utility_type
                    })
        
        return readings

async def main():
    """Start the Document Processing Agent"""
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    
    agent = DocumentProcessingAgent()
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main()) 