import subprocess
import threading

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from werkzeug.serving import make_server

from api.app import app


def test_put_get_free_drop(browser: webdriver.Remote, react_server):
    br = browser
    br.get('http://env:3000/')

    put_input = visible(br, '#put input[type=text]')
    get_btn = clickable(br, '#get input[type=submit]')
    free_input = visible(br, '#free input[type=text]')
    drop_input = visible(br, '#drop input[type=text]')

    get_btn.click()
    assert visible(br, '#get div').text == 'Error: the pool is empty'

    drop_input.send_keys('1' + Keys.ENTER)
    assert visible(br, '#drop div').text == "There's no object 1 in the pool"

    put_input.send_keys('1' + Keys.ENTER)
    assert visible(br, '#put div').text == 'Put 1 into the pool'
    put_input.send_keys(Keys.ENTER)
    assert visible(br, '#put div').text == 'Object 1 is already in the pool'

    free_input.send_keys('1' + Keys.ENTER)
    assert visible(br, '#free div').text == 'Freed object 1'

    get_btn.click()
    assert visible(br, '#get div').text == 'Got object 1'

    get_btn.click()
    assert visible(br, '#get div').text == 'Error: all objects are acquired'

    drop_input.send_keys(Keys.ENTER)
    assert visible(br, '#drop div').text == 'Error: cannot drop an acquired object'

    free_input.send_keys(Keys.ENTER)
    assert visible(br, '#free div').text == 'Freed object 1'

    drop_input.send_keys(Keys.ENTER)
    assert visible(br, '#drop div').text == 'Removed object 1 from the pool'

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
def api_server():
    server = make_server('127.0.0.1', 5000, app, threaded=True)
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
        command_executor=f'http://selenium:4444/wd/hub',
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
