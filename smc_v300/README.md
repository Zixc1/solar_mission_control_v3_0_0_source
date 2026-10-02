# Solar Mission Control v3.0.0

A modular wrapper around the validated v2.7 scientific engine with PDF, interactive charts, SQLite run history, webhook/email helpers, typed configuration flow, and packaging.

## Install

```bash
conda env create -f environment.yml
conda activate solar-mission-control
pip install -e ".[full]"
```

## Run

```bash
solar-mission-control run --pdf --interactive
solar-mission-control quick --no-plots --no-images
solar-mission-control alert --dry-run
solar-mission-control monitor --interval 15
solar-mission-control health
```

Secrets are read from environment variables: `NASA_API_KEY`, `SPACE_WEATHER_WEBHOOK`, `SMC_SMTP_HOST`, `SMC_SMTP_USER`, and `SMC_SMTP_PASSWORD`.
