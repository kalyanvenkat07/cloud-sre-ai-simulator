FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

CMD ["bash", "-c", "uvicorn app:app --host 0.0.0.0 --port 7860 & streamlit run ui.py --server.port 7861 --server.address 0.0.0.0"]
