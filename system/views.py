from datetime import datetime
import os

import cv2
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
import base64
# from SEResNet50_call_function import call_seresnet50
from . import Fundus_grading, division, ratio
from .models import *

st_id = 80


# Create your views here.

@csrf_exempt  # 取消csrf验证
def login(request):
    print(request.method, type(request.method))
    if request.method == "GET":
        return render(request, "login/Login.html")
    else:
        u = request.POST.get('userName')
        p = request.POST.get('password')
        print(u)
        print(p)
        if u and p:
            user = Patient.objects.filter(pat_id=u, pat_password=p).count()
            username = Patient.objects.filter(pat_id=u, pat_password=p)
            if user >= 1:
                request.session["pat_username"] = u
                print(u)
                return HttpResponseRedirect("index")
            else:
                messages.error(request, '用户名或密码不正确')
                return render(request, "login/Login.html")
        else:
            messages.error(request, '请输入用户名和密码')
            return render(request, "login/Login.html")

@csrf_exempt  # 取消csrf验证
def register(request):
    print(request.method, type(request.method))
    if request.method == "GET":
        return render(request, "login/Register.html")
    else:
        u = request.POST.get('userName')
        p = request.POST.get('password')
        sex=request.POST.get('sex')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        new_pat = Patient(
            pat_id=u,
            pat_password=p,
            pat_sex=sex,
            pat_age=age,
            pat_phone=phone
        )
        new_pat.save()
        messages.error(request, '注册成功')
        return render(request, "login/Login.html")

def welcome(req):
    return render(req, 'index.html')


# user
def index(request):
    if request.method == 'GET':
        pat_id = request.session.get("pat_username")
        print(pat_id)
        imgs = IMG.objects.filter(pat_id_id=pat_id)
        context = {}
        context['imgs'] = imgs
        return render(request, 'user/index.html', context)


def searchreport(request):
    id = request.POST.get("id")
    pat_id = request.session.get("pat_username")
    pat = Patient.objects.filter(pat_id=pat_id)
    imgs = IMG.objects.filter(id=id)
    context = {}
    context['imgs'] = imgs
    context['pats'] = pat
    return render(request, 'user/searchReport.html', context)


def report(request):
    id = st_id
    pat_id = request.session.get("pat_username")
    pat = Patient.objects.filter(pat_id=pat_id)
    imgs = IMG.objects.filter(id=id)
    context = {}
    context['imgs'] = imgs
    context['pats'] = pat
    return render(request, 'user/searchReport.html', context)


@csrf_exempt  # 取消csrf验证
def decode1(request):
    if request.method == 'GET':
        id = st_id
        pat_id = IMG.objects.get(id=id).pat_id
        imgs = IMG.objects.filter(id=id)
        pat = Patient.objects.filter(pat_id=pat_id)
        context = {}
        context['imgs'] = imgs
        context['pats'] = pat
        return render(request, 'doctor/Decode.html', context)
    else:
        id = st_id
        advice = request.POST.get("advice")
        about = request.POST.get("about")
        img = IMG.objects.get(id=id)
        img.advice = about
        img.propose = advice
        img.state = "已诊断"
        img.save()
        return render(request, 'doctor/index1.html')


@csrf_exempt  # 取消csrf验证
def decode(request):
    if request.method == 'GET':
        id = request.GET.get("id")
        pat_id = IMG.objects.get(id=id).pat_id
        imgs = IMG.objects.filter(id=id)
        pat = Patient.objects.filter(pat_id=pat_id)
        context = {}
        context['imgs'] = imgs
        context['pats'] = pat
        return render(request, 'doctor/Decode.html', context)
    else:
        id = request.POST.get("id")
        advice = request.POST.get("advice")
        about = request.POST.get("about")
        img = IMG.objects.get(id=id)
        img.advice = about
        img.propose = advice
        img.state = "已诊断"
        img.save()
        return render(request, 'doctor/index1.html')


def history(request):
    imgs = IMG.objects.filter(state="已诊断")
    context = {}
    context['imgs'] = imgs
    return render(request, 'doctor/History.html', context)

@csrf_exempt
def doc_login(request):
    if request.method=='POST':
        password=request.POST.get("password")
        print(password)
        if password=="12138":
            return HttpResponseRedirect("index1")
        else:
            messages.error(request, '用户名或密码不正确')
            return render(request, "doctor/Login.html")
    else:
        return render(request,"doctor/Login.html")

