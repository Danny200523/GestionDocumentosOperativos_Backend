from fastapi import APIRouter, Depends
from ..verification.verificar_administracion import admin_required
from sqlmodel  import Session
from ...core.database import get_session
from ...controllers.user.users_controllers import get_user, delete_user_by_id
from ...auth.dependencias import get_current_user

router = APIRouter(tags=["Users"])

@router.get("/me")
def get_my_users(user: dict = Depends(get_current_user)):
    return user

@router.get("/all", dependencies=[Depends(admin_required)])
def read_users(db: Session = Depends(get_session)):
    return get_user(db)

@router.delete("/{user_id}", dependencies=[Depends(admin_required)])
def remove_user(user_id: int, db: Session = Depends(get_session)):
    return delete_user_by_id(db, user_id)
