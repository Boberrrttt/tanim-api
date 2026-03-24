"""
Farmer API Documentation
"""

# Get All Farmers Documentation
GET_ALL_FARMERS_DOCS = {
    "summary": "Get All Farmers",
    "description": """
    Retrieve all farmers in the system.

    **Process:**
    1. Query all farmer records from database
    2. Return list of farmer objects (passwords excluded)

    **Returns:**
    - List of all farmers with farmer_id, username, farm_id, created_at
    - Empty list if no farmers exist
    """,
    "responses": {
        200: {
            "description": "Farmers retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Farmers retrieved successfully",
                        "data": [
                            {
                                "farmer_id": "550e8400-e29b-41d4-a716-446655440000",
                                "username": "farmer1",
                                "farm_id": "123e4567-e89b-12d3-a456-426614174000",
                                "created_at": "2024-01-25T10:24:00.000000"
                            },
                            {
                                "farmer_id": "660f9511-f29c-52e5-b827-557766551111",
                                "username": "farmer2",
                                "farm_id": None,
                                "created_at": "2024-01-25T11:30:00.000000"
                            }
                        ],
                        "total": 2
                    }
                }
            }
        },
        401: {
            "description": "Farmer retrieval failed",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Failed to retrieve farmers"
                    }
                }
            }
        }
    }
}
