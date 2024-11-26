import os
from PIL import Image
from PyPDF2 import PdfMerger

def jpgs_to_pdf(folder_path, output_pdf):
    # ������ ��� �������� ���� ������
    jpg_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    jpg_files.sort(key=lambda x: int(x.replace('output', '').replace('.jpg', '')))  # ���������� �� ������ ��������
    print(jpg_files)


    # �������� ��������� ���������� ��� ���������� ��������� PDF
    temp_pdf_folder = 'temp_pdfs'
    os.makedirs(temp_pdf_folder, exist_ok=True)

    # ����������� ������� JPG � PDF � ���������� �� ��������� �����
    for jpg_file in jpg_files:
        img_path = os.path.join(folder_path, jpg_file)
        img = Image.open(img_path)
        pdf_path = os.path.join(temp_pdf_folder, f"{jpg_file}.pdf")
        img.convert('RGB').save(pdf_path)

    # ����������� ���� ��������� PDF � ����
    pdf_files=os.listdir(temp_pdf_folder)
    pdf_files.sort(key=lambda x: int(x.replace('output', '').replace('.jpg.pdf', '')))
    print(pdf_files)
    merger = PdfMerger()
    for pdf_file in pdf_files:
        merger.append(os.path.join(temp_pdf_folder, pdf_file))

    merger.write(output_pdf)
    merger.close()

    # �������� ��������� �����
    for pdf_file in os.listdir(temp_pdf_folder):
        os.remove(os.path.join(temp_pdf_folder, pdf_file))
    os.rmdir(temp_pdf_folder)

# ������ �������������
folder_with_jpgs = 'book'  # �������� �� ���� � ����� ����� � JPG
output_pdf_file = 'result.pdf'  # ��� ��������� PDF �����
jpgs_to_pdf(folder_with_jpgs, output_pdf_file)