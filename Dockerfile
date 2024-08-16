FROM python:3.12-slim

WORKDIR /Users/lucyabney/bobert

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "__main__.py"]
