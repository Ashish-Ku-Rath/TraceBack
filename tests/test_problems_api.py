"""
Automated tests for Problem Management System (Day 3).
Tests problem creation, retrieval, filtering, pagination, validation, and idempotent seeding.
Uses an isolated in-memory SQLite database via FastAPI dependency overrides.
"""

from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from backend.main import app
from backend.models.problem import Problem
from database.base import Base
from database.connection import get_db
from database.seed import seed_problems

# Configure isolated in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create fresh database schema per test and tear it down cleanly."""
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Provide FastAPI TestClient with overridden database dependency."""
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# ==============================================================================
# Problem Creation Tests
# ==============================================================================

def test_create_valid_problem(client: TestClient) -> None:
    """Test 1: Creating a valid problem succeeds and returns 201 Created."""
    payload = {
        "title": "Merge Two Sorted Lists",
        "slug": "merge-two-sorted-lists",
        "description": "Merge two sorted linked lists and return it as a sorted list.",
        "difficulty": "Easy",
        "constraints": "The number of nodes in both lists is in the range [0, 50].",
        "tags": ["Linked List", "Recursion", "Linked List"],  # Test tag deduplication
        "examples": [
            {
                "input": "list1 = [1,2,4], list2 = [1,3,4]",
                "expected_output": "[1,1,2,3,4,4]",
                "explanation": "Merged list in non-decreasing order.",
            },
            {
                "input": "list1 = [], list2 = []",
                "expected_output": "[]",
                "explanation": "Both lists are empty.",
            },
        ],
    }
    response = client.post("/problems", json=payload)
    assert response.status_code == 201
    data = response.json()

    assert data["id"] > 0
    assert data["title"] == "Merge Two Sorted Lists"
    assert data["slug"] == "merge-two-sorted-lists"
    assert data["difficulty"] == "Easy"
    assert data["constraints"] == "The number of nodes in both lists is in the range [0, 50]."
    # Tags should be deduplicated
    assert data["tags"] == ["Linked List", "Recursion"]
    assert len(data["examples"]) == 2
    assert data["examples"][0]["input"] == "list1 = [1,2,4], list2 = [1,3,4]"
    assert data["examples"][0]["expected_output"] == "[1,1,2,3,4,4]"
    assert data["examples"][0]["problem_id"] == data["id"]
    assert "created_at" in data
    assert "updated_at" in data


def test_reject_empty_title(client: TestClient) -> None:
    """Test 2: Reject problem with empty or whitespace-only title."""
    payload = {
        "title": "   ",
        "slug": "test-problem",
        "description": "Valid description.",
        "difficulty": "Easy",
    }
    response = client.post("/problems", json=payload)
    assert response.status_code == 422
    assert "Problem title cannot be empty" in response.text


def test_reject_empty_description(client: TestClient) -> None:
    """Test 2b: Reject problem with empty or whitespace-only description."""
    payload = {
        "title": "Valid Title",
        "slug": "valid-slug",
        "description": "    ",
        "difficulty": "Easy",
    }
    response = client.post("/problems", json=payload)
    assert response.status_code == 422
    assert "Problem description cannot be empty" in response.text


def test_reject_invalid_difficulty(client: TestClient) -> None:
    """Test 3: Reject problem creation with invalid difficulty level."""
    payload = {
        "title": "Valid Title",
        "slug": "valid-slug",
        "description": "Valid description.",
        "difficulty": "Impossible",
    }
    response = client.post("/problems", json=payload)
    assert response.status_code == 422
    assert "Invalid difficulty" in response.text


def test_reject_duplicate_slug(client: TestClient) -> None:
    """Test 4: Reject problem creation with duplicate slug (returns 400)."""
    payload = {
        "title": "First Problem",
        "slug": "unique-slug",
        "description": "Description one.",
        "difficulty": "Easy",
    }
    res1 = client.post("/problems", json=payload)
    assert res1.status_code == 201

    duplicate_payload = {
        "title": "Second Problem",
        "slug": "unique-slug",
        "description": "Description two.",
        "difficulty": "Medium",
    }
    res2 = client.post("/problems", json=duplicate_payload)
    assert res2.status_code == 400
    assert "already exists" in res2.text


def test_reject_empty_sample_example_fields(client: TestClient) -> None:
    """Test 4b: Reject sample example with blank input or expected output."""
    payload = {
        "title": "Example Validation",
        "description": "Testing example validation.",
        "difficulty": "Easy",
        "examples": [{"input": "", "expected_output": "out"}],
    }
    response = client.post("/problems", json=payload)
    assert response.status_code == 422
    assert "Sample input cannot be empty" in response.text


# ==============================================================================
# Problem Retrieval & Listing Tests
# ==============================================================================

def test_get_all_problems_summary(client: TestClient, db_session: Session) -> None:
    """Test 5: Retrieve problem listing returns clean summary schema without description/examples."""
    seed_problems(db_session)

    response = client.get("/problems")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 3
    for item in data:
        assert "id" in item
        assert "title" in item
        assert "slug" in item
        assert "difficulty" in item
        assert "tags" in item
        # Ensure description and examples are NOT in summary
        assert "description" not in item
        assert "examples" not in item

    assert response.headers.get("X-Total-Count") == "3"


def test_filter_by_difficulty(client: TestClient, db_session: Session) -> None:
    """Test 6: Filter problems by difficulty level."""
    seed_problems(db_session)

    # Filter Easy (case-insensitive)
    res_easy = client.get("/problems?difficulty=easy")
    assert res_easy.status_code == 200
    easy_items = res_easy.json()
    assert len(easy_items) == 2
    for item in easy_items:
        assert item["difficulty"] == "Easy"

    # Filter Medium
    res_med = client.get("/problems?difficulty=Medium")
    assert res_med.status_code == 200
    med_items = res_med.json()
    assert len(med_items) == 1
    assert med_items[0]["title"] == "Valid Parentheses"

    # Filter Hard (none exist in initial seed)
    res_hard = client.get("/problems?difficulty=Hard")
    assert res_hard.status_code == 200
    assert len(res_hard.json()) == 0

    # Invalid difficulty query parameter returns 400
    res_inv = client.get("/problems?difficulty=Extreme")
    assert res_inv.status_code == 400
    assert "Invalid difficulty" in res_inv.text


def test_filter_by_tag(client: TestClient, db_session: Session) -> None:
    """Test 7: Filter problems by category tag."""
    seed_problems(db_session)

    # Filter tag 'array' (case-insensitive)
    res_array = client.get("/problems?tag=array")
    assert res_array.status_code == 200
    array_items = res_array.json()
    assert len(array_items) == 1
    assert array_items[0]["title"] == "Two Sum"

    # Filter tag 'string'
    res_str = client.get("/problems?tag=string")
    assert res_str.status_code == 200
    str_items = res_str.json()
    assert len(str_items) == 2
    titles = {p["title"] for p in str_items}
    assert "Reverse String" in titles
    assert "Valid Parentheses" in titles

    # Filter nonexistent tag
    res_none = client.get("/problems?tag=dynamic-programming")
    assert res_none.status_code == 200
    assert len(res_none.json()) == 0


def test_search_by_title(client: TestClient, db_session: Session) -> None:
    """Test 8: Search problems by case-insensitive title keyword."""
    seed_problems(db_session)

    # Search 'two'
    res_two = client.get("/problems?search=two")
    assert res_two.status_code == 200
    items = res_two.json()
    assert len(items) == 1
    assert items[0]["title"] == "Two Sum"

    # Search 'parentheses'
    res_paren = client.get("/problems?search=Parentheses")
    assert res_paren.status_code == 200
    items = res_paren.json()
    assert len(items) == 1
    assert items[0]["title"] == "Valid Parentheses"

    # Search nonexistent string
    res_empty = client.get("/problems?search=nonexistent_xyz")
    assert res_empty.status_code == 200
    assert len(res_empty.json()) == 0


def test_get_individual_problem_by_id(client: TestClient, db_session: Session) -> None:
    """Test 9: Retrieve full individual problem details by ID."""
    seed_problems(db_session)

    response = client.get("/problems/1")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Two Sum"
    assert data["slug"] == "two-sum"
    assert "target" in data["description"]
    assert "nums.length" in data["constraints"]
    assert "Array" in data["tags"]
    assert "Hash Map" in data["tags"]
    assert len(data["examples"]) == 3
    assert data["examples"][0]["input"] == "nums = [2, 7, 11, 15], target = 9"
    assert data["examples"][0]["expected_output"] == "[0, 1]"
    assert data["examples"][0]["explanation"] is not None


def test_get_problem_by_slug(client: TestClient, db_session: Session) -> None:
    """Test 9b: Retrieve full individual problem details by unique slug."""
    seed_problems(db_session)

    response = client.get("/problems/slug/valid-parentheses")
    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Valid Parentheses"
    assert data["difficulty"] == "Medium"
    assert len(data["examples"]) == 3


def test_get_nonexistent_problem_404(client: TestClient, db_session: Session) -> None:
    """Test 10: Nonexistent problem returns 404 for both ID and Slug routes."""
    # By ID
    res_id = client.get("/problems/999999")
    assert res_id.status_code == 404
    assert "not found" in res_id.text

    # By Slug
    res_slug = client.get("/problems/slug/nonexistent-problem-slug")
    assert res_slug.status_code == 404
    assert "not found" in res_slug.text


def test_return_public_examples_correctly(client: TestClient, db_session: Session) -> None:
    """Test 11: Public sample examples are returned cleanly without hidden test metadata."""
    seed_problems(db_session)

    response = client.get("/problems/2")
    assert response.status_code == 200
    data = response.json()

    assert data["slug"] == "reverse-string"
    assert len(data["examples"]) == 2
    for ex in data["examples"]:
        assert "id" in ex
        assert "problem_id" in ex
        assert "input" in ex
        assert "expected_output" in ex
        assert "explanation" in ex
        # Ensure no hidden test case fields exist
        assert "is_hidden" not in ex
        assert "hidden" not in ex
        assert "score" not in ex


def test_pagination_behavior(client: TestClient, db_session: Session) -> None:
    """Test 12: Pagination using skip and limit parameters."""
    seed_problems(db_session)

    # Page 1: skip 0, limit 2
    res_p1 = client.get("/problems?skip=0&limit=2")
    assert res_p1.status_code == 200
    p1_items = res_p1.json()
    assert len(p1_items) == 2
    assert p1_items[0]["id"] == 1
    assert p1_items[1]["id"] == 2

    # Page 2: skip 2, limit 2
    res_p2 = client.get("/problems?skip=2&limit=2")
    assert res_p2.status_code == 200
    p2_items = res_p2.json()
    assert len(p2_items) == 1
    assert p2_items[0]["id"] == 3

    # Page 3: skip 10, limit 2 (out of bounds)
    res_p3 = client.get("/problems?skip=10&limit=2")
    assert res_p3.status_code == 200
    assert len(res_p3.json()) == 0

    # Negative skip rejected by validation
    res_inv_skip = client.get("/problems?skip=-1&limit=10")
    assert res_inv_skip.status_code == 422

    # Limit <= 0 rejected by validation
    res_inv_limit = client.get("/problems?skip=0&limit=0")
    assert res_inv_limit.status_code == 422


# ==============================================================================
# Seeding Tests
# ==============================================================================

def test_seed_process_idempotent(db_session: Session) -> None:
    """Test 13: Seed process is idempotent and creates exactly 3 records on repeated runs."""
    # First seeding pass
    first_run = seed_problems(db_session)
    assert len(first_run) == 3

    initial_count = db_session.query(Problem).count()
    assert initial_count == 3

    # Second seeding pass on same database session
    second_run = seed_problems(db_session)
    assert len(second_run) == 3

    final_count = db_session.query(Problem).count()
    assert final_count == 3  # Count remains strictly 3

    # Verify problem slugs and example counts
    p_map = {p.slug: p for p in final_count_problems(db_session)}
    assert "two-sum" in p_map
    assert "reverse-string" in p_map
    assert "valid-parentheses" in p_map
    assert len(p_map["two-sum"].examples) == 3
    assert len(p_map["reverse-string"].examples) == 2
    assert len(p_map["valid-parentheses"].examples) == 3


def final_count_problems(session: Session) -> list[Problem]:
    """Helper to query all problems."""
    return session.query(Problem).all()

