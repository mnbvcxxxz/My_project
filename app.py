from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta


## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


# 주문하기(POST) API
@app.route('/order', methods=['POST'])
def save_order():

# 여길 채워나가세요!
    name_receive = request.form['name_give']  # 클라이언트로부터 url을 받는 부분
    count_receive = request.form['count_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']

    order = {
      'name': name_receive,
      'count': count_receive,
      'address': address_receive,
      'phone': phone_receive}

    db.orders.insert_one(order)

    return jsonify({'result': 'success'})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    # 여길 채워나가세요!
    all_orders = list(db.orders.find({},{'_id':False}))
    for order in all_orders:
        print(order)

    return jsonify({'result': 'success', 'orders': all_orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)