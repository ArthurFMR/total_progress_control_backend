from typing import List

from sqlalch import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    __table_args__ = (
        db.UniqueConstraint("list_id", "title", name="unique_list_item"),
    )

    item_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    notes = db.Column(db.String)
    total_qty = db.Column(db.Integer, nullable=False, default=0)
    qty_done = db.Column(db.Integer, default=0)

    list_id = db.Column(db.Integer, db.ForeignKey("lists.list_id"), nullable=False)
    _list = db.relationship("ListModel")

    @classmethod
    def find_by_title(cls, title: str) -> "ItemModel":
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "ItemModel":
        return cls.query.filter_by(item_id=_id).first()

    @classmethod
    def find_by_title_list_id(cls, title: str, _id: int) -> "ItemModel":
        return cls.query.filter_by(title=title, list_id=_id).first()

    @classmethod
    def find_all(cls, _id) -> List["ItemModel"]:
        return cls.query.filter_by(list_id=_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit() 