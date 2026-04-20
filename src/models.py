import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from eralchemy2 import render_er

Base = declarative_base()

# -------------------------
# USER
# -------------------------
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(250), nullable=False)

    posts = relationship("Post", backref="user")
    comments = relationship("Comment", backref="user")
    likes = relationship("Like", backref="user")

    followers = relationship(
        "Follow",
        foreign_keys="Follow.user_id",
        back_populates="user"
    )

    following = relationship(
        "Follow",
        foreign_keys="Follow.follower_id",
        back_populates="follower"
    )

    def __repr__(self):
        return f"<User {self.username}>"


# -------------------------
# POST
# -------------------------
class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    image_url = Column(String(250), nullable=False)
    caption = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))

    comments = relationship("Comment", backref="post")
    likes = relationship("Like", backref="post")

    def __repr__(self):
        return f"<Post {self.id}>"


# -------------------------
# COMMENT
# -------------------------
class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    text = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    def __repr__(self):
        return f"<Comment {self.text[:20]}>"


# -------------------------
# LIKE
# -------------------------
class Like(Base):
    __tablename__ = 'like'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    def __repr__(self):
        return f"<Like user={self.user_id} post={self.post_id}>"


# -------------------------
# FOLLOW
# -------------------------
class Follow(Base):
    __tablename__ = 'follow'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))      # seguido
    follower_id = Column(Integer, ForeignKey('user.id'))  # seguidor

    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="followers"
    )

    follower = relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="following"
    )

    def __repr__(self):
        return f"<Follow {self.follower_id} -> {self.user_id}>"


# -------------------------
# DIAGRAMA UML
# -------------------------
def draw_er_diagram():
    try:
        render_er(Base, 'diagram.png')
        print("✔️ Diagrama generado correctamente: diagram.png")
    except Exception as e:
        print("❌ Error generando el diagrama:", e)
        raise e


if __name__ == '__main__':
    draw_er_diagram()
