from fastapi import FastAPI
from typing import Sequence
from maleo_core.models import BaseTransfers
from .authorization import add_authorization_middleware
from .cors import add_cors_middleware
from .exception import add_exception_middleware
from .process_time import add_process_time_middleware
from .rate_limit import add_rate_limit_middleware

class MiddlewareManager:
    def __init__(self, app:FastAPI):
        self.app = app

    def add_all_middlewares(
        self,
        allow_origins:Sequence[str] = (),
        allow_methods:Sequence[str] = ("GET",),
        allow_headers:Sequence[str] = (),
        allow_credentials:bool = False,
        expose_headers:Sequence[str] = (),
        permissions:BaseTransfers.Parameter.RoutesPermissions = {}
    ):
        self.add_rate_limit_middleware()
        self.add_exception_middleware()
        self.add_cors_middleware(allow_origins, allow_methods, allow_headers, allow_credentials, expose_headers)
        self.add_authorization_middleware(permissions)
        self.add_process_time_middleware()

    def add_rate_limit_middleware(self):
        add_rate_limit_middleware(self.app)

    def add_exception_middleware(self):
        add_exception_middleware(self.app)

    def add_cors_middleware(
        self,
        allow_origins:Sequence[str] = (),
        allow_methods:Sequence[str] = ("GET",),
        allow_headers:Sequence[str] = (),
        allow_credentials:bool = False,
        expose_headers:Sequence[str] = ()
    ):
        add_cors_middleware(self.app, allow_origins, allow_methods, allow_headers, allow_credentials, expose_headers)

    def add_authorization_middleware(self, permissions:BaseTransfers.Parameter.RoutesPermissions = {}):
        add_authorization_middleware(self.app, permissions)

    def add_process_time_middleware(self):
        add_process_time_middleware(self.app)