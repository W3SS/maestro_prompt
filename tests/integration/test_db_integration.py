"""Integration test for Database Persistence."""

import pytest
import asyncio
from typing import AsyncGenerator

from src.infrastructure.db.session import init_db, get_session_factory, close_db
from src.adapters.output.persistence.sqlalchemy_repository import SqlAlchemyRepository
from src.application.services.batch_manager import BatchManager
from src.domain.models.batch import Batch, BatchItem
from src.infrastructure.config import get_settings

@pytest.fixture(scope="module")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.mark.asyncio
async def test_sqlalchemy_repository_persistence():
    """Test full cycle of save and get using SQLAlchemy Repository."""
    # 1. Init DB (creates tables in memory or file)
    # Ensure usage of a test DB or temp file to avoid messing pro DB if configured?
    # Settings default is ./maestro.db. For test we might want to override?
    # But for simplicity we use default for now (or patch settings).
    
    await init_db()
    
    repo = SqlAlchemyRepository()
    
    # 2. Create Batch
    batch = Batch(name="Test DB Batch")
    batch.add_item(BatchItem(prompt="Test Prompt", style_tags=["test"]))
    
    # 3. Save
    await repo.save(batch)
    
    # 4. Get
    retrieved_batch = await repo.get(batch.id)
    
    assert retrieved_batch is not None
    assert retrieved_batch.id == batch.id
    assert retrieved_batch.name == "Test DB Batch"
    assert len(retrieved_batch.items) == 1
    assert retrieved_batch.items[0].prompt == "Test Prompt"
    
    # 5. Update
    batch.name = "Updated DB Batch"
    await repo.update(batch)
    
    updated_batch = await repo.get(batch.id)
    assert updated_batch.name == "Updated DB Batch"
    
    # 6. Delete
    await repo.delete(batch.id)
    
    deleted_batch = await repo.get(batch.id)
    assert deleted_batch is None
    
    await close_db()


@pytest.mark.asyncio
async def test_batch_manager_with_db():
    """Test BatchManager using the DB repository."""
    await init_db()
    
    repo = SqlAlchemyRepository()
    manager = BatchManager(repository=repo)
    
    # Create
    batch_dto = await manager.create_batch(name="Manager DB Test")
    
    # Verify persistence
    retrieved = await manager.get_batch(batch_dto.id)
    assert retrieved.name == "Manager DB Test"
    assert retrieved.status == "pending"
    
    await close_db()
