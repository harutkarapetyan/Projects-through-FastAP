from pydantic import BaseModel, EmailStr


class UserSignupSchema(BaseModel):
    user_name: str
    user_email: EmailStr
    user_password: str


class UserLoginSchema(BaseModel):
    user_email: EmailStr
    user_password: str


class User(BaseModel):
    user_id: int


class OperationSchema(BaseModel):
    operation_kind: str
    operation_amount: float
    operation_description: str


class PasswordReset(BaseModel):
    new_password: str
    mail: str
    confirm_password: str
