"""Crops / planting timeline API documentation."""

GET_CROP_TIMELINES_DOCS = {
    "summary": "Get crop growth cycle timelines",
    "description": """
    Returns approximate phase timelines (`total_days`, `phases`, optional `planting_window_note`)
    keyed by crop id. Matches client constants in `tanim-app/constants/crop-cycle.ts`.
    Day 1 = planting or transplant; dates are computed client-side from a chosen start date.
    """,
    "responses": {
        200: {
            "description": "Timelines retrieved",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Crop cycle timelines retrieved",
                        "data": {
                            "crops": {
                                "tomato": {
                                    "total_days": 85,
                                    "planting_window_note": "Warm-season…",
                                    "phases": [],
                                }
                            }
                        },
                    }
                }
            },
        }
    },
}
