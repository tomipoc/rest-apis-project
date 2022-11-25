from db import db

class StoreModel(db.Model):
    __tablename__ = "stores" # we want to create/use the table items
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items  = db.relationship("ItemModel", back_populates="store", lazy="dynamic") # lazy="dynamic" will only fetch items when we use it, until I tell it to use this
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")  #back_populates should match the field name in TagModel
