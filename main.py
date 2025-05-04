from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Настройка браузера
browser = webdriver.Firefox()

def open_wikipedia_article(query):
    url = f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}"
    browser.get(url)
    time.sleep(2)  # Ждём загрузки страницы

def list_paragraphs():
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    index = 0
    for paragraph in paragraphs:
        text = paragraph.text.strip()
        if text:
            print(f"\n--- Параграф {index + 1} ---")
            print(text)
            input("Нажмите Enter для следующего параграфа...")
            index += 1
    if index == 0:
        print("Нет доступных параграфов для отображения.")

def get_internal_links():
    links = browser.find_elements(By.CSS_SELECTOR, "div#bodyContent a")
    internal_links = []
    for link in links:
        href = link.get_attribute("href")
        text = link.text.strip()
        if (
            href and text
            and "/wiki/" in href
            and not href.startswith("https://ru.wikipedia.org/wiki/Служебная:")
            and not ":" in href.split("/wiki/")[-1]  # Исключить технические страницы
        ):
            internal_links.append((text, href))
    return list(dict.fromkeys(internal_links))[:10]  # Удаление дубликатов, максимум 10

def choose_internal_link(links):
    print("\n--- Связанные статьи ---")
    for i, (text, href) in enumerate(links):
        print(f"{i + 1}. {text}")
    choice = input("Введите номер статьи для перехода или Enter для отмены: ")
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(links):
            browser.get(links[index][1])
            time.sleep(2)
            return True
    print("Некорректный выбор. Возврат к меню.")
    return False

try:
    while True:
        query = input("Введите запрос для Википедии (или 'выход' для завершения): ")
        if query.lower() == "выход":
            break

        open_wikipedia_article(query)

        while True:
            print("\nВыберите действие:")
            print("1. Читать параграфы статьи")
            print("2. Перейти на связанную статью")
            print("3. Ввести новый запрос")
            print("4. Выйти из программы")
            action = input("Ваш выбор: ")

            if action == "1":
                list_paragraphs()
            elif action == "2":
                links = get_internal_links()
                if links:
                    choose_internal_link(links)
                else:
                    print("Связанных статей не найдено.")
            elif action == "3":
                break
            elif action == "4":
                exit()
            else:
                print("Неверный ввод. Попробуйте снова.")

finally:
    print("Программа завершена.")
    browser.quit()

