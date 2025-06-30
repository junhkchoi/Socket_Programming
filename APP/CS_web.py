from flask import Flask, render_template_string, request
from CLIENT import client  # client.py에 CASE1 ~ CASE9 함수 존재

app = Flask(__name__)

# HTML 템플릿
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>HTTP 테스트 클라이언트</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        a button { width: 120px; height: 35px; margin: 5px; font-size: 14px; }
        textarea { width: 100%; height: 200px; margin-top: 10px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>📡 TCP 소켓 기반 HTTP 테스트 클라이언트</h1>
    <div>
        {% for i in range(1, 10) %}
            <a href="/run/CASE{{ i }}"><button type="button">CASE{{ i }}</button></a>
        {% endfor %}
    </div>

    {% if request_msg %}
        <h2>📤 Request</h2>
        <textarea readonly>{{ request_msg }}</textarea>
    {% endif %}

    {% if response_msg %}
        <h2>📥 Response</h2>
        <textarea readonly>{{ response_msg }}</textarea>
    {% endif %}
</body>
</html>
'''

@app.route("/")
def index():
    # 처음 들어올 때는 아무 메시지 없음
    return render_template_string(HTML_TEMPLATE, request_msg=None, response_msg=None)

@app.route("/run/<case_name>")
def run_case(case_name):
    try:
        case_func = getattr(client, case_name)
        request_msg, response_msg = case_func()
        print(f"[{case_name}] 실행 완료")
    except Exception as e:
        request_msg = f"[ERROR] {e}"
        response_msg = ""

    return render_template_string(
        HTML_TEMPLATE,
        request_msg=request_msg,
        response_msg=response_msg
    )

if __name__ == "__main__":
    app.run(debug=True)