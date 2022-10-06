from peewee import *
from config.db import db_descriptor

db = SqliteDatabase(db_descriptor)


class AMR(Model):

    class Meta:
        database = db  # This model uses the "people.db" database.
        db_table = 'amr'

    # 第0位：设备类型
    e_type = CharField()
    # 第1位：小车编号（int，1，2，3，4）
    number = IntegerField(primary_key=True, unique=True)
    # 第2位：时间（字符串）
    timestamp = CharField(null=True)
    # 第3位：小车负载（int，0无负载，1负载）
    load = IntegerField(null=True)
    # 第4位：小车x坐标（float_x）
    x = FloatField(null=True)
    # 第5位：小车y坐标（float_y）
    y = FloatField(null=True)
    # 第5位：小车偏航角（float \theat）
    yaw = FloatField(null=True)
    # 第6位：小车线速度（float v）
    line_velocity = FloatField(null=True)
    # 第7位：小车角速度（float w）
    angular_velocity = FloatField(null=True)
    # 第8位：小车电量（float）
    quantity = FloatField(null=True)
    # 第9位：预留位1（float）
    unknown_1 = FloatField(null=True)
    # 第10位：预留位2（字符串）
    unknown_2 = CharField(null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.table_exists():
            self.create_table()

    def input(self, data: dict):
        if 'number' not in data:
            # 数据错误
            return {False, "number 不存在数据中"}
        amr_selected = AMR.select().where(AMR.number == data['number'])
        if not amr_selected.exists():
            # 目标AMR数据不存在
            try:
                AMR.create(**data)
                return {True, "新建行：{}".format(data)}
            except Exception as e:
                return {False, "创建行失败：{}".format(e)}
        # 数据存在，更新数据
        try:
            amr_selected.get().update(**data).execute()
            return {True, "更新行：{}".format(data)}
        except Exception as e:
            return {False, "更新数据失败：{}".format(e)}

    def get(self, number: int):
        amr_selected = AMR.select().where(AMR.number == number)
        if not amr_selected.exists():
            # 目标AMR数据不存在
            return False, "数据不存在"
        return True, amr_selected.dicts().get()
