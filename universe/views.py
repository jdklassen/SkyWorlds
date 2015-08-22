
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings


INDEX_TEMPLATE = 'universe/index.html'


@login_required
def index(request):
    return render(request, INDEX_TEMPLATE)

