import datetime

from dateutil import parser
from discord.ext import commands

from .datetime_util import timezone_lookup
from .raid_info import Raid, raids


class RaidConverter(commands.Converter):
    """Converts a string to a specific raid"""

    async def convert(self, ctx: commands.Context, raid_str: str) -> Raid:
        # try to find based on name first, then alias
        for r in raids:
            if r.name.lower() == raid_str.lower():
                return r
            if raid_str.lower() in r.aliases:
                return r
        raise ValueError(f"{raid_str} is not a registered raid or raid alias")


class DateTime(commands.Converter):
    """Converts a generic string to a date time"""

    async def convert(
        self, ctx: commands.Context, datetime_string: str
    ) -> datetime.datetime:
        try:
            return parser.parse(datetime_string, tzinfos=timezone_lookup)
        except parser.ParserError:
            raise ValueError(f"`{datetime_string}` is not a valid date and time")


class ISODateTime(commands.Converter):
    """Converts an ISO-8601 datetime string into a datetime.datetime."""

    async def convert(
        self, ctx: commands.Context, datetime_string: str
    ) -> datetime.datetime:
        """
        Converts a ISO-8601 `datetime_string` into a `datetime.datetime` object.

        The converter is flexible in the formats it accepts, as it uses the `isoparse` method of
        `dateutil.parser`. In general, it accepts datetime strings that start with a date,
        optionally followed by a time. Specifying a timezone offset in the datetime string is
        supported, but the `datetime` object will be converted to UTC. If no timezone is specified,
        the datetime will
        be assumed to be in UTC already. In all cases, the returned object will have the UTC
        timezone.

        See: https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.isoparse

        Formats that are guaranteed to be valid by our tests are:

        - `YYYY-mm-ddTHH:MM:SSZ` | `YYYY-mm-dd HH:MM:SSZ`
        - `YYYY-mm-ddTHH:MM:SS±HH:MM` | `YYYY-mm-dd HH:MM:SS±HH:MM`
        - `YYYY-mm-ddTHH:MM:SS±HHMM` | `YYYY-mm-dd HH:MM:SS±HHMM`
        - `YYYY-mm-ddTHH:MM:SS±HH` | `YYYY-mm-dd HH:MM:SS±HH`
        - `YYYY-mm-ddTHH:MM:SS` | `YYYY-mm-dd HH:MM:SS`
        - `YYYY-mm-ddTHH:MM` | `YYYY-mm-dd HH:MM`
        - `YYYY-mm-dd`
        - `YYYY-mm`
        - `YYYY`

        Note: ISO-8601 specifies a `T` as the separator between the date and the time part of the
        datetime string. The converter accepts both a `T` and a single space character.
        """
        try:
            dt = parser.isoparse(datetime_string)
        except ValueError:
            raise ValueError(
                f"`{datetime_string}` is not a valid ISO-8601 datetime string"
            )

        if dt.tzinfo:
            dt = dt.astimezone(datetime.timezone.utc)
        else:  # Without a timezone, assume it represents UTC.
            dt = dt.replace(tzinfo=datetime.timezone.utc)

        return dt
