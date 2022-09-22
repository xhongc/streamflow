from django.shortcuts import render
from rest_framework.response import Response

from component.drf.viewsets import GenericViewSet


class OverviewSet(GenericViewSet):
    def list(self, request, *args, **kwargs):
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
            "top5_agent_name": ["host", "localhost", "remote"],
            "top5_agent_num": [1, 2, 3]
        })


class TodayJobViewSet(GenericViewSet):
    def list(self, request, *args, **kwargs):
        return Response({
            "finished_job_num": [2, 2, 2],
            "error_job_num": [1, 2, 3],
            "unfinished_job_num": [3, 2, 1],
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
