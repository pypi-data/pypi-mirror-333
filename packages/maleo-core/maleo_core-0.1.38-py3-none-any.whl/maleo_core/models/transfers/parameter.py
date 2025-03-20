from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Optional, Union

class DateFilter(BaseModel):
    name:str
    start:Optional[datetime] = None
    end:Optional[datetime] = None

class SortColumn(BaseModel):
    name:str
    order:Literal["asc", "desc"] = "asc"

class StatusUpdate(BaseModel):
    action:Literal["activate", "deactivate", "restore", "delete"] = Field(..., description="Status update's action to be executed")

class Check(BaseModel):
    is_active:Optional[bool] = Field(None, description="Filter results based on active status.")
    is_deleted:Optional[bool] = Field(None, description="Filter results based on deletion status.")

class GetQueryParameters(Check):
    page:int = Field(1, ge=1, description="Page number, must be >= 1.")
    limit:int = Field(10, ge=1, le=1000, description="Page size, must be 1 <= limit <= 1000.")
    search:Optional[str] = Field(None, description="Search parameter string.")

class GetBody(BaseModel):
    date_filters:list[DateFilter] = Field([], description="List of date filters to apply.")
    sort_columns:list[SortColumn] = Field([SortColumn(name="order", order="asc"), SortColumn(name="id", order="asc")], description="List of columns to sort by.")

    class Config:
        arbitrary_types_allowed = True

class Get(GetQueryParameters, GetBody): pass

AllowedMethods = Literal["GET", "POST", "PATCH", "PUT", "DELETE", "*"]
AllowedRoles = Union[List[int], Literal["*"]]
RoutesPermissions = Dict[str, Dict[AllowedMethods, AllowedRoles]]