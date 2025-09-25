"""
Flask Backend for Medical Search Interface
==========================================

Provides REST API endpoints for the medical search tools.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os

# Add the current directory to Python path to import main.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the search function from main.py
from main import search_medical_query

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    """
    Search endpoint for medical queries with intelligent routing
    
    Expected JSON payload:
    {
        "query": "search query string",
        "tools": ["tool1", "tool2", ...],  # optional, if not provided uses intelligent routing
        "use_intelligent_routing": true  # optional, defaults to true
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Query is required',
                'status': 'error'
            }), 400
        
        query = data['query'].strip()
        if not query:
            return jsonify({
                'error': 'Query cannot be empty',
                'status': 'error'
            }), 400
        
        # Get intelligent routing preference (default: True)
        use_intelligent_routing = data.get('use_intelligent_routing', True)
        
        # Get selected tools (only used if intelligent routing is disabled)
        selected_tools = data.get('tools', None)
        
        # Validate tools if provided and intelligent routing is disabled
        valid_tools = ["MedicalWebSearchTool", "heart_disease_query", "cancer_query", "diabetes_query"]
        if not use_intelligent_routing and selected_tools:
            invalid_tools = [tool for tool in selected_tools if tool not in valid_tools]
            if invalid_tools:
                return jsonify({
                    'error': f'Invalid tools: {", ".join(invalid_tools)}',
                    'valid_tools': valid_tools,
                    'status': 'error'
                }), 400
        
        # Perform the search with intelligent routing
        results = search_medical_query(query, selected_tools, use_intelligent_routing)
        
        return jsonify({
            'data': results,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/tools', methods=['GET'])
def get_tools():
    """Get available tools information"""
    tools_info = [
        {
            'name': 'MedicalWebSearchTool',
            'description': 'Use this tool for general medical knowledge (definitions, symptoms, cures).',
            'type': 'web_search'
        },
        {
            'name': 'heart_disease_query',
            'description': 'Query the Heart Disease database for patient statistics and insights.',
            'type': 'database'
        },
        {
            'name': 'cancer_query',
            'description': 'Query the Cancer database for patient statistics and insights.',
            'type': 'database'
        },
        {
            'name': 'diabetes_query',
            'description': 'Query the Diabetes database for patient statistics and insights.',
            'type': 'database'
        }
    ]
    
    return jsonify({
        'tools': tools_info,
        'status': 'success'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
