"""
API route handlers for SheShield AI Women Safety Route Assistant
"""
from fastapi import APIRouter, HTTPException, status
from models.schemas import (
    RouteRequest,
    SafeRouteRequest,
    RoutesResponse,
    SafeRoutesResponse,
    ErrorResponse
)
from services.mapbox_service import MapboxService
from services.safety_service import SafetyService

# Create router instance
router = APIRouter()

# Initialize services
mapbox_service = MapboxService()
safety_service = SafetyService()


@router.post(
    "/get-routes",
    response_model=RoutesResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Get routes between source and destination",
    description="Fetches 2-3 alternative routes using Mapbox Directions API"
)
async def get_routes(request: RouteRequest):
    """
    Fetch available routes between source and destination

    This endpoint uses the Mapbox Directions API to retrieve multiple
    route options with distance, duration, and coordinate information.

    Args:
        request: RouteRequest containing source and destination

    Returns:
        RoutesResponse with list of available routes

    Raises:
        HTTPException: If route fetching fails or no routes are found
    """
    try:
        # Fetch routes from Mapbox API
        routes = mapbox_service.fetch_routes(
            source=request.source,
            destination=request.destination,
            alternatives=True,
            max_routes=3
        )

        # Return successful response
        return RoutesResponse(routes=routes, status="success")

    except Exception as e:
        # Log error and return appropriate HTTP exception
        error_message = str(e)

        # Return bad request for invalid input or no routes found
        if "No routes found" in error_message or "API error" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "Unable to fetch routes",
                    "details": error_message
                }
            )

        # Return internal server error for other exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Internal server error while fetching routes",
                "details": error_message
            }
        )


@router.post(
    "/get-safe-routes",
    response_model=SafeRoutesResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Get safe routes with safety scoring",
    description="Fetches routes and evaluates their safety based on time of day and other factors"
)
async def get_safe_routes(request: SafeRouteRequest):
    """
    Fetch routes with safety assessment and scoring

    This endpoint combines route fetching with safety analysis.
    It evaluates each route based on:
    - Time of day (day/night)
    - Route distance and complexity
    - Simulated risk factors

    Each route receives:
    - Safety score (0-100)
    - Risk level (Low/Medium/High)
    - Explanation of safety assessment

    Args:
        request: SafeRouteRequest containing source, destination, and time

    Returns:
        SafeRoutesResponse with list of routes and safety information

    Raises:
        HTTPException: If route fetching fails or invalid input provided
    """
    try:
        # Validate time parameter
        if request.time.lower() not in ["day", "night"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "Invalid time parameter",
                    "details": "Time must be either 'day' or 'night'"
                }
            )

        # Step 1: Fetch routes from Mapbox API
        routes = mapbox_service.fetch_routes(
            source=request.source,
            destination=request.destination,
            alternatives=True,
            max_routes=3
        )

        # Step 2: Calculate safety scores for each route
        safe_routes = safety_service.score_multiple_routes(
            routes=routes,
            time_of_day=request.time
        )

        # Return successful response with safety-enhanced routes
        return SafeRoutesResponse(routes=safe_routes, status="success")

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        # Log error and return appropriate HTTP exception
        error_message = str(e)

        # Return bad request for invalid input or no routes found
        if "No routes found" in error_message or "API error" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "Unable to fetch safe routes",
                    "details": error_message
                }
            )

        # Return internal server error for other exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "Internal server error while processing safe routes",
                "details": error_message
            }
        )
