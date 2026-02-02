from fastapi import FastAPI, HTTPException
from typing import List, Any
from src.application.tools import MaestroTools
from src.application.tool_schema import (
    DesignAlbumInput, DesignAlbumOutput,
    CreateBatchInput, CreateBatchOutput,
    AddItemsInput, AddItemsOutput,
    StartBatchInput,
    GetBatchInput, GetBatchOutput,
    ListBatchesInput, ListBatchesOutput,
    CompleteBatchInput, CompleteBatchOutput,
    CancelBatchInput, CancelBatchOutput
)

from contextlib import asynccontextmanager
from src.infrastructure.db.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events."""
    # Startup
    await init_db()
    yield
    # Shutdown
    # await close_db() # Optional, depends on session management

app = FastAPI(
    title="Maestro AI API",
    description="Neural Audio Workstation API - Generate albums and manage Suno batches",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# ===== ALBUM DESIGN =====
@app.post("/album/design", response_model=DesignAlbumOutput, tags=["Album Design"])
async def design_album(input_data: DesignAlbumInput) -> DesignAlbumOutput:
    """
    Design a complete concept album using AI.
    
    Generates album title and 8 tracks with lyrics based on archetype and genres.
    """
    try:
        return await MaestroTools.design_album(input_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== BATCH MANAGEMENT =====
@app.post("/batch", response_model=CreateBatchOutput, tags=["Batch Management"])
async def create_batch(input_data: CreateBatchInput) -> CreateBatchOutput:
    """Create a new Suno generation batch."""
    try:
        return await MaestroTools.create_batch(input_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch/{batch_id}/items", response_model=AddItemsOutput, tags=["Batch Management"])
async def add_items_to_batch(batch_id: str, items: List[dict]) -> AddItemsOutput:
    """Add tracks to an existing batch."""
    try:
        input_data = AddItemsInput(batch_id=batch_id, items=items)
        return await MaestroTools.add_items_to_batch(input_data)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Batch {batch_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/batch/{batch_id}", response_model=GetBatchOutput, tags=["Batch Management"])
async def get_batch(batch_id: str) -> GetBatchOutput:
    """Get batch details by ID."""
    try:
        input_data = GetBatchInput(batch_id=batch_id)
        return await MaestroTools.get_batch(input_data)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Batch {batch_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/batches", response_model=ListBatchesOutput, tags=["Batch Management"])
async def list_batches(status: str = None) -> ListBatchesOutput:
    """
    List all batches.
    
    Optionally filter by status: pending, processing, completed, failed, cancelled.
    """
    try:
        input_data = ListBatchesInput(status=status)
        return await MaestroTools.list_batches(input_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch/{batch_id}/start", tags=["Batch Operations"])
async def start_batch(batch_id: str) -> Any:
    """Start processing a batch."""
    try:
        input_data = StartBatchInput(batch_id=batch_id)
        return await MaestroTools.start_batch(input_data)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Batch {batch_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch/{batch_id}/complete", response_model=CompleteBatchOutput, tags=["Batch Operations"])
async def complete_batch(batch_id: str) -> CompleteBatchOutput:
    """Mark batch as completed."""
    try:
        input_data = CompleteBatchInput(batch_id=batch_id)
        return await MaestroTools.complete_batch(input_data)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Batch {batch_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch/{batch_id}/cancel", response_model=CancelBatchOutput, tags=["Batch Operations"])
async def cancel_batch(batch_id: str) -> CancelBatchOutput:
    """Cancel a batch."""
    try:
        input_data = CancelBatchInput(batch_id=batch_id)
        return await MaestroTools.cancel_batch(input_data)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Batch {batch_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== SYSTEM =====
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.2.0", "tools": 8}

