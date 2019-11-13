FROM python:3.6-buster

WORKDIR /opt/pyahoo/ 

COPY *.py ./
COPY Pip* ./
COPY README.md ./
COPY util/ util/

RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

# CMD [ "tail", "-f", "/opt/pyahoo/README.md" ]
CMD [ "python", "main.py" ]

