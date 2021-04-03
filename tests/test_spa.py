import subprocess
import threading

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from werkzeug.serving import make_server

from api import app
from api.object_manager import ObjectManager3


def test_get_free(browser: webdriver.Remote, react_server):
    app.mgr = ObjectManager3()

    br = browser
    br.get('http://env:3000/')

    get_btn = clickable(br, '#get input[type=submit]')
    free_input = visible(br, '#free input[type=text]')

    get_btn.click()
    assert visible(br, '#get div').text == 'Error: the pool is empty'

    app.mgr.put_object(1)

    free_input.send_keys('1' + Keys.ENTER)
    assert visible(br, '#free div').text == 'Freed object 1'

    get_btn.click()
    assert visible(br, '#get div').text == 'Got object 1'

    get_btn.click()
    assert visible(br, '#get div').text == 'Error: all objects are acquired'

    free_input.send_keys(Keys.ENTER)
    assert visible(br, '#free div').text == 'Freed object 1'

    app.mgr.drop_object(1)

    get_btn.click()
    assert visible(br, '#get div').text == 'Error: the pool is empty'


@pytest.fixture
def react_server(api_server):
    p = subprocess.Popen(['yarn', 'start'], stdout=subprocess.PIPE)
    while True:
        line = p.stdout.readline()
        if b'Compiled successfully' in line:
            break
        if not line:
            raise Exception('yarn did not start')
    yield p
    p.terminate()
    p.wait()


@pytest.fixture
def api_server(restore_manager):
    server = make_server('127.0.0.1', 5000, app.app, threaded=True)
    th = threading.Thread(target=server.serve_forever, daemon=True)
    th.start()
    yield
    server.shutdown()
    th.join()


@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    remote = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        desired_capabilities=webdriver.DesiredCapabilities.CHROME.copy(),
        options=options,
    )
    yield remote
    remote.quit()


def visible(browser, selector):
    return wait_for(
        browser,
        EC.visibility_of_element_located((By.CSS_SELECTOR, selector)),
    )


def clickable(browser, selector):
    return wait_for(
        browser,
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector)),
    )


def wait_for(browser, condition, timeout=10):
    wait = WebDriverWait(browser, timeout)
    return wait.until(condition)
