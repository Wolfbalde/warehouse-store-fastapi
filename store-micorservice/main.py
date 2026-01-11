import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
import requests
from fastapi.background import BackgroundTasks

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:3000'],
  allow_methods=['*'],
  allow_headers=['*']
)

redis = get_redis_connection(
    host='redis-13525.crce182.ap-south-1-1.ec2.cloud.redislabs.com',
    port=13525,
    decode_responses=True,
    password="GFbHVtEdrhw7M2KyiGHxadQB6OoOF0OG"
)

class ProductOrder(HashModel):
  product_id: str
  quantity: int
  class Meta:
    database = redis

class Order(HashModel):
  product_id: str
  price: float
  fee: float
  total: float
  quantity: int
  status: str
  class Meta:
    database = redis

@app.post("/orders", tags=['store'])
def create(productOrder: ProductOrder, backgroundTasks: BackgroundTasks):
  req = requests.get(f'http://localhost:8000/product/{productOrder.product_id}')
  product = req.json()
  fee = product['price'] * 0.2

  order = Order(
      product_id=productOrder.product_id,
      price=product['price'],
      quantity=productOrder.quantity,
      status='pending',
      total=product['price'] + fee,
      fee=fee
  )
  backgroundTasks.add_task(complete_order,order)
  order.save()

  return order

@app.get('/orders/{pk}', tags=['store'])
def get(pk: str):
  return format(pk)

@app.get('/orders', tags=['store'])
def get_all():
  return [format(pk) for pk in Order.all_pks()]

def format(pk: str):
  order = Order.get(pk)
  return {
    'id': order.pk,
    'product_id': order.product_id,
    'fee': order.fee,
    'total': order.total,
    'quantity': order.quantity,
    'status': order.status
  }


def complete_order(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order-completed',fields=order.dict())