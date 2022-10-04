from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os


url = "https://dodopizza.kz/petropavlovsk"
html_file = "saved_page.html"


def get_page():
    chrome_options = Options()

    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
    chrome_options.add_argument('--disable-gpu')  # applicable to windows os only
    chrome_options.add_argument('start-minimized')  #
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--disable-extensions")
    driver = Chrome(executable_path="chromedriver.exe", options=chrome_options)
    driver.get(url)

    with open(html_file, "w", encoding="utf-8") as w:
        w.write(driver.page_source)

def try_get_page():
    try:
        current_time = time.time()
        get_creation_time = os.stat(html_file).st_mtime

        if current_time - get_creation_time >= 3600:

            return "Идет запрос до сервера", get_page()
        else:
            return "Запрос успешен!"
    except FileExistsError:
        print("File does`nt exist")


def main(product_type, ingredience="С мясом"):
    def read_menu():
        with open(html_file, "r", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")

        drinks = "drinks"

        title = []
        description = []
        drinks_title = []
        drinks_description = []
        avilability_list_food = []
        avilability_list_drinks = []

        for titles in soup.find("section", class_="sc-1n2d0ov-2 bxiXBh",
                                attrs={"id": product_type}).find_all("div", class_="sc-1tpn8pe-1 jbQjVh"):
            title.append(titles.text)
        for desk in soup.find("section", class_="sc-1n2d0ov-2 bxiXBh",
                              attrs={"id": product_type}).find_all("main", class_="sc-1tpn8pe-0 jDJosZ"):
            description.append(desk.text.strip("\n"))

        for drinks_titles in soup.find("section", class_="sc-1n2d0ov-2 bxiXBh",
                                       attrs={"id": drinks}).find_all("div", class_="sc-1tpn8pe-1 jbQjVh"):
            drinks_title.append(drinks_titles.text)
        for drinks_desc in soup.find("section", class_="sc-1n2d0ov-2 bxiXBh",
                                            attrs={"id": drinks}).find_all("main", class_="sc-1tpn8pe-0 jDJosZ"):
            drinks_description.append(drinks_desc.text)

        for avilability_drinks in soup.find("section", class_="sc-1n2d0ov-2 bxiXBh", attrs={"id": drinks}):
            for button in avilability_drinks.find_all("button", class_="sc-1rmt3mq-0 jFZvXc product-control"):
                if button.text == "В корзину":
                    avilability_list_drinks.append("В наличии")
                elif button.text == "Будет позже":
                    avilability_list_drinks.append("Временно отсутствует")

        for avilability in soup.find("section", class_="sc-1n2d0ov-2 bxiXBh", attrs={"id": product_type}):
            for button in avilability.find_all("button", class_="sc-1rmt3mq-0 jFZvXc product-control"):
                if button.text == "Собрать" or button.text == "Выбрать" or button.text == "В корзину":
                    avilability_list_food.append("В наличии")
                elif button.text == "Будет позже":
                    avilability_list_food.append("Временно отсутствует")

        new_list = []
        for desk, avail in zip(description, avilability_list_food):
            new_list.append(f"{desk} @{avail}@\n")

        complite_drinks_list = []
        for titles, avail in zip(drinks_title, avilability_list_drinks):
            complite_drinks_list.append(f"{titles} @{avail}@\n")

        cut_description = []

        n = 0
        while n < len(new_list):
            for item in title:
                cut_description.append(new_list[n][len(item):])
                n += 1

        full_menu = dict(zip(title, cut_description))

        return cut_description, full_menu, complite_drinks_list, avilability_list_food

    def sort_menu():
        full_menu = read_menu()
        meat_menu = []
        vegan_menu = full_menu[0].copy()

        forbiden_words = ["вет", "цып", "инд", "индейки", "чор", "гов", "говядина", "пастр", "кур", "курица", "крыл"]

        for elem in full_menu[0]:
            for n in forbiden_words:
                if n in elem.lower().replace(",", ""):
                    meat_menu.append(elem)
                    break

        for elem in meat_menu:
            if elem in vegan_menu:

                vegan_menu.remove(elem)


        return vegan_menu, meat_menu
    sort_menu()


    def get_key(val):
        full_menu = read_menu()

        for key, value in full_menu[1].items():
            if val == value:
                return key

        return "key doesn't exist"


    def print_request_menu():

        request_menu = sort_menu()
        drinks_title = read_menu()

        result = ""
        if ingredience == "Без мяса":
            for item in request_menu[0]:
                result += f"\n {get_key(item)}-{item}"
            return result
        elif ingredience == "С мясом":
            for item in request_menu[1]:
                result += f"\n {get_key(item)}-{item}"
            return result
        elif ingredience == "Напитки":
            for drinks in drinks_title[2]:
                result += f"{drinks}"
            return result
        elif ingredience == "Десерты":
            for item in request_menu[0]:
                result += f"\n {get_key(item)}-{item}"
            return result
    return print_request_menu()




