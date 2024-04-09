FROM python:3.10-alpine
COPY raid_info.py datetime_util.py converters.py __main__.py __init__.py /app/
RUN python3.10 -m venv .venv && source .venv/bin/activate && pip install python-dotenv python-dateutil discord.py
CMD ["/.venv/bin/python", "-m", "app"]