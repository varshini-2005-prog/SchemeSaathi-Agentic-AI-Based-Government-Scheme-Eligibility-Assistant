"""
app/models/schemas.py
Pydantic schemas for request/response validation and status reporting.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class SystemStatusResponse(BaseModel):
    """Health check & status schema for SchemeSaathi Phase 1."""
    app_name: str = Field(..., json_schema_extra={"example": "SchemeSaathi"})
    version: str = Field(..., json_schema_extra={"example": "0.1.0"})
    status: str = Field(..., json_schema_extra={"example": "healthy"})
    environment: str = Field(..., json_schema_extra={"example": "development"})
    database_connected: bool = Field(..., json_schema_extra={"example": True})
    directories_ready: bool = Field(..., json_schema_extra={"example": True})
    details: Optional[Dict[str, Any]] = None

