"""
API v1 router
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    pipelines,
    data_sources,
    transforms,
    executions,
    users,
    auth
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(pipelines.router, prefix="/pipelines", tags=["pipelines"])
api_router.include_router(data_sources.router, prefix="/data-sources", tags=["data-sources"])
api_router.include_router(transforms.router, prefix="/transforms", tags=["transforms"])
api_router.include_router(executions.router, prefix="/executions", tags=["executions"])
