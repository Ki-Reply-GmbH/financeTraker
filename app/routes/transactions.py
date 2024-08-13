from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from services.transaction_services import get_all_transactions_by_user, create_new_transaction, get_catagory_by_id, create_catagory, get_all_catagories
from fastapi import Depends, HTTPException
from logger import get_logger
from services.auth import get_current_user

logger = get_logger(__name__)

router = APIRouter()

@router.get("/transactions")
def get_transactions(current_user: str = Depends(get_current_user)):
    user_id = current_user["user"].id
    logger.info(f"Current user: {user_id}")
    transactions=get_all_transactions_by_user(user_id)
    transactions_dict = [transaction.dict() for transaction in transactions]

    return JSONResponse(content=transactions_dict, status_code=200)

@router.post("/transactions")
async def create_transaction(transaction: TransactionCreate, current_user: str = Depends(get_current_user)):

    user_id = current_user["user"].id
    logger.info(f"Transaction: {transaction}")
    if transaction.category.isdigit():
        category_id = int(transaction.category)
        category = get_catagory_by_id(category_id)
        transaction.category = category
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found create a new one")
    # If transaction.category is a new name, create a new category in the database
    else:
        category_name = transaction.category
        category = create_catagory(CatagoryCreate(name=category_name))
        transaction.category = category
    try:
        created_transaction = create_new_transaction(transaction,user_id)
    except Exception as e:
        logger.error(f"Error creating transaction: {e}")
        raise HTTPException(status_code=500, detail="Error creating transaction")
    return JSONResponse(status_code=201,content={"message": "Transaction created successfully"})
@router.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):
    # Logic to retrieve a specific transaction
    pass

@router.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int):
    # Logic to update a specific transaction
    pass

@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    # Logic to delete a specific transaction
    pass

@router.get("/categories")
async def get_categories():
    categories = get_all_catagories()
    return JSONResponse(content=categories, status_code=200)


@router.post("/categories")
async def create_categories():
    categories = create_categories()
    return JSONResponse(status_code=201)


