"""Wrappers for data that can be garbled during read/write"""

from __future__ import annotations

import logging
import re
from calendar import monthrange
from collections import namedtuple
from datetime import MINYEAR, MAXYEAR, date, datetime, time
from math import log10, modf
from typing import Any


logger = logging.getLogger(__name__)


ExtendedDate = namedtuple("ExtendedDate", ["year", "month", "day"])


class EMuType:
    """Container for data types that may be garbled during read/write

    For example, transforming a year to a date using datetime.strptime()
    imposes a month and date, which could be bad news if that data is ever
    loaded back into the database. This class tracks the original string
    and format while coercing the string to a Python data type and
    providing support for basic operations.

    Parameters
    ----------
    val : Any
        value to wrap
    fmt : str
        formatting string used to translate value back to a string

    Attributes
    ----------
    value : Any
        value coerced to the correct type from a string
    format : str
        a formatting string
    verbatim : Any
        the original, unparsed value
    """

    def __init__(self, val: Any, fmt: str = "{}"):
        self.verbatim = val
        self.value = val
        self.format = fmt
        self.always_compare_range = False

    def __str__(self) -> str:
        return self.format.format(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{str(self)}')"

    def __eq__(self, other: Any) -> bool:
        if self.value == other:
            return True
        try:
            other = self.coerce(other)
        except (TypeError, ValueError):
            return False
        if self.is_range() or self.always_compare_range:
            return (
                self.comp == other.comp
                and self.min_comp == other.min_comp
                and self.max_comp == other.max_comp
            )
        return self.value == other.value

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: Any) -> bool:
        try:
            other = self.coerce(other)
        except:
            raise TypeError(
                f"'<' not supported between instances of '{self.__class__.__name__}'"
                f" and '{type(other)}'"
            )
        if self.is_range() or self.always_compare_range:
            return self.max_comp < other.min_comp
        return self.value < other.value

    def __le__(self, other: Any) -> bool:
        try:
            other = self.coerce(other)
        except:
            raise TypeError(
                f"'<=' not supported between instances of '{self.__class__.__name__}'"
                f" and '{type(other)}'"
            )
        if self.is_range() or self.always_compare_range:
            return self.min_comp <= other.max_comp
        return self.value <= other.value

    def __gt__(self, other: Any) -> bool:
        try:
            other = self.coerce(other)
        except:
            raise TypeError(
                f"'>' not supported between instances of '{self.__class__.__name__}'"
                f" and '{type(other)}'"
            )
        if self.is_range() or self.always_compare_range:
            other = self.coerce(other)
            return self.min_comp > other.max_comp
        return self.value > other.value

    def __ge__(self, other: Any) -> bool:
        try:
            other = self.coerce(other)
        except:
            raise TypeError(
                f"'>=' not supported between instances of '{self.__class__.__name__}'"
                f" and '{type(other)}'"
            )
        if self.is_range() or self.always_compare_range:
            return self.max_comp >= other.min_comp
        return self.value >= other.value

    def __contains__(self, other: Any) -> bool:
        if self.is_range():
            other = self.coerce(other)
            return self.min_comp <= other.min_comp and self.max_comp >= other.max_comp
        raise ValueError(f"{self.__class__.__name__} is not a range")

    def __add__(self, other) -> EMuType | int | float:
        return self._math_op(other, "__add__")

    def __sub__(self, other) -> EMuType | int | float:
        return self._math_op(other, "__sub__")

    def __mul__(self, other) -> EMuType | int | float:
        return self._math_op(other, "__mul__")

    def __floordiv__(self, other) -> EMuType | int | float:
        return self._math_op(other, "__floordiv__")

    def __truediv__(self, other) -> EMuType | int | float:
        return self._math_op(other, "__truediv__")

    def __mod__(self, other) -> EMuType | int | float:
        return self._math_op(other, "__mod__")

    def __divmod__(self, other) -> EMuType | int | float:
        return self._math_op(other, "__divmod__")

    def __pow__(self, other) -> EMuType | int | float:
        return self._math_op(other, "__pow__")

    def __iadd__(self, other: Any) -> EMuType:
        result = self + other
        return self.__class__(result.value, result.format)

    def __isub__(self, other: Any) -> EMuType:
        result = self - other
        return self.__class__(result.value, result.format)

    def __imul__(self, other: Any) -> EMuType:
        result = self * other
        return self.__class__(result.value, result.format)

    def __ifloordiv__(self, other: Any) -> EMuType:
        result = self // other
        return self.__class__(result.value, result.format)

    def __itruediv__(self, other: Any) -> EMuType:
        result = self / other
        return self.__class__(result.value, result.format)

    def __imod__(self, other: Any) -> EMuType:
        result = self % other
        return self.__class__(result.value, result.format)

    def __ipow__(self, other: Any) -> EMuType:
        result = self**other
        return self.__class__(result.value, result.format)

    def __setattr__(self, attr: str, val: Any) -> None:
        try:
            existing = getattr(self, attr)
        except AttributeError:
            super().__setattr__(attr, val)
        else:
            if val != existing:
                raise AttributeError(
                    f"Cannot modify existing attribute ({attr}={repr(existing)},"
                    f" tried to assign {repr(val)})"
                )

    def __delattr__(self, attr: str) -> None:
        raise AttributeError("Cannot delete attribute")

    @property
    def min_value(self) -> Any:
        """Minimum value needed to express the original string"""
        return self.value

    @property
    def max_value(self) -> Any:
        """Maximum value needed to express the original string"""
        return self.value

    @property
    def comp(self) -> Any:
        """Value to use for comparisons"""
        return self.value

    @property
    def min_comp(self) -> Any:
        """Minimum value to use for comparisons"""
        return self.value

    @property
    def max_comp(self) -> Any:
        """Maximum value to use for comparisons"""
        return self.value

    def emu_str(self) -> str:
        """Returns a string representation suitable for EMu"""
        return str(self)

    def coerce(self, other: Any) -> EMuType:
        """Coerces another object to the current class

        Parameters
        ----------
        other : Any
            an object to convert to this class

        Returns
        -------
        EMuType
            other as EMuType
        """
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        return other

    def is_range(self) -> bool:
        """Checks if class represents a range"""
        return self.min_comp != self.max_comp

    def _math_op(self, other, operation) -> EMuType | int | float:
        """Performs the specified arithmetic operation

        Wraps result in instance class if possible. In the case of values that
        can't be expressed using the original class (for example, the difference
        between two dates), it returns the result itself.
        """

        if self.is_range():
            min_val = self.__class__(self.min_value)._math_op(other, operation)
            max_val = self.__class__(self.max_value)._math_op(other, operation)
            return (min_val, max_val)

        if isinstance(other, self.__class__):
            val = getattr(self.value, operation)(other.value)
            # Raise an error if values are not floats and formats differ
            if isinstance(self.value, float):
                # Use the more precise format for add/substract
                i = -1 if operation in {"__add__", "__sub__"} else 0
                try:
                    fmt = sorted([o.format for o in [self, other] if o.dec_places])[i]
                except IndexError:
                    fmt = self.format
            elif self.format != other.format:
                raise ValueError(
                    f"{self.__class__.__name__} have different formats: {[self.format, other.format]}"
                )
            else:
                fmt = self.format
        else:
            try:
                val = getattr(self.value, operation)(other)
            except AttributeError:
                raise ValueError(f"Operation not available: {operation}")
            fmt = self.format

        if isinstance(val, tuple):
            return tuple([self.__class__(str(val), fmt=fmt) for val in val])

        try:
            return self.__class__(str(val), fmt=fmt)
        except ValueError:
            # Some operations return values that cannot be coerced to the original
            # class, for example, subtracting one date from another
            return val

    def _set_default_attr(self, attr: str, val: Any = None) -> None:
        try:
            getattr(self, attr)
        except AttributeError:
            setattr(self, attr, val)


