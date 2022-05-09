import json

from django.http import HttpResponse
from django.shortcuts import render
from fuzzywuzzy import fuzz

from .models import Questions, Keywords


def bot(request):
    if request.method == "POST":
        lists = list()
        user_text = request.POST.get('message')
        questions = Questions.objects.all()
        keywords = Keywords.objects.all()

        for i in questions:
            fuzzy_response = fuzz.ratio(user_text, i.question_text)
            print(user_text)
            if fuzzy_response >= 70:
                return HttpResponse(json.dumps({'is_data': i.chevy_words}), content_type='application/json')
        
        for i in keywords:
            text_fuzz = fuzz.token_sort_ratio(user_text, i.keyword)
            if text_fuzz >= 33:
                if fuzz.WRatio(i.keyword, user_text):
                    lists.append(i.keyword)
        
        return HttpResponse(json.dumps({"not_data": lists}), content_type='application/json')