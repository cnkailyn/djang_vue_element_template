import json

import arrow

from utils.http import ApiResponse
from loguru import logger
import os
from project.settings import IMG_UPLOAD
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.db.models import Count, Max
from django.contrib.auth.decorators import login_required
from modules.module.models import SystemConfig
from utils.http import ApiResponse


def page_example(request):
    return render(request, "example.html")


@csrf_exempt
@login_required
def api_example(request):
    req_params = json.loads(request.body)
    user_ids = req_params.get("user_ids", "")
    data = serialize("json", SystemConfig.objects.all())
    return ApiResponse.success(data)
