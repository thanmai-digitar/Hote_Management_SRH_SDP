# Assuming you have these imports
from fastapi import APIRouter, HTTPException
from typing import List
from ..crud.crud import MySQLCRUD
from ..schemas.schemas import TransactionCreate, TransactionUpdate, Transaction

router = APIRouter()
db = MySQLCRUD('host', 'user', 'password', 'database')

@router.post("/", response_model=Transaction)
async def create_transaction(transaction: TransactionCreate):
    transaction_id = db.create('Transactions', list(transaction.dict().keys()), list(transaction.dict().values()))
    created_transaction = db.read('Transactions', conditions=f"WHERE transactionid = {transaction_id}")[0]
    return {
        "transactionid": created_transaction[0],
        "bookingid": created_transaction[1],
        "customerid": created_transaction[2],
        "total_amount": created_transaction[3],
        "payment_type": created_transaction[4]
    }

@router.get("/", response_model=List[Transaction])
async def read_transactions():
    transactions_data = db.read('Transactions')
    return [{"transactionid": trans[0], "bookingid": trans[1], "customerid": trans[2], "total_amount": trans[3], "payment_type": trans[4]} for trans in transactions_data]

@router.get("/{transaction_id}", response_model=Transaction)
async def read_transaction(transaction_id: int):
    transaction = db.read('Transactions', conditions=f"WHERE transactionid = {transaction_id}")
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {
        "transactionid": transaction[0][0],
        "bookingid": transaction[0][1],
        "customerid": transaction[0][2],
        "total_amount": transaction[0][3],
        "payment_type": transaction[0][4]
    }

@router.put("/{transaction_id}", response_model=Transaction)
async def update_transaction(transaction_id: int, transaction: TransactionUpdate):
    db.update('Transactions', transaction.dict(), f"transactionid = {transaction_id}")
    updated_transaction = db.read('Transactions', conditions=f"WHERE transactionid = {transaction_id}")[0]
    return {
        "transactionid": updated_transaction[0],
        "bookingid": updated_transaction[1],
        "customerid": updated_transaction[2],
        "total_amount": updated_transaction[3],
        "payment_type": updated_transaction[4]
    }

@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: int):
    db.delete('Transactions', f"transactionid = {transaction_id}")
    return {"message": "Transaction deleted successfully."}
