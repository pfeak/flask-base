import time
from datetime import datetime, timedelta

FORMAT_STR = "%Y-%m-%dT%H:%M:%S.%f"


class TimeUtils:

    @staticmethod
    def utc2local(utc_str: str, hours: int = 0, format_str: str = FORMAT_STR) -> int:
        """utc str format to timestamp by timezone"""
        localtime: datetime = datetime.strptime(utc_str, format_str) + timedelta(hours=hours)
        return int(time.mktime(localtime.timetuple()))

    @staticmethod
    def timestamp2format(timestamp: int, format_str: str = FORMAT_STR) -> str:
        """10-bit timestamp format to str"""
        localtime = time.localtime(timestamp)
        return time.strftime(format_str, localtime)

    @staticmethod
    def format2timestamp(time_str: str, format_str: str = FORMAT_STR) -> int:
        """str format to 10-bit timestamp"""
        localtime = time.strptime(time_str, format_str)
        return int(time.mktime(localtime))

    @staticmethod
    def datetime2timestamp(time_obj: datetime) -> int:
        """datetime format to 10-bit timestamp"""
        return int(time.mktime(time_obj.timetuple()))
