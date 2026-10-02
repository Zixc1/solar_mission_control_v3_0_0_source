FROM python:3.11-slim
RUN useradd -m smc
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .
USER smc
ENTRYPOINT ["solar-mission-control"]
CMD ["run"]
