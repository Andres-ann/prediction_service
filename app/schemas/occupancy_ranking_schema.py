from pydantic import BaseModel, Field
from typing import List, Dict


class OccupancyRankingResponse(BaseModel):
    ranking: Dict[str, List[dict]] = Field(
        ...,
        example={
            "monday": [
                {"room": "Sala A1", "expected_occupancy": 0.85},
                {"room": "Sala B2", "expected_occupancy": 0.73}
            ],
            "tuesday": [
                {"room": "Sala A1", "expected_occupancy": 0.81},
                {"room": "Sala B2", "expected_occupancy": 0.66}
            ]
        },
        description="Predicted ranking of room occupancy by weekday."
    )