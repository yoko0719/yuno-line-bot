# ベースイメージ
FROM python:3.10-slim

# 作業ディレクトリの作成
WORKDIR /app

# 依存ファイルをコピー
COPY requirements.txt .

# 依存パッケージのインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリのコードをコピー
COPY . .

# ポート開放
EXPOSE 8080

# アプリ起動コマンド
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]