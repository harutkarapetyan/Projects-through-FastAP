import time

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

import psycopg2
from psycopg2.extras import RealDictCursor

from database import engine
from models import Base


from auth import auth_router
from operations import operations_router
from forgot_password import forgot_router

Base.metadata.create_all(bind=engine)

while True:
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",
            port=5432,
            database="forgot",
            user="postgres",
            password="password",
            cursor_factory=RealDictCursor
            )
        print("Connection successfully")

        cursor = conn.cursor()
        break
    except Exception as error:
        print(error)
        time.sleep(3)

app = FastAPI(
    title='Financial Tracker'
)


@app.get("/")
def main():
    return JSONResponse(content={"Message": "Ok"}, status_code=status.HTTP_200_OK)


app.include_router(auth_router)
app.include_router(operations_router)
app.include_router(forgot_router)
