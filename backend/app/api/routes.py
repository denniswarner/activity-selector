"""
API routes for the Activity Selector application.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from ..models import (
    Category, 
    Activity, 
    ActivityRequest, 
    ActivityResponse, 
    ErrorResponse,
    PriceLevel
)
from ..services.sheets_service import sheets_service

router = APIRouter(prefix="/api", tags=["activities"])


@router.get("/categories", response_model=List[Category])
async def get_categories():
    """
    Get all available activity categories.
    
    Returns:
        List[Category]: List of available categories
    """
    try:
        categories = sheets_service.get_categories()
        return categories
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch categories: {str(e)}"
        )


@router.get("/activities", response_model=List[Activity])
async def get_activities(
    category: str = Query(..., description="Category name"),
    price_level: PriceLevel = Query(None, description="Price level filter")
):
    """
    Get all activities for a specific category and optional price level.
    
    Args:
        category (str): Category name
        price_level (PriceLevel, optional): Price level filter
        
    Returns:
        List[Activity]: List of activities matching the criteria
    """
    try:
        activities = sheets_service.get_activities_by_category(category, price_level)
        return activities
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid request: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch activities: {str(e)}"
        )


@router.post("/suggest", response_model=ActivityResponse)
async def suggest_activities(request: ActivityRequest):
    """
    Get random activity suggestions based on category and price level.
    
    Args:
        request (ActivityRequest): Request containing category, price level, and limit
        
    Returns:
        ActivityResponse: Random suggestions with metadata
    """
    try:
        activities = sheets_service.get_random_activities(
            category=request.category,
            price_level=request.price_level,
            limit=request.limit or 5
        )
        
        # Get total count for the category/price combination
        all_activities = sheets_service.get_activities_by_category(
            request.category, 
            request.price_level
        )
        
        return ActivityResponse(
            activities=activities,
            total_found=len(all_activities),
            category=request.category,
            price_level=request.price_level
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid request: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get suggestions: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "service": "activity-selector-api",
        "version": "1.0.0"
    }


@router.get("/cache/stats")
async def get_cache_stats():
    """
    Get cache statistics (for debugging).
    
    Returns:
        dict: Cache statistics
    """
    from ..services.cache_service import cache_service
    return cache_service.get_cache_stats()


@router.delete("/cache/clear")
async def clear_cache():
    """
    Clear all cached data (for debugging).
    
    Returns:
        dict: Clear operation result
    """
    from ..services.cache_service import cache_service
    cache_service.clear()
    return {"message": "Cache cleared successfully"} 