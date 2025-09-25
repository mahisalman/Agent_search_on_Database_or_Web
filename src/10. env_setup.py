"""
Environment Setup for Medical Search Agent
==========================================

This script helps you set up the required environment variables for the Medical Search Agent.

Required API Keys:
1. GitHub API Token - for OpenAI models
2. Tavily API Key - for web search functionality

Setup Instructions:
1. Copy your API keys to the variables below
2. Run this script to set up your environment
3. Or set them manually in your system environment
"""

import os

def setup_environment():
    """
    Set up environment variables for the Medical Search Agent
    """
    
    print("🔧 Setting up environment variables for Medical Search Agent")
    print("=" * 60)
    
    # GitHub API Token
    github_token = input("Enter your GitHub API Token (for OpenAI models): ").strip()
    if github_token:
        os.environ["GITHUB_API_TOKEN"] = github_token
        print("✅ GitHub API Token set")
    else:
        print("⚠️  GitHub API Token not provided - using default")
    
    # Tavily API Key
    tavily_key = input("Enter your Tavily API Key (for web search): ").strip()
    if tavily_key:
        os.environ["TAVILY_API_KEY"] = tavily_key
        print("✅ Tavily API Key set")
    else:
        print("⚠️  Tavily API Key not provided - using default")
    
    print("\n🎉 Environment setup complete!")
    print("\n💡 You can also set these variables manually:")
    print("export GITHUB_API_TOKEN='your_token_here'")
    print("export TAVILY_API_KEY='your_key_here'")

if __name__ == "__main__":
    setup_environment()
