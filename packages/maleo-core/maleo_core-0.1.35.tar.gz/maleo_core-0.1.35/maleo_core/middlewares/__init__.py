from fastapi import FastAPI

from .authorization import add_authorization_middleware
from .cors import add_cors_middleware
from .exception import add_exception_middleware
from .process_time import add_process_time_middleware
from .rate_limit import add_rate_limit_middleware

class MiddlewareManager:
    def __init__(self, app:FastAPI):
        self.app = app

    def add_all_middlewares(self):
        self.add_rate_limit_middleware()
        self.add_exception_middleware()
        self.add_cors_middleware()
        self.add_authorization_middleware()
        self.add_process_time_middleware()

    def add_rate_limit_middleware(self):
        add_rate_limit_middleware(self.app)

    def add_exception_middleware(self):
        add_exception_middleware(self.app)

    def add_cors_middleware(self):
        add_cors_middleware(self.app)

    def add_authorization_middleware(self):
        add_authorization_middleware(self.app)

    def add_process_time_middleware(self):
        add_process_time_middleware(self.app)