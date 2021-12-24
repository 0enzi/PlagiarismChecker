FROM python:3.9

# setup project into docker
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# predownloaded machine learning model from spacy
RUN pip install ./en_core_web_sm-3.2.0.tar.gz 

# run on terminal
CMD ["python", "app.py"]