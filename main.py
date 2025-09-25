"""
Hybrid Medical Agent with Intelligent Routing
============================================

- DB Tools for patient stats (Heart, Cancer, Diabetes).
- Web Search Tool for general medical queries.
- Math utility tools.
- Intelligent AI Agent routes queries between DB & Web Search.
"""

import os
from pyprojroot import here
import pandas as pd

from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch

# --------------------------------
# 1. Database Setup
# --------------------------------
db_path = os.path.join(str(here("/assignment17/src/databases")), "PatientsDB.db")

# Restrict DB agent to a specific table
def build_db_agent(table_name: str, verbose: bool = False):
    db_subset = SQLDatabase.from_uri(f"sqlite:///{db_path}", include_tables=[table_name])
    return create_sql_agent(
        llm,
        db=db_subset,
        agent_type="openai-tools",
        verbose=verbose,
    )

# --------------------------------
# 2. LLM Setup (GitHub Models)
# --------------------------------
# Load API keys from environment variables for security
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY", "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")
token = "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"
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4.1-mini"

llm = ChatOpenAI(
    model_name=model_name,
    openai_api_key=token,
    openai_api_base=endpoint,
    temperature=0.2,
)

# --------------------------------
# 3. DB-Specific Agents
# --------------------------------
HeartDiseaseDBToolAgent = build_db_agent("heart_disease_patients")
CancerDBToolAgent = build_db_agent("cancer_patients")
DiabetesDBToolAgent = build_db_agent("diabetes_patients")

# --------------------------------
# 4. Web Search Tool (Medical)
# --------------------------------
MedicalWebSearchTool = TavilySearch(
    max_results=5,
    topic="general",  # Tavily only supports 'general', 'news', 'finance'
)
MedicalWebSearchTool.name = "MedicalWebSearchTool"
MedicalWebSearchTool.description = "Use this tool for general medical knowledge (definitions, symptoms, cures)."

# --------------------------------
# 5. Utility Tools
# --------------------------------
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def get_maximum_age(file_path: str) -> int:
    """Get maximum age from a CSV dataset."""
    df = pd.read_csv(file_path)
    return int(df["Age"].max())

# --------------------------------
# 6. Wrap DB Agents as Tools
# --------------------------------
@tool
def heart_disease_query(query: str) -> str:
    """Query the Heart Disease database."""
    return HeartDiseaseDBToolAgent.invoke({"input": query})

@tool
def cancer_query(query: str) -> str:
    """Query the Cancer database."""
    return CancerDBToolAgent.invoke({"input": query})

@tool
def diabetes_query(query: str) -> str:
    """Query the Diabetes database."""
    return DiabetesDBToolAgent.invoke({"input": query})

# --------------------------------
# 7. Create Main Agent
# --------------------------------
memory = MemorySaver()

tools = [
    multiply,
    add,
    get_maximum_age,
    MedicalWebSearchTool,
    heart_disease_query,
    cancer_query,
    diabetes_query,
]

agent_executor = create_react_agent(
    llm,
    tools=tools,
    checkpointer=memory,
)

# --------------------------------
# 8. Run Example Queries
# --------------------------------
config = {"configurable": {"thread_id": "med123"}}

# Example 1: DB query
# input_message = {"role": "user", "content": "Show me top 5 ages with highest heart disease cases"}
# for step in agent_executor.stream({"messages": [input_message]}, config, stream_mode="values"):
#     step["messages"][-1].pretty_print()

# Example 2: Web search query
# input_message = {"role": "user", "content": "What are common symptoms of diabetes?"}
# for step in agent_executor.stream({"messages": [input_message]}, config, stream_mode="values"):
#     step["messages"][-1].pretty_print()

# Example 3: Mixed math utility
# input_message = {"role": "user", "content": "Add 40 and 60, then multiply by 2"}
# for step in agent_executor.stream({"messages": [input_message]}, config, stream_mode="values"):
#     step["messages"][-1].pretty_print()

# Example 4: CSV dataset query
# csv_path = os.path.join("data", "diabetes.csv")  # ensure this file exists
# input_message = {"role": "user", "content": f"Get the maximum age from this file path {csv_path}"}
# for step in agent_executor.stream({"messages": [input_message]}, config, stream_mode="values"):
#     step["messages"][-1].pretty_print()

