import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#запуск всех тестов
# python3 -m pytest -v --driver Chrome --driver-path /Users/demidenokys/chromedriver-mac-arm64/chromedriver tests/test_selenium_petfriends.py
#запуск конкретного теста
# python3 -m pytest -v --driver Chrome --driver-path /Users/demidenokys/chromedriver-mac-arm64/chromedriver tests/test_selenium_petfriends.py::test_show_all_pets

# 0. Проверка всех питомцев пользователя на наличие фото, имени, вида и возраста
def test_show_all_pets(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('yan32615854@yandex.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('123456')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()

    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

# Ex. 30.3.1, 30.5.1
# 1. Проверка присутствия всех питомцев пользователя (с неявным ожиданием)
def test_presence_for_all_pets(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('yan32615854@yandex.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('123456')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    #Задаем неявное ожидание
    driver.implicitly_wait(5)

    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()

    pets_num = driver.find_element(By.XPATH, '//*[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    pets_card = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    assert int(pets_num) == len(pets_card)

# 2. Проверка того , что хотя бы у половины питомцев есть фото (с явным ожиданием)
def test_half_of_the_pets_with_photos(driver):
    # Задаем переменную для явного ожидания
    wait = WebDriverWait(driver, 5)

    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('yan32615854@yandex.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('123456')

    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Явное ожидание. Ожидаем что кнопка Мои питомцы кликабельна и нажимаем на неё
    My_pets = driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a')
    wait.until(EC.element_to_be_clickable(My_pets)).click()

    pets_num = driver.find_element(By.XPATH, '//*[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    images = driver.find_elements(By.XPATH, '//img[starts-with(@src, "data:image")]')
    assert len(images) >= int(pets_num)/2

# 3. Проверка того, что у всех питомцев есть имя, возраст и порода. (с неявным ожиданием)
def test_check_pets_for_name_age_breed(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('yan32615854@yandex.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('123456')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()

    #Задаем неявное ожидание
    driver.implicitly_wait(5)

    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

# 4. Проверка того, что у всех питомцев разные имена. (с явным ожиданием)
def test_different_names_pets(driver):
    # Задаем переменную для явного ожидания
    wait = WebDriverWait(driver, 5)

    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('yan32615854@yandex.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('123456')

    # Явное ожидание. Ожидаем что кнопка Войти кликабельна и нажимаем на неё
    Login_button = driver.find_element(By.XPATH, '//button[text() = "Войти"]')
    wait.until(EC.element_to_be_clickable(Login_button)).click()
    # Явное ожидание. Ожидаем что кнопка Войти не отображается на странице
    wait.until(EC.invisibility_of_element_located(Login_button))

    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')

    name_my_pets = []
    for i in range(len(names)):
        name_my_pets.append(names[i].text)
    assert len(name_my_pets) == len(set(name_my_pets))

# 5. Проверка того, что в списке нет повторяющихся питомцев. (с явным ожиданием)
def test_no_duplicates_pets(driver):
    # Задаем переменную для явного ожидания
    wait = WebDriverWait(driver, 5)

    # Явное ожидание. Ожидаем, что поле Электронная почта кликабельно и заполняем его email
    email = driver.find_element(By.ID, 'email')
    wait.until(EC.element_to_be_clickable(email)).send_keys('yan32615854@yandex.ru')

    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('123456')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()

    pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')

    # Явное ожидание. Ожидаем , что карточки питоицев видны на странице
    for i in range(len(pets)):
        assert wait.until(EC.visibility_of(pets[i]))

    list_pets = []
    for i in range(len(pets)):
        list_data = pets[i].text.split("\n")
        list_pets.append(list_data[0])
    assert len(set(list_pets)) == len(pets)




