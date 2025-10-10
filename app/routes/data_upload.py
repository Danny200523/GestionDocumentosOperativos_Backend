from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import json
from ..auth.dependencias import get_current_user
from ..utils.pdf_table_extractor import extract_tables_from_pdf
from ..models.extrated_data import ExtratedData
from ..models.key_data import KeyData
from sqlmodel import Session
from ..core.database import get_session

upload_router = APIRouter()


@upload_router.post("/upload/")
async def upload_file(file: UploadFile = File(...), user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    if not file:
        raise HTTPException(status_code=400, detail="No se ha proporcionado ningún archivo")
    
    # Validar que el archivo tenga nombre
    if not file.filename:
        raise HTTPException(status_code=400, detail="El archivo debe tener un nombre válido")
    
    # Validar tipo de archivo (solo PDFs por defecto)
    allowed_extensions = ['.pdf']
    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    try:
        # Extraer tablas del PDF directamente desde el archivo subido
        tables_data = extract_tables_from_pdf(file.file)

        if not tables_data:
            raise HTTPException(status_code=400, detail="El PDF no contiene tablas para procesar.")

        department_id = user["department_id"]

        saved_tables = []
        for table in tables_data:
            # Guardar estructura de tabla en ExtratedData
            table_json = json.dumps(table)
            extrated_data = ExtratedData(department_id=department_id, table_data=table_json)
            session.add(extrated_data)
            session.commit()
            session.refresh(extrated_data)

            table_id = extrated_data.id_table
            assert table_id is not None

            # Extraer datos clave: primera fila como headers, luego guardar cada celda como key-value con header como key
            data_rows = table["data"]
            if data_rows and len(data_rows) > 0:
                headers = data_rows[0]
                for i in range(1, len(data_rows)):
                    row = data_rows[i]
                    for j, cell in enumerate(row):
                        if j < len(headers):
                            key = str(headers[j]).strip() if headers[j] else f"col_{j}"
                            value = str(cell).strip() if cell else ""
                            key_data = KeyData(department_id=department_id, table_id=table_id, key=key, value=value)
                            session.add(key_data)

            session.commit()
            saved_tables.append({"id_table": table_id, "page": table["page"], "table_index": table["table_index"]})

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar el PDF: {str(e)}")
    
    return JSONResponse(content={
        "message": "Archivo procesado exitosamente",
        "filename": file.filename,
        "saved_tables": saved_tables
    })
