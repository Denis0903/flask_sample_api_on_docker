import os
import io
import subprocess
from string import Template
from flask import Flask, request, jsonify
from flask import json
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
from sqlalchemy import asc, desc
import psycopg2
from psycopg2.extras import RealDictCursor
from logging.config import dictConfig
import logging
from flask_cors import CORS, cross_origin
import boto3
from botocore.exceptions import ClientError
import pyotp
import time
import asyncio

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s [%(levelname)s] [prismscaler] %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)
CORS(app, support_credentials=True)
# log=logging.getLogger("werkzeug")
# log.setLevel(logging.ERROR)
logging.getLogger("werkzeug").disabled = True

@app.before_request
def log_request_info():
    app.logger.info("%s %s", request.method, request.path)

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.route("/api/healthcheck", methods=["GET"])
@cross_origin(supports_credentials=True)
def health_checks():
    """
    ヘルスチェック用API
    """
    res={
        "APICondition":"Healthy",
    }
    return jsonify(res), 200

if __name__ == "__main__":
    app.run()