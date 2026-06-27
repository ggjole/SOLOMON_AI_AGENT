# PROJECT LIBS
from Core.response_api import response,get_models
# from Core.commands.web_command import


# BASIC LIBS
import uuid
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware



print('aman')