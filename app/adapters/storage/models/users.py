# from datetime import date
#
# import sqlalchemy as sa
# from fastapi_users.db import SQLAlchemyBaseUserTable
# from sqlalchemy.orm import Mapped, mapped_column
#
# from app.adapters.storage.db.base_model import BaseModel
#
#
# class User(BaseModel, SQLAlchemyBaseUserTable[int]):
#     """Пользователи."""
#
#     __tablename__ = "users"
#
#     id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
#     username: Mapped[str] = mapped_column(sa.String(64), unique=True)
#     created: Mapped[date]
#
#     def __str__(self) -> str:
#         return self.username
