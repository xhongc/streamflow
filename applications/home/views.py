import random

import redis
from django.conf import settings
from django.shortcuts import render
from rest_framework.response import Response

from applications.flow.models import ProcessRun
from component.drf.viewsets import GenericViewSet

import datetime
import time
from django.http import StreamingHttpResponse
from django.core.cache import cache


def stream(request):
    def event_stream():
        while True:
            pool = redis.ConnectionPool(host=settings.REDIS_HOST, password="", port=6379, db=0)
            r = redis.Redis(connection_pool=pool)
            res = r.get("localhost_monitor")
            if res:
                res = res.decode().replace("\n", "")
            yield f'data:{res}\n\n'
            time.sleep(5)

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


class OverviewSet(GenericViewSet):
    def list(self, request, *args, **kwargs):
        ProcessRun.objects.filter()
        return Response({
            "today_wait_job_num": 1,
            "today_job_num": 2,
            "today_job_flow_num": 3,
            "today_error_job_num": 4,
            "jobDynamicState": []
        })


class WeeklyJobViewSet(GenericViewSet):
    def list(self, request, *args, **kwargs):
        return Response({
            "weekly_time": ["2020-01-01", "2020-01-02", "2020-01-03"],
            "weekly_job_num": [1, 2, 3],
            "weekly_error_job_num": [3, 2, 1]
        })


class TopAgentViewSet(GenericViewSet):
    def list(self, request, *args, **kwargs):
        return Response({
            "cpu": "22",
            "disk": "33",
            "mem": "33",
        })


class TodayJobViewSet(GenericViewSet):
    def list(self, request, *args, **kwargs):
        return Response({
            "finished_job_num": [1, 2, 3],
            "error_job_num": [1, 0, 1],
            "unfinished_job_num": [0, 2, 1],
            "time_line": ["2020-01-01", "2020-01-02", "2020-01-03"],
        })


class JobDynamicViewSet(GenericViewSet):
    def list(self, request, *args, **kwargs):
        return Response([{
            "condition": "作业任务1",
            "finish_time": "2020-01-01"
        },
            {
                "condition": "作业任务2",
                "finish_time": "2020-01-02"
            },
            {
                "condition": "作业任务3",
                "finish_time": "2020-01-03"
            },
            {
                "condition": "作业任务4",
                "finish_time": "2020-01-04"
            }
        ])
