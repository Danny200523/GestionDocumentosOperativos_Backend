# Simulación de datos (esto luego lo traes de MySQL con SQLAlchemy)
from typing import List
from app.models.departments import Department
from fastapi import APIRouter

router = APIRouter(tags=["Departments"])

departments_data = [
    {"id_department": 1, "name_department": "Finanzas"},
    {"id_department": 2, "name_department": "Compras"},
    {"id_department": 3, "name_department": "Talento Humano"},
    {"id_department": 4, "name_department": "Producción"},
    {"id_department": 5, "name_department": "Ventas"},
    {"id_department": 6, "name_department": "Logística"},
    {"id_department": 7, "name_department": "Tecnología"},
    {"id_department": 8, "name_department": "Marketing"},
    {"id_department": 9, "name_department": "Administración"},
]

@router.get("/departments", response_model=List[Department])
def get_departments():
    return departments_data