# --------------------------------
# 9. Intelligent Routing Agent
# --------------------------------
class MedicalRoutingAgent:
    """
    Intelligent agent that routes medical queries to appropriate tools:
    - Statistics/Data/Numbers → Database tools
    - Definitions/Symptoms/Cures → Web Search tool
    """
    
    def __init__(self, llm, memory):
        self.llm = llm
        self.memory = memory
        
        # Create specialized tool groups
        self.db_tools = [heart_disease_query, cancer_query, diabetes_query]
        self.web_tools = [MedicalWebSearchTool]
        self.utility_tools = [multiply, add, get_maximum_age]
        
        # Create routing agent
        self.routing_agent = create_react_agent(
            llm,
            tools=self.db_tools + self.web_tools + self.utility_tools,
            checkpointer=memory,
        )
    
    def analyze_query_intent(self, query: str) -> dict:
        """
        Analyze query to determine intent and routing strategy
        """
        analysis_prompt = f"""
        Analyze this medical query and determine the best routing strategy:
        
        Query: "{query}"
        
        Determine if this query is about:
        1. STATISTICS/DATA/NUMBERS - Use database tools (heart_disease_query, cancer_query, diabetes_query)
        2. DEFINITIONS/SYMPTOMS/CURES - Use web search tool (MedicalWebSearchTool)
        3. MIXED - Use both database and web search tools
        
        Keywords for DATABASE tools: statistics, data, numbers, count, average, maximum, minimum, 
        distribution, percentage, cases, patients, records, database
        
        Keywords for WEB SEARCH: what is, definition, symptoms, causes, treatment, cure, 
        prevention, diagnosis, signs, effects, complications
        
        Respond with JSON format:
        {{
            "intent": "database|web|mixed",
            "confidence": 0.0-1.0,
            "reasoning": "explanation of decision",
            "recommended_tools": ["tool1", "tool2"]
        }}
        """
        
        try:
            response = self.llm.invoke(analysis_prompt)
            # Extract JSON from response
            import json
            import re
            
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: simple keyword-based routing
                return self._fallback_routing(query)
                
        except Exception as e:
            print(f"Error in query analysis: {e}")
            return self._fallback_routing(query)
    
    def _fallback_routing(self, query: str) -> dict:
        """
        Fallback routing based on simple keyword matching
        """
        query_lower = query.lower()
        
        # Database keywords
        db_keywords = [
            'statistics', 'data', 'numbers', 'count', 'average', 'maximum', 'minimum',
            'distribution', 'percentage', 'cases', 'patients', 'records', 'database',
            'show me', 'how many', 'what is the', 'top', 'highest', 'lowest'
        ]
        
        # Web search keywords
        web_keywords = [
            'what is', 'definition', 'symptoms', 'causes', 'treatment', 'cure',
            'prevention', 'diagnosis', 'signs', 'effects', 'complications',
            'explain', 'describe', 'tell me about'
        ]
        
        db_score = sum(1 for keyword in db_keywords if keyword in query_lower)
        web_score = sum(1 for keyword in web_keywords if keyword in query_lower)
        
        if db_score > web_score:
            return {
                "intent": "database",
                "confidence": 0.7,
                "reasoning": "Query contains database-related keywords",
                "recommended_tools": ["heart_disease_query", "cancer_query", "diabetes_query"]
            }
        elif web_score > db_score:
            return {
                "intent": "web",
                "confidence": 0.7,
                "reasoning": "Query contains web search-related keywords",
                "recommended_tools": ["MedicalWebSearchTool"]
            }
        else:
            return {
                "intent": "mixed",
                "confidence": 0.5,
                "reasoning": "Query could benefit from both database and web search",
                "recommended_tools": ["heart_disease_query", "cancer_query", "diabetes_query", "MedicalWebSearchTool"]
            }
    
    def route_and_execute(self, query: str, config: dict = None) -> dict:
        """
        Route query to appropriate tools and execute
        """
        if config is None:
            config = {"configurable": {"thread_id": "med_agent"}}
        
        # Analyze query intent
        analysis = self.analyze_query_intent(query)
        
        # Execute with the routing agent
        input_message = {"role": "user", "content": query}
        
        try:
            # Use the routing agent to execute
            response = self.routing_agent.invoke({"messages": [input_message]}, config)
            
            # Extract the final response
            final_message = response["messages"][-1]
            
            return {
                "query": query,
                "analysis": analysis,
                "response": final_message.content,
                "status": "success",
                "tools_used": self._extract_tools_used(response),
                "routing_decision": analysis
            }
            
        except Exception as e:
            return {
                "query": query,
                "analysis": analysis,
                "response": f"Error executing query: {str(e)}",
                "status": "error",
                "tools_used": [],
                "routing_decision": analysis
            }
    
    def _extract_tools_used(self, response: dict) -> list:
        """
        Extract which tools were used from the agent response
        """
        tools_used = []
        messages = response.get("messages", [])
        
        for message in messages:
            if hasattr(message, 'tool_calls') and message.tool_calls:
                for tool_call in message.tool_calls:
                    tools_used.append(tool_call.get('name', 'unknown_tool'))
        
        return list(set(tools_used))  # Remove duplicates

