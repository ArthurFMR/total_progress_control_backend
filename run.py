from app import app
from sqlalch import db
from marsh import marsh

db.init_app(app)
marsh.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
