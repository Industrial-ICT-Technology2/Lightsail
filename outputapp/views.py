from datetime import datetime
import os
from enum import auto
from django.http import HttpResponse
from datetime import date
import pandas as pd
import openpyxl
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect
import csv

from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from openpyxl.styles import PatternFill, Alignment

from mainapp.models import Category, Review, SecondLabeledData, FirstLabeledData


def output(request):
    try:

        # category_product 변수를 get 방식 으로 받으면 세션에 저장
        if request.method == "GET":
            if 'category_product' in request.GET:
                request.session['category_product'] = request.GET['category_product']
                print(request.session['category_product'])
                request.session.set_expiry(300)

                category_product = request.session['category_product']
                category_detail = Category.objects.filter(category_product=category_product)
                alltotal = Review.objects.filter(category_product=category_product).count()
                first_num = Review.objects.filter(category_product=category_product).filter(first_status=True).count()
                second_num = Review.objects.filter(category_product=category_product).filter(second_status=True).count()
                dummy_num = Review.objects.filter(category_product=category_product).filter(dummy_status=True).count()

                context = {'category_detail': category_detail}
                context['alltotal'] = alltotal
                context['first_num'] = first_num
                context['dummy_num'] = dummy_num
                context['second_num'] = second_num
                return render(request, 'outputapp/output.html', context)

            else:
                context = {'message': '제품을 다시 선택해주세요.'}
                return render(request, 'outputapp/output.html', context)

        elif request.method == "POST" and 'export' in request.POST:
            if 'export' in '.xlsx export':
                resultdata = FirstLabeledData.objects.filter(category_id__category_product=request.session['category_product'])
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=' + datetime.now().strftime(
                    "%Y-%m-%d_%I-%M-%S_%p") + '.csv'
                response.write(u'\ufeff'.encode('utf8'))

                writer = csv.writer(response)
                writer.writerow(
                    ['category_id_id', 'first_labeled_emotion', 'first_labeled_target', 'first_labeled_expression'])
                results = resultdata.values_list('category_id__category_middle', 'first_labeled_emotion',
                                                 'first_labeled_target', 'first_labeled_expression')
                for rlt in results:
                    writer.writerow(rlt)
                return response

            elif 'export' in '.data analysis':
                print("분석입니다.")

            else:
                print("에러입니다.")

        else:
            print("에러")


    except Exception as identifier:
        print(identifier)
    return render(request, 'outputapp/output.html')
