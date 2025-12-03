from flask import Flask, request, render_template_string, jsonify
import json
import customer_classifier

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Customer Classifier — UI</title>
  <style>
    :root{
      --blue:#145ea8;
      --blue-600:#1f6feb;
      --green:#2bb673;
      --muted:#6b7280;
      --card:#ffffff;
      --bg:#f3f7fb;
      --radius:10px;
    }
    html,body{height:100%;margin:0;font-family:Inter,Segoe UI,Roboto,Arial,sans-serif;background:var(--bg);color:#0f1724}
    .wrap{max-width:1100px;margin:28px auto;padding:20px;display:grid;grid-template-columns:260px 1fr 320px;gap:20px;align-items:start}
    .panel{background:var(--card);border-radius:var(--radius);box-shadow:0 6px 20px rgba(15,23,42,0.06);padding:18px}
    .logo-placeholder{height:72px;border-radius:8px;background:linear-gradient(90deg,var(--blue-600),var(--green));display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:18px}
    nav ul{list-style:none;padding:0;margin:14px 0 0}
    nav li{padding:10px 6px;border-radius:8px;color:var(--blue-600);cursor:pointer}
    nav li:hover{background:linear-gradient(90deg, rgba(31,111,235,0.06), rgba(43,182,115,0.04))}
    .card-title{font-size:16px;color:var(--blue);margin:0 0 10px}
    form textarea{width:100%;min-height:140px;padding:12px;border:1px solid #e6edf7;border-radius:8px;resize:vertical;font-size:14px}
    .controls{display:flex;gap:10px;margin-top:12px;align-items:center}
    .btn{background:var(--blue-600);color:#fff;border:none;padding:10px 14px;border-radius:8px;cursor:pointer;font-weight:600}
    .btn.alt{background:#eef9f3;color:var(--green);border:1px solid rgba(43,182,115,0.12)}
    .muted{color:var(--muted);font-size:13px}
    .result{background:#0b1220;color:#e6eef8;padding:12px;border-radius:8px;overflow:auto;font-family:Consolas,monospace;font-size:13px}
    .section{margin-bottom:14px}
    /* FAQ right panel */
    .faq h3{margin-top:0;margin-bottom:8px;color:var(--green)}
    .faq p{margin:0;color:var(--muted);font-size:14px}
    @media (max-width:1000px){
      .wrap{grid-template-columns:1fr;padding:12px}
      .faq{order:3}
    }
  </style>
</head>
<body>
  <div class="wrap">
    <aside class="panel">
      <div class="logo-placeholder"><img src='/static/images/SCB logo.jpg'></div>
      <nav>
        <ul>
          <li>History</li>
          <li>Favourite</li>
          <li>Others</li>
        </ul>
      </nav>
    </aside>

    <main class="panel">
      <h2 class="card-title">Customer Attribute Classifier</h2>
      <p class="muted">Enter natural language prompt describing the customer data you need extracted. The agent will return categorized attributes.</p>

      <form method="post" id="query-form">
        <div class="section">
          <label for="prompt" class="muted">Prompt</label>
          <textarea id="prompt" name="prompt" placeholder="e.g. rel_id: REL-12345 customer email john.doe@example.com age 34"></textarea>
        </div>

        <div class="controls">
          <button class="btn" type="submit">Extract Attributes</button>
          <button type="button" class="btn alt" id="example-btn">Insert Example</button>
          <span class="muted" style="margin-left:auto">Blue &amp; Green theme • Read-only</span>
        </div>
      </form>

      {% if result %}
      <div style="margin-top:16px">
        <h3 style="margin:0 0 8px;color:var(--blue)">Output</h3>
        <div class="result">
          <pre>{{ result }}</pre>
        </div>
      </div>
      {% endif %}
    </main>

    <aside class="panel faq">
      <h3>FAQ</h3>
      <p>Instructions</p>
      <hr style="margin:12px 0;border:none;border-top:1px solid #eef4f9">
      <p class="muted"><strong>Tips:</strong><br>- Mention rel_id or customer id when possible.<br>- Use explicit attributes like "email", "date_of_birth".</p>
    </aside>
  </div>

  <script>
    (function(){
      const form = document.getElementById('query-form');
      const exampleBtn = document.getElementById('example-btn');
      exampleBtn.addEventListener('click', function(){
        document.getElementById('prompt').value = "rel_id: REL-12345 customer: John Doe email: john.doe@example.com age: 34 date_of_birth: 1990-05-12";
      });
      // Allow Ctrl+Enter submit
      document.getElementById('prompt').addEventListener('keydown', function(e){
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') form.submit();
      });
    })();
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    query = ""
    if request.method == "POST":
        query = request.form.get("prompt", "").strip()
        if query:
            try:
                # Call classifier (may use LLM or fallback rules)
                result = customer_classifier.extract_attributes_via_llm(query)
            except Exception as e:
                result = f"Error: {str(e)}"
        else:
            result = "Error: empty prompt"
    return render_template_string(HTML_TEMPLATE, result=result, query=query)

@app.route("/api/extract", methods=["POST"])
def api_extract():
    data = request.get_json(force=True, silent=True) or {}
    prompt = data.get("prompt") or ""
    if not prompt:
        return jsonify({"error": "Missing 'prompt' in request body"}), 400
    try:
        out = customer_classifier.extract_attributes_via_llm(prompt)
        return jsonify({"result": out})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Local development server
    app.run(host="127.0.0.1", port=5050, debug=True)
