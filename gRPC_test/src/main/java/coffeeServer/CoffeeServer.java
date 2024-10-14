// CoffeeServer.java

package coffeeServer;

import io.grpc.Server;
import io.grpc.ServerBuilder;

import java.io.IOException;

public class CoffeeServer {

    private final int port;
    private final Server server;

    public CoffeeServer(int port) {
        this.port = port;
        this.server = ServerBuilder.forPort(port)
                .addService(new CoffeeServiceImpl())
                .build();
    }

    public void start() throws IOException {
        server.start();
        System.out.println("CoffeeServer started, listening on " + port);

        // Shutdown hook
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.err.println("*** Shutting down CoffeeServer since JVM is shutting down ***");
            CoffeeServer.this.stop();
            System.err.println("*** CoffeeServer shut down ***");
        }));
    }

    public void stop() {
        if (server != null) {
            server.shutdown();
        }
    }

    private void blockUntilShutdown() throws InterruptedException {
        if (server != null) {
            server.awaitTermination();
        }
    }

    public static void main(String[] args) throws IOException, InterruptedException {
        CoffeeServer server = new CoffeeServer(50051);
        server.start();
        server.blockUntilShutdown();
    }
}

