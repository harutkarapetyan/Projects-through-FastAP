# FastAPI
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

# Own
from schemas import UserSignupSchema, UserLoginSchema

# main
import main

# Security
import security

auth_router = APIRouter()


@auth_router.post('/sign_up', response_model=UserSignupSchema)
def sign_up(user_data: UserSignupSchema):
    main.cursor.execute("""INSERT INTO users (user_name, user_email, user_password) 
                        VALUES (%s, %s, %s)""",
                        (user_data.user_name,
                         user_data.user_email,
                         security.hash_password(user_data.user_password)))
    main.conn.commit()

    return JSONResponse(content={"Message": "You have successfully registered"},
                        status_code=status.HTTP_201_CREATED)


@auth_router.post('/login', response_model=UserLoginSchema)
def log_in(login_data: UserLoginSchema):
    user_email = login_data.user_email
    main.cursor.execute("""SELECT * FROM users WHERE user_email=%s""",
                        (user_email,))

    user = main.cursor.fetchone()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email '{user_email}' was not found!")
    user = dict(user)
    user_hashed_password = user.get("user_password")

    if not security.verify_password(login_data.user_password, user_hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Wrong password!")

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"Access_token": security.create_token({"user_id": user.get("user_i")})})


