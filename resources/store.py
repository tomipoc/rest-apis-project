from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema

# name, import name
blp = Blueprint("Stores", __name__, description="Operations on stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)  # get by the primary key
        return store
        # try:
        #     return stores[store_id]
        # except KeyError:
        #     abort(404, message="Store not found.")
    
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}
        # try:
        #     del stores[store_id]
        #     return {"message": "Store deleted."}
        # except KeyError:
        #     abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
        # return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema) # marshmallow can turn an object into json
    def post(self, store_data):
        store = StoreModel(**store_data)
        
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the store.")
        # for store in stores.values():
        #     if store_data["name"] == store["name"]:
        #         abort(400, message="Store already exists")
        
        # store_id = uuid.uuid4().hex
        # store = {**store_data, "id": store_id} # {"name": request_data["name"], "items": []}
        # stores[store_id] = store
        return store
