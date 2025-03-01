#! /usr/bin/env bash
cd api
uv run alembic upgrade head
cd ..
export PYTHONPATH=$PYTHONPATH:`pwd`
uv run api/initial_data.py