from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,Table,Column,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()



follower_table = Table(
    "follower",
    db.Model.metadata,
    Column("user_from_id", ForeignKey("user.id"), primary_key=True),
    Column("user_to_id", ForeignKey("user.id"), primary_key=True)
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    correos: Mapped[list["Correo"]] = relationship(back_populates="author")
    comentarios: Mapped[list["Comentario"]] = relationship(back_populates="author")

    following = relationship(
        "User",
        secondary=follower_table,
        primaryjoin=(follower_table.c.user_from_id == id),
        secondaryjoin=(follower_table.c.user_to_id == id),
        backref="followers"
    )
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "follower": [follower.serialize() for follower in self.following]
            
        }
    



class Correo(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="correos")
    
    media: Mapped[list["Media"]] = relationship(back_populates="correo")
    comentarios: Mapped[list["Comentario"]] = relationship(back_populates="post")


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    correo_id: Mapped[int] = mapped_column(ForeignKey("correo.id"))
    correo: Mapped["Correo"] = relationship(back_populates="media")


class Comentario(db.Model):
     id: Mapped[int] = mapped_column(primary_key=True)
     comment_text: Mapped[str] = mapped_column(String(120), nullable=False)

     author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
     author: Mapped["User"] = relationship(back_populates="comentarios")

     post_id: Mapped[int] = mapped_column(ForeignKey("correo.id"))  
     post: Mapped["Correo"] = relationship(back_populates="comentarios")


     def serialize(self):
      return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }

     
    

    