# Create the intelligent routing agent
intelligent_medical_agent = MedicalRoutingAgent(llm, memory)

# --------------------------------
# 10. Web Interface Function (Updated)
# --------------------------------
def search_medical_query(query: str, selected_tools: list = None, use_intelligent_routing: bool = True):
    """
    Search medical query using intelligent routing or specified tools.
    
    Args:
        query (str): The search query
        selected_tools (list): List of tool names to use. If None, uses intelligent routing.
        use_intelligent_routing (bool): Whether to use intelligent routing agent
    
    Returns:
        dict: Results with tool information and routing analysis
    """
    if use_intelligent_routing and selected_tools is None:
        # Use the intelligent routing agent
        try:
            result = intelligent_medical_agent.route_and_execute(query)
            
            # Format the result to match the expected structure
            return {
                "query": result["query"],
                "analysis": result["analysis"],
                "routing_decision": result["routing_decision"],
                "response": result["response"],
                "tools_used": result["tools_used"],
                "status": result["status"],
                "intelligent_routing": True,
                "results": [{
                    "tool_name": "intelligent_agent",
                    "tool_description": f"AI Agent routed to {result['routing_decision']['intent']} tools",
                    "result": result["response"],
                    "status": result["status"],
                    "routing_analysis": result["routing_decision"]
                }]
            }
        except Exception as e:
            return {
                "query": query,
                "error": f"Intelligent routing failed: {str(e)}",
                "status": "error",
                "intelligent_routing": True
            }
    
    else:
        # Fallback to manual tool selection (original behavior)
        if selected_tools is None:
            selected_tools = ["MedicalWebSearchTool", "heart_disease_query", "cancer_query", "diabetes_query"]
        
        # Filter tools based on selection
        available_tools = {
            "MedicalWebSearchTool": MedicalWebSearchTool,
            "heart_disease_query": heart_disease_query,
            "cancer_query": cancer_query,
            "diabetes_query": diabetes_query,
        }
        
        results = []
        
        for tool_name in selected_tools:
            if tool_name in available_tools:
                try:
                    tool = available_tools[tool_name]
                    if tool_name == "MedicalWebSearchTool":
                        # Web search tool returns different format
                        response = tool.invoke(query)
                        result_text = str(response)
                    else:
                        # Database query tools
                        response = tool.invoke(query)
                        result_text = str(response)
                    
                    results.append({
                        "tool_name": tool_name,
                        "tool_description": tool.description if hasattr(tool, 'description') else f"Query the {tool_name.replace('_', ' ').title()} database",
                        "result": result_text,
                        "status": "success"
                    })
                except Exception as e:
                    results.append({
                        "tool_name": tool_name,
                        "tool_description": tool.description if hasattr(tool, 'description') else f"Query the {tool_name.replace('_', ' ').title()} database",
                        "result": f"Error: {str(e)}",
                        "status": "error"
                    })
        
        return {
            "query": query,
            "results": results,
            "total_results": len(results),
            "intelligent_routing": False
        }

if __name__ == "__main__":
    # Run examples when script is executed directly
    pass
