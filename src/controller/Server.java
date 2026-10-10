package controller;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class Server {
    public HttpServer startServer(int port) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        TaskController controller = new TaskController();

        server.createContext("/api/auth", controller::handle);
        server.createContext("/api/tasks/create", controller::handle);
        server.createContext("/api/tasks/user", controller::handle);
        server.createContext("/api/tasks", controller::handle);
        server.createContext("/api/calendar", controller::handle);
        server.createContext("/api/subtasks", controller::handle);
        server.createContext("/api/collaborators", controller::handle);
        server.createContext("/api", controller::handle);
        server.createContext("/", exchange -> handleStaticFile(exchange, controller));

        server.setExecutor(java.util.concurrent.Executors.newCachedThreadPool());
        server.start();
        System.out.println("Smart Assignment Tracker HTTP server started on http://localhost:" + port);
        return server;
    }

    private void handleStaticFile(HttpExchange exchange, TaskController controller) throws IOException {
        String path = exchange.getRequestURI().getPath();
        if (path.startsWith("/api/")) {
            controller.handle(exchange);
            return;
        }

        if ("/favicon.ico".equals(path)) {
            sendStaticResponse(exchange, 204, "image/x-icon", new byte[0]);
            return;
        }

        if ("/".equals(path) || path == null || path.isEmpty()) {
            path = "/index.html";
        }

        if (path.contains("..")) {
            sendStaticResponse(exchange, 400, "text/plain", "Bad Request".getBytes());
            return;
        }

        File file = new File("src/main/resources" + path);
        byte[] content = null;
        if (file.exists() && file.isFile()) {
            try (FileInputStream fis = new FileInputStream(file)) {
                content = fis.readAllBytes();
            }
        } else {
            InputStream is = Server.class.getResourceAsStream(path);
            if (is == null) {
                is = Server.class.getResourceAsStream("/" + path);
            }
            if (is != null) {
                try (InputStream stream = is) {
                    content = stream.readAllBytes();
                }
            }
        }

        if (content == null) {
            sendStaticResponse(exchange, 404, "text/plain", "404 Not Found".getBytes());
            return;
        }

        String contentType = "text/plain";
        if (path.endsWith(".html")) contentType = "text/html; charset=UTF-8";
        else if (path.endsWith(".css")) contentType = "text/css; charset=UTF-8";
        else if (path.endsWith(".js")) contentType = "application/javascript; charset=UTF-8";
        else if (path.endsWith(".json")) contentType = "application/json; charset=UTF-8";

        sendStaticResponse(exchange, 200, contentType, content);
    }

    private void sendStaticResponse(HttpExchange exchange, int statusCode, String contentType, byte[] data) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", contentType);
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        exchange.getResponseHeaders().set("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS");
        exchange.getResponseHeaders().set("Access-Control-Allow-Headers", "Content-Type, Accept");
        exchange.sendResponseHeaders(statusCode, data.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(data);
        }
    }

    public static void main(String[] args) throws IOException {
        int port = 8080;
        String envPort = System.getenv("PORT");
        if (envPort != null && !envPort.isBlank()) {
            try {
                port = Integer.parseInt(envPort.trim());
            } catch (NumberFormatException ignored) {}
        }
        new Server().startServer(port);
    }
}