class EMuFloat(EMuType):
    """Wraps floats read from strings to preserve precision

    Parameters
    ----------
    val : str | float
        float as a string or float
    fmt : str
        formatting string used to convert the float back to a string. Computed
        for strings but must be included if val is a float.

    Attributes
    ----------
    value : float
        float parsed from string
    format : str
        formatting string used to convert the float back to a string
    verbatim : Any
        the original, unparsed value
    """

    def __init__(self, val: str | float, fmt: str = None):
        """Initialize an EMuFloat object

        Parameters
        ----------
        val : str or float
            the number to wrap
        fmt : str
            a Python formatting string. Recommended if val is a float,
            otherwise it will be determined from val.
        """

        self.verbatim = val
        self.always_compare_range = False

        fmt_provided = fmt is not None

        if isinstance(val, str):
            val = val.replace(",", "")

        if isinstance(val, float) and not fmt_provided:
            val = str(val)

        if isinstance(val, self.__class__):
            self.value = val.value
            self.format = val.format
            val = str(val)  # convert to string so the verification step works
        elif fmt_provided:
            self.value = float(val)
            self.format = fmt
        else:
            self.value = float(val)
            val = str(val)
            dec_places = len(val.split(".")[1]) if "." in val else 0
            self.format = f"{{:.{dec_places}f}}"

        # Verify that the parsed value is the same as the original string if
        # the format string was calculated
        if not fmt_provided and val.lstrip("0").rstrip(".") != str(self).lstrip("0"):
            raise ValueError(f"Parsing changed value ({repr(val)} became {repr(self)})")

    def __format__(self, format_spec: str) -> str:
        try:
            return format(str(self), format_spec)
        except ValueError:
            return format(float(self), format_spec)

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return self.value

    @property
    def dec_places(self) -> int:
        """Number of decimal places from the formatting string"""
        return int(self.format.strip("{:.f}"))

    def round(self, dec_places: int) -> "EMuFloat":
        """Rounds the float to the given number of decimal places

        Parameters
        ----------
        dec_places : int
            the number of decimal places

        Returns
        -------
        EMuFloat
            the rounded value
        """
        return self.__class__(("{:." + str(dec_places) + "f}").format(self))


