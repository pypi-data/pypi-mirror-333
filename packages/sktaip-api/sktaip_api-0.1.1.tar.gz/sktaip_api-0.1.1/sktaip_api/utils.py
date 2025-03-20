import os
import re
from functools import wraps
from typing import Any, Dict
from uuid import uuid4

# from agentapp.package.runnables.handler.agent_handlers import NodeCallbackHandler
from sktaip_api.enum import HeaderKeys
from sktaip_api.playground_login import login_html
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, RedirectResponse
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langserve import add_routes
from starlette.datastructures import MutableHeaders
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv
import os
from pathlib import Path


ROOT_PATH = os.environ.get("ROOT_PATH", "")


def load_environment(path: str | None):
    """Load environment variables from .env file"""
    if path:
        env_path = Path(path)
        load_dotenv(dotenv_path=env_path)

    return os.environ


def formatting_token(auth_header: str) -> str:
    # from agent-gateway
    if auth_header.startswith("Bearer "):
        return auth_header[7:]
    # from swagger
    else:
        return auth_header


def is_from_graph_playground(request):
    try:
        referer = request.headers.get("referer", "")
        # /graph/playground 또는 /graph/playground/ 패턴을 찾음
        pattern = r"/graph/playground/?"
        return bool(re.search(pattern, referer))
    except (AttributeError, TypeError):
        return False


class AIPHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip middleware logic for /docs path
        playground_pattern = re.compile(f"^{re.escape(ROOT_PATH)}.*?/playground")
        if (
            (request.url.path == f"{ROOT_PATH}/docs")
            | (request.url.path in ["/favicon.ico"])
            | (request.url.path == f"{ROOT_PATH}/openapi.json")
            | (bool(playground_pattern.match(request.url.path)))
            | (request.url.path.startswith(f"{ROOT_PATH}/login"))
        ):
            return await call_next(request)

        new_headers = MutableHeaders()

        if is_from_graph_playground(request):
            # request from langserve playground
            # key: the key supposed to be / value: the key created from playground.
            aip_playground_header_map = {
                "Authorization": "authorization",
                HeaderKeys.AIP_USER.value: "AIP_USER",
                HeaderKeys.AIP_APP_SERVING_ID.value: "AIP_APP_SERVING_ID",
            }
            # transfer headers to required_headers key
            for header_name, cookie_name in aip_playground_header_map.items():
                if request.cookies.get(cookie_name):
                    new_headers.append(header_name, request.cookies.get(cookie_name))

        else:
            # request from swagger or agent gateway
            # 1. validate required headers
            required_aip_header_keys_set = set(
                [
                    "authorization",
                    HeaderKeys.AIP_USER.value,
                ]
            )
            missing_headers = required_aip_header_keys_set - set(
                [key.decode("utf-8").lower() for key, _ in request.headers.raw]
            )
            if missing_headers:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required header: {missing_headers}",
                )
            # 2. formatting token
            old_headers = [
                (key.decode("utf-8"), value.decode("utf-8"))
                for key, value in request.headers.raw
            ]
            for k, v in old_headers:
                if k.lower() == "authorization":
                    # (key) authorization -> Authorization
                    # (value) Bearer skxxxx -> skxxxx
                    v = formatting_token(v)
                    new_headers.append("Authorization", v)
                else:
                    new_headers.append(k, v)

        # if aip-transaction-id is not in headers, create value and append in headers
        transaction_id = new_headers.get(
            HeaderKeys.AIP_TRANSACTION_ID.value, str(uuid4())
        )
        if new_headers.get(HeaderKeys.AIP_TRANSACTION_ID.value) is None:
            new_headers.append(HeaderKeys.AIP_TRANSACTION_ID.value, transaction_id)
        request.scope["headers"] = new_headers.raw

        response = await call_next(request)
        response.headers[HeaderKeys.AIP_TRANSACTION_ID.value] = transaction_id
        return response


async def per_req_config_modifier(config: Dict, request: Request) -> Dict:
    """Modify the config for each request."""

    # config["configurable"] = {
    configurable = {
        HeaderKeys.AIP_TOKEN.value: request.headers["Authorization"],
        HeaderKeys.AIP_USER.value: request.headers[HeaderKeys.AIP_USER.value],
        HeaderKeys.AIP_TRANSACTION_ID.value: request.headers[
            HeaderKeys.AIP_TRANSACTION_ID.value
        ],  # insert in middleware
        HeaderKeys.AIP_APP_SERVING_ID.value: request.headers.get(
            HeaderKeys.AIP_APP_SERVING_ID
        ),
    }
    # add handler, 2025.01.20 kim dong-hun
    # handler = NodeCallbackHandler()
    app_name = os.environ.get("APP_NAME", "Local Dev")
    app_version = os.environ.get("APP_VERSION", "1.0.0")
    # handler.set_app_id(app_id=f"{app_name}-{app_version}")
    # handler.set_user_id(user_id=HeaderKeys.AIP_USER.value)
    # return config
    return RunnableConfig(configurable=configurable, callbacks=[])


