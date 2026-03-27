from ...helpers.responses import success_response
from .timeline_data import CROP_TIMELINES


async def get_crop_timelines_controller():
    return success_response(
        message="Crop cycle timelines retrieved",
        data={"crops": CROP_TIMELINES},
    )