class EMuCoord(EMuFloat):
    """Wraps coordinates read from strings

    Attributes
    ----------
    value : str | float
        coordinate as a string or float
    format : str
        formatting string used to convert the float back to a string
    degrees : EMuFloat
        degrees parsed from original
    minutes : EMuFloat
        minutes parsed from original, if any
    seconds : EMuFloat
        seconds parsed from original, if any
    verbatim : Any
        the original, unparsed value
    """

    #: str : pattern for hemisphere for positive coordinates
    pos = ""

    #: str : pattern for hemisphere for negative coordinates
    neg = ""

    #: tuple of int : range of allowable values
    bounds = (0, 0)

    #: float : width of one degree lat (anywhere) or lon (at the equator)
    deg_dist_m = 110567

    # dict : uncertainty in meters for deg/min/sec at the equator
    dms_unc_m = {
        "degrees": deg_dist_m,
        "minutes": deg_dist_m / 60,
        "seconds": deg_dist_m / 3600,
    }

    # dict : uncertainty in meters for decimal degrees at the equator
    dec_unc_m = {
        0: deg_dist_m,
        1: deg_dist_m / 10,
        2: deg_dist_m / 100,
        3: deg_dist_m / 1000,
        4: deg_dist_m / 10000,
        5: deg_dist_m / 100000,
    }

    def __init__(self, val: str | float, fmt: str = None):
        """Initializes an EMuCoord object

        Parameters
        ----------
        val : str | float
            coordinate
        fmt : str
            formatting string used to convert a float back to a string
        """

        self.always_compare_range = False

        if isinstance(val, str):
            self.verbatim = val.strip()
            parts = re.findall(r"(\d+(?:\.\d+)?)", self.verbatim)
            if len(parts) > 3:
                raise ValueError(f"Invalid coordinate: {self.verbatim}")
            self.degrees = EMuFloat(parts[0])
            if len(parts) == 1:
                self.format = self.degrees.format
            elif len(parts) > 1:
                self.minutes = EMuFloat(parts[1])
                self.format = "{}"
            if len(parts) > 2:
                self.seconds = EMuFloat(parts[2])
        elif isinstance(val, EMuCoord):
            self.verbatim = val.verbatim
            for attr in ("degrees", "minutes", "seconds", "format"):
                if getattr(val, attr) is not None:
                    setattr(self, attr, getattr(val, attr))
        else:
            self.verbatim = val
            self.degrees = EMuFloat(abs(val), fmt=fmt)
            self.format = self.degrees.format

        self._set_default_attr("minutes", None)
        self._set_default_attr("seconds", None)

        self._sign = EMuFloat(self._get_sign(), fmt="{:.0f}")

        self.value = float(self)
        if self.value < min(self.bounds) or self.value > max(self.bounds):
            raise ValueError(f"Coordinate out of bounds ({val} not in {self.bounds})")

        if self.minutes and self.minutes > 60:
            raise ValueError(f"Invalid minutes: {val}")

        if self.seconds and self.seconds > 60:
            raise ValueError(f"Invalid seconds: {val}")

    def __format__(self, format_spec: str) -> str:
        try:
            return format(str(self), format_spec)
        except ValueError:
            return format(float(self), format_spec)

    def __str__(self) -> str:
        if self.kind == "dms":
            parts = (self.degrees, self.minutes, self.seconds)
            return f"{' '.join([str(p) for p in parts if p is not None])} {self.hemisphere}"
        return str(self._sign * self.degrees)

    def __int__(self) -> int:
        return int(float(self))

    def __float__(self) -> float:
        val = EMuFloat(self.degrees)
        if self.minutes:
            val += self.minutes / 60
        if self.seconds:
            val += self.seconds / 3600
        return float(self._sign * val)

    @property
    def hemisphere(self) -> str:
        """Gets the hemisphere in which a coordinate is located"""
        return self.pos[0] if self._sign > 0 else self.neg[0]

    @property
    def kind(self) -> str:
        """Gets kind of verbatim coordinate string"""
        try:
            float(self.verbatim)
        except ValueError:
            return "dms"
        return "decimal"

    def to_dms(self, unc_m: int = None) -> str:
        """Expresses coordinate as degrees-minutes-seconds

        Parameters
        ----------
        unc_m : int
            uncerainty in meters

        Returns
        -------
        str
            coordinate as degrees-minutes-seconds
        """

        orig_unc_m = self.coord_uncertainty_m()
        if unc_m is None:
            if self.kind == "dms":
                parts = [
                    p if p else 0 for p in (self.degrees, self.minutes, self.seconds)
                ]
                for i, part in enumerate(parts):
                    if i < 2:
                        frac, num = modf(part)
                        parts[i] = num
                        parts[i + 1] += 60 * frac
                    parts[i] = int(parts[i])
                return f"{' '.join([str(p) for p in parts if p is not None])} {self.hemisphere}"
            unc_m = orig_unc_m

        # Round to approximate the given uncertainty
        unc_m = self._round_to_exp_10(unc_m)
        if unc_m < orig_unc_m:
            raise ValueError(
                f"unc_m cannot be smaller than the uncertainty implied by verbatim ({orig_unc_m} m)"
            )

        last_unc_m = 1e7
        for key, ref_unc_m in self.dms_unc_m.items():
            ref_unc_m = self._round_to_exp_10(ref_unc_m)

            if ref_unc_m <= unc_m <= last_unc_m:
                tenths = False
                break
            last_unc_m = ref_unc_m

            # Gaps between deg/min/sec ranks are huge, so try tenths as well
            if ref_unc_m / 10 <= unc_m <= last_unc_m:
                tenths = True
                break
            last_unc_m = ref_unc_m / 10

        val = self.value

        # Reverse sign for negative coords. Hemisphere is given using a letter.
        if val < 0:
            val *= -1

        parts = []
        for attr in ["degrees", "minutes", "seconds"]:
            fractional, integer = modf(val)
            if key == attr and tenths:
                integer += round(fractional, 1)
                parts.append(f"{integer:.1f}")
            else:
                parts.append(str(int(integer)))
            if key == attr:
                break
            val = fractional * 60

        return f"{' '.join([str(p) for p in parts])} {self.hemisphere}"

    def to_dec(self, unc_m: int = None) -> str:
        """Expresses coordinate as a decimal

        Parameters
        ----------
        unc_m : int
            uncerainty in meters

        Returns
        -------
        str
            coordinate as decimal
        """
        orig_unc_m = self.coord_uncertainty_m()
        if unc_m is None:
            if self.kind == "decimal":
                return str(self._sign * self.degrees)
            unc_m = orig_unc_m

        unc_m = self._round_to_exp_10(unc_m)
        if unc_m < orig_unc_m:
            raise ValueError(
                f"unc_m cannot be smaller than the uncertainty implied by verbatim ({orig_unc_m} m)"
            )

        last_unc_m = 1e7
        for key, ref_unc_m in self.dec_unc_m.items():
            ref_unc_m = self._round_to_exp_10(ref_unc_m)
            if ref_unc_m <= unc_m <= last_unc_m:
                break
            last_unc_m = ref_unc_m
        return f"{{:.{key}f}}".format(self)

    def coord_uncertainty_m(self) -> int:
        """Estimates coordinate uncertainty in meters based on distance at equator

        Returns
        -------
        int
            uncertainty in meters, rounded to an exponent of 10
        """
        if self.seconds:
            unc_m = self.deg_dist_m / (3600 * 10**self.seconds.dec_places)
        elif self.minutes:
            unc_m = self.deg_dist_m / (60 * 10**self.minutes.dec_places)
        else:
            unc_m = self.deg_dist_m / 10**self.degrees.dec_places
        return self._round_to_exp_10(unc_m)

    def _get_sign(self) -> int:
        """Gets the sign of the decimal coordinate represented as +1 or -1"""
        if isinstance(self.verbatim, str):
            val = self.verbatim.strip()

            try:
                return 1 if float(self.verbatim) >= 0 else -1
            except ValueError:
                pass

            for pat, mod in {
                r"(^\+|^{0}|{0}\.?$)".format(self.pos): 1,
                r"(^-|^{0}|{0}\.?$)".format(self.neg): -1,
            }.items():
                if re.search(pat, val, flags=re.I):
                    return mod

            raise ValueError(
                f"Could not parse as {self.__class__.__name__}: {self.verbatim}"
            )

        return 1 if self.verbatim >= 0 else -1

    @staticmethod
    def _round_to_exp_10(val: int | float) -> int:
        """Rounds value to an exponent of 10"""
        frac, exp = modf(log10(val))
        if frac > log10(4.99999999):
            exp += 1
        return int(10**exp)


