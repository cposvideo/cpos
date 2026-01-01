venv\Scripts\activate
set PYTHONPATH=C:\cpos
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
