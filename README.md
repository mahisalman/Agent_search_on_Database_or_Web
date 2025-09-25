# 🧠 AI Medical Search Interface

A modern web interface with intelligent AI routing for the Medical Search Agent that automatically routes queries to the most appropriate medical search tools.

## ✨ Key Features

### 🧠 **Intelligent AI Routing**
- **Automatic Query Analysis**: AI analyzes your query to determine the best routing strategy
- **Smart Tool Selection**: 
  - 📊 **Statistics/Data/Numbers** → Database tools (heart_disease_query, cancer_query, diabetes_query)
  - 🌐 **Definitions/Symptoms/Cures** → Web Search tool (MedicalWebSearchTool)
  - 🔄 **Mixed Queries** → Both database and web search tools
- **Confidence Scoring**: Shows AI confidence level for routing decisions
- **Routing Analysis**: Displays reasoning behind tool selection

### 🔧 **4 Medical Search Tools:**
  - `MedicalWebSearchTool`: General medical knowledge search
  - `heart_disease_query`: Heart disease database queries
  - `cancer_query`: Cancer database queries  
  - `diabetes_query`: Diabetes database queries

### 🎨 **Modern Web Interface:**
  - Intelligent routing mode (recommended) or manual tool selection
  - Responsive design that works on desktop and mobile
  - Real-time search with loading indicators
  - Routing analysis display with confidence scores
  - Results display with tool information and AI reasoning
  - Error handling and user feedback

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

The application requires API keys for GitHub models and Tavily web search:

```bash
# Option 1: Use the setup script
python env_setup.py

# Option 2: Set manually
export GITHUB_API_TOKEN="your_github_token_here"
export TAVILY_API_KEY="your_tavily_api_key_here"
```

**API Keys Required:**
- **GitHub API Token**: Get from [GitHub Settings > Tokens](https://github.com/settings/tokens)
- **Tavily API Key**: Get from [Tavily.com](https://tavily.com/)

### 3. Start the Web Server

```bash
python app.py
```

The web interface will be available at: `http://localhost:5000`

## Usage

### Web Interface

1. **Open your browser** and navigate to `http://localhost:5000`
2. **Enter your medical query** in the search box
3. **Select tools** you want to use (you can select one or more)
4. **Click "Search Medical Resources"** to execute the search
5. **View results** with tool information displayed for each result

### Example Queries

#### 📊 **Database/Statistics Queries** (Auto-routed to DB tools)
- "Show me the top 5 ages with highest heart disease cases"
- "What is the average age of cancer patients?"
- "How many diabetes patients are there by gender?"
- "Show me heart disease statistics by age group"

#### 🌐 **Definition/Symptom Queries** (Auto-routed to Web Search)
- "What are the common symptoms of diabetes?"
- "What is heart disease and how is it treated?"
- "Tell me about cancer prevention methods"
- "Explain the causes of diabetes"

#### 🔄 **Mixed Queries** (Auto-routed to both tools)
- "What is diabetes and show me the statistics of diabetic patients"
- "Explain heart disease symptoms and show me the age distribution"
- "Tell me about cancer and how many patients do we have?"

### API Endpoints

#### Search Endpoint
```
POST /api/search
Content-Type: application/json

{
    "query": "your search query",
    "use_intelligent_routing": true,  // optional, defaults to true
    "tools": ["tool1", "tool2"] // optional, only used if intelligent routing is false
}
```

#### Tools Information Endpoint
```
GET /api/tools
```

Returns information about available tools.

## File Structure

```
├── app.py                 # Flask backend application
├── main.py               # Modified with web interface function
├── templates/
│   └── index.html        # Frontend HTML with CSS and JavaScript
├── requirements.txt      # Updated with Flask dependencies
└── README_WEB_INTERFACE.md
```

## Technical Details

### Backend (Flask)
- RESTful API with JSON responses
- CORS enabled for frontend requests
- Error handling and validation
- Integration with existing medical search tools

### Frontend (HTML/CSS/JavaScript)
- Modern responsive design
- Real-time tool selection
- Loading states and error handling
- Results display with tool badges
- Mobile-friendly interface

### Integration
- Uses intelligent `MedicalRoutingAgent` class with OpenAI Agent SDK + Langchain
- Enhanced `search_medical_query()` function with intelligent routing option
- Maintains backward compatibility with manual tool selection
- No changes to existing medical search logic - all original functionality preserved

## Troubleshooting

### Common Issues

1. **Port 5000 already in use:**
   ```bash
   # Change port in app.py or kill existing process
   python app.py
   ```

2. **Database connection errors:**
   - Ensure `src/databases/PatientsDB.db` exists
   - Check that database files are accessible

3. **API key errors:**
   - Verify Tavily API key is set in `main.py`
   - Check GitHub API token configuration

### Error Messages

- **"Query is required"**: Enter a search query
- **"Invalid tools"**: Select valid tool names
- **"Internal server error"**: Check backend logs for details

## Testing Intelligent Routing

### Test Script
Run the test script to see intelligent routing in action:

```bash
python test_intelligent_routing.py
```

This will test various query types and show how the AI routes them:
- Statistics queries → Database tools
- Definition queries → Web search
- Mixed queries → Both tools

### Manual Testing
Try these queries in the web interface:

1. **"Show me heart disease statistics"** → Should route to database tools
2. **"What are diabetes symptoms?"** → Should route to web search
3. **"What is cancer and show me patient data?"** → Should route to both

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development
python app.py
```

### Customizing the Interface

- **Styling**: Edit CSS in `templates/index.html`
- **API**: Modify endpoints in `app.py`
- **Tools**: Add new tools in `main.py` and update the frontend

## Security Notes

- API keys are hardcoded for development
- For production, use environment variables
- Consider adding authentication for sensitive medical data
