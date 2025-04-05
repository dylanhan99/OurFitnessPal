from sqlalchemy import text, MetaData, Table, Column, Integer, String, inspect, select
from sqlalchemy.dialects.postgresql import JSONB 
from sqlalchemy.ext.mutable import MutableDict
from ofpdb import db, BaseTable

#####
# Schema classes
class db_MacroCalorie(db.Model):
    __tablename__ = "MacroCalorie"

    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(20), nullable=False)

class db_Food(db.Model):
    __tablename__  = "Food"

    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(80), nullable=False)
    description         = db.Column(db.String(120), nullable=False)
    nutritional_info    = db.Column(JSONB)

    __table_args__ = (
        db.Index('idx_food_tags', nutritional_info, postgresql_using='gin'),
    )

class db_FoodLog(db.Model):
    __tablename__ = "FoodLogs"

    id                  = db.Column(db.Integer, primary_key=True)
    food_id             = db.Column(db.Integer, db.ForeignKey("Food.id"))
    grams               = db.Column(db.Float, nullable=False)
    log_date            = db.Column(db.DateTime, nullable=False)
#####

####
## DB operation wrapper classes
class MacroCalorie(BaseTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def select_all(self):
        results = db_MacroCalorie.query.all()
        return results
    
    @property 
    def db_type(self):
        return db_MacroCalorie

class Food(BaseTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def select_all(self):
        results = db_Food.query.all()
        return results

    def insert_food(self, name: str, description: str, carbs: int, fats: int, proteins: int):
        new_food = db_Food(
            name = name,
            description = description,
            nutritional_info = {
                "carbs":    carbs,
                "fats":     fats,
                "proteins": proteins
            }
        )

        #self.engine.execute_with_commit(obj=new_food)
        self.engine.execute_with_commit(lambda session: session.add(new_food))

    def erase_row(self, row_num: int):
        all_rows = self.select_all()
        if not (0 < row_num <= len(all_rows)):
            return
        row_to_delete = all_rows[row_num - 1]
        self.engine.execute_with_commit(lambda session: session.delete(row_to_delete))

    @property 
    def db_type(self):
        return db_Food


class FoodLog(BaseTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def select_all(self):
        results = db_FoodLog.query.all()
        return results
    
    @property 
    def db_type(self):
        return db_FoodLog
####