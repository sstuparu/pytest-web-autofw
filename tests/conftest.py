import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

driver = None


def pytest_addoption(parser):
    """
    PyTest's method used to add options to the parser
    (e.g.: browser to be used).
    """
    parser.addoption("--browser_name", action="store", default="chrome")


@pytest.fixture(scope="class")
def setup(request):  # request is an instance of the fixture
    global driver
    browser_name = request.config.getoption("browser_name")

    if browser_name == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--disable-search-engine-choice-screen")
        # chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("headless")
        # chrome_options.add_argument("--ignore-certificate-errors")

        driver = webdriver.Chrome(options=chrome_options)
    elif browser_name == "firefox":
        firefox_options = FirefoxOptions()

        driver = webdriver.Firefox(options=firefox_options)

    driver.implicitly_wait(5)
    driver.get("https://rahulshettyacademy.com/angularpractice")
    driver.maximize_window()

    request.cls.driver = driver
    yield
    driver.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Method used to extend the PyTest Plugin to take
    and embed a screenshot in html report, whenever a test fails.
    """
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = (
                        '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" '
                        'onclick="window.open(this.src)" align="right"/></div>' % file_name
                )
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
    """
    Method used to capture page screenshots.
    """
    driver.get_screenshot_as_file(name)
