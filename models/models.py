from sqlalchemy import String, Integer, Float, ForeignKey, Text, Column, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# 1. Users
class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    disabled = Column(Boolean, default=False)

    # Связи
    portfolio: Mapped["Portfolio"] = relationship(back_populates="user", uselist=False)
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")


# 2. Portfolio
class Portfolio(Base):
    __tablename__ = "Portfolio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    crypto_currency: Mapped[str] = mapped_column(Text, nullable=False)
    buy_price: Mapped[float] = mapped_column(Float, nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"), nullable=False)

    # Связь
    user: Mapped["User"] = relationship(back_populates="portfolio")


# 3. Transactions
class Transaction(Base):
    __tablename__ = "Transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    crypto_currency: Mapped[str] = mapped_column(Text, nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_date: Mapped[str] = mapped_column(String, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String, nullable=False)
    price_per_unit: Mapped[float] = mapped_column(Float, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"), nullable=False)

    # Связь
    user: Mapped["User"] = relationship(back_populates="transactions")

