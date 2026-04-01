from fastapi import APIRouter

# Create a router for user-related routes
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def get_users():
    """Get all users"""
    return {
        "message": "List of all users",
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
        ]
    }


@router.get("/{user_id}")
async def get_user(user_id: int):
    """Get a specific user by ID"""
    return {
        "message": f"User with ID {user_id}",
        "id": user_id,
        "name": "John Doe",
        "email": "john@example.com"
    }


@router.post("/")
async def create_user(name: str, email: str):
    """Create a new user"""
    return {
        "message": "User created successfully",
        "id": 4,
        "name": name,
        "email": email
    }


@router.put("/{user_id}")
async def update_user(user_id: int, name: str, email: str):
    """Update an existing user"""
    return {
        "message": f"User {user_id} updated",
        "id": user_id,
        "name": name,
        "email": email
    }


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """Delete a user"""
    return {
        "message": f"User {user_id} deleted successfully"
    }
