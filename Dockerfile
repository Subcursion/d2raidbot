FROM python:3.10-alpine
COPY raid_info.py datetime_util.py converters.py __main__.py __init__.py /app/
COPY requirements.txt /
RUN pip install -r requirements.txt
CMD ["python3", "-m", "app"]