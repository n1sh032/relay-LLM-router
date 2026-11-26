import asyncio

import httpx
import pytest

import main
from app.providers.base import ChatResponse, IncompleteResponseError
from app.routing.router import Router

