"""
Farm API Documentation
Separate file for Swagger documentation definitions
"""

from fastapi import Body
from ..modules.farm.schemas import CreateFarm

# Farm Creation Documentation
CREATE_FARM_DOCS = {
    "summary": "Create Farm",
    "description": """
    Create a new farm for a farmer.
    
    **Process:**
    1. Validate farm data
    2. Create farm record in database
    3. Update farmer with farm_id reference
    4. Return farm information
    
    **Requirements:**
    - farmer_id must exist in database
    - farm_name must be provided
    - farm_measurement must be positive
    - farm_location is optional
    """,
    "responses": {
        200: {
            "description": "Farm created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Farm created successfully",
                        "data": {
                            "farm_id": "123e4567-e89b-12d3-a456-426614174000",
                            "farm_name": "Green Valley Farm",
                            "farm_measurement": 150,
                            "farm_location": {
                                "latitude": 40.7128,
                                "longitude": -74.0060,
                                "address": "123 Farm Road, Countryside, ST 12345"
                            },
                            "created_at": "2024-01-25T10:24:00.000000"
                        }
                    }
                }
            }
        },
        401: {
            "description": "Farm creation failed",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Farm creation failed"
                    }
                }
            }
        }
    }
}

create_farm_example = Body(
    ..., 
    description="Farm creation data",
    example={
        "farmer_id": "550e8400-e29b-41d4-a716-446655440000",
        "farm_name": "Green Valley Farm",
        "farm_measurement": 150,
        "farm_location": {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "address": "123 Farm Road, Countryside, ST 12345"
        }
    }
)

# Get All Farms Documentation
GET_ALL_FARMS_DOCS = {
    "summary": "Get All Farms",
    "description": """
    Retrieve all farms in the system.
    
    **Process:**
    1. Query all farm records from database
    2. Return list of farm objects
    
    **Returns:**
    - List of all farms with their details
    - Empty list if no farms exist
    """,
    "responses": {
        200: {
            "description": "Farms retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Farm retrieval successful",
                        "data": [
                            {
                                "farm_id": "123e4567-e89b-12d3-a456-426614174000",
                                "farmer_id": "550e8400-e29b-41d4-a716-446655440000",
                                "farm_name": "Green Valley Farm",
                                "farm_measurement": 150,
                                "farm_location": {
                                    "latitude": 40.7128,
                                    "longitude": -74.0060,
                                    "address": "123 Farm Road, Countryside, ST 12345"
                                },
                                "created_at": "2024-01-25T10:24:00.000000"
                            },
                            {
                                "farm_id": "456e7890-e89b-12d3-a456-426614174111",
                                "farmer_id": "660f9511-f29c-52e5-b827-557766551111",
                                "farm_name": "Sunshine Acres",
                                "farm_measurement": 75,
                                "farm_location": None,
                                "created_at": "2024-01-25T11:30:00.000000"
                            }
                        ]
                    }
                }
            }
        },
        401: {
            "description": "Farm retrieval failed",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Farm retrieval failed"
                    }
                }
            }
        }
    }
}