class EMuLatitude(EMuCoord):
    """Wraps latitudes read from strings"""

    #: str : pattern for hemisphere for positive coordinates
    pos = "N(orth)?"

    #: str : pattern for hemisphere for negative coordinates
    neg = "S(outh)?"

    #: tuple of int : range of allowable values
    bounds = (-90, 90)

    def __init__(self, val: str | float, fmt: str = None):
        """Initialize an EMuLatitude object

        Parameters
        ----------
        val : str or float
            latitude
        fmt : str
            formatting string used to convert a float back to a string
        """
        super().__init__(val, fmt)


class EMuLongitude(EMuCoord):
    """Wraps longitudes read from strings"""

    #: str : pattern for hemisphere for positive coordinates
    pos = "E(ast)?"

    #: str : pattern for hemisphere for negative coordinates
    neg = "W(est)?"

    #: tuple of int : range of allowable values
    bounds = (-180, 180)

    def __init__(self, val: str | float, fmt: str = None):
        """Initialize an EMuLongitude object

        Parameters
        ----------
        val : str or float
            longitude
        fmt : str
            formatting string used to convert a float back to a string
        """
        super().__init__(val, fmt)


class EMuDate(EMuType):
    """Wraps dates read from strings to preserve meaning

    For dates in the range supported by the native EMu datetime module, this
    class supports both comparisons and addition/subtraction using timedelta objects
    but not augmented assignment using += or -=. For dates outside this range,
    comparisons and operations are currently not possible.

    Parameters
    ----------
    val : str or datetime.date
        date as a string or date object
    fmt : str
        formatting string used to convert the value back to a string. If
        omitted, the class will try to determine the correct format.

    Attributes
    ----------
    value : datetime.date or ExtendedDate
        date parsed from string
    format : str
        date format string used to convert the date back to a string
    verbatim : Any
        the original, unparsed value
    """

    directives = {
        "day": ("%d", "%-d"),
        "month": ("%B", "%b", "%m", "%-m"),
        "year": ("%Y", "%y"),
    }
    formats = {"day": "%Y-%m-%d", "month": "%b %Y", "year": "%Y"}

    def __init__(self, *val, fmt: str = None):
        """Initialize an EMuDate object

        Parameters
        ----------
        val : str, int, datetime.date, Iterable[int, int, int]
            the date. If an int, must be a year only. If multiple values are given,
            they must be a year, month, and day as ints. If the string "today" is
            given, returns today's date.
        fmt : str
            a date format string
        """

        if len(val) == 1:
            val = val[0]
        if val == "today":
            val = datetime.now().strftime("%Y-%m-%d")

        self.verbatim = val
        self.always_compare_range = True

        fmt_provided = fmt is not None

        # Convert integers to strings
        if isinstance(val, int):
            val = str(val)

        # Convert tuples to ExtendedDate
        if isinstance(val, tuple) and not isinstance(val, ExtendedDate):
            val = ExtendedDate(*val)

        # Remove periods and trailing hyphens before parsing
        if isinstance(val, str):
            val = val.replace(".", "").rstrip("-")

        # Zero-pad two-to-three-digit years if no format is provided. EMu does
        # not zero-pad years less than 1000 during export, which trips up the
        # date parsing below. Assumes year-month-day format.
        if (
            not fmt_provided
            and isinstance(val, str)
            and re.match(r"^\d{1,3}-\d{1,2}-(\d{1,2})?$", val)
        ):
            val = re.sub(
                r"^(-?\d{1,3})\b",
                lambda s: s.group(1).zfill(5 if val[0] == "-" else 4),
                val,
            )

        # Common data formats
        fmts = [
            # EMu date formats
            ("day", "%Y-%m-%d"),
            ("day", "%d %b %Y"),
            ("month", "%b %Y"),
            ("month", "%Y-%m-"),
            ("year", "%Y"),
            # Other common date formats
            ("day", "%d-%b-%Y"),
            ("day", "%b %d %Y"),
            ("day", "%b %d, %Y"),
            ("day", "%B %d %Y"),
            ("day", "%B %d, %Y"),
            ("month", "%B %Y"),
            ("month", "%Y-%m"),
        ]

        if isinstance(val, EMuDate):
            self.value = val.value
            self.kind = val.kind
            self.format = val.format
            val = val.strftime(self.format)
            fmt = self.format
            fmts.clear()

        elif isinstance(val, (date, ExtendedDate)):
            if val.day:
                self.kind = "day"
                self.format = "%Y-%m-%d"
            elif val.month:
                self.kind = "month"
                self.format = "%b %Y"
            else:
                self.kind = "year"
                self.format = "%Y"

            # Convert ExtendedDate that can be handled by the datetime module
            if isinstance(val, ExtendedDate) and MINYEAR <= val.year <= MAXYEAR:
                self.value = date(*(n if n else 1 for n in val))
            else:
                self.value = val

            val = self._strftime(val, self.format)
            fmt = self.format
            fmts.clear()

            self._validate_extended_date(self)

        elif fmt:
            # Assess speciicity of date if custom formatting string provided
            for kind, directives in self.directives.items():
                if any((d in fmt for d in directives)):
                    self.value = self.strptime(str(val), fmt)
                    self.kind = kind
                    self.format = self.formats[kind]
                    fmts.clear()
                    break

        for kind, fmt in fmts:
            try:
                self.value = self.strptime(str(val), fmt)
                self.kind = kind
                self.format = self.formats[kind]
                break
            except (TypeError, ValueError):
                pass
        else:
            if fmts:
                raise ValueError(f"Could not parse date: {repr(val)}")

        # Verify that the parsed value is the same as the original string if
        # the format string was calculated
        # if not fmt_provided and str(val) != self.strftime(fmt):
        #    raise ValueError(f"Parsing changed value ('{val}' became '{self}')")

    def __str__(self) -> str:
        return self.strftime(self.format)

    def strftime(self, fmt: str = None) -> str:
        """Formats date as a string

        Parameters
        ----------
        fmt : str
            date format string

        Returns
        -------
        str
            date as string
        """
        return self._strftime(self, fmt if fmt is not None else self.format)

    def to_datetime(self, tm: time) -> datetime:
        """Combines date and time into a single datetime

        Parameters
        ----------
        tm : datetime.time
            time to use with date

        Returns
        -------
        datetime.datetime
            combined datetime
        """
        if self.min_value != self.max_value:
            raise ValueError("Cannot convert range to datetime")
        return datetime(
            self.year,
            self.month,
            self.day,
            tm.hour,
            tm.minute,
            tm.second,
            tm.microsecond,
            tm.tzinfo,
        )

    def emu_str(self) -> str:
        """Returns a string representation of the date suitable for EMu"""
        if self.year < 0:
            year = str(self.year).zfill(5)
            return f"{self} BC".replace(year, year.lstrip("-"))
        if 0 <= self.year < 100:
            return f"{self} AD"
        return str(self)

    @property
    def min_value(self) -> date | ExtendedDate:
        """Minimum date needed to express the original string

        For example, the first day of the month for a date that specifies
        only a month and year or the first day of the year for a year.
        """
        if self.kind == "day":
            return self.value
        if self.kind == "month":
            return self.value.__class__(self.value.year, self.value.month, 1)
        if self.kind == "year":
            return self.value.__class__(self.value.year, 1, 1)
        raise ValueError(f"Invalid kind: {self.kind}")

    @property
    def max_value(self) -> date | ExtendedDate:
        """Maximum date needed to express the original string

        For example, the last day of the month for a date that specifies
        only a month and year or the last day of the year for a year.
        """
        if self.kind == "day":
            return self.value
        if self.kind == "month":
            _, last_day = monthrange(self.value.year, self.value.month)
            return self.value.__class__(self.value.year, self.value.month, last_day)
        if self.kind == "year":
            return self.value.__class__(self.value.year, 12, 31)
        raise ValueError(f"Invalid kind: {self.kind}")

    @property
    def comp(self) -> tuple[int, int, int]:
        """Value to use for comparisons"""
        val = self.min_value
        return (val.year, val.month if val.month else 1, val.day if val.day else 1)

    @property
    def min_comp(self) -> tuple[int, int, int]:
        """Minimum value to use for comparisons"""
        val = self.min_value
        return (val.year, val.month, val.day)

    @property
    def max_comp(self) -> tuple[int, int, int]:
        """Maximum value to use for comparisons"""
        val = self.max_value
        return (val.year, val.month, val.day)

    @property
    def year(self) -> int:
        """Year of the parsed date"""
        return self.value.year

    @property
    def month(self) -> int:
        """Month of the parsed date"""
        return self.value.month if self.kind != "year" else None

    @property
    def day(self) -> int:
        """Day of the parsed date"""
        return self.value.day if self.kind == "day" else None

    def date(self) -> date:
        """Returns the datetime.date corresponding to this object

        Included to allow instances of this class to play well with functions that
        accept dates using both the datetime.date and datetime.datetime classes;
        instances of datetime.datetime include a date method that allows them to
        be easily converted to dates, for example, for comparisons.

        Returns
        -------
        datetime.date
            the date corresponding to this object
        """
        return self.value

    @staticmethod
    def strptime(val: str, fmt: str) -> date | ExtendedDate:
        """Formats a string as a date

        Parameters
        ----------
        val : str
            date string
        fmt : str
            date format string

        Returns
        -------
        datetime.date or ExtendedDate
            date as an object. If year is out-of-range for the native date class,
            returns an ExtendedDate tuple instead.
        """
        try:
            parsed = datetime.strptime(val, fmt)
            return date(parsed.year, parsed.month, parsed.day)
        except ValueError:
            # Set up a regex pattern based on the date format string
            pattern = (
                fmt.replace("%Y", r"(?P<year>-?\d+)")
                .replace("%m", r"(?P<month>\d+)")
                .replace("%d", r"(?P<day>\d+)")
                .replace("%b", r"(?P<month>[A-Z]{3})")
            )
            match = re.search(
                "^" + pattern + r"( (A[\. ]*D\.?|B[\. ]*C[\. ]*(E\.?)?))?$",
                val,
                flags=re.I,
            )

            ymd = []
            for key in ("year", "month", "day"):
                try:
                    ymd.append(int(match.group(key)))
                except AttributeError as exc:
                    raise ValueError(
                        f"Could not parse string as ExtendedDate: {val}"
                    ) from exc
                except IndexError:
                    ymd.append(None)
                except ValueError:
                    ymd.append(int(datetime.strptime(match.group(key), "%b").month))

            # Handle AD and BC
            if ymd[0] is not None and ymd[0] > 0:
                pattern = r"\b(A[\. ]*D\.?|B[\. ]*C[\. ]*(E\.?)?)\b"
                ad_bc = re.search(pattern, val, flags=re.I)
                if ad_bc is not None:
                    ad_bc = re.sub(r"[^A-Z]", "", ad_bc.group().upper(), flags=re.I)
                    if ad_bc.startswith("BC"):
                        ymd[0] *= -1

            ext_date = ExtendedDate(*ymd)
            EMuDate._validate_extended_date(ext_date)
            return ext_date

    def _strftime(self, val: str, fmt: str = None) -> str:
        """Formats date as a string

        Parameters
        ----------
        val: datetime.date, EMuDate, or ExtendedDate
            date
        fmt : str
            date format string

        Returns
        -------
        str
            date as string
        """

        # Forbid formats that are more specific than the original string. Users
        # can force the issue by formatting the value attribute directly.
        if not val.day:
            allowed = []
            if val.year is not None:
                allowed.extend(self.directives["year"])
            if val.month:
                allowed.extend(self.directives["month"])

            directives = re.findall(r"%[a-z]", fmt, flags=re.I)
            disallowed = set(directives) - set(allowed)
            if disallowed:
                raise ValueError(
                    f"Invalid directives for ({val.year}, {val.month}, {val.day}): {disallowed}"
                )

        # Use the value attribute if passing an EMuDate
        if isinstance(val, EMuDate):
            val = val.value

        try:
            return val.strftime(fmt)
        except AttributeError:
            date_str = (
                fmt.replace("%Y", str(val.year).zfill(5 if val.year < 0 else 4))
                .replace("%m", str(val.month).zfill(2))
                .replace("%d", str(val.day).zfill(2))
            )
            if "%b" in fmt:
                month_abbr = datetime.strptime(str(val.month), "%m").strftime("%b")
                date_str = date_str.replace("%b", month_abbr)
            return date_str

    @staticmethod
    def _validate_extended_date(val: date | datetime | ExtendedDate | EMuDate) -> None:
        if val.month and (val.month < 1 or val.month > 12):
            raise ValueError(f"Month out of range: {val}")
        if val.day:
            if val.day > monthrange(val.year, val.month)[1]:
                raise ValueError(f"Day out of range: {val}")


