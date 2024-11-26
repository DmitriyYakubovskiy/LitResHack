# coding=windows-1251
import requests
import json
import os
from PIL import Image
from PyPDF2 import PdfMerger
from datetime import datetime, timedelta

def jpgs_to_pdf(folder_path, output_pdf):
    # Список для хранения имен файлов
    jpg_files = [f for f in os.listdir(folder_path) if (f.endswith('.jpg')or f.endswith('.gif'))]
    jpg_files.sort(key=lambda x: int(x.replace('output', '').replace('.jpg', '').replace('.gif', '')))  # Сортировка по номеру страницы
    print(jpg_files)


    # Создание временной директории для сохранения отдельных PDF
    temp_pdf_folder = 'temp_pdfs'
    os.makedirs(temp_pdf_folder, exist_ok=True)

    # Конвертация каждого JPG в PDF и сохранение во временной папке
    i=0
    for jpg_file in jpg_files:
        img_path = os.path.join(folder_path, jpg_file)
        img = Image.open(img_path)
        pdf_path = os.path.join(temp_pdf_folder, f"{jpg_file}.pdf")
        img.convert('RGB').save(pdf_path)
        print(f"page {str(i)} converted")
        i+=1

    # Объединение всех временных PDF в один
    pdf_files=os.listdir(temp_pdf_folder)
    pdf_files.sort(key=lambda x: int(x.replace('output', '').replace('.jpg.pdf', '').replace('.gif.pdf', '')))
    print(pdf_files)
    merger = PdfMerger()
    for pdf_file in pdf_files:
        merger.append(os.path.join(temp_pdf_folder, pdf_file))

    merger.write(output_pdf)
    merger.close()

    # Удаление временной папки
    for pdf_file in os.listdir(temp_pdf_folder):
        os.remove(os.path.join(temp_pdf_folder, pdf_file))
    os.rmdir(temp_pdf_folder)

s = requests.Session()
files=os.listdir("book")
for file in os.listdir("book"):
    os.remove(os.path.join("book", file))

book_url=input("Номер книги в литресе--")
bookname=input("Название книги--")
pages=int(input("Количество страниц--"))
w=input("w--")
print("https://www.litres.ru/pages/get_pdf_page/?file="+book_url+"&page=" + "1" + "&rt=w2500&ft=gif")

# Login URL and headers
login_url = "https://api.litres.ru/foundation/api/auth/login"
login_headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Origin": "https://www.litres.ru",
    "Referer": "https://www.litres.ru/",
    "App-Id": "115",  # Ensure this header is necessary
    "Ui-Language-Code": "ru",  # Ensure this is required
    "Ui-Currency": "RUB"  # Ensure this is required
}

# Replace with your login details
login_data = {
    "login": "student_kb@inbox.ru",
    "password": "199/575"
}

# Send the login request

login_response = s.post(login_url, headers=login_headers, json=login_data)

sid = json.loads(login_response.content)["payload"]["data"]["sid"]

print(f"SID--{sid}")


for i in range(pages):
    # Check if login was successful by inspecting the response
    if login_response.status_code == 200:
        # PDF URL and headers for the GIF request

        gif_url = f"https://www.litres.ru/pages/get_pdf_page/?file={book_url}&page={str(i)}&rt=w{w}&ft=gif"
        gif_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Referer": "https://www.litres.ru/book/dem-mihaylov/krepost-nadezhdy-28957174/",
            "Upgrade-Insecure-Requests": "1",
            "session-id": sid,
            "Cookie": f"SID={sid}"
        }
        gif_response = s.get(gif_url, headers=gif_headers)
        print(gif_url)
        print(gif_response.status_code)
        if gif_response.status_code == 200:
            with open("book/output" + str(i) + ".gif", "wb") as f:
                f.write(gif_response.content)
            print(str(gif_response.status_code)+" "+str(i) + " page saved gif")
        else:
            gif_url = f"https://www.litres.ru/pages/get_pdf_page/?file={book_url}&page={str(i)}&rt=w{w}&ft=jpg"
            gif_headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                "Referer": "https://www.litres.ru/book/dem-mihaylov/krepost-nadezhdy-28957174/",
                "Upgrade-Insecure-Requests": "1",
                "session-id": sid,
                "Cookie": f"SID={sid}"
            }
            gif_response = s.get(gif_url, headers=gif_headers)
            if gif_response.status_code == 200:
                with open("book/output" + str(i) + ".jpg", "wb") as f:
                    f.write(gif_response.content)
                print(str(gif_response.status_code) + " " + str(i) + " page saved jpg")



folder_with_jpgs = 'book'  # Замените на путь к вашей папке с JPG

output_pdf_file = bookname+'.pdf'  # Имя выходного PDF файла
jpgs_to_pdf(folder_with_jpgs, output_pdf_file)

