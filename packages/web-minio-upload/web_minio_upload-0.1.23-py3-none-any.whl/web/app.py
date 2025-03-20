import os
import uuid
from datetime import timedelta
from flask import Flask, request, jsonify, render_template
from minio import Minio
from dotenv import load_dotenv

# 获取用户家目录路径
home_dir = os.path.expanduser("~")

# 根据操作系统构建路径
if os.name == 'nt':  # Windows
    config_file = os.path.join(home_dir, 'AppData', 'Local', 'web-upload')
else:  # Unix-like系统 (Linux/macOS)
    config_file = os.path.join(home_dir, '.config', 'web-upload')

# 加载用户家目录下的 ~/.config/web-upload 或 Windows 下的 AppData/Local/web-upload
load_dotenv(dotenv_path=config_file)

# 加载项目目录下的 .env 文件
load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

app = Flask(__name__)

# 读取 MinIO 配置
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")

if MINIO_ENDPOINT is None:
    if not os.path.exists(".env"):
        with open(".env", "w", encoding="utf-8") as f:
            f.write(
                "MINIO_ENDPOINT=\n"
                "MINIO_ACCESS_KEY=\n"
                "MINIO_SECRET_KEY=\n"
                "MINIO_BUCKET_NAME=\n"
            )
        raise RuntimeError(
            "Missing MinIO configuration. Please add the configuration to .env file."
        )


# MinIO 客户端
minio_client = Minio(MINIO_ENDPOINT, ACCESS_KEY, SECRET_KEY, secure=True)



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_presigned_url", methods=["POST"])
def get_presigned_url():
    file_name = request.json.get("file_name")
    if not file_name:
        return jsonify({"error": "Missing file name"}), 400

    # 生成唯一的文件名，防止覆盖
    unique_file_name = f"uploads/{uuid.uuid4().hex}_{file_name}"

    # 生成预签名 URL
    presigned_url = minio_client.presigned_put_object(
        BUCKET_NAME, unique_file_name, expires=timedelta(minutes=10)
    )

    # MinIO 文件访问 URL（适用于 MinIO 提供的公开访问）
    file_url = f"{MINIO_ENDPOINT}/{BUCKET_NAME}/{unique_file_name}"

    file_url = minio_client.get_presigned_url(
        "GET", BUCKET_NAME, unique_file_name, expires=timedelta(minutes=10)
    )

    return jsonify({"upload_url": presigned_url, "file_url": file_url})


def main(host="127.0.0.1", port=5000, debug=False):
    app.run( host=host, port=port, debug=debug)


if __name__ == "__main__":
    app.run(debug=True)
