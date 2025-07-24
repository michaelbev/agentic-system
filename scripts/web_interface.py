#!/usr/bin/env python3
"""
Web-based CLI for Redaptive Agentic Platform
Provides expandable/collapsible log sections
"""

import asyncio
import sys
import json
import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify
import threading
import queue

# Add src to path - now that we're in the scripts directory
src_dir = str(Path(__file__).parent.parent / "src")
sys.path.insert(0, src_dir)

from redaptive.orchestration import OrchestrationEngine
from redaptive.agents import AGENT_REGISTRY

app = Flask(__name__)

# Global queue for log messages
log_queue = queue.Queue()

class LogCapture:
    """Capture and store log messages"""
    def __init__(self):
        self.logs = []
    
    def add_log(self, level, message):
        self.logs.append({
            'level': level,
            'message': message,
            'timestamp': asyncio.get_event_loop().time()
        })
    
    def get_logs(self):
        return self.logs

log_capture = LogCapture()

async def process_user_request(user_request: str, **context):
    """
    Process a user request using the orchestration engine.
    This fully delegates to the orchestration system for all logic.
    """
    try:
        # Initialize the orchestration engine
        engine = OrchestrationEngine()
        
        # Initialize all available agents
        agent_names = list(AGENT_REGISTRY.keys())
        success = await engine.initialize_agents(agent_names)
        
        if not success:
            return {
                "error": "Failed to initialize agents",
                "workflow": "user_request",
                "user_goal": user_request,
                "steps_executed": 0
            }
        
        # Delegate ALL logic to the orchestration system
        from redaptive.orchestration.matchers import KeywordMatcher
        from redaptive.orchestration.planners import DynamicPlanner
        
        # Step 1: Intent Matching (handled by orchestration)
        matcher = KeywordMatcher()
        intent_result = await matcher.match_intent(user_request)
        
        # Step 2: Create workflow using the planner (handled by orchestration)
        planner = DynamicPlanner()
        workflow_plan = await planner.create_workflow(user_request, agent_names)
        
        # Add planning path information
        planning_path = {
            "intent": intent_result,
            "workflow_plan": workflow_plan
        }
        
        # Step 3: Execute the workflow (handled by orchestration)
        workflow_result = await engine.execute_workflow(
            workflow_plan["workflow_id"], 
            workflow_plan
        )
        
        # Step 4: Format the response based on orchestration results
        if workflow_result["status"] == "completed":
            return {
                "workflow": intent_result["intent"],
                "user_goal": user_request,
                "steps_executed": len(workflow_result["results"]),
                "summary": f"Processed {intent_result['intent']} request: {user_request}",
                "results": workflow_result["results"],
                "planning_path": planning_path,
                "planning_method": workflow_plan.get("planning_method", "unknown"),
                "planning_reason": workflow_plan.get("planning_reason", "No planning reason provided")
            }
        else:
            return {
                "error": workflow_result.get("error", "Workflow execution failed"),
                "workflow": intent_result["intent"],
                "user_goal": user_request,
                "steps_executed": 0
            }
        
    except ImportError as e:
        if "psycopg2" in str(e):
            return {
                "error": "Database functionality disabled (psycopg2 not installed). Core functionality still available.",
                "workflow": "user_request",
                "user_goal": user_request,
                "steps_executed": 0,
                "suggestion": "Install psycopg2-binary to enable full database functionality"
            }
        else:
            return {
                "error": f"Import error: {str(e)}",
                "workflow": "user_request", 
                "user_goal": user_request,
                "steps_executed": 0
            }
    except Exception as e:
        return {
            "error": f"Failed to process request: {str(e)}",
            "workflow": "user_request",
            "user_goal": user_request,
            "steps_executed": 0
        }

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Redaptive Agentic Platform - Web CLI</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
            .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .input-section { margin-bottom: 20px; }
            .input-row { display: flex; gap: 10px; align-items: center; margin-bottom: 10px; }
            #userInput { flex: 1; padding: 10px; font-size: 16px; border: 2px solid #3498db; border-radius: 4px; }
            #sampleSelect { padding: 8px; border: 2px solid #95a5a6; border-radius: 4px; background: white; }
            #submitBtn { padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
            #submitBtn:hover { background: #2980b9; }
            .results { margin-top: 20px; }
            .log-section { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px; margin: 10px 0; }
            .log-header { padding: 10px; background: #e9ecef; cursor: pointer; font-weight: bold; }
            .log-content { padding: 10px; display: none; font-family: monospace; font-size: 12px; }
            .log-content.expanded { display: block; }
            .success { color: #28a745; }
            .error { color: #dc3545; }
            .info { color: #17a2b8; }
            .sample-category { font-weight: bold; color: #2c3e50; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Redaptive Agentic Platform - Web CLI</h1>
                <p>Send natural language prompts to the system</p>
            </div>
            
            <div class="input-section">
                <div class="input-row">
                    <input type="text" id="userInput" placeholder="Enter your request or select a sample below..." />
                    <select id="sampleSelect" onchange="loadSample()">
                        <option value="">📋 Select a sample question...</option>
                        <optgroup label="🕐 Time & Date">
                            <option value="What is the current time?">What is the current time?</option>
                            <option value="What is the current date?">What is the current date?</option>
                            <option value="Get the current time">Get the current time</option>
                        </optgroup>
                        <optgroup label="💰 Financial Analysis">
                            <option value="Calculate ROI for LED retrofit project for building 123">Calculate ROI for LED retrofit project for building 123</option>
                            <option value="Calculate ROI for HVAC upgrade project">Calculate ROI for HVAC upgrade project</option>
                            <option value="Calculate ROI for solar installation project">Calculate ROI for solar installation project</option>
                            <option value="Show me financial analysis for energy efficiency project">Show me financial analysis for energy efficiency project</option>
                        </optgroup>
                        <optgroup label="⚡ Energy Analysis">
                            <option value="Analyze energy consumption for building 123">Analyze energy consumption for building 123</option>
                            <option value="Analyze energy consumption for building 456">Analyze energy consumption for building 456</option>
                            <option value="Show me energy usage patterns">Show me energy usage patterns</option>
                            <option value="Find energy optimization opportunities">Find energy optimization opportunities</option>
                            <option value="What is the date of the most recent energy usage reading?">What is the date of the most recent energy usage reading?</option>
                            <option value="Get the latest meter readings">Get the latest meter readings</option>
                            <option value="Show me the most recent energy data">Show me the most recent energy data</option>
                        </optgroup>
                        <optgroup label="📊 Portfolio Management">
                            <option value="Show me portfolio performance metrics">Show me portfolio performance metrics</option>
                            <option value="Analyze portfolio energy usage">Analyze portfolio energy usage</option>
                            <option value="Benchmark portfolio performance">Benchmark portfolio performance</option>
                            <option value="Generate sustainability report">Generate sustainability report</option>
                        </optgroup>
                        <optgroup label="📄 Document Processing">
                            <option value="Summarize this utility bill document">Summarize this utility bill document</option>
                            <option value="Extract data from energy report">Extract data from energy report</option>
                            <option value="Process ESG report">Process ESG report</option>
                        </optgroup>
                        <optgroup label="🔍 Out-of-Scope Examples">
                            <option value="Who was the first president of the United States?">Who was the first president of the United States?</option>
                            <option value="What's the weather like today?">What's the weather like today?</option>
                            <option value="Tell me about the history of Rome">Tell me about the history of Rome</option>
                            <option value="How do I make a chocolate cake?">How do I make a chocolate cake?</option>
                        </optgroup>
                    </select>
                    <button id="submitBtn" onclick="submitRequest()">Submit</button>
                </div>
                <div style="font-size: 12px; color: #7f8c8d; margin-top: 5px;">
                    💡 Tip: Select a sample question above, or type your own request
                </div>
            </div>
            
            <div class="results" id="results"></div>
        </div>
        
        <script>
            function loadSample() {
                const select = document.getElementById('sampleSelect');
                const input = document.getElementById('userInput');
                if (select.value) {
                    input.value = select.value;
                    // Reset dropdown to placeholder
                    select.value = '';
                }
            }
            
            function submitRequest() {
                const input = document.getElementById('userInput');
                if (!input.value.trim()) return;
                
                document.getElementById('results').innerHTML = '<p>Processing...</p>';
                
                fetch('/process', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({request: input.value})
                })
                .then(response => response.json())
                .then(data => {
                    displayResults(data);
                })
                .catch(error => {
                    document.getElementById('results').innerHTML = '<p class="error">Error: ' + error + '</p>';
                });
            }
            
            function displayResults(data) {
                const resultsDiv = document.getElementById('results');
                let html = '<h3>📊 Results</h3>';
                
                if (data.error) {
                    html += '<p class="error">❌ Error: ' + data.error + '</p>';
                } else {
                    html += '<p class="success">✅ Workflow: ' + data.workflow + '</p>';
                    html += '<p>📋 Steps executed: ' + data.steps_executed + '</p>';
                    
                    // Add planning method info
                    if (data.planning_method) {
                        const method = data.planning_method;
                        const reason = data.planning_reason || 'No reason provided';
                        
                        let methodIcon = '❓';
                        let methodText = method;
                        
                        if (method === 'learning_based') {
                            methodIcon = '🧠';
                            methodText = 'Learning-based (AI-powered)';
                        } else if (method === 'rule_based') {
                            methodIcon = '🔧';
                            methodText = 'Rule-based (Systematic)';
                        }
                        
                        html += '<p><strong>' + methodIcon + ' Planning Method:</strong> ' + methodText + '</p>';
                        html += '<p><strong>💭 Planning Reason:</strong> ' + reason + '</p>';
                    }
                    
                    // Add planning path details
                    if (data.planning_path) {
                        html += '<div class="log-section">';
                        html += '<div class="log-header" onclick="toggleLog(this)">';
                        html += '🧠 Planning Path Details';
                        html += '</div>';
                        html += '<div class="log-content">';
                        
                        const intent = data.planning_path.intent;
                        const workflow = data.planning_path.workflow_plan;
                        
                        html += '<h5>🔍 Intent Matching:</h5>';
                        html += '<ul>';
                        html += '<li><strong>Intent:</strong> ' + (intent.intent || 'Unknown') + '</li>';
                        html += '<li><strong>Confidence:</strong> ' + (intent.confidence || 0).toFixed(2) + '</li>';
                        html += '<li><strong>Reason:</strong> ' + (intent.reason || 'No reason provided') + '</li>';
                        html += '</ul>';
                        
                        html += '<h5>⚙️ Workflow Planning:</h5>';
                        html += '<ul>';
                        html += '<li><strong>Workflow ID:</strong> ' + (workflow.workflow_id || 'Unknown') + '</li>';
                        html += '<li><strong>Steps Planned:</strong> ' + (workflow.steps ? workflow.steps.length : 0) + '</li>';
                        html += '</ul>';
                        
                        if (workflow.steps) {
                            html += '<h5>📋 Planned Steps:</h5>';
                            html += '<ul>';
                            workflow.steps.forEach((step, index) => {
                                html += '<li><strong>Step ' + (index + 1) + ':</strong> ' + (step.agent || 'Unknown') + ' → ' + (step.tool || 'Unknown') + '</li>';
                            });
                            html += '</ul>';
                        }
                        
                        html += '</div>';
                        html += '</div>';
                    }
                    
                    if (data.results) {
                        html += '<h4>🔄 Step-by-step execution:</h4>';
                        for (const [stepName, stepData] of Object.entries(data.results)) {
                            html += '<div class="log-section">';
                            html += '<div class="log-header" onclick="toggleLog(this)">';
                            html += '📋 ' + stepName + ' - ' + (stepData.status || 'Success');
                            html += '</div>';
                            html += '<div class="log-content">';
                            html += '<pre>' + JSON.stringify(stepData, null, 2) + '</pre>';
                            html += '</div>';
                            html += '</div>';
                        }
                    }
                    
                    if (data.summary) {
                        html += '<p><strong>📝 Summary:</strong> ' + data.summary + '</p>';
                    }
                }
                
                resultsDiv.innerHTML = html;
            }
            
            function toggleLog(header) {
                const content = header.nextElementSibling;
                content.classList.toggle('expanded');
            }
            
            // Allow Enter key to submit
            document.getElementById('userInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    submitRequest();
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/process', methods=['POST'])
def process_request():
    data = request.get_json()
    user_request = data.get('request', '')
    
    # Run the async function in a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        result = loop.run_until_complete(process_user_request(user_request))
        return jsonify(result)
    finally:
        loop.close()

if __name__ == '__main__':
    print("🌐 Starting Web CLI...")
    print("📱 Open your browser to: http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080) 