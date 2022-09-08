FROM python:3.9.14-alpine

ENV PYTHONUNBUFFERED=TRUE

RUN adduser -D appuser

WORKDIR /usr/share/appuser/

COPY --chown=appuser . .

USER appuser

RUN pip install --upgrade pip
RUN pip install -r req.txt

CMD [ "python", "-m", "manage.py", "runserver", "8000" ]