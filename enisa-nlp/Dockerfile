FROM python:3.6.5-jessie

RUN pip install nltk==3.3 elasticsearch==6.3.0 \
progressbar-latest==2.4 scikit-learn==0.19.1 scipy==1.1.0 \
numpy==1.14.5 pandas==0.23.1 beautifulsoup4==4.6.0

WORKDIR /opt/enisa-nlp
COPY . /opt/enisa-nlp
RUN pip install -r requirements.txt

RUN python setup.py install

ENTRYPOINT [ "python" ]
CMD [ "topic/topic.py" ]
