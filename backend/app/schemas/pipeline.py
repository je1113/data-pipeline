"""
Pipeline Pydantic schemas
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.db.models import PipelineStatus, ExecutionStatus


class PipelineNodeBase(BaseModel):
    node_id: str
    node_type: str
    config: Dict[str, Any]
    position_x: int
    position_y: int


class PipelineNodeCreate(PipelineNodeBase):
    pass


class PipelineNodeResponse(PipelineNodeBase):
    id: int
    pipeline_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PipelineBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class PipelineCreate(PipelineBase):
    nodes: Optional[List[PipelineNodeCreate]] = []


class PipelineUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    status: Optional[PipelineStatus] = None
    nodes: Optional[List[PipelineNodeCreate]] = None


class PipelineResponse(PipelineBase):
    id: int
    status: PipelineStatus
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    nodes: List[PipelineNodeResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


class PipelineValidationResult(BaseModel):
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []


class ExecutionStepBase(BaseModel):
    node_id: str
    step_name: str
    status: ExecutionStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None


class ExecutionStepResponse(ExecutionStepBase):
    id: int
    execution_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ExecutionBase(BaseModel):
    status: ExecutionStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    logs: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None


class ExecutionCreate(BaseModel):
    pipeline_id: int


class ExecutionResponse(ExecutionBase):
    id: int
    pipeline_id: int
    created_at: datetime
    steps: List[ExecutionStepResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


class PipelineExecuteRequest(BaseModel):
    parameters: Optional[Dict[str, Any]] = {}


class PipelineListResponse(BaseModel):
    pipelines: List[PipelineResponse]
    total: int
    page: int
    size: int
    pages: int
