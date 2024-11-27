from datetime import datetime
import pytz


class DateTimeUtility:
    def __init__(self, server_timezone: str, local_timezone: str):
        """
        Initializes the TimeUtility class with the server's timezone.

        :param server_timezone: The timezone of the server (e.g., "UTC", "America/New_York").
        """
        self.server_timezone = pytz.timezone(server_timezone)
        self.local_timezone = pytz.timezone(local_timezone)

    def get_server_time(self) -> datetime:
        """
        creates datetime as of UTC now
        :return:
        """
        return datetime.now(self.server_timezone)

    def server_to_local(self, server_time: datetime) -> datetime:
        """
        Converts server time to local time.

        :param server_time: The datetime object representing the server time.
        :return: A datetime object in the local timezone.
        """
        # Convert to local timezone
        return server_time.astimezone(self.local_timezone)

