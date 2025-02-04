from faker import Faker
from src.core.models import Postman, District, Subscriber, Publication, Subscription
from src.core.db import db
from peewee import chunked

fake = Faker()


def seed_postmen(count):
    data = [{'first_name': fake.first_name(),
             'middle_name': fake.first_name(),
             'last_name': fake.last_name()} for _ in range(count)]

    with db.atomic():
        for batch in chunked(data, 1000):
            Postman.insert_many(batch).execute()


def seed_districts(count):
    postmen_ids = [postman.postman_id for postman in Postman.select()]
    data = []
    for _ in range(count):
        name = fake.unique.street_name()
        data.append({'name': name, 'postman': fake.random.choice(postmen_ids)})

    with db.atomic():
        for batch in chunked(data, 1000):
            District.insert_many(batch).execute()


def seed_subscribers(count):
    district_ids = [district.district_id for district in District.select()]
    data = [{'first_name': fake.first_name(),
             'middle_name': fake.first_name(),
             'last_name': fake.last_name(),
             'address': fake.street_name(),
             'district': fake.random.choice(district_ids)} for _ in range(count)]

    with db.atomic():
        for batch in chunked(data, 1000):
            Subscriber.insert_many(batch).execute()
    result = data[count // 2]
    return result


def seed_publications(count):
    data = []
    for i in range(1, count + 1):
        name = fake.unique.text(max_nb_chars=20)
        data.append({'index': i,
                     'name': name,
                     'price': fake.pydecimal(left_digits=5, right_digits=2, positive=True)})

    with db.atomic():
        for batch in chunked(data, 1000):
            Publication.insert_many(batch).execute()


def seed_subscriptions(count):
    subscriber_ids = [
        subscriber.subscriber_id for subscriber in Subscriber.select()]
    publication_ids = [
        publication.index for publication in Publication.select()]

    unique_subscriptions = set()
    data = []

    for _ in range(count):
        while True:
            subscriber = fake.random.choice(subscriber_ids)
            publication = fake.random.choice(publication_ids)
            subscription_key = (subscriber, publication)

            if subscription_key not in unique_subscriptions:
                unique_subscriptions.add(subscription_key)
                break

        data.append({
            'subscriber': subscriber,
            'publication': publication,
            'issue_date': fake.date_time_between(start_date='-1y', end_date='now'),
            'period': fake.random_int(min=1, max=12),
            'amount': fake.random_int(min=1, max=10),
            'total_price': None
        })

    with db.atomic():
        for batch in chunked(data, 1000):
            Subscription.insert_many(batch).execute()


def faker_seed_data(amount=100):
    seed_postmen(amount)
    seed_districts(amount)
    _ = seed_subscribers(amount)
    seed_publications(amount)
    seed_subscriptions(amount)


if __name__ == '__main__':
    faker_seed_data()
