from sqlalchemy import text, MetaData, Table, Column, Integer, String, inspect
from sqlalchemy.dialects.postgresql import JSONB 
from sqlalchemy.ext.mutable import MutableDict
from ofpdb import db, BaseTable

#####
# Schema classes
class db_MacroCalories(db.Model):
    __tablename__ = "MacroCalories"

    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(20), nullable=False)

class db_FoodTable(db.Model):
    __tablename__  = "Food"

    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(80), nullable=False)
    description         = db.Column(db.String(120), nullable=False)
    nutritional_info    = db.Column(JSONB)

    __table_args__ = (
        db.Index('idx_food_tags', nutritional_info, postgresql_using='gin'),
    )

class db_FoodLogs(db.Model):
    __tablename__ = "FoodLogs"

    id                  = db.Column(db.Integer, primary_key=True)
    food_id             = db.Column(db.Integer, db.ForeignKey("Food.id"))
    grams               = db.Column(db.Float, nullable=False)
    log_date            = db.Column(db.DateTime, nullable=False)
#####

####
## DB operation wrapper classes
class FoodTable(BaseTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def insert_food(self, name: str, description: str, carbs: int, fats: int, proteins: int):
        new_food = db_FoodTable(
            name = name,
            description = description,
            nutritional_info = {
                "carbs":    carbs,
                "fats":     fats,
                "proteins": proteins
            }
        )

        self._db.execute_with_commit(obj=new_food)
####