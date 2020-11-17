import pprint

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta


## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


# SEARCH TAB: 검색 (인터넷에서 GET)
@app.route('/search/place', methods=['GET'])
def search_place():
    pass


# 네비게이션 (현재위치에서 목적지)
@app.route('/search/route', methods=['GET'])
def search_route():
    # X-NCP-APIGW-API-KEY-ID: xscwyxumfh
    # X-NCP-APIGW-API-KEY: X0ukDd6Z4n1DT4QUW7GlN8Jf0hXq13Alqk825xes

    response_start_long = request.args.get('long_give')
    response_start_lat = request.args.get('lat_give')
    response_goal = request.args.get('place_give')
    print(response_goal, response_start_lat, response_start_long)

    # 목적지 좌표 얻기
    geocode_goal = requests.get('https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode',
                                headers={'X-NCP-APIGW-API-KEY-ID': 'xscwyxumfh',
                                         'X-NCP-APIGW-API-KEY': 'X0ukDd6Z4n1DT4QUW7GlN8Jf0hXq13Alqk825xes'
                                         },
                                params={'query': response_goal
                                        })
    geocode_goal_json = geocode_goal.json()
    if geocode_goal_json['status'] != 'OK':
        print("status is not ok")
        return jsonify({'result': 'failure'})

    addresses = geocode_goal_json['addresses']
    if len(addresses) < 1:
        print("failed to get address")
        return jsonify({'result': 'failure'})

    address = addresses[0]
    x = address['x']
    y = address['y']

    # 경로찾기

    driving_response = requests.get('https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving',
                                    headers={'X-NCP-APIGW-API-KEY-ID': 'xscwyxumfh',
                                             'X-NCP-APIGW-API-KEY': 'X0ukDd6Z4n1DT4QUW7GlN8Jf0hXq13Alqk825xes'
                                             },
                                    params={'start': f'{response_start_long},{response_start_lat}',
                                            'goal': f'{x},{y}'
                                            }
                                    )

    driving_response_json = driving_response.json()
    if driving_response_json['code'] != 0:
        print(driving_response_json['code'])
        print("code is not ok")
        return jsonify({'result': 'failure'})
    pp = pprint.PrettyPrinter(depth=6)
    pp.pprint(driving_response_json)

    # route = driving_response.json(['route']['traoptimal']['path'])
    # distance = driving_response.json(['route']['traoptimal']['summary']['distance'])
    # tollfare = driving_response.json(['route']['traoptimal']['summary']['tollFare'])

    # response_goal_
    print(driving_response_json['route']['traoptimal'][0]['summary']['duration'])
    return jsonify({'result': 'success', 'route': driving_response_json['route']})


# 장소 저장
@app.route('/save/place', methods=['POST'])
def save_place():
    pass


# Savedlist : 저장장소 불러오기 (DB에서 GET)
@app.route('/read', methods=['GET'])
def view_list():
    pass


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    # 여길 채워나가세요!
    all_orders = list(db.orders.find({}, {'_id': False}))
    for order in all_orders:
        print(order)

    return jsonify({'result': 'success', 'orders': all_orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
