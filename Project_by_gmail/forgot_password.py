from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

import main
from service_mail import send_email
from schemas import PasswordReset

forgot_router = APIRouter()

subject = "Password Reset E-mail"
URL = "http://127.0.0.1:8000/reset_password"

body = f"""You're receiving this email because you or someone else has requested a password reset for your user account at.
          Click the link below to reset your password:
          {URL}

          If you did not request a password reset you can safely ignore this emai
          """

sender = "harut.karapetyan.2022@gmail.com"

recipients = ["rehoyig740@fincainc.com"]

password = "dzok bydv rbqw lsab"


@forgot_router.get("/forgot_password")
def forgot_password(email):
    main.cursor.execute("""SELECT * FROM users WHERE user_email=%s""",
                        (email,))

    target_user = main.cursor.fetchone()

    if target_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email '{email}' was not found!")

    else:
        send_email(subject, body, sender, recipients, password)


@forgot_router.post('/reset_password')
def reset_password(reset_data: PasswordReset):
    if reset_data.new_password != reset_data.confirm_password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="You have entered incorrect information")

    email = reset_data.mail
    main.cursor.execute("""SELECT * FROM users WHERE user_email =%s""",
                        (email,))

    user_data = main.cursor.fetchone()

    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User by {email} was nut found")

    main.cursor.execute("""Update users set user_password=%s where user_email=%s""",
                        (reset_data.new_password, email))

    main.conn.commit()

    return "OK"





