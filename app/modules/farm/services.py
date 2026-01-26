from sqlalchemy.orm import Session
from sqlalchemy import text
from app.modules.farm.schemas import CreateFarm
from app.modules.farm.models import Farm
import json


async def create(db: Session, payload: CreateFarm) -> dict:
    farm = Farm(
        farm_name=payload.farm_name,
        farm_measurement=payload.farm_measurement,
        farm_location=payload.farm_location
    )
    
    query = text("""
        INSERT INTO farm (farm_id, farm_name, farmer_id, farm_measurement, farm_location, created_at)
        VALUES (:farm_id, :farm_name, :farmer_id, :farm_measurement, :farm_location, :created_at)
    """)
    
    db.execute(query, {
        'farm_id': farm.farm_id,
        'farm_name': farm.farm_name,
        'farmer_id': payload.farmer_id,
        'farm_measurement': farm.farm_measurement,
        'farm_location': json.dumps(farm.farm_location) if farm.farm_location else None,
        'created_at': farm.created_at.isoformat()
    })
    
    db.commit()
    
    return {
        "status": "success",
        "data": farm.to_dict()
    }

async def get_all(db: Session) -> dict:
    query = text("""
        SELECT * FROM farm
    """)
    
    result = db.execute(query)

    if result.rowcount == 0:
        return {
            "status": "success",
            "data": {
                "farms": [],
                "total": 0
            }
        }
    
    farms = []
    for row in result:
        farm_location = None
        if row.farm_location:
            try:
                farm_location = json.loads(row.farm_location)
            except:
                farm_location = row.farm_location
        
        farm = Farm(
            farm_id=row.farm_id,
            farm_name=row.farm_name,
            farm_measurement=row.farm_measurement,
            farm_location=farm_location,
            created_at=row.created_at
        )
        farms.append(farm.to_dict())
    
    return {
        "status": "success",
        "data": {
            "farms": farms,
            "total": len(farms)
        }
    }