package util;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public final class DBConnection {
    private static final String URL = getConfigValue("DB_URL", "jdbc:mysql://localhost:3306/smart_task_tracker");
    private static final String USER = getConfigValue("DB_USER", "root");
    private static final String PASSWORD = getConfigValue("DB_PASSWORD", "");
    private static Connection connection;

    private DBConnection() {
    }

    static {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException exception) {
            throw new ExceptionInInitializerError("MySQL JDBC driver not found: " + exception.getMessage());
        }
    }

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }

    private static String getConfigValue(String name, String defaultValue) {
        String value = System.getenv(name);
        return value == null ? defaultValue : value;
    }
}