package test;

import dao.UserDAO;
import model.User;

import java.sql.Timestamp;

public class UserDAOTest {
    public static void main(String[] args) {
        UserDAO userDAO = new UserDAO();
        String gmail = "test.assignment.tracker@gmail.com";

        System.out.println("Checking Gmail: " + gmail);
        if (userDAO.gmailExists(gmail)) {
            System.out.println("Gmail already exists.");
        } else {
            User user = new User(0, gmail, "temporary-password", new Timestamp(System.currentTimeMillis()));
            boolean registered = userDAO.registerUser(user);
            System.out.println("Registration result: " + registered);
        }

        User foundUser = userDAO.findByGmail(gmail);
        if (foundUser != null) {
            System.out.println("Retrieved user: " + foundUser);
        } else {
            System.err.println("User was not found after registration attempt.");
            System.exit(1);
        }
    }
}
