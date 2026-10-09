"""
app/models/scheme.py
Pydantic data models for structured government scheme definitions and eligibility rules.
"""

from pydantic import BaseModel, Field
from typing import List, Any, Optional


class EligibilityRule(BaseModel):
    """Represents a single deterministic eligibility condition for a scheme."""
    rule_id: str = Field(..., description="Unique rule identifier")
    field: str = Field(..., description="Profile field name being evaluated (e.g. age, annual_family_income)")
    operator: str = Field(..., description="Comparison operator (equals, in, less_than_or_equal, greater_than_or_equal, less_than)")
    target_value: Any = Field(..., description="Target threshold or required value")
    description: str = Field(..., description="Human-readable rule explanation")
    source: str = Field(..., description="Citation from official government document")


class Scheme(BaseModel):
    """Represents an official government scheme with metadata, eligibility rules, and documents."""
    scheme_id: str = Field(..., description="Unique scheme identifier code")
    scheme_name: str = Field(..., description="Official name of the scheme")
    scheme_category: str = Field(..., description="Category (Women Welfare, Student, Farmer Support, etc.)")
    government_level: str = Field(..., description="State, Central, or Central-State Joint")
    state: str = Field(..., description="Target state (e.g. Tamil Nadu, All India)")
    description: str = Field(..., description="Summary of scheme objectives")
    benefits: str = Field(..., description="Detailed monetary or service benefits provided")
    eligibility_rules: List[EligibilityRule] = Field(default_factory=list, description="List of deterministic rules")
    required_documents: List[str] = Field(default_factory=list, description="Mandatory supporting documents required")
    application_method: str = Field(..., description="Official submission method and portal details")
    official_url: str = Field(..., description="Official government web link")
    source_document: str = Field(..., description="Government Order (G.O.) or official document citation")
    last_verified_date: str = Field(..., description="ISO date of last rule verification")
