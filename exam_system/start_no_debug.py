"""
启动脚本 - 禁用 debug 模式
"""
import sys
print(f"Python: {sys.executable}")
print(f"Version: {sys.version}")

try:
    from langchain_openai import ChatOpenAI
    print("langchain_openai: OK")
except ImportError as e:
    print(f"langchain_openai import failed: {e}")

from app import create_app
app = create_app()
app.run(debug=False, host='0.0.0.0', port=5000)