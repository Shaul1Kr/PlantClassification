from main import app
from website import auth, db, models
import unittest
from flask import session
from website import db
import time
from unittest import TextTestRunner
from unittest.runner import TextTestResult
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from website.models import User, Photos


class TimeLoggingTestResult(TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_timings = []

    def startTest(self, test):
        self._test_started_at = time.time()
        super().startTest(test)

    def addSuccess(self, test):
        elapsed = time.time() - self._test_started_at
        name = self.getDescription(test)
        self.test_timings.append((name, elapsed))
        super().addSuccess(test)

    def getTestTimings(self):
        return self.test_timings


class TimeLoggingTestRunner(unittest.TextTestRunner):

    def __init__(self, slow_test_threshold=0.01, *args, **kwargs):
        print(slow_test_threshold)
        self.slow_test_threshold = slow_test_threshold
        return super().__init__(
            resultclass=TimeLoggingTestResult,
            *args,
            **kwargs,
        )

    def run(self, test):
        result = super().run(test)
        Success = result.testsRun-len(result.failures)
        mail_content = ''

        mail_content += "\nSuccessed Tests (%d test\s):\n" % Success
        self.stream.writeln(
            "\nSuccessed Tests (%d test\s):" %
            Success)

        for name, elapsed in result.getTestTimings():

            mail_content += "({:.03}s) {}\n".format(elapsed, name)
            self.stream.writeln(
                "({:.03}s) {}".format(
                    elapsed, name))

        mail_content += "\nFailed Tests (%d test\s):\n" % len(result.failures)
        self.stream.writeln(
            "\nFailed Tests (%d test\s):" %
            len(result.failures))

        for name, err in result.failures:
            mail_content += "{}\n".format(name)
            self.stream.writeln(
                "{}".format(
                    name))

        mail_content += "\nSlow Tests (>{:.03}s):\n".format(
            self.slow_test_threshold)
        self.stream.writeln(
            "\nSlow Tests (>{:.03}s):".format(
                self.slow_test_threshold))

        for name, elapsed in result.getTestTimings():
            if elapsed > self.slow_test_threshold:
                mail_content += "({:.03}s) {}\n".format(elapsed, name)
                self.stream.writeln(
                    "({:.03}s) {}".format(
                        elapsed, name))
        return result


class LoginTestCase(unittest.TestCase):
    # Ensure that flask was set up corrently
    def test_Login_response(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    # Ensure that the login page loads correctly

    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertIn(b'Login', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_Login(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(email="shauli@gmail.com", password="12345678"),
            follow_redirects=True
        )
        self.assertIn(b'homepage', response.data)

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(email="wrong", password="wrong"),
            follow_redirects=True
        )
        print(response.data)
        self.assertIn(b'login', response.data)
    # Ensure logout behaves correctly


if __name__ == '__main__':
    test_runner = TimeLoggingTestRunner(slow_test_threshold=0.04)
    unittest.main(testRunner=test_runner)
    # unittest.main()
