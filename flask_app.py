from flask import Flask, request, jsonify, render_template_string
import json
from db_agent_app import get_user_prompt

app = Flask(__name__)

HTML_FORM = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent</title>
    <style>
        :root {
            --primary-color: #1f6feb;
            --secondary-color: #f4f4f4;
            --text-color: #333;
            --background-color: #f9f9f9;
            --border-radius: 8px;
        }
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            height: 100vh;
            background-color: var(--background-color);
        }
        .side-menu {
            width: 200px;
            background: var(--primary-color);
            color: white;
            padding: 20px;
            box-sizing: border-box;
        }
        .side-menu h2 {
            margin-top: 0;
            font-size: 18px;
        }
        .side-menu ul {
            list-style: none;
            padding: 0;
        }
        .side-menu ul li {
            margin: 10px 0;
        }
        .side-menu ul li a {
            color: white;
            text-decoration: none;
        }
        .main-content {
            flex: 1;
            padding: 20px;
            box-sizing: border-box;
        }
        .main-content h1 {
            font-size: 24px;
            color: var(--primary-color);
        }
        .main-content input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: var(--border-radius);
        }
        .main-content button {
            padding: 10px 20px;
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: var(--border-radius);
            cursor: pointer;
        }
        .faq-panel {
            width: 300px;
            background: var(--secondary-color);
            padding: 20px;
            box-sizing: border-box;
            border-left: 1px solid #ddd;
            display: none;
        }
        .faq-panel h2 {
            margin-top: 0;
        }
        .faq-toggle {
            position: absolute;
            right: 320px;
            top: 20px;
            cursor: pointer;
            color: var(--primary-color);
            text-decoration: underline;
        }
        .result { 
            background: #f4f4f4; 
            padding: 15px; 
            margin-top: 20px; 
            border-radius: 5px; 
        }
    </style>
    <script>
        function toggleFAQ() {
            const faqPanel = document.getElementById('faq-panel');
            if (faqPanel.style.display === 'none' || faqPanel.style.display === '') {
                faqPanel.style.display = 'block';
            } else {
                faqPanel.style.display = 'none';
            }
        }
    </script>
</head>
<body>
    <div class="side-menu">
        <h2>Menu</h2>
        <ul>
            <li><a href="#">History</a></li>
            <li><a href="#">Favourite</a></li>
            <li><a href="#">Others</a></li>
        </ul>
    </div>
    <div class="main-content">
        <h1><img src='/static/images/logo.jpg' height="40"> Welcome, Leo!</h1>
        <form method="post">
            <input type="text" id="prompt" name="prompt">
            <button type=submit>Submit</button>
        </form>
        {% if result %}
        <div class="result">
            <strong>Result(s):</strong>
            <pre>{{ result }}</pre>
        </div>
        {% endif %}
    </div>
    <div id="faq-panel" class="faq-panel">
        <h2>FAQ</h2>
        <p>Tips to ask better questions</p>
        <ul>
            <li>Extract data for 1 data product at a time</li>
            <li>Case-sentitive</li>
            <li>Know the data elements</li>
            <li>get help from Ops team</li>
        </ul>
        <p><b>Supported Data Products</b></p>
        <ul>
            <li><a href="#">Case</a></li>
            <li><a href="#">Event</a></li>
        </ul>
    </div>
    <div class="faq-toggle" onclick="toggleFAQ()">FAQ</div>
</body>
</html>

"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        if prompt:
            try:
                # get_user_prompt returns a JSON string
                result_json = get_user_prompt(prompt)
                # pretty-print for the web form
                parsed = json.loads(result_json)
                result = json.dumps(parsed, indent=2, default=str)
            except Exception as e:
                result = json.dumps({"error": str(e)}, indent=2)
        else:
            result = json.dumps({"error": "Empty prompt"}, indent=2)
    return render_template_string(HTML_FORM, result=result)

@app.route("/api/query", methods=["POST"])
def api_query():
    data = request.get_json(force=True, silent=True)
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' in JSON body"}), 400
    prompt = str(data["prompt"]).strip()
    if not prompt:
        return jsonify({"error": "Empty prompt"}), 400
    try:
        result_json = get_user_prompt(prompt)
        # get_user_prompt returns stringified JSON; convert to proper JSON response
        result = json.loads(result_json)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # For local development only. Set FLASK_APP and use flask run in production.
    app.run(host="127.0.0.1", port=5000, debug=True)
