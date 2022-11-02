FROM tensorflow/tensorflow:2.8.3-gpu-jupyter

RUN apt-get update \
    && apt-get install -y ffmpeg \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* 

WORKDIR /inaSpeechSegmenter

COPY . ./

RUN pip install --upgrade pip && pip install . \
    && pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0","--port","80"]

