from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(prefix="/users", tags=["Users"])

# POST /users
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# GET /users/{id}
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user_search = db.query(models.User).filter(models.User.id == id)
    user_result = user_search.first()
    if user_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
    return user_result