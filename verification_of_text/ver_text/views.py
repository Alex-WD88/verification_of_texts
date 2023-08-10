from django.shortcuts import render, redirect
from .models import File, ChildFile
import difflib
import chardet
from PyPDF2 import PdfFileReader
from django.http import HttpResponse
from . import models


def upload(request):
    if request.method == 'POST':
        new_file = models.File()
        new_file.document = request.FILES['document']
        new_file.save()
        return redirect('/')
    return render(request, 'ver_text/index.html')


def file(request, id):
    file = models.File.objects.get(id=id)
    child_files = models.ChildFile.objects.filter(parent=file)

    if request.method == 'POST':
        child_files = models.ChildFile()
        child_files.parent = file

        if 'document' in request.FILES:
            child_files.document = request.FILES['document']

        child_files.save()
        return redirect('file', id=file.id)

    return render(request, 'ver_text/file.html', {'file': file, 'child_files': child_files})


def all_file(request):
    files = models.File.objects.all()
    return render(request, 'ver_text/allFiles.html', {'files': files})


def all_child_files(request):
    child_files = models.ChildFile.objects.all()
    return render(request, 'ver_text/allchildfiles.html', {'child_files': child_files})


def compare(request, id):
    file = File.objects.get(id=id)
    child_files = ChildFile.objects.filter(parent=file)

    # Сравнить содержимое File и ChildFile
    diffs = []
    for child_file in child_files:
        diff = compare_files(file.document.path, child_file.document.path)
        diffs.append(diff)

    # Создать словарь diff с правильными значениями для ключей 'equal' и 'replace'
    diff = {
        0: {'equal': 'Совпадение'},
        1: {'replace': 'Замена'}
    }

    return render(request, 'ver_text/compare.html',
                  {'file': file, 'child_files': child_files, 'diffs': diffs, 'diff': diff})


def compare_files(file1_path, file2_path):
    # Определить кодировку файлов
    file1_encoding = detect_encoding(file1_path)
    file2_encoding = detect_encoding(file2_path)

    # Открыть и прочитать оба файла с определенной кодировкой
    with open(file1_path, 'r', encoding=file1_encoding) as file1, open(file2_path, 'r',
                                                                       encoding=file2_encoding) as file2:
        file1_content = file1.readlines()
        file2_content = file2.readlines()

    # Использовать difflib для сравнения содержимого строк-по-строчно
    diff = difflib.Differ()
    diff_result = list(diff.compare(file1_content, file2_content))

    return diff_result


def compare_pdf_files(file1_path, file2_path):
    # Открыть PDF-файлы
    with open(file1_path, 'rb') as file1, open(file2_path, 'rb') as file2:
        pdf1 = PdfFileReader(file1)
        pdf2 = PdfFileReader(file2)

        # Получить количество страниц в каждом PDF-файле
        num_pages_pdf1 = pdf1.getNumPages()
        num_pages_pdf2 = pdf2.getNumPages()

        # Создать список для хранения результатов сравнения
        diff_result = []

        # Сравнивать страницы по одной
        for page_num in range(min(num_pages_pdf1, num_pages_pdf2)):
            page_pdf1 = pdf1.getPage(page_num).extractText()
            page_pdf2 = pdf2.getPage(page_num).extractText()

            # Использовать difflib для сравнения содержимого страниц
            diff = difflib.Differ()
            page_diff_result = list(diff.compare(page_pdf1.splitlines(), page_pdf2.splitlines()))

            # Добавить результат сравнения страницы в общий список результатов
            diff_result.extend(page_diff_result)

    return diff_result


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        byte_data = file.read()

    encoding = chardet.detect(byte_data)['encoding']
    if encoding is None:  # Если chardet не удалось определить кодировку
        encoding = 'utf-8'  # Используйте кодировку utf-8 по умолчанию

    return encoding
