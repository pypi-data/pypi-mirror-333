#!/usr/bin/env python
import uvicorn
import os
import yaml
import logging.config
from autologging import logged
from typing import Dict, Any, Iterator, AsyncIterator
from pathlib import Path
from autologging import logged
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from starlette.datastructures import MutableHeaders
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableLambda
from langserve import add_routes
from fastapi.responses import HTMLResponse, RedirectResponse
from sktaip_api.utils import (
    AIPHeaderMiddleware,
    per_req_config_modifier,
    custom_openapi,
    get_login_html_content,
    init_app,
    add_login,
    load_environment,
)

import importlib.util


def set_up_graph_routes(app: FastAPI, graph_path: str):
    # graph_execution_chain = (
    #     create_state
    #     | compiled_graph
    #     | RunnableLambda(parse_result, afunc=aparse_result)
    # )
    # graph_path의 형식은 "/path/to/module.py:object_name" 입니다.
    try:
        module_file, object_name = graph_path.split(":")
    except ValueError:
        raise ValueError(
            "graph_path 형식이 올바르지 않습니다. 예시: '/path/to/module.py:object_name'"
        )
    module_file = module_file.strip()
    object_name = object_name.strip()
    # importlib를 사용하여 모듈을 동적으로 로드합니다.
    spec = importlib.util.spec_from_file_location("dynamic_module", module_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"모듈 {module_file}을(를) 찾을 수 없습니다.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # 지정한 이름의 객체를 모듈에서 가져옵니다.
    try:
        graph = getattr(module, object_name)
    except AttributeError:
        raise AttributeError(
            f"모듈 {module_file}에 {object_name}이(가) 존재하지 않습니다."
        )
    add_routes(
        app,
        graph,
        path="",
        per_req_config_modifier=per_req_config_modifier,
    )
    return app


@logged
def create_app(graph_path: str) -> FastAPI:
    app = init_app()
    app = set_up_graph_routes(app=app, graph_path=graph_path)
    app = add_login(app=app)
    return app


@logged
def run_server(
    host: str,
    port: int,
    graph_name: str,
    graph_path: str,
    reload: bool = False,
    env_file: str | None = None,
):
    load_environment(env_file)
    app = create_app(graph_path)

    uvicorn.run(app, host="0.0.0.0", port=port)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=18080)
