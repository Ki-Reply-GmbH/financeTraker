from app.models.models import SessionLocal,get_db,Category,Transaction
from app.services.user_services import get_user_by_id
from app.models.transaction import CatagoryCreate,TransactionCreate
from app.logger import get_logger

logger = get_logger(__name__)
def get_all_catagories():
    with get_db() as db:
        categories = db.query(Category).all()
        return [category.to_dict() for category in categories]
def get_catagory_by_id(id: int):
    with get_db() as db:
        catagory = db.query(Category).filter(Category.id == id).first()
        return catagory
    
def create_catagory(catagory: CatagoryCreate):
    with get_db() as db:
        db_catagory = Category(**catagory.model_dump())
        db.add(db_catagory)
        db.commit()
        db.refresh(db_catagory)
        return db_catagory
    
def create_new_transaction(transaction: TransactionCreate,user_id: int,):
    with get_db() as db:
        db_transaction = Transaction(user_id=user_id, category_id=Transaction.category, **transaction.dict())
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    
def get_transaction_by_id(id: int):
    with get_db() as db:
        transaction = db.query(Transaction).filter(Transaction.id == id).first()
        return transaction
    
def get_all_transactions_by_user(user_id: int):
    with get_db() as db:
        transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
        transaction_creates = []
        for transaction in transactions:
            # Fetch the associated Category object from the database
            category = db.query(Category).filter(Category.id == transaction.category_id).first()
            # Convert the Transaction object to a TransactionCreate object
            transaction_create = TransactionCreate(
                type=transaction.type,
                source=transaction.source,
                category=category.name,  # use the category name
                trxdate=transaction.trxdate.date(),
                description=transaction.description,
                amount=transaction.amount
            )
            transaction_creates.append(transaction_create)
        return transaction_creates
    
def get_all_transactions():
    with get_db() as db:
        transactions = db.query(Transaction).all()
        return [transaction.to_dict() for transaction in transactions]