from sqlalchemy.orm import Session
from sqlalchemy import text
from app.modules.soil_health_test.models import SoilHealthTest
from app.modules.soil_health_test.schemas import CreateSoilHealthTest
from ...helpers.responses import success_response, error_response
import uuid

async def create(db: Session, soil_health_test: CreateSoilHealthTest):
    try:
        test = SoilHealthTest(
            nitrogen=soil_health_test.nitrogen,
            phosphorus=soil_health_test.phosphorus,
            potassium=soil_health_test.potassium,
            ph=soil_health_test.ph,
            salinity=soil_health_test.salinity,
            temperature=soil_health_test.temperature,
            moisture=soil_health_test.moisture,
            farm_id=soil_health_test.farm_id,
            classification=soil_health_test.classification
        )
        
        test_id = str(uuid.uuid4())
        
        query = text("""
            INSERT INTO soil_health_test (test_id, farm_id, nitrogen, phosphorus, potassium, ph, salinity, temperature, moisture, classification, created_at)
            VALUES (:test_id, :farm_id, :nitrogen, :phosphorus, :potassium, :ph, :salinity, :temperature, :moisture, :classification, :created_at)
        """)

        result = db.execute(query, {
            'test_id': test_id,
            'farm_id': soil_health_test.farm_id,
            'nitrogen': soil_health_test.nitrogen,
            'phosphorus': soil_health_test.phosphorus,
            'potassium': soil_health_test.potassium,
            'ph': soil_health_test.ph,
            'salinity': soil_health_test.salinity,
            'temperature': soil_health_test.temperature,
            'moisture': soil_health_test.moisture,
            'classification': soil_health_test.classification,
            'created_at': test.created_at.isoformat()
        })
        
        if result.rowcount == 0:
            db.rollback()
            return error_response(
                message="Failed to create soil health test - no rows affected"
            )
        
        db.commit()

        test_data = test.to_dict()
        test_data['test_id'] = test_id
        
        return success_response(
            message="Soil health test created successfully",
            data=test_data
        )
    
    except Exception as e:
        db.rollback()
        print(f"Error creating soil health test: {str(e)}") 
        return error_response(
            message=f"Failed to create soil health test: {str(e)}"
        )


async def get_by_farm_id(db: Session, farm_id: str):
    try:
        query = text("""
            SELECT * FROM soil_health_test 
            WHERE farm_id = :farm_id 
            ORDER BY created_at DESC
        """)
        
        result = db.execute(query, {'farm_id': farm_id})
        
        if result.rowcount == 0:
            return success_response(
                message="No soil health tests found for this farm",
                data=[],
            )
        
        tests = []
        for row in result:
            test = SoilHealthTest(
                nitrogen=row.nitrogen,
                phosphorus=row.phosphorus,
                potassium=row.potassium,
                ph=row.ph,
                salinity=row.salinity,
                temperature=row.temperature,
                moisture=row.moisture,
                farm_id=row.farm_id,
                classification=row.classification,
                created_at=row.created_at
            )
            test_data = test.to_dict()
            test_data['test_id'] = row.test_id
            tests.append(test_data)
        
        return success_response(
            message="Soil health tests retrieved successfully",
            data=tests,
        )
    
    except Exception as e:
        print(f"Error retrieving soil health tests: {str(e)}")
        return error_response(
            message=f"Failed to retrieve soil health tests: {str(e)}"
        )