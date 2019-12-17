from sqlalch import db

from typing import List


class ListModel(db.Model):
    __tablename__ = 'lists'

    __table_args__ = (
        db.UniqueConstraint("user_id", "title", name="unique_user_list"),
    )

    list_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    user = db.relationship("UserModel")

    items = db.relationship("ItemModel", lazy="dynamic")

    @classmethod
    def find_by_title(cls, title: str) -> "ListModel":
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "ListModel":
        return cls.query.filter_by(list_id=_id).first()

    @classmethod
    def find_by_title_user_id(cls, title: str, _id: int) -> "ListModel":
        return cls.query.filter_by(title=title, user_id=_id).first()

    @classmethod
    def find_all(cls, _id) -> List["ListModel"]:
        return cls.query.filter_by(user_id=_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()