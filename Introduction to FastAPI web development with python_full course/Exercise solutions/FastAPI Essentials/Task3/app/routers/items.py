from fastapi import APIRouter

# Create a router for item-related routes
router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def get_items():
    """Get all items"""
    return {
        "message": "List of all items",
        "items": [
            {"id": 1, "name": "Laptop", "price": 999.99},
            {"id": 2, "name": "Mouse", "price": 25.50},
            {"id": 3, "name": "Keyboard", "price": 79.99}
        ]
    }


@router.get("/{item_id}")
async def get_item(item_id: int):
    """Get a specific item by ID"""
    return {
        "message": f"Item with ID {item_id}",
        "id": item_id,
        "name": "Sample Item",
        "price": 49.99,
        "description": "A great product"
    }


@router.post("/")
async def create_item(name: str, price: float):
    """Create a new item"""
    return {
        "message": "Item created successfully",
        "id": 4,
        "name": name,
        "price": price
    }


@router.put("/{item_id}")
async def update_item(item_id: int, name: str, price: float):
    """Update an existing item"""
    return {
        "message": f"Item {item_id} updated",
        "id": item_id,
        "name": name,
        "price": price
    }


@router.delete("/{item_id}")
async def delete_item(item_id: int):
    """Delete an item"""
    return {
        "message": f"Item {item_id} deleted successfully"
    }
