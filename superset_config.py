FROM apache/superset:6.1.0

USER root

# Install Shillelagh with the Generic JSON API extra (pulls the correct dependencies)
RUN pip install --no-cache-dir \
    --target=/app/.venv/lib/python3.10/site-packages \
    --timeout 120 \
    --retries 10 \
    "shillelagh[genericjsonapi]==1.4.5"

# Make sure the correct jsonpath library is present (same one as your local venv)
RUN pip install --no-cache-dir \
    --target=/app/.venv/lib/python3.10/site-packages \
    --timeout 120 \
    --retries 10 \
    "python-jsonpath==2.2.1"

# Verify with the same interpreter Superset uses (the build fails here if the adapter can't load)
RUN /app/.venv/bin/python -c "import shillelagh; print('SHILLELAGH VERSION:', shillelagh.__version__)"
RUN /app/.venv/bin/python -c "import jsonpath; print('JSONPATH FILE:', jsonpath.__file__)"
RUN /app/.venv/bin/python -c "from shillelagh.adapters.api.generic_json import GenericJSONAPI; print('GENERIC JSON API ADAPTER: OK')"

USER superset

COPY superset_config.py /app/pythonpath/superset_config.py

ENV SUPERSET_CONFIG_PATH=/app/pythonpath/superset_config.py
ENV SUPERSET_LOAD_EXAMPLES=no
ENV SUPERSET_WEBSERVER_WORKERS=1
ENV SERVER_THREADS_AMOUNT=2

EXPOSE 10000

# set-database-uri recreates the Shillelagh connection on every boot (your SQLite DB is wiped on each deploy)
CMD ["sh", "-c", "superset db upgrade && (superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@example.com
