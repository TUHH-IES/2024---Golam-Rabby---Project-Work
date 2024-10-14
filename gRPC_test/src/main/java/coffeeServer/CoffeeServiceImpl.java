// CoffeeServiceImpl.java

package coffeeServer;




import com.example.coffee.*;
import com.example.coffee.CoffeeProto.*;
import com.example.coffee.CoffeeServiceGrpc.CoffeeServiceImplBase;
import io.grpc.stub.StreamObserver;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

public class CoffeeServiceImpl extends CoffeeServiceGrpc.CoffeeServiceImplBase {

    // In-memory storage for orders
    private final Map<Integer, String> orderStatusMap = new ConcurrentHashMap<>();
    private final AtomicInteger orderIdGenerator = new AtomicInteger(1);

    @Override
    public void makeCoffee(MakeCoffeeRequest request, StreamObserver<MakeCoffeeResponse> responseObserver) {
        int orderId = orderIdGenerator.getAndIncrement();
        String status = "Order received";

        orderStatusMap.put(orderId, "Preparing");


        MakeCoffeeResponse response = MakeCoffeeResponse.newBuilder()
                .setOrderId(orderId)
                .setStatus(status)
                .build();

        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }

    @Override
    public void getOrderStatus(GetOrderStatusRequest request, StreamObserver<GetOrderStatusResponse> responseObserver) {
        int orderId = request.getOrderId();
        String status = orderStatusMap.get(orderId);

        if (status != null) {
            GetOrderStatusResponse response = GetOrderStatusResponse.newBuilder()
                    .setOrderId(orderId)
                    .setStatus(status)
                    .build();
            responseObserver.onNext(response);
            responseObserver.onCompleted();
        } else {
            responseObserver.onError(io.grpc.Status.NOT_FOUND
                    .withDescription("Order ID " + orderId + " not found.")
                    .asRuntimeException());
        }
    }
}

