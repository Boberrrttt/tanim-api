# Create Soil Health Test Documentation
CREATE_SOIL_HEALTH_TEST_DOCS = {
    "summary": "Create Soil Health Test",
    "description": """
    Create a new soil health test record for a specific farm.
    
    **Process:**
    1. Validate the soil health test data
    2. Create a new soil health test record in the database
    3. Link the test to the specified farm
    4. Return the created test details
    
    **Required Fields:**
    - All soil health metrics (nitrogen, phosphorus, potassium, pH, etc.)
    - Farm ID to link the test to a specific farm
    - Classification of the soil health test
    
    **Returns:**
    - Created soil health test data with unique ID
    - Timestamp of creation
    """,
    "responses": {
        200: {
            "description": "Soil health test created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Soil health test created successfully",
                        "data": {
                            "soil_health_test_id": "550e8400-e29b-41d4-a716-446655440000",
                            "nitrogen": 45.5,
                            "phosphorus": 28.3,
                            "potassium": 120.7,
                            "ph": 6.8,
                            "salinity": 0.5,
                            "temperature": 22.5,
                            "moisture": 65.2,
                            "farm_id": "123e4567-e89b-12d3-a456-426614174000",
                            "classification": "Good",
                            "created_at": "2024-01-25T14:30:00.000000"
                        }
                    }
                }
            }
        },
        400: {
            "description": "Bad request - Invalid data",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Failed to create soil health test"
                    }
                }
            }
        }
    }
}

# Get Soil Health Tests by Farm ID Documentation
GET_SOIL_HEALTH_TESTS_BY_FARM_ID_DOCS = {
    "summary": "Get Soil Health Tests by Farm ID",
    "description": """
    Retrieve all soil health tests for a specific farm.
    
    **Process:**
    1. Query soil health tests by farm ID
    2. Return tests ordered by creation date (newest first)
    3. Include total count of tests
    
    **Parameters:**
    - farm_id: UUID of the farm to retrieve tests for
    
    **Returns:**
    - List of soil health tests for the specified farm
    - Total count of tests
    - Empty list if no tests found
    """,
    "responses": {
        200: {
            "description": "Soil health tests retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Soil health tests retrieved successfully",
                        "data": [
                            {
                                "test_id": "550e8400-e29b-41d4-a716-446655440000",
                                "nitrogen": 45.5,
                                "phosphorus": 28.3,
                                "potassium": 120.7,
                                "ph": 6.8,
                                "salinity": 0.5,
                                "temperature": 22.5,
                                "moisture": 65.2,
                                "farm_id": "123e4567-e89b-12d3-a456-426614174000",
                                "classification": "Good",
                                "created_at": "2024-01-25T14:30:00.000000"
                            },
                            {
                                "test_id": "661f9511-f29c-52e5-b827-557766551111",
                                "nitrogen": 42.1,
                                "phosphorus": 25.7,
                                "potassium": 115.3,
                                "ph": 6.5,
                                "salinity": 0.4,
                                "temperature": 21.8,
                                "moisture": 63.1,
                                "farm_id": "123e4567-e89b-12d3-a456-426614174000",
                                "classification": "Fair",
                                "created_at": "2024-01-24T10:15:00.000000"
                            }
                        ],
                        "total": 2
                    }
                }
            }
        },
        404: {
            "description": "No soil health tests found",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "No soil health tests found for this farm",
                        "data": [],
                        "total": 0
                    }
                }
            }
        }
    }
}
