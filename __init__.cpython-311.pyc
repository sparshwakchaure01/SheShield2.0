"""
Pydantic models for request and response validation
"""
from pydantic import BaseModel, Field
from typing import List, Tuple, Optional


class RouteRequest(BaseModel):
    """
    Request model for basic route fetching
    """
    source: str = Field(..., description="Source location (address or coordinates)")
    destination: str = Field(..., description="Destination location (address or coordinates)")


class SafeRouteRequest(BaseModel):
    """
    Request model for safe route fetching with time context
    """
    source: str = Field(..., description="Source location (address or coordinates)")
    destination: str = Field(..., description="Destination location (address or coordinates)")
    time: str = Field(..., description="Time of travel: 'day' or 'night'")


class RouteInfo(BaseModel):
    """
    Basic route information from Mapbox
    """
    distance: float = Field(..., description="Distance in kilometers")
    duration: float = Field(..., description="Duration in minutes")
    coordinates: List[List[float]] = Field(..., description="List of [longitude, latitude] coordinates")


class SafeRouteInfo(BaseModel):
    """
    Enhanced route information with safety metrics
    """
    path: List[List[float]] = Field(..., description="Route coordinates [longitude, latitude]")
    distance: float = Field(..., description="Distance in kilometers")
    duration: float = Field(..., description="Duration in minutes")
    safety_score: int = Field(..., description="Safety score from 0-100")
    risk_level: str = Field(..., description="Risk level: Low, Medium, or High")
    reason: str = Field(..., description="Explanation of safety assessment")


class RoutesResponse(BaseModel):
    """
    Response containing multiple routes
    """
    routes: List[RouteInfo]
    status: str = "success"


class SafeRoutesResponse(BaseModel):
    """
    Response containing multiple routes with safety information
    """
    routes: List[SafeRouteInfo]
    status: str = "success"


class ErrorResponse(BaseModel):
    """
    Error response model
    """
    status: str = "error"
    message: str
    details: Optional[str] = None
