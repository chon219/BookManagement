# -*- coding: utf-8 -*-
# Chon<chon219@gmail.com>

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from models import Book, Log
from forms import BookAddForm, LoginForm

def user_login(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if "next" in request.REQUEST:
                    return HttpResponseRedirect(request.REQUEST["next"])
                else:
                    return HttpResponseRedirect("/")
            else:
                form.errors['password'] = u"帐号验证失败！"
                context = RequestContext(request, {
                    'form': form })
                return render_to_response("login.html", context)
        else:
            context = RequestContext(request, {
                'form': form })
            return render_to_response("login.html", context)
    else:
        form = LoginForm()
        context = RequestContext(request, {
            'form': form })
        return render_to_response("login.html", context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def index(request):
    paginator = Paginator(Book.objects.all().order_by("-id"), 10)
    page = request.REQUEST.get("page", 1)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    context = RequestContext(request, {
        "books": books,
        "page": page})
    return render_to_response("index.html", context)

@login_required
def add(request):
    if request.method == "POST":
        form = BookAddForm(request.POST)
        if form.is_valid():
            book = Book()
            book.title = form.cleaned_data['title']
            book.author = form.cleaned_data['author']
            book.press = form.cleaned_data['press']
            book.year = form.cleaned_data['year']
            book.save()
            messages.success(request, "已保存")
            form = BookAddForm()
        else:
            messages.error(request, "保存失败，请检查所填写的内容！")
    else:
        form = BookAddForm()
    context = RequestContext(request, {
        "form":form,
        })
    return render_to_response("add.html", context)

@login_required
def log(request):
    paginator = Paginator(Log.objects.all().order_by("-id"), 10)
    page = request.REQUEST.get("page", 1)
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        logs = paginator.page(1)
    except EmptyPage:
        logs = paginator.page(paginator.num_pages)
    context = RequestContext(request, {
        "logs": logs,
        "page": page})
    return render_to_response("log.html", context)

@login_required
def book_borrow(request):
    if request.method == "POST":
        id = request.POST.get("id")
        username = request.POST.get("username", "")
        next = request.POST.get("next", "")
        book = Book.objects.get(id=int(id))
        if book.available:
            log = Log()
            log.username = username
            log.book = book
            log.save()
            book.available = False
            book.username = username
            book.save()
            messages.success(request, "借阅成功！")
            return HttpResponseRedirect(next)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

@login_required
def book_return(request):
    if request.method == "POST":
        id = request.POST.get("id")
        next = request.POST.get("next", "")
        log = Log.objects.get(id=int(id))
        log.returned = True
        log.save()
        book = log.book
        book.available = True
        book.username = None
        log.book.save()
        messages.success(request, "还书成功！")
        return HttpResponseRedirect(next)
    else:
        return HttpResponseForbidden()
