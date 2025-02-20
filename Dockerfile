FROM python

WORKDIR /gerenciadorCondominio

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py migrate && pyhton manage.py runserver 0.0.0.0:8000

