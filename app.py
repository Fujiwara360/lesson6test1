# app.py
# 標準ライブラリのみで動作するBMI計算機Webアプリ
# ローカル / Render 共通で動作する

import os
import html
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs


def calc_bmi(height_cm, weight_kg):
    """BMIと評価を計算する。例外時は0扱いにする簡易ハンドリング"""
    try:
        height_m = float(height_cm) / 100
        weight = float(weight_kg)
        if height_m <= 0 or weight <= 0:
            return 0.0, "入力値を正しく入力してください"
        bmi = weight / (height_m ** 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0.0, "入力値を正しく入力してください"

    if bmi < 18.5:
        judge = "低体重（やせ型）"
    elif bmi < 25:
        judge = "普通体重"
    elif bmi < 30:
        judge = "肥満（1度）"
    elif bmi < 35:
        judge = "肥満（2度）"
    elif bmi < 40:
        judge = "肥満（3度）"
    else:
        judge = "肥満（4度）"

    return round(bmi, 2), judge


def render_page(height_val="", weight_val="", result_html=""):
    """HTMLページを生成する"""
    height_val = html.escape(str(height_val))
    weight_val = html.escape(str(weight_val))

    page = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>BMI計算機</title>
<style>
  body {{
    font-family: "Hiragino Kaku Gothic ProN", "Meiryo", sans-serif;
    background-color: #f4f6f8;
    display: flex;
    justify-content: center;
    padding-top: 40px;
  }}
  .card {{
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    padding: 24px 32px;
    width: 320px;
  }}
  h1 {{
    font-size: 20px;
    text-align: center;
    margin-bottom: 20px;
  }}
  label {{
    display: block;
    margin-top: 12px;
    font-size: 14px;
    color: #333;
  }}
  input[type="text"] {{
    width: 100%;
    padding: 8px;
    margin-top: 4px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 14px;
  }}
  .buttons {{
    display: flex;
    gap: 10px;
    margin-top: 20px;
  }}
  button {{
    flex: 1;
    padding: 10px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
  }}
  .btn-calc {{
    background-color: #4a90e2;
    color: #fff;
  }}
  .btn-clear {{
    background-color: #e0e0e0;
    color: #333;
  }}
  .result {{
    margin-top: 20px;
    padding: 12px;
    background-color: #f0f8ff;
    border-radius: 8px;
    text-align: center;
    font-size: 15px;
  }}
</style>
</head>
<body>
<div class="card">
  <h1>BMI計算機</h1>
  <form method="POST" action="/">
    <label for="height">身長 (cm)</label>
    <input type="text" id="height" name="height" value="{height_val}" placeholder="例: 170">

    <label for="weight">体重 (kg)</label>
    <input type="text" id="weight" name="weight" value="{weight_val}" placeholder="例: 60">

    <div class="buttons">
      <button type="submit" class="btn-calc">計算する</button>
      <button type="button" class="btn-clear" onclick="clearForm()">クリア</button>
    </div>
  </form>
  {result_html}
</div>
<script>
  // 入力値をすべて削除する
  function clearForm() {{
    document.getElementById('height').value = '';
    document.getElementById('weight').value = '';
  }}
</script>
</body>
</html>"""
    return page


class BMIHandler(BaseHTTPRequestHandler):

    def _send_html(self, body: str, status=200):
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == "/" or self.path == "":
            self._send_html(render_page())
        else:
            self._send_html("<h1>404 Not Found</h1>", status=404)

    def do_POST(self):
        if self.path != "/":
            self._send_html("<h1>404 Not Found</h1>", status=404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
        except (TypeError, ValueError):
            length = 0

        body = self.rfile.read(length).decode("utf-8") if length > 0 else ""
        params = parse_qs(body)
        height_raw = params.get("height", [""])[0]
        weight_raw = params.get("weight", [""])[0]

        bmi, judge = calc_bmi(height_raw, weight_raw)
        result_html = f"""
<div class="result">
  BMI: <strong>{bmi}</strong><br>
  判定: <strong>{html.escape(judge)}</strong>
</div>"""

        self._send_html(render_page(height_raw, weight_raw, result_html))

    def log_message(self, format, *args):
        # アクセスログを簡潔にする（標準出力に出すだけ）
        print("%s - %s" % (self.address_string(), format % args))


def main():
    # Render本番でもローカルでも共通で動くようPORTを環境変数から取得
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), BMIHandler)
    print(f"BMI計算機サーバーを起動しました: http://0.0.0.0:{port}/")
    server.serve_forever()


if __name__ == "__main__":
    main()