def custom_openapi(app):
    if not app.openapi_schema:
        app_name = os.environ.get("APP_NAME", "Local Dev")
        app_version = os.environ.get("APP_VERSION", "1.0.0")
        openapi_schema = get_openapi(
            title="LangChain Server",
            description=f"PlatForm Agent App: {app_name}",
            version=app_version,
            routes=app.routes,
            servers=[{"url": ROOT_PATH}] if ROOT_PATH else None,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
        }

        openapi_schema["components"]["securitySchemes"] = {
            "APIKeyHeader": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
            }
        }

        # Add global security requirement
        openapi_schema["security"] = [{"APIKeyHeader": []}]

    else:
        openapi_schema = app.openapi_schema

    for path in openapi_schema["paths"].values():
        for method in path.values():
            # method.setdefault("parameters", []).extend(
            method["security"] = [{"APIKeyHeader": []}]
            method.setdefault("parameters", []).extend(
                [
                    {
                        "name": HeaderKeys.AIP_USER.value,
                        "in": "header",
                        "description": "user id",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "default": "aiplatform3/agenttest",
                        },
                    },
                    {
                        "name": HeaderKeys.AIP_APP_SERVING_ID.value,
                        "in": "header",
                        "description": "Serving ID to Identify Deployed Agent App",
                        "required": False,
                        "schema": {
                            "type": "string",
                        },
                    },
                    {
                        "name": HeaderKeys.AIP_TRANSACTION_ID.value,
                        "in": "header",
                        "description": "A unique identifier for each request(graph query)",
                        "required": False,
                        "schema": {
                            "type": "string",
                        },
                    },
                ]
            )

    return openapi_schema


def get_login_html_content(hasError: bool = False):
    error_message = "<p>Invalid API Key</p>" if hasError else ""
    return login_html.format(root_path=ROOT_PATH, error_message=error_message)


def init_app() -> FastAPI:
    print("Initializing App")

    app = FastAPI(root_path=ROOT_PATH)

    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    app.add_middleware(AIPHeaderMiddleware)
    return app


def add_login(app: FastAPI) -> FastAPI:
    print("Adding Login")
    app.openapi_schema = custom_openapi(app=app)

    @app.get("/login", response_class=HTMLResponse)
    def login_form():
        return HTMLResponse(content=get_login_html_content())

    @app.post("/login")
    def login(
        api_key: str = Form(),
        aip_user: str = Form(),
        aip_app_serving_id: str | None = Form(default=None),
        prefix: str | None = Form(default=""),
    ):
        if api_key:
            prefix = prefix if prefix else ""
            response = RedirectResponse(
                url=f"{ROOT_PATH}{prefix}/playground", status_code=303
            )
            kv_list = [
                ("api_key", "authorization"),
                ("aip_user", "AIP_USER"),
                ("aip_app_serving_id", "AIP_APP_SERVING_ID"),
            ]
            for k, v in kv_list:
                if locals().get(k):
                    response.set_cookie(
                        key=v,
                        value=locals()[k],
                        httponly=True,
                        secure=True,
                        samesite="strict",
                    )
            return response
        return HTMLResponse(content=get_login_html_content(hasError=True))

    return app


def add_routes_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Code to be executed before add_routes
        print("Executing pre-add_routes logic")

        app = FastAPI(root_path=ROOT_PATH)

        # Set all CORS enabled origins
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
        )
        app.add_middleware(AIPHeaderMiddleware)
        # Call the original function (which includes add_routes)
        kwargs.pop("app", None)
        setup_routes = func(app, *args, **kwargs)
        app = setup_routes()

        # Code to be executed after add_routes
        print("Executing post-add_routes logic")
        app.openapi_schema = custom_openapi(app=app)

        @app.get("/login", response_class=HTMLResponse)
        def login_form():
            return HTMLResponse(content=get_login_html_content())

        @app.post("/login")
        def login(
            api_key: str = Form(...),
            aip_user: str = Form(...),
            aip_app_serving_id: str = Form(...),
            prefix: str = Form(...),
        ):
            if api_key:
                response = RedirectResponse(
                    url=f"{ROOT_PATH}{prefix}/playground", status_code=303
                )
                kv_list = [
                    ("api_key", "authorization"),
                    ("aip_user", "AIP_USER"),
                    ("aip_app_serving_id", "AIP_APP_SERVING_ID"),
                ]
                for k, v in kv_list:
                    response.set_cookie(
                        key=v,
                        value=locals()[k],
                        httponly=True,
                        secure=True,
                        samesite="strict",
                    )
                return response
            return HTMLResponse(content=get_login_html_content(hasError=True))

        return app

    return wrapper
