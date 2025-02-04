from flask import Flask, request, jsonify
from peewee import *
from src.core.models import Postman, District, Subscriber, Publication, Subscription

app = Flask(__name__)


# 1. Эндпоинт для получения количества копий каждой публикации
@app.route('/get_publication_copies', methods=['GET'])
def get_publication_copies():
    query = (Publication
             .select(Publication.name.alias('publication_name'), fn.SUM(Subscription.amount).alias('total_copies'))
             .join(Subscription, on=(Subscription.publication == Publication.index))
             .group_by(Publication.name))

    result = []
    for row in query.execute():
        result.append({
            'publication_name': row.publication_name,
            'total_copies': row.total_copies
        })
    return jsonify(result)


# 2. Эндпоинт для получения почтальона по адресу
@app.route('/get_postman_by_address', methods=['GET'])
def get_postman_by_address():
    address = request.args.get('address')  # Получаем адрес из запроса
    if not address:
        return jsonify({'error': 'Address parameter is required'}), 400

    query = (Postman
             .select(Postman.last_name.alias('postman_last_name'))
             .join(District, on=(District.postman == Postman.postman_id))
             .join(Subscriber, on=(Subscriber.district == District.district_id))
             .where(Subscriber.address == address))

    result = []
    for row in query.execute():
        result.append({'postman_last_name': row.postman_last_name})
    return jsonify(result)


# 3. Эндпоинт для получения публикаций, подписанных определенным подписчиком
@app.route('/get_publications_by_subscriber', methods=['GET'])
def get_publications_by_subscriber():
    last_name = request.args.get('last_name')
    first_name = request.args.get('first_name')
    middle_name = request.args.get('middle_name')

    if not (last_name and first_name and middle_name):
        return jsonify({'error': 'All name parameters (last_name, first_name, middle_name) are required'}), 400

    query = (Publication
             .select(Publication.name.alias('publication_name'), Subscription.amount.alias('amount'))
             .join(Subscription, on=(Subscription.publication == Publication.index))
             .join(Subscriber, on=(Subscription.subscriber == Subscriber.subscriber_id))
             .where((Subscriber.last_name == last_name) &
                    (Subscriber.first_name == first_name) &
                    (Subscriber.middle_name == middle_name)))

    result = []
    for row in query.execute():
        result.append({
            'publication_name': row.publication_name
        })
    return jsonify(result)


# 4. Эндпоинт для получения общего количества почтальонов
@app.route('/get_total_postmen', methods=['GET'])
def get_total_postmen():
    query = Postman.select(fn.COUNT(Postman.postman_id).alias('total_postmen'))
    total_postmen = query.scalar()  # Получаем результат запроса как число
    return jsonify({'total_postmen': total_postmen})


# 5. Эндпоинт для получения района с максимальным количеством копий
@app.route('/get_max_copies_district', methods=['GET'])
def get_max_copies_district():
    query = (District
             .select(Subscriber.district.alias('district_id'),
                     District.name.alias('district_name'),
                     fn.SUM(Subscription.amount).alias('total_copies'))
             .join(Subscriber, on=(Subscriber.district == District.district_id))
             .join(Subscription, on=(Subscription.subscriber == Subscriber.subscriber_id))
             .group_by(Subscriber.district, District.name)
             .order_by(fn.SUM(Subscription.amount).desc())
             .limit(1))

    result = query.first()  # Получаем только первую запись
    if result:
        return jsonify({
            'district_name': result.district_name,
            'total_copies': result.total_copies
        })
    else:
        return jsonify({'message': 'No data available'}), 404


# 6. Эндпоинт для получения среднего периода подписки на каждую публикацию
@app.route('/get_average_subscription_period', methods=['GET'])
def get_average_subscription_period():
    query = (Publication
             .select(Publication.name.alias('publication_name'), fn.AVG(Subscription.period).alias('avg_period'))
             .join(Subscription, on=(Subscription.publication == Publication.index))
             .group_by(Publication.name))

    result = []
    for row in query.execute():
        result.append({
            'publication_name': row.publication_name,
            'avg_period': row.avg_period
        })

    return jsonify(result)


@app.route('/')
def home():
    return {'1 query': 'get_publication_copies',
            '2 query': 'get_postman_by_address',
            '3 query': 'get_publications_by_subscriber',
            '4 query': 'get_total_postmen',
            '5 query': 'get_max_copies_district',
            '6 query': 'get_average_subscription_period'}


if __name__ == '__main__':
    app.run(debug=True)
