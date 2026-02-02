"""
SQLAlchemy implementation of Batch Repository.

Persists Domain Models using SQL database via SQLAlchemy AsyncSession.
"""

import json
from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from src.ports.output.batch_repository import IBatchRepository
from src.domain.models.batch import Batch, BatchItem, BatchStatus
from src.infrastructure.db.session import get_session
from src.infrastructure.db.models import Batch as DbBatch, BatchItem as DbBatchItem

class SqlAlchemyRepository(IBatchRepository):
    """Async SQLAlchemy Batch Repository."""
    
    async def save(self, batch: Batch) -> None:
        """Save or update a batch."""
        print(f"DEBUG: Saving batch {batch.id}")
        async with get_session() as session:
            # Check if exists
            print("DEBUG: Checking if exists")
            stmt = select(DbBatch).where(DbBatch.id == batch.id).options(selectinload(DbBatch.items))
            result = await session.execute(stmt)
            db_batch = result.scalar_one_or_none()
            
            if db_batch:
                print("DEBUG: Updating existing")
                # Update existing
                db_batch.name = batch.name
                db_batch.status = batch.status.value
                db_batch.completed_at = batch.completed_at
                db_batch.error_message = batch.metadata.get("error")
                
                # Reconcile items (Simple strategy: delete all and recreate, or diff)
                # Ideally diff is better but for MVP delete-recreate is safer for consistency
                # Actually, cascading delete might handle it if we clear items.
                
                # Update existing items or add new ones
                # This logic is complex for ORMs. 
                # Let's map domain items to DB items.
                
                # Clear current items relationship (careful with orphans)
                # db_batch.items.clear() # This might not trigger delete if cascade not set right
                
                # Strategy: Map domain items to dicts and check differences?
                # Or simply update the simple fields and assume items are mostly appended.
                
                # FULL SYNC STRATEGY:
                # 1. Update batch fields
                # 2. Iterate items. If id matches DB item id, update. If new, insert.
                # Since Domain Batch doesn't hold DB IDs (it might in metadata), this is tricky.
                
                # FOR MVP: We assume Batch is the Aggregate Root.
                # However, Domain BatchItem implies it's a value object or entity.
                
                # Let's delete all items and re-insert them.
                # Not efficient but safe.
                # db_batch.items = []
                # await session.flush()
                
                # Re-add items
                new_items = []
                for item in batch.items:
                    new_items.append(DbBatchItem(
                        title=item.title,
                        prompt=item.prompt,
                        style_tags=json.dumps(item.style_tags),
                        status=item.status.value if hasattr(item.status, 'value') else item.status,
                        suno_id=item.suno_id
                    ))
                db_batch.items = new_items
                
            else:
                print("DEBUG: Creating new")
                # Create new
                db_batch = DbBatch(
                    id=batch.id,
                    name=batch.name,
                    status=batch.status.value,
                    created_at=batch.created_at,
                    completed_at=batch.completed_at,
                    error_message=batch.metadata.get("error")
                )
                
                print("DEBUG: Creating items")
                db_items = []
                for item in batch.items:
                    print(f"DEBUG: Processing item {item.title}")
                    db_items.append(DbBatchItem(
                        title=item.title,
                        prompt=item.prompt,
                        style_tags=json.dumps(item.style_tags),
                        status=item.status.value if hasattr(item.status, 'value') else item.status,
                        suno_id=item.suno_id
                    ))
                
                db_batch.items = db_items
                session.add(db_batch)
                
            await session.commit()

    async def get(self, batch_id: str) -> Optional[Batch]:
        """Get a batch by ID."""
        async with get_session() as session:
            stmt = select(DbBatch).where(DbBatch.id == batch_id).options(selectinload(DbBatch.items))
            result = await session.execute(stmt)
            db_batch = result.scalar_one_or_none()
            
            if not db_batch:
                return None
                
            return self._to_domain(db_batch)

    async def list_all(self) -> List[Batch]:
        """List all batches."""
        async with get_session() as session:
            stmt = select(DbBatch).options(selectinload(DbBatch.items)).order_by(DbBatch.created_at.desc())
            result = await session.execute(stmt)
            db_batches = result.scalars().all()
            
            return [self._to_domain(b) for b in db_batches]

    async def update(self, batch: Batch) -> None:
        """Update a batch."""
        await self.save(batch)

    async def delete(self, batch_id: str) -> None:
        """Delete a batch by ID."""
        async with get_session() as session:
            stmt = delete(DbBatch).where(DbBatch.id == batch_id)
            await session.execute(stmt)
            await session.commit()
            
    def _to_domain(self, db_batch: DbBatch) -> Batch:
        """Convert DB Model to Domain Model."""
        items = []
        for db_item in db_batch.items:
            # Handle style_tags (JSON string or list if using certain drivers, but we used dumps)
            style_tags = []
            if db_item.style_tags:
                try:
                    style_tags = json.loads(db_item.style_tags)
                except (json.JSONDecodeError, TypeError):
                    style_tags = []

            items.append(BatchItem(
                prompt=db_item.prompt,
                style_tags=style_tags,
                title=db_item.title,
                status=db_item.status, # String
                suno_id=db_item.suno_id
            ))
            
        return Batch(
            name=db_batch.name,
            id=str(db_batch.id),
            items=items,
            status=db_batch.status, # String cast to Enum in post_init
            created_at=db_batch.created_at,
            completed_at=db_batch.completed_at,
            metadata={"error": db_batch.error_message} if db_batch.error_message else {}
        )
