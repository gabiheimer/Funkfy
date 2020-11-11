FROM python:3.8-slim 
RUN apt-get update
RUN apt-get install -y ffmpeg
# RUN pip install pydub
# RUN pip install --upgrade pip
# RUN pip install spleeter
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 5000
# ENTRYPOINT [ "python" ]
# CMD [ "-m", "flask", "run", "--host", "0.0.0.0" ]