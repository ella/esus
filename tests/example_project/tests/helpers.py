from djangosanetesting import SeleniumTestCase

class EsusTestCase(SeleniumTestCase):
    fixtures = ['test_users']

    SUPERUSER_USERNAME = u"superuser"
    SUPERUSER_PASSWORD = u"xxx"

    USER_USERNAME = u"Tester"
    USER_PASSWORD = u"xxx"

    TEST_PROJECT_URI = "/"

    def __init__(self):
        super(EsusTestCase, self).__init__()
        self.elements = {
            'navigation' : {
                'login' : 'link-login',
                'logout' : 'link-logout',
                'categories' : 'link-categories',
                'submit_form' : 'form-submit',
            },
            'pages' : {
                'login' : {
                    'submit' : "//input[@type='submit']"
                },
                'welcome' : {
                    'category_add' : '//a[@href="phorum/category/add/"]',
                    'category_list' : '//a[@href="phorum/category/"]',
                },
                'category' : {
                    "categories_list" : "//div[@id='categories']/ul/li",
                    "table_add" : "//a[@id='link_table_add']",
                    "tables_list" : "//div[@id='tables']/ul/li",
                },
                'profile' : {
                    'username' : "//h1",
                },
                'table' : {
                    'name' : "//h1",
                },
            }
        }

    def setUp(self):
        super(EsusTestCase, self).setUp()
        self.selenium.window_maximize()
        self.login_user()

    def login_user(self):
        self.selenium.open(self.TEST_PROJECT_URI)
        self.selenium.click(self.elements['navigation']['login'])
        self.selenium.wait_for_page_to_load(30000)
        self.selenium.type("id_username", self.USER_USERNAME)
        self.selenium.type("id_password", self.USER_PASSWORD)
        self.selenium.click(self.elements['pages']['login']['submit'])
        self.selenium.wait_for_page_to_load(30000)
        self.assert_equals(self.USER_USERNAME, self.selenium.get_text(self.elements['pages']['profile']['username']))

    def logout(self):
        self.selenium.click(self.elements['navigation']['logout'])

    def tearDown(self):
        super(EsusTestCase, self).tearDown()
        self.logout()
