package util;

import java.sql.Connection;
import java.sql.SQLException;

public class ConnectionTest {
    public static void main(String[] args) {
        try (Connection connection = DBConnection.getConnection()) {
            System.out.println("Database connection successful.");
        } catch (SQLException exception) {
            System.err.println("Database connection failed: " + exception.getMessage());
            System.exit(1);
        }
    }
}