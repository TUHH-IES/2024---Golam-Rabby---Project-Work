# client.py

import grpc
from coffeeService_pb2 import MakeCoffeeRequest, CoffeeType, CoffeeSize, GetOrderStatusRequest
from coffeeService_pb2_grpc import CoffeeServiceStub

def make_coffee(stub):
    print("Placing an order for a MEDIUM AMERICANO...")
    request = MakeCoffeeRequest(
        type=CoffeeType.AMERICANO,
        size=CoffeeSize.MEDIUM,
        customer_name="Ronaldo"
    )
    response = stub.MakeCoffee(request)
    print(f"Order ID: {response.order_id}")
    print(f"Status: {response.status}")
    return response.order_id

def get_order_status(stub, order_id):
    request = GetOrderStatusRequest(order_id=order_id)
    try:
        response = stub.GetOrderStatus(request)
        print(f"Order ID: {response.order_id}")
        print(f"Status: {response.status}")
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            print(f"Order not found: {e.details()}")
        else:
            print(f"An error has occurred: {e.details()}")

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = CoffeeServiceStub(channel)

        order_id = make_coffee(stub)

        get_order_status(stub, order_id)

if __name__ == '__main__':
    run()
