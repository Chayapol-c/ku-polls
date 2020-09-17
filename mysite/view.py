from django.shortcuts import redirect

def index(reqest):
    return redirect("polls:index")