from fastapi import FastAPI, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes.data_upload import upload_router
from app.routes.sesion import sesion
from app.routes.user.users import router as user_router
from app.routes.department.departments import router as department_router
from app.routes.forgot_password import router as forgot_router
from app.auth.dependencias import get_current_user

app = FastAPI(
    title="API Proyecto",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",  # si usas Vite
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, DELETE...
    allow_headers=["*"],     # Authorization, Content-Type...
)

# Routers
app.include_router(upload_router)
app.include_router(sesion.router, prefix="/auth"    )
app.include_router(forgot_router)
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(department_router, prefix="/departments", tags=["Departments"])

# Health check
@app.get("/", dependencies=[Depends(get_current_user)])
def health_check():
    return {"status": "ok"}
