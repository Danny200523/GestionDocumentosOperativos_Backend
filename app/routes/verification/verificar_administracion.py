from fastapi import HTTPException, Depends
from ...auth.dependencias import get_current_user

def admin_required(user = Depends(get_current_user)):
    if user["role"].lower() != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    return user
