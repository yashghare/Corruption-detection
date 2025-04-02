from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class ProcurementTransaction(Base):
    __tablename__ = "procurement_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    department = Column(String)
    contract_value = Column(Float)
    supplier = Column(String)
    contract_duration = Column(Integer)
    bidding_process = Column(String)
    num_bidders = Column(Integer)
    winning_bid_ratio = Column(Float)
    previous_contracts = Column(Integer)
    officer_tenure = Column(Integer)
    predicted_fraud = Column(Boolean)
    fraud_probability = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    reviewed = Column(Boolean, default=False)
    confirmed_fraud = Column(Boolean, nullable=True)