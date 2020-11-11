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
    response_data = requests.get('https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving',
                                 params = {'start':'response_start_long,response_start_lat','goal':'value2'})

    # X-NCP-APIGW-API-KEY-ID: xscwyxumfh
    # X-NCP-APIGW-API-KEY: X0ukDd6Z4n1DT4QUW7GlN8Jf0hXq13Alqk825xes

    response_start_long = request.args.get('long_give')
    response_start_lat = request.args.get('lat_give')
    response_goal = request.args.get('place_give')
    print(response_goal,response_start_lat,response_start_long)

    # route = response_data.json(['route']['traoptimal']['path'])
    # distance = response_data.json(['route']['traoptimal']['summary']['distance'])
    # tollfare = response_data.json(['route']['traoptimal']['summary']['tollFare'])

    # response_goal_

    jsonify({'result': 'success'})


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
