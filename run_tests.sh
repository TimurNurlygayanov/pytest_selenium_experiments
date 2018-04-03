pytest -m functional -n 10 --alluredir=allure-results --driver Firefox --driver-path /tests/firefox

pytest -m functional -n 20 --alluredir=allure-results --driver Chrome --driver-path /tests/chrome

