#!/usr/bin/env python3
"""Check AI/ML credentials status for the Redaptive platform."""

import os
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Load .env file from project root
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        print(f"📁 Loaded environment from: {env_file}")
    else:
        print(f"⚠️  .env file not found at: {env_file}")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
except Exception as e:
    print(f"⚠️  Error loading .env file: {e}")

def check_openai_credentials():
    """Check OpenAI credentials."""
    print("🔍 Checking OpenAI Credentials...")
    
    # Check environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("   The system will use rule-based planning instead of learning-based planning")
        return False
    
    # Check if key looks valid (starts with sk-)
    if not api_key.startswith("sk-"):
        if "your_openai_api_key_here" in api_key:
            print("⚠️  OPENAI_API_KEY is set to placeholder value")
            print("   Please replace with your actual OpenAI API key")
        else:
            print("⚠️  OPENAI_API_KEY format looks incorrect (should start with 'sk-')")
        return False
    
    # Check if openai package is available
    try:
        import openai
        print("✅ OpenAI package installed")
    except ImportError:
        print("❌ OpenAI package not installed")
        print("   Install with: pip install openai")
        return False
    
    print("✅ OpenAI credentials configured")
    return True

def check_anthropic_credentials():
    """Check Anthropic/Claude credentials."""
    print("\n🔍 Checking Anthropic/Claude Credentials...")
    
    # Check environment variable
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment variables")
        print("   The system will use rule-based planning instead of learning-based planning")
        return False
    
    # Check if key looks valid (starts with sk-ant-)
    if not api_key.startswith("sk-ant-"):
        if "your_anthropic_api_key_here" in api_key:
            print("⚠️  ANTHROPIC_API_KEY is set to placeholder value")
            print("   Please replace with your actual Anthropic API key")
        else:
            print("⚠️  ANTHROPIC_API_KEY format looks incorrect (should start with 'sk-ant-')")
        return False
    
    # Check if anthropic package is available
    try:
        import anthropic
        print("✅ Anthropic package installed")
    except ImportError:
        print("❌ Anthropic package not installed")
        print("   Install with: pip install anthropic")
        return False
    
    print("✅ Anthropic/Claude credentials configured")
    return True

def check_google_credentials():
    """Check Google credentials."""
    print("\n🔍 Checking Google Credentials...")
    
    # Check environment variable
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        print("   Document summarization features will be limited")
        return False
    
    # Check if key is placeholder
    if "your_google_api_key_here" in api_key:
        print("⚠️  GOOGLE_API_KEY is set to placeholder value")
        print("   Please replace with your actual Google API key")
        return False
    
    # Check if google-generativeai package is available
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI package installed")
    except ImportError:
        print("❌ Google Generative AI package not installed")
        print("   Install with: pip install google-generativeai")
        return False
    
    print("✅ Google credentials configured")
    return True

def check_aws_credentials():
    """Check AWS credentials."""
    print("\n🔍 Checking AWS Credentials...")
    
    # Check environment variables
    region = os.getenv("AWS_REGION")
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    if not all([region, access_key, secret_key]):
        print("❌ AWS credentials not found in environment variables")
        print("   PDF document processing features will be limited")
        return False
    
    # Check if credentials are placeholders
    if any("your_aws" in str(val) for val in [region, access_key, secret_key]):
        print("⚠️  AWS credentials are set to placeholder values")
        print("   Please replace with your actual AWS credentials")
        return False
    
    # Check if boto3 package is available
    try:
        import boto3
        print("✅ AWS boto3 package installed")
    except ImportError:
        print("❌ AWS boto3 package not installed")
        print("   Install with: pip install boto3")
        return False
    
    print("✅ AWS credentials configured")
    return True

def check_env_file():
    """Check if .env file exists and has required variables."""
    print("\n🔍 Checking Environment File...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("   Create one by copying .env.example:")
        print("   cp .env.example .env")
        return False
    
    print("✅ .env file exists")
    
    # Check if it contains the required variables
    with open(env_file) as f:
        content = f.read()
        
    if "OPENAI_API_KEY" not in content:
        print("⚠️  OPENAI_API_KEY not found in .env file")
    else:
        print("✅ OPENAI_API_KEY found in .env file")
    
    if "GOOGLE_API_KEY" not in content:
        print("⚠️  GOOGLE_API_KEY not found in .env file")
    else:
        print("✅ GOOGLE_API_KEY found in .env file")
    
    if "AWS_REGION" not in content:
        print("⚠️  AWS_REGION not found in .env file")
    else:
        print("✅ AWS_REGION found in .env file")
    
    if "AWS_ACCESS_KEY_ID" not in content:
        print("⚠️  AWS_ACCESS_KEY_ID not found in .env file")
    else:
        print("✅ AWS_ACCESS_KEY_ID found in .env file")
    
    return True

def main():
    """Main credential check function."""
    print("🚀 Redaptive Platform - Credential Check")
    print("=" * 50)
    
    openai_ok = check_openai_credentials()
    anthropic_ok = check_anthropic_credentials()
    google_ok = check_google_credentials()
    aws_ok = check_aws_credentials()
    env_ok = check_env_file()
    
    print("\n" + "=" * 50)
    print("📊 Summary:")
    
    if openai_ok or anthropic_ok:
        print("✅ Learning-based planning: AVAILABLE")
        if openai_ok and anthropic_ok:
            print("   (OpenAI and Anthropic/Claude both configured)")
        elif openai_ok:
            print("   (OpenAI configured)")
        else:
            print("   (Anthropic/Claude configured)")
    else:
        print("❌ Learning-based planning: UNAVAILABLE (will use rule-based)")
    
    if google_ok:
        print("✅ AI document summarization: AVAILABLE")
    else:
        print("❌ AI document summarization: UNAVAILABLE")
    
    if aws_ok:
        print("✅ PDF document processing: AVAILABLE")
    else:
        print("❌ PDF document processing: UNAVAILABLE")
    
    if env_ok:
        print("✅ Environment configuration: OK")
    else:
        print("❌ Environment configuration: NEEDS SETUP")
    
    print("\n💡 Next Steps:")
    if not openai_ok:
        print("   • Get OpenAI API key from: https://platform.openai.com/api-keys")
        print("   • Add to .env file: OPENAI_API_KEY=your_key_here")
        print("   • Install OpenAI package: pip install openai")
    
    if not google_ok:
        print("   • Get Google API key from: https://makersuite.google.com/app/apikey")
        print("   • Add to .env file: GOOGLE_API_KEY=your_key_here")
        print("   • Install Google package: pip install google-generativeai")
    
    if not aws_ok:
        print("   • Get AWS credentials from: https://aws.amazon.com/iam/")
        print("   • Add to .env file:")
        print("     AWS_REGION=your_region_here")
        print("     AWS_ACCESS_KEY_ID=your_access_key_here")
        print("     AWS_SECRET_ACCESS_KEY=your_secret_key_here")
        print("   • Install AWS package: pip install boto3")
    
    print("\n🎯 The system will work without API keys using rule-based planning!")

if __name__ == "__main__":
    main() 