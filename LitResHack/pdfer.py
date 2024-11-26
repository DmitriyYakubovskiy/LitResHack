import os
from PIL import Image
from PyPDF2 import PdfMerger

def jpgs_to_pdf(folder_path, output_pdf):
    # Список для хранения имен файлов
    jpg_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    jpg_files.sort(key=lambda x: int(x.replace('output', '').replace('.jpg', '')))  # Сортировка по номеру страницы
    print(jpg_files)


    # Создание временной директории для сохранения отдельных PDF
    temp_pdf_folder = 'temp_pdfs'
    os.makedirs(temp_pdf_folder, exist_ok=True)

    # Конвертация каждого JPG в PDF и сохранение во временной папке
    for jpg_file in jpg_files:
        img_path = os.path.join(folder_path, jpg_file)
        img = Image.open(img_path)
        pdf_path = os.path.join(temp_pdf_folder, f"{jpg_file}.pdf")
        img.convert('RGB').save(pdf_path)

    # Объединение всех временных PDF в один
    pdf_files=os.listdir(temp_pdf_folder)
    pdf_files.sort(key=lambda x: int(x.replace('output', '').replace('.jpg.pdf', '')))
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

# Пример использования
folder_with_jpgs = 'book'  # Замените на путь к вашей папке с JPG
output_pdf_file = 'result.pdf'  # Имя выходного PDF файла
jpgs_to_pdf(folder_with_jpgs, output_pdf_file)