from flask import Flask, render_template_string, request
import importlib

# TCP 요청 함수 정의한 파일명 (예: dong_client.py)
HTTP_Client = importlib.import_module("dong_client")

app = Flask(__name__)

# 케이스 목록
cases = [
    ("CASE1", "GET / 200 OK"),
    ("CASE2", "GET /NotFound 404"),
    ("CASE3", "POST Expect 100/200"),
    ("CASE4", "POST Expect 400"),
    ("CASE5", "POST /no_such_path 404"),
    ("CASE6", "PUT 200 OK"),
    ("CASE7", "PUT 400 Bad Request"),
    ("CASE8", "HEAD / 200 OK"),
    ("CASE9", "HEAD /missing 404"),
]

# HTML 템플릿
template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>HTTP 테스트 대시보드</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f8f9fa;
            padding: 40px;
        }
        h2 {
            color: #343a40;
        }
        form {
            margin-bottom: 30px;
        }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 8px 8px 8px 0;
            cursor: pointer;
            border-radius: 6px;
            font-weight: bold;
        }
        button:hover {
            background-color: #0056b3;
        }
        .panel {
            display: flex;
            gap: 20px;
        }
        textarea {
            width: 100%;
            height: 300px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            padding: 10px;
            resize: vertical;
            font-family: monospace;
            background-color: #fff;
        }
        .section {
            flex: 1;
        }
        .error {
            color: red;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h2>🔍 HTTP 테스트 케이스 실행기</h2>
    <form method="POST">
        {% for case, label in cases %}
            <button name="case" value="{{ case }}">{{ case }} - {{ label }}</button>
        {% endfor %}
    </form>

    {% if request_msg %}
        <div class="panel">
            <div class="section">
                <h3>📤 Request</h3>
                <textarea readonly>{{ request_msg }}</textarea>
            </div>
            <div class="section">
                <h3>📥 Response</h3>
                <textarea readonly>{{ response_msg }}</textarea>
            </div>
        </div>
    {% elif error_msg %}
        <p class="error">❌ {{ error_msg }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    request_msg = ""
    response_msg = ""
    error_msg = ""

    if request.method == "POST":
        selected_case = request.form.get("case")
        try:
            case_func = getattr(HTTP_Client, selected_case)
            request_msg, response_msg = case_func()
        except AttributeError:
            error_msg = f"해당 CASE 함수 '{selected_case}'가 존재하지 않습니다."
        except Exception as e:
            error_msg = f"예외 발생: {e}"

    return render_template_string(template, cases=cases,
                                  request_msg=request_msg,
                                  response_msg=response_msg,
                                  error_msg=error_msg)

if __name__ == "__main__":
    app.run(port=5000, debug=True)