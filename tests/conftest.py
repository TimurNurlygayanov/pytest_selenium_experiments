import pytest
import uuid
import allure
from pyvirtualdisplay import Display


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(10)
    selenium.maximize_window()
    return selenium


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.binary_location = '/usr/bin/google-chrome-stable'
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--log-level=DEBUG')

    return chrome_options


@pytest.fixture
def driver_args():
    # Arguments for PhantomJS:
    return ['--web-security=no', '--ssl-protocol=any',
            '--ignore-ssl-errors=yes', '--webdriver-logfile=phantomjs.log']


@pytest.fixture(scope="session")
def display(request):
    display = Display(visible=False, size=(1500, 1100))
    display.start()

    yield display

    display.stop()


@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.binary = '/usr/bin/firefox'
    firefox_options.add_argument('-headless')
    firefox_options.set_preference('dom.disable_beforeunload', True)
    firefox_options.set_preference('browser.tabs.warnOnClose', False)

    return firefox_options


@pytest.fixture(scope="function")
def web_browser(request, selenium):
    # Example how to properly configure PhantomJS
    # without using of pytest-selenium plugin:
    # b = webdriver.PhantomJS(executable_path='/tests/phantomjs',
    #                         desired_capabilities=dict(webdriver.DesiredCapabilities.PHANTOMJS),
    #                         service_args=['--web-security=no', '--ssl-protocol=any',
    #                                       '--ignore-ssl-errors=yes'],
    #                         service_log_path = '/tmp/phantomjs.log')

    b = selenium

    b.set_window_size(1400, 1000)

    # Return browser instance to test case:
    yield b

    # Do teardown (this code will be executed after each test):

    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            b.execute_script("document.body.bgColor = 'white';")

            allure.attach(b.get_screenshot_as_png(),
                          name=request.function.__name__,
                          attachment_type=allure.attachment_type.PNG)

            # Make screen-shot for local debug:
            b.save_screenshot(str(uuid.uuid4()) + '.png')

            print("URL: ", b.current_url)
        except:
            pass # just ignore

    try:
        # Close browser window:
        b.quit()
    except:
        pass  # just ignore any errors if we can't close the browser.