def index1(request):
    imgs = IMG.objects.filter(state="未诊断")
    context = {}
    context['imgs'] = imgs
    return render(request, 'doctor/index1.html', context)


def report1(request):
    if request.method == 'GET':
        id = request.GET.get("id")
        pat_id = IMG.objects.get(id=id).pat_id
        imgs = IMG.objects.filter(id=id)
        pat = Patient.objects.filter(pat_id=pat_id)
        context = {}
        context['imgs'] = imgs
        context['pats'] = pat
        return render(request, 'doctor/Report1.html', context)


def scaleRadius(img, scale):
    x = img[int(img.shape[0] / 2), :, :].sum(1)  # 图像中间1行的像素的3个通道求和。输出（width*1）
    r = (x > x.mean() / 10).sum() / 2  # x均值/10的像素是为眼球，计算半径
    s = scale * 1.0 / r
    return cv2.resize(img, (0, 0), fx=s, fy=s)


def create(request):
    context = {}
    # request.session['lei'] = 'oc'
    context['path'] = './static/src/eyeai_resize.jpg'
    context['before_path'] = './static/src/肺结节.jpg'
    context['after_path'] = './static/src/V0001.bmp'
    print(context['before_path'])
    try:
        if request.method == 'POST':
            pat_id = request.session.get("pat_username")
            print(pat_id)
            # request.session["type"] = "oc"
            # IMG.objects.filter(pat_id_id=pat_id, img_type='oc').delete()
            new_img = IMG(
                pat_id_id=pat_id,
                img=request.FILES.get('img'),
                name=request.FILES.get('img').name
            )
            name = new_img.name
            name = name.replace(' ', '_')
            context['before_path'] = './media/img/' + name
            path = context['before_path']
            after_path = context['before_path'][:-4] + '_resize.jpg'
            if os.path.exists(path):
                os.remove(path)
            if os.path.exists(after_path):
                os.remove(after_path)
            new_img.after_img = after_path
            new_img.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_img.save()

            temp_img = cv2.imread(path)
            dim = (256, 256)
            resize_img = cv2.resize(temp_img, dim)
            cv2.imwrite(after_path, resize_img)

            context['before_path'] = after_path
            context['after_path'], context['time'] = division.division(path)

            context['ratio'] = ratio.cd_ratio(context['after_path'])
            new_img.oc = context['ratio']
            rat = float(context['ratio'])
            if rat <= 0.4:
                context['oc_identify'] = "有青光眼"
            else:
                context['oc_identify'] = "无青光眼"
            new_img.oc_rate = context['oc_identify']
            scale = 300
            temp_img = cv2.imread(path)
            temp_img = scaleRadius(temp_img, scale)
            # subtract local mean color
            temp_img = cv2.addWeighted(temp_img, 4,
                                       cv2.GaussianBlur(temp_img, (0, 0), scale / 30, sigmaY=16), -4, 128)
            dim = (224, 224)
            resize_img = cv2.resize(temp_img, dim)
            cv2.imwrite(after_path, resize_img)
            context['identify'], context['time'], context['a0'], context['a1'], context['a2'], context['a3'], context[
                'a4'] = Fundus_grading.main(after_path)
            dr = Dr.objects.get(dr_id=context['identify'])
            context['dr_identify'] = dr.dr_name
            context['advice'] = dr.advice
            advice = dr.describe
            new_img.dr_rate = context['dr_identify']

            if rat >= 0.6:
                advice = advice + ";杯盘比较大，如果视野正常的话是暂时可以排除青光眼的诊断，可以坚持每三个月到半年检查一次。避免向青光眼发展，若出现眼涩，眼痛等异常症状，请尽快就医。"
            elif 0.4 < rat < 0.6:
                advice = advice + ";尚处于正常范围内，但杯盘比偏大，请平时注意呵护眼睛，健康用眼。"
            elif 0.2 < rat <= 0.4:
                advice = advice + ";杯盘比正常，请继续保持，健康用眼，从你我做起。"
            elif rat <= 0.2:
                advice = advice + ";分割错误请重试。"

            context['des'] = advice
            new_img.advice = advice
            new_img.propose = context['advice']
            new_img.img = './media/img/' + name
            new_img.after_img = context['after_path']
            new_img.save()

            return render(request, 'user/Create.html', context)

    except AttributeError:
        pass
    else:
        pass
    return render(request, 'user/Create.html', context)
