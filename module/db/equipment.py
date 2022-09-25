from peewee import Model
class Equipment(Model):
    def __init__(self) -> None:
        if not self.table_exists(self):
            self.create_table()