from datetime import datetime
from zoneinfo import ZoneInfo

class ModelUtils:

    # In Java, using Date includes timezone offset in JSON whereas using LocalDateTime does not

    est_zone = ZoneInfo("US/Eastern")

    @staticmethod
    def convertoToEst(dt: datetime) -> datetime:
        return dt.astimezone(ModelUtils.est_zone)

    @staticmethod
    def localizeDateTime(dt: datetime) -> datetime:
        return dt.replace(tzinfo=ModelUtils.est_zone)


    @staticmethod
    def parseDatetime(date_str: str) -> datetime:
        dateFormat = '%Y-%m-%dT%H:%M:%S.%f' if "." in date_str else '%Y-%m-%dT%H:%M:%S'
        dt = datetime.strptime(date_str, dateFormat)
        dt = dt.astimezone(ModelUtils.est_zone)
        return dt

    @staticmethod
    def formatDatetime(dt: datetime) -> str:
        return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')

    @staticmethod
    def parseZonedDatetime(date_str: str) -> datetime:
        dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        dt = dt.astimezone(ModelUtils.est_zone)
        return dt

    @staticmethod
    def formatZonedDatetime(dt: datetime) -> str:
        return dt.strftime('%Y-%m-%dT%H:%M:%S.%f%z')