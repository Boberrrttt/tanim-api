"""
System API Documentation
Separate file for Swagger documentation definitions
"""

from fastapi import Body
from ..modules.system.schemas import CreateSystem, UpdateBatteryStatus

# Create System Documentation
CREATE_SYSTEM_DOCS = {
    "summary": "Create System",
    "description": """
    Create a new system in the database.
    
    **Process:**
    1. Validate system data
    2. Create system record in database
    3. Return system information
    
    **Requirements:**
    - system_id must be unique
    - battery_status must be a valid float value (0.0 to 100.0)
    """,
    "responses": {
        200: {
            "description": "System created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "System created successfully",
                        "data": {
                            "system_id": "sys_12345",
                            "battery_status": 85.5
                        }
                    }
                }
            }
        },
        500: {
            "description": "Failed to create system",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Failed to create system"
                    }
                }
            }
        }
    }
}

create_system_example = Body(
    ..., 
    description="System creation data",
    example={
        "system_id": "sys_12345",
        "battery_status": 85.5
    }
)

# Update Battery Status Documentation
UPDATE_BATTERY_STATUS_DOCS = {
    "summary": "Update Battery Status",
    "description": """
    Update the battery status of a system.
    
    **Process:**
    1. Validate system data
    2. Update battery status in database
    3. Return updated system information
    
    **Requirements:**
    - system_id must exist in database
    - battery_status must be a valid float value (0.0 to 100.0)
    """,
    "responses": {
        200: {
            "description": "Battery status updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Battery status updated successfully",
                        "data": {
                            "system_id": "sys_12345",
                            "battery_status": 85.5
                        }
                    }
                }
            }
        },
        404: {
            "description": "System not found",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "System not found"
                    }
                }
            }
        },
        500: {
            "description": "Failed to update battery status",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Failed to update battery status"
                    }
                }
            }
        }
    }
}

update_battery_status_example = Body(
    ..., 
    description="Battery status update data",
    example={
        "system_id": "sys_12345",
        "battery_status": 85.5
    }
)
