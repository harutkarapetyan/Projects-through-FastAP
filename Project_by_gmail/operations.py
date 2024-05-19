from fastapi import APIRouter, Depends, HTTPException, status

import main

from schemas import OperationSchema

import security

operations_router = APIRouter()


@operations_router.post("/add-operation")
def add_operation(operation_data: OperationSchema, current_user=Depends(security.get_current_user)):
    current_user = dict(current_user)
    user_id = current_user.get("user_id")
    main.cursor.execute("""INSERT INTO operations 
                        (operation_kind, operation_amount, operation_description, user_id)
                        VALUES (%s, %s, %s, %s)""",
                        (operation_data.operation_kind,
                         operation_data.operation_amount,
                         operation_data.operation_description,
                         user_id))
    main.conn.commit()

    return "Operation has been added"


@operations_router.get("/get-all-operations")
def get_all_operations(current_user=Depends(security.get_current_user)):
    current_user = dict(current_user)
    user_id = current_user.get("user_id")

    main.cursor.execute("""SELECT * FROM operations WHERE user_id=%s""",
                        (user_id,))
    operations = main.cursor.fetchall()

    return operations


@operations_router.get("/get-operation-by-id/{operation_id}")
def get_operation_by_id(operation_id: int, current_user=Depends(security.get_current_user)):
    current_user = dict(current_user)
    user_id = current_user.get("user_id")
    main.cursor.execute("""SELECT * FROM operations WHERE operation_id=%s AND user_id=%s""",
                        (operation_id,
                         user_id))
    operation = main.cursor.fetchone()

    if operation is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Operation not found,!!!!")

    return operation


@operations_router.get("/get-operation-by-kind/{operation_kind}")
def get_operation_by_kind(operation_kind: str, current_user=Depends(security.get_current_user)):
    current_user = dict(current_user)
    user_id = current_user.get("user_id")
    main.cursor.execute("""SELECT * FROM operations WHERE operation_kind=%s AND user_id=%s""",
                        (operation_kind,
                         user_id))
    operations = main.cursor.fetchall()

    return operations


@operations_router.delete("/delete-operation-by-id/{operation_id}")
def delete_operation_by_id(operation_id: int, current_user=Depends(security.get_current_user)):
    current_user = dict(current_user)
    user_id = current_user.get("user_id")
    main.cursor.execute("""DELETE FROM operations WHERE operation_id=%s AND user_id=%s""",
                        (operation_id,
                         user_id))
    main.conn.commit()
