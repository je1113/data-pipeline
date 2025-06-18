"""
Pipeline management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.pipeline import (
    Pipeline,
    PipelineCreate,
    PipelineUpdate,
    PipelineResponse
)
from app.services.pipeline_service import PipelineService

router = APIRouter()


@router.get("/", response_model=List[PipelineResponse])
async def get_pipelines(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of pipelines"""
    service = PipelineService(db)
    return await service.get_pipelines(skip=skip, limit=limit, search=search)


@router.post("/", response_model=PipelineResponse)
async def create_pipeline(
    pipeline: PipelineCreate,
    db: Session = Depends(get_db)
):
    """Create a new pipeline"""
    service = PipelineService(db)
    return await service.create_pipeline(pipeline)


@router.get("/{pipeline_id}", response_model=PipelineResponse)
async def get_pipeline(
    pipeline_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific pipeline by ID"""
    service = PipelineService(db)
    pipeline = await service.get_pipeline(pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline


@router.put("/{pipeline_id}", response_model=PipelineResponse)
async def update_pipeline(
    pipeline_id: int,
    pipeline_update: PipelineUpdate,
    db: Session = Depends(get_db)
):
    """Update a pipeline"""
    service = PipelineService(db)
    pipeline = await service.update_pipeline(pipeline_id, pipeline_update)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline


@router.delete("/{pipeline_id}")
async def delete_pipeline(
    pipeline_id: int,
    db: Session = Depends(get_db)
):
    """Delete a pipeline"""
    service = PipelineService(db)
    success = await service.delete_pipeline(pipeline_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return {"message": "Pipeline deleted successfully"}


@router.post("/{pipeline_id}/execute")
async def execute_pipeline(
    pipeline_id: int,
    db: Session = Depends(get_db)
):
    """Execute a pipeline"""
    service = PipelineService(db)
    execution = await service.execute_pipeline(pipeline_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return {"execution_id": execution.id, "status": execution.status}


@router.post("/{pipeline_id}/validate")
async def validate_pipeline(
    pipeline_id: int,
    db: Session = Depends(get_db)
):
    """Validate a pipeline configuration"""
    service = PipelineService(db)
    validation_result = await service.validate_pipeline(pipeline_id)
    if not validation_result:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return validation_result
