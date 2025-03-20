from typing import List
from pydantic import Field
from at_common_schemas.base import BaseSchema
from at_common_schemas.core.directory import Symbol, Exchange, Sector, Industry, Country

# Symbol
class DirectorySymbolListRequest(BaseSchema):
    pass

class DirectorySymbolListResponse(BaseSchema):
    items: List[Symbol] = Field(..., description="List of symbols")

# Exchange
class DirectoryExchangeListRequest(BaseSchema):
    pass

class DirectoryExchangeListResponse(BaseSchema):
    items: List[Exchange] = Field(..., description="List of exchanges")

# Sector
class DirectorySectorListRequest(BaseSchema):
    pass

class DirectorySectorListResponse(BaseSchema):
    items: List[Sector] = Field(..., description="List of sectors")

# Industry
class DirectoryIndustryListRequest(BaseSchema):
    pass

class DirectoryIndustryListResponse(BaseSchema):
    items: List[Industry] = Field(..., description="List of industries")

# Country
class DirectoryCountryListRequest(BaseSchema):
    pass

class DirectoryCountryListResponse(BaseSchema):
    items: List[Country] = Field(..., description="List of countries")