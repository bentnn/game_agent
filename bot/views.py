import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from fuzzywuzzy import fuzz

from .models import Questions, Keywords, SettingsBot, Themes


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
                    print(i)
                    lists.append([i.theme, i.keyword])
        
        return HttpResponse(json.dumps({"not_data": lists}), content_type='application/json')


def link_test_bot(request, ids=None):
    data =list()

    for i in Themes.objects.filter(ids=ids):
        data.append([i.ids, i.theme.title])

    return HttpResponse(json.dumps({"data": data}), content_type='application/json')


def settings_bot(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.pk)

        query = SettingsBot()
        query.user_id=user
        query.level=request.POST.get('level')
        query.save()
        
        # messages.success(request, 'Настройки успешно установленны! ')
        return HttpResponse(json.dumps({"message": 'Success'}), content_type='application/json')


def get_settings_bot(request):
    if request.method == "GET":
        return HttpResponse(json.dumps({
            "data": str(SettingsBot.objects.get(user_id=request.user.pk))
        }), content_type='application/json')


def update_settings_bot(request):
    if request.method == "POST":
        # Update settings
        SettingsBot.objects.filter(user_id=request.user.pk).update(level=request.POST.get('data'))
        # END
        return HttpResponse(json.dumps({"message": "Success"}), content_type='application/json')