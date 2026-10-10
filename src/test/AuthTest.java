package test;

import dao.UserDAO;
import model.Session;
import model.User;
import util.PasswordUtil;

import java.security.GeneralSecurityException;
import java.sql.Timestamp;

public class AuthTest {
    private static final String TEST_GMAIL = "test.assignment.tracker@gmail.com";
    private static final String TEST_PASSWORD = "TestPassword123!";
    private static final String SECOND_TEST_GMAIL = "test.assignment.login." + System.currentTimeMillis() + "@gmail.com";

    public static void main(String[] args) {
        try {
            UserDAO userDAO = new UserDAO();

            System.out.println("1. Valid Gmail registration");
            printResult("Valid registration", registerUser(userDAO, SECOND_TEST_GMAIL, TEST_PASSWORD));

            System.out.println("2. Invalid Gmail");
            printResult("Invalid Gmail rejected", !registerUser(userDAO, "invalid", TEST_PASSWORD));

            System.out.println("3. Duplicate Gmail");
            printResult("Duplicate Gmail rejected", !registerUser(userDAO, SECOND_TEST_GMAIL, TEST_PASSWORD));

            System.out.println("4. Empty Gmail");
            printResult("Empty Gmail rejected", !registerUser(userDAO, "", TEST_PASSWORD));

            System.out.println("5. Empty password");
            printResult("Empty password rejected", !registerUser(userDAO, SECOND_TEST_GMAIL, ""));

            System.out.println("6. Correct login");
            Session session = loginUser(userDAO, SECOND_TEST_GMAIL, TEST_PASSWORD);
            printResult("Correct login", session != null && session.getUserId() > 0);

            System.out.println("7. Incorrect password");
            printResult("Incorrect password rejected", loginUser(userDAO, SECOND_TEST_GMAIL, "WrongPassword123!") == null);

            System.out.println("8. Nonexistent Gmail");
            printResult("Nonexistent Gmail rejected", loginUser(userDAO, "missing.user@gmail.com", TEST_PASSWORD) == null);

            System.out.println("9. Password hashing");
            String hash = PasswordUtil.hashPassword(TEST_PASSWORD);
            printResult("Password hash verifies", PasswordUtil.verifyPassword(TEST_PASSWORD, hash));

            System.out.println("10. Password hash mismatch");
            printResult("Wrong password rejected", !PasswordUtil.verifyPassword("DifferentPassword123!", hash));
        } catch (GeneralSecurityException exception) {
            System.err.println("Authentication test failed: " + exception.getMessage());
            System.exit(1);
        }
    }

    private static boolean registerUser(UserDAO userDAO, String gmail, String password) throws GeneralSecurityException {
        if (gmail == null || gmail.trim().isEmpty() || password == null || password.isEmpty()) {
            return false;
        }

        if (!gmail.endsWith("@gmail.com")) {
            return false;
        }

        if (userDAO.gmailExists(gmail)) {
            return false;
        }

        User user = new User();
        user.setGmail(gmail);
        user.setPassword(PasswordUtil.hashPassword(password));
        user.setCreatedAt(new Timestamp(System.currentTimeMillis()));
        return userDAO.registerUser(user);
    }

    private static Session loginUser(UserDAO userDAO, String gmail, String password) {
        User user = userDAO.findByGmail(gmail);
        if (user == null || !PasswordUtil.verifyPassword(password, user.getPassword())) {
            return null;
        }
        return new Session(user.getUserId(), user.getGmail());
    }

    private static void printResult(String testName, boolean passed) {
        System.out.println(testName + ": " + (passed ? "PASS" : "FAIL"));
        if (!passed) {
            System.exit(1);
        }
    }
}
