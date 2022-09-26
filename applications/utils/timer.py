from datetime import datetime

from dateutil.relativedelta import relativedelta


def now_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_datetime_range(period, period_count=1):
    """
    返回现在到之前的时间区间
    params: kwargs
    type: dict
    usage: get_datetime_range("days",1)
    return: (datetime.datetime(2020, 11, 19, 17, 39, 56, 817884), datetime.datetime(2020, 11, 20, 17, 39, 56, 817884))
    """
    format_map = {
        "hours": "%Y-%m-%d %H:%M:00",
        "days": "%Y-%m-%d %H:00:00",
        "months": "%Y-%m-%d 00:00:00",
        "years": "%Y-%m-01 00:00:00",
    }
    now = datetime.now()
    ago = now - relativedelta(**{period: period_count})
    return string_to_datetime(datetime_to_string(ago, format_map[period])), now


def get_datetime_range_string(period, period_count=1):
    """
    返回现在到之前的时间区间
    params: kwargs
    type: dict
    usage: get_datetime_range("days",1)
    return: (datetime.datetime(2020, 11, 19, 17, 39, 56, 817884), datetime.datetime(2020, 11, 20, 17, 39, 56, 817884))
    """
    format_map = {
        "hours": "%Y-%m-%d %H:%M:00",
        "days": "%Y-%m-%d %H:00:00",
        "months": "%Y-%m-%d 00:00:00",
        "years": "%Y-%m-01 00:00:00",
    }
    now = datetime.now()
    ago = now - relativedelta(**{period: period_count})
    return datetime_to_string(ago, format_map[period]), datetime_to_string(now)


def datetime_to_string(dt, formatter="%Y-%m-%d %H:%M:%S"):
    try:
        return dt.strftime(formatter)
    except Exception:
        return ""


def string_to_datetime(datetime_str, formatter="%Y-%m-%d %H:%M:%S"):
    return datetime.strptime(datetime_str, formatter)


def get_datetime_range_list(start, end, period):
    """
    返回间隔时间内每小时的时间列表
    period: minutes
    """
    if isinstance(start, str):
        start = string_to_datetime(start)
    if isinstance(end, str):
        end = string_to_datetime(end)
    datetime_list = []
    format_map = {
        "minutes": "%Y-%m-%d %H:%M:00",
        "hours": "%Y-%m-%d %H:00:00",
        "days": "%Y-%m-%d 00:00:00",
        "months": "%Y-%m-01 00:00:00",
    }
    offset = 1
    if period == "minutes":
        offset = 5
        start = datetime.strptime(
            "{}-{}-{} {}:{}:00".format(start.year, start.month, start.day, start.hour, (start.minute // 5) * 5),
            "%Y-%m-%d %H:%M:00",
        )
    while start <= end:
        datetime_list.append(datetime_to_string(start, format_map.get(period)))
        start += relativedelta(**{period: offset})
    return datetime_list


def convert_simple_datetime(date_list, period_type):
    """转化成精简的时间格式"""
    format_map = {
        "minutes": "%H:%M",
        "hours": "%H:00",
        "days": "%m-%d",
        "months": "%Y-%m",
    }
    return [datetime_to_string(string_to_datetime(date_str), format_map.get(period_type)) for date_str in date_list]
