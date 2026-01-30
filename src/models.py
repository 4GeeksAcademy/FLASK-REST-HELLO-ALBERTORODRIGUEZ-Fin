from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,Table,Column,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

post_table = Table(
    "post",
    db.Model.metadata,
    Column("user_id",ForeignKey("user.id"), primary_key= True),
    Column("comment_id",ForeignKey("comment.id"), primary_key=True)
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    post: Mapped[list["Comment"]] = relationship(
        "Comment",
        secondary=post_table,
        back_populates="post_by" 
    )

    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "post": [comment.serialize() for comment in self.post]
            # do not serialize the password, its a security breach
        }
    

class Comment(db.Model):
     id: Mapped[int] = mapped_column(primary_key=True)
     comment_text: Mapped[str] = mapped_column(String(120), nullable=False)
     post_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=post_table,
        back_populates="post" 
    )

     def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            # do not serialize the password, its a security breach
        }
     