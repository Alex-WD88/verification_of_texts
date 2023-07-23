from django.shortcuts import render, redirect
from .models import File
import difflib
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
    file = models.File.objects.filter(id=id)
    if request.method == 'POST':
        child_file = models.Child_file()
        child_file.parent_id = id
        child_file.document = request.FILES['document']
        child_file.save()
        return redirect('/')

    return render(request, 'ver_text/file.html', {'file': file[0]})


def all_file(request):
    files = models.File.objects.all()
    return render(request, 'ver_text/allFiles.html', {'files': files})


def all_child_files(request):
    child_files = models.Child_file.objects.all()
    return render(request, 'ver_text/allchildfiles.html', {'child_files': child_files})


# def compare(request, id):
#     file1 = File.objects.get(id=id)
#     if request.method == 'POST':
#         file2 = request.FILES['document']
#         differences = compare_files(file1.document.path, file2.path)
#         return render(request, 'ver_text/compare.html', {'differences': differences})
#     return render(request, 'ver_text/compare.html')
#
#
# def compare_files(file1, file2):
#     with open(file1, 'r') as f1, open(file2, 'r') as f2:
#         lines1 = f1.readlines()
#         lines2 = f2.readlines()
#     differ = difflib.HtmlDiff()
#     diff_html = differ.make_table(lines1, lines2)
#     return diff_html
