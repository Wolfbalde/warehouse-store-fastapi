import time
from main import redis,Product

key='order-completed'
group='warehouse-group'

try:
    redis.xgroup_create(name=key,groupname=group,mkstream=True)
    print("Group Created")
except Exception as e:
    print(str(e))


while True:
    try:
        results=redis.xreadgroup(groupname=group,consumername=key,streams={key:'>'})
        print(results)
        if results !=[]:
            for r in results:
                obj=r[1][0][1]
                try:
                    product = Product.get(obj['product_id'])
                    product.quantity -= int(obj['quantity'])
                    product.save()
                    print(product)
                except Exception as e:
                    redis.xadd(name='refund-initiated',fields=obj)
    except Exception as e:
        print(str(e))
    time.sleep(3)