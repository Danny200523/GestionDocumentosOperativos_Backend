from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import json
import logging
from ..auth.dependencias import get_current_user
from ..utils.pdf_table_extractor import extract_tables_from_pdf
from ..models.extrated_data import ExtractedData
from ..models.key_data import KeyData
from sqlmodel import Session
from ..core.database import get_session
from sqlalchemy.exc import IntegrityError, DataError, OperationalError

logger = logging.getLogger(__name__)
upload_router = APIRouter()


@upload_router.post("/upload/")
def upload_file(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="Archivo inválido")
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    try:
        tables_data = extract_tables_from_pdf(file.file)
        if not tables_data:
            raise HTTPException(400, "El PDF no contiene tablas para procesar.")
        department_id = int(user["department_id"])
        saved_tables = []
        # start txn
        for table in tables_data:
            # pass dict to JSON column
            table_json = table
            extrated_data = ExtractedData(
                department_id=department_id,
                table_data=table_json,
                file_name=(file.filename or "Sin nombre"),
                status="Aprobado",
            )
            session.add(extrated_data)
            session.flush()  # gets id without committing
            table_id = extrated_data.id_table
            data_rows = table.get("data") or []
            if data_rows:
                headers = data_rows[0]
                for row in data_rows[1:]:
                    for j, cell in enumerate(row):
                        key = str(headers[j]).strip() if j < len(headers) and headers[j] else f"col_{j}"
                        value = "" if cell is None else str(cell).strip()
                        session.add(KeyData(department_id=department_id, table_id=table_id, key=key, value=value))
            saved_tables.append({"id_table": table_id, "page": table.get("page"), "table_index": table.get("table_index")})
        session.commit()
    except (IntegrityError, DataError, OperationalError) as e:
        session.rollback()
        logger.exception("DB error en /upload: %s", getattr(e, "orig", e))
        raise HTTPException(400, detail=str(getattr(e, "orig", e)))
    except Exception as e:
        session.rollback()
        logger.exception("Error inesperado en /upload")
        raise HTTPException(500, detail=f"Error al procesar el PDF: {e}")
    return {"message": "Archivo procesado exitosamente", "filename": file.filename, "saved_tables": saved_tables}

@upload_router.get("/documents/")
def get_uploaded_documents(
    user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    department_id = user["department_id"]
    documents = (
        session.query(ExtractedData)
        .filter_by(department_id=department_id)
        .order_by(ExtractedData.created_at.desc())
        .all()
    )

    seen = set()
    unique_docs = []
    for doc in documents:
        fname = (doc.file_name or "Sin nombre").strip()
        if fname in seen:
            continue
        seen.add(fname)
        unique_docs.append({
            "id": doc.id_table,
            "filename": fname,
            "date": doc.created_at.strftime("%Y-%m-%d %H:%M:%S") if doc.created_at else "Desconocida",
            "status": doc.status or "Pendiente"
        })

    return unique_docs


@upload_router.get("/documents/all")
def get_all_uploaded_documents(session: Session = Depends(get_session)):
    documents = session.query(ExtractedData).order_by(ExtractedData.created_at.desc()).all()

    result = [
        {
            "id": doc.id_table,
            "filename": doc.file_name or "Sin nombre",
            "date": doc.created_at.strftime("%Y-%m-%d %H:%M:%S") if doc.created_at else "Desconocida",
            "status": doc.status or "Pendiente"
        }
        for doc in documents
    ]

    return result

@upload_router.get("/documents/{document_id}")
def get_document_by_id(document_id: int, session: Session = Depends(get_session)):
    document = session.get(ExtractedData, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    return {
        "id": document.id_table,
        "file_name": document.file_name,
        "status": document.status,
        "created_at": document.created_at,
        "department_id": document.department_id,
        "user_id": document.user_id,
        "data": document.table_data  
    }
