CREATE_CROP_RECOMMENDATION_DOCS = {
    "summary": "Create crop recommendation",
    "description": """
    Create a new crop recommendation row for a farm with model `probabilities` (JSONB).

    If `created_at` is omitted, the current UTC time is used. For the **same UTC calendar day**
    as today, only one row per `farm_id` is allowed; if one already exists, use PUT instead.
    """,
    "responses": {
        200: {
            "description": "Created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Crop recommendation created successfully",
                        "data": {
                            "recommendation_id": "550e8400-e29b-41d4-a716-446655440000",
                            "farm_id": "123e4567-e89b-12d3-a456-426614174000",
                            "probabilities": [
                                {
                                    "crop_class": "Corn",
                                    "probability": 0.2279,
                                }
                            ],
                            "created_at": "2024-01-25T14:30:00.000000+00:00",
                            "updated_at": "2024-01-25T14:30:00.000000+00:00",
                        },
                    }
                }
            },
        },
        409: {
            "description": "A recommendation for this farm already exists for today (UTC)",
        },
    },
}

UPDATE_CROP_RECOMMENDATION_DOCS = {
    "summary": "Update today's crop recommendation",
    "description": """
    Updates `probabilities` for the most recent row for this `farm_id` whose `created_at`
    falls on the current UTC date. Optional `created_at`, if sent, must be today (UTC).
    `updated_at` is set to the current UTC time.

    Returns **404** if there is no row for today — use POST to create one.
    """,
    "responses": {
        200: {"description": "Updated successfully"},
        400: {"description": "created_at is not today"},
        404: {"description": "No row for today for this farm"},
    },
}

GET_CROP_RECOMMENDATIONS_BY_FARM_ID_DOCS = {
    "summary": "List crop recommendations by farm",
    "description": "Returns all recommendations for the farm, newest first.",
    "responses": {
        200: {
            "description": "List (may be empty)",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Crop recommendations retrieved successfully",
                        "data": [],
                    }
                }
            },
        },
    },
}
