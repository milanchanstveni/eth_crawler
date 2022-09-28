FROM python:latest

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["streamlit", "run", "app.py", "--server.runOnSave=true", "--server.address=0.0.0.0", "--server.port=5000", "--server.baseUrlPath=/app", "--server.enableCORS=true", "--ui.hideTopBar=true", "--ui.hideSidebarNav=true", "--theme.base=dark"]