class EMuTime(EMuType):
    def __init__(self, val: str | datetime.time, fmt: str = None):
        """Initialize an EMuTime object

        Parameters
        ----------
        val : str or datetime.time
            the time
        fmt : str
            a time format string
        """

        self.verbatim = val
        self.always_compare_range = False

        fmt_provided = fmt is not None

        # Include both naive and timezoned formats
        fmts = [
            "%H:%M",
            "%H%M",
            "%I%M %p",
            "%I:%M %p",
            "%H:%M:%S",
            "%I:%M:%S %p",
        ]
        num_formats = len(fmts)
        fmts.extend([f"{f} %z" for f in fmts[:num_formats]])
        fmts.extend([f"{f} UTC%z" for f in fmts[:num_formats]])
        fmts.insert(0, "%H:%M:")

        if isinstance(val, EMuTime):
            self.value = val.value
            fmt = val.format
            val = val.strftime(fmt)
            fmts.clear()

        elif isinstance(val, time):
            self.value = val
            fmt = fmts[0]
            val = val.strftime(fmt)
            fmts.clear()

        for fmt in fmts:
            try:
                parsed = datetime.strptime(val, fmt)
                self.value = time(
                    parsed.hour,
                    parsed.minute,
                    parsed.second,
                    parsed.microsecond,
                    parsed.tzinfo,
                )
                break
            except (TypeError, ValueError):
                pass
        else:
            if fmts:
                raise ValueError(f"Could not parse time: {repr(val)}")

        # Verify that the parsed value is the same as the original string if
        # the format string was calculated
        if not fmt_provided and val.lstrip("0") != self.strftime(fmt).lstrip("0"):
            raise ValueError(f"Parsing changed value ('{val}' became '{self}')")

        # Enforce a consistent output format
        self.format = "%H:%M:%S" if "%S" in fmt else "%H:%M"

    def __str__(self) -> str:
        return self.value.strftime(self.format)

    def strftime(self, fmt: str = None) -> str:
        """Formats time as a string

        Parameters
        ----------
        fmt : str
            time format string

        Returns
        -------
        str
            time as string
        """
        return self.value.strftime(fmt if fmt else self.format)

    def to_datetime(self, dt: date) -> datetime:
        """Combines date and time into a single datetime

        Parameters
        ----------
        dt : datetime.date
            date to use with time

        Returns
        -------
        datetime.datetime
            combined datetime
        """
        return EMuDate(dt).to_datetime(self)

    @property
    def hour(self) -> int:
        """Hour of the parsed time"""
        return self.value.hour

    @property
    def minute(self) -> int:
        """Minute of the parsed time"""
        return self.value.minute

    @property
    def second(self) -> int:
        """Second of the parsed time"""
        return self.value.second

    @property
    def microsecond(self) -> int:
        """Microsecond of the parsed time"""
        return self.value.microsecond

    @property
    def tzinfo(self) -> str:
        """Time zone info for the parsed time"""
        return self.value.tzinfo
