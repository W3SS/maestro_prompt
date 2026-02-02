import json
import os
import pytest
from src.adapters.output.persistence.json_file_repository import JsonFileRepository
from src.domain.models.batch import Batch, BatchStatus

@pytest.fixture
def temp_json_file(tmp_path):
    """Create a temporary JSON file for testing."""
    file_path = tmp_path / "test_batches.json"
    return str(file_path)

@pytest.fixture
def repository(temp_json_file):
    """Create a repository instance using the temp file."""
    return JsonFileRepository(data_file=temp_json_file)

@pytest.fixture
def sample_batch():
    """Create a sample batch for testing."""
    return Batch(
        id="batch-123",
        name="Test Batch",
        items=[],
        status=BatchStatus.PENDING
    )

class TestJsonFileRepository:
    def test_repository_initialization_creates_file(self, temp_json_file):
        """Test that initialization creates the file if it doesn't exist."""
        assert not os.path.exists(temp_json_file)
        JsonFileRepository(data_file=temp_json_file)
        assert os.path.exists(temp_json_file)
        with open(temp_json_file, 'r') as f:
            data = json.load(f)
            assert data == {}

    def test_save_and_get_batch(self, repository, sample_batch):
        """Test saving and retrieving a batch."""
        repository.save(sample_batch)
        
        retrieved = repository.get(sample_batch.id)
        assert retrieved is not None
        assert retrieved.id == sample_batch.id
        assert retrieved.name == sample_batch.name

    def test_get_nonexistent_batch(self, repository):
        """Test retrieving a batch that doesn't exist."""
        result = repository.get("nonexistent-id")
        assert result is None

    def test_list_all_batches(self, repository, sample_batch):
        """Test listing all batches."""
        batch2 = Batch(id="batch-456", name="Batch 2")
        
        repository.save(sample_batch)
        repository.save(batch2)
        
        all_batches = repository.list_all()
        assert len(all_batches) == 2
        
        ids = [b.id for b in all_batches]
        assert sample_batch.id in ids
        assert batch2.id in ids

    def test_update_batch(self, repository, sample_batch):
        """Test updating an existing batch."""
        repository.save(sample_batch)
        
        # Modify batch
        sample_batch.status = BatchStatus.COMPLETED
        repository.save(sample_batch)
        
        retrieved = repository.get(sample_batch.id)
        assert retrieved.status == BatchStatus.COMPLETED

    def test_delete_batch(self, repository, sample_batch):
        """Test deleting a batch."""
        repository.save(sample_batch)
        assert repository.get(sample_batch.id) is not None
        
        repository.delete(sample_batch.id)
        assert repository.get(sample_batch.id) is None

    def test_persistence_across_instances(self, temp_json_file, sample_batch):
        """Test that data persists when reloading the repository."""
        repo1 = JsonFileRepository(data_file=temp_json_file)
        repo1.save(sample_batch)
        
        # New instance pointing to same file
        repo2 = JsonFileRepository(data_file=temp_json_file)
        retrieved = repo2.get(sample_batch.id)
        
        assert retrieved is not None
        assert retrieved.id == sample_batch.id
