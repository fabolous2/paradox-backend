#!/bin/bash

alembic upgrade head

uvicorn src.main.main:app --reload