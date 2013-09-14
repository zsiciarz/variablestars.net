# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated():
        return redirect(request.user)
    return render(request, "index.html", {})
