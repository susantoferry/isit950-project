import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import LiveServerTestCase


class TestCaseLogin(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_page_login(self):

        from django.core.management import call_command
        from multiprocessing import Process
        from time import sleep
        
        def start_server():
            call_command('runserver')

        server_process = Process(target=start_server)
        server_process.start()

        browser = self.browser
        browser.get('http://127.0.0.1:8000/tasks')

        #elements
        test_email = browser.find_element(By.NAME, "email")
        test_password = self.browser.find_element(By.NAME, "password")
        submit = self.browser.find_element(By.NAME, "submit")

        assert "ISIT950 Group Project" in self.browser.title
        # test_email.send_keys('ferry@gmail.com')
        # test_password.send_keys('password')

        # submit.send_keys(Keys.RETURN)
        # self.assertEqual(self.browser.status_code, 200)

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.google.com")
        self.assertIn("Google", driver.title)
        elem = driver.find_element(By.id, "APjFqb")
        elem.send_keys("selenium tutorial")
        elem.send_keys(Keys.RETURN)
        elem = driver.find_element(By.id, "name")

        self.assertNotIn("No results found.", driver.page_source)


    # def tearDown(self):
    #     self.driver.close()

if __name__ == "__main__":
    unittest.main()