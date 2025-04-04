from sqlalchemy import text, MetaData, Table, Column, Integer, String, inspect
from ofpdb import db, BaseTable

#####
# Schema classes
class db_FoodTable(db.Model):
    __tablename__  = "Food"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
#####

####
## DB operation wrapper classes
class FoodTable(BaseTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
####