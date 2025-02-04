from peewee import Model, CharField, IntegerField, ForeignKeyField, AutoField, DecimalField, DateTimeField
from src.core.db import db


class BaseModel(Model):
    class Meta:
        database = db


class Postman(BaseModel):
    postman_id = AutoField()
    first_name = CharField(max_length=50)
    middle_name = CharField(max_length=50, null=True)
    last_name = CharField(max_length=50)

    class Meta:
        table_name = 'postman'
        indexes = [
            (('last_name', 'first_name'), False),
        ]


class District(BaseModel):
    district_id = AutoField()
    name = CharField(max_length=50)
    postman = ForeignKeyField(Postman, backref='districts', on_delete="RESTRICT")

    class Meta:
        table_name = 'district'
        indexes = [
            (('name',), True),
            (('postman',), False),
        ]


class Subscriber(BaseModel):
    subscriber_id = AutoField()
    first_name = CharField(max_length=50)
    middle_name = CharField(max_length=50, null=True)
    last_name = CharField(max_length=50)
    address = CharField(max_length=100)
    district = ForeignKeyField(District, backref='subscribers', on_delete="RESTRICT")

    class Meta:
        table_name = 'subscriber'
        indexes = [
            (('last_name', 'first_name', 'middle_name'), False),
            (('address',), False),
        ]


class Publication(BaseModel):
    index = IntegerField(primary_key=True)
    name = CharField(max_length=100)
    price = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table_name = 'publication'
        indexes = [
            (('name',), True)
        ]


class Subscription(BaseModel):
    subscription_id = AutoField()
    subscriber = ForeignKeyField(Subscriber, backref='subscriptions', on_delete="RESTRICT")
    publication = ForeignKeyField(Publication, backref='subscriptions', to_field='index')
    issue_date = DateTimeField()
    period = IntegerField()
    amount = IntegerField()
    total_price = DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        table_name = 'subscription'
        indexes = [
            (('subscriber', 'publication'), True),
            (('issue_date',), False),
        ]
