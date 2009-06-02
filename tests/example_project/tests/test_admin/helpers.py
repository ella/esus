from djangosanetesting import SeleniumTestCase
from django.utils.translation import ugettext_lazy as _

class AdminTestCase(SeleniumTestCase):
    fixtures = ['admin_user']

    SUPERUSER_USERNAME = u"superuser"
    SUPERUSER_PASSWORD = u"xxx"

    ADMIN_URI = "/admin/"

    def __init__(self):
        super(AdminTestCase, self).__init__()
        self.elements = {
            'navigation' : {
                'logout' : '//a[@href="%slogout/"]' % self.ADMIN_URI,
                'home' : '//div[@class="breadcrumbs"]/a[position()=1]',
            },
            'listing' : {
                'save' : '//input[@name="_save"]',
                'delete' : '//a[@class="deletelink"]',
                'delete_confirm' : '//div[@id="content"]//form/div/input[@type="submit"]',
                'list_first' : '//div[@id="changelist"]/form/table/tbody/tr[@class="row1"]/th/a',
            },
            'pages' : {
                'login' : {
                    'submit' : "//input[@type='submit']"
                },
                'welcome' : {
                    'category_add' : '//a[@href="phorum/category/add/"]',
                    'category_list' : '//a[@href="phorum/category/"]',
                },
                'hall' : {

                },
            }
        }

    def setUp(self):
        super(AdminTestCase, self).setUp()
        self.selenium.window_maximize()
        self.login_superuser()

    def login_superuser(self):
        self.selenium.open(self.ADMIN_URI)
        self.selenium.type("id_username", self.SUPERUSER_USERNAME)
        self.selenium.type("id_password", self.SUPERUSER_PASSWORD)
        self.selenium.click(self.elements['pages']['login']['submit'])

    def logout(self):
        self.selenium.click(self.elements['navigation']['logout'])
        self.selenium.is_text_present(unicode(_(u"Thanks for spending some quality time with the Web site today.")))

    def tearDown(self):
        super(AdminTestCase, self).tearDown()
        self.logout()
