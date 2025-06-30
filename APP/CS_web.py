from flask import Flask, render_template_string, Response
from CLIENT import client 

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>HTTP 테스트 클라이언트</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        a button { width: 120px; height: 35px; margin: 5px; font-size: 14px; }
    </style>
</head>
<body>
    <h1>📡 TCP 소켓 기반 HTTP 테스트 클라이언트</h1>
    <div>
        {% for i in range(1, 10) %}
            <a href="/run/CASE{{ i }}"><button type="button">CASE{{ i }}</button></a>
        {% endfor %}
    </div>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/run/<case_name>")
def run_case(case_name):
    try:
        case_func = getattr(client, case_name)
        request_msg, response_msg = case_func()
        print(f"[{case_name}] 실행 완료")
    except Exception as e:
        print(f"[{case_name}] 실행 실패: {e}")

    # HTML 없이 204 응답
    return Response(status=204)

if __name__ == "__main__":
    app.run(debug=True)