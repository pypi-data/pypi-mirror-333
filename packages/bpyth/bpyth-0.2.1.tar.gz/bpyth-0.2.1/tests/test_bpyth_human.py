import math
from bpyth.bpyth_human import (
    human_readable_number,
    human_readable_number_1,
    human_readable_number_2,
    human_readable_number_3,
    human_readable_number_4,
    human_readable_seconds,
    human_readable_bytes,
)


class TestHumanReadableNumber:
    def test_human_readable_number_positive(self):
        assert human_readable_number(12345) == 12300
        assert human_readable_number(12345, digits=4) == 12350
        assert human_readable_number(123.45) == 123
        assert human_readable_number(1.2345) == 1.23
        assert human_readable_number(0.012345) == 0.0123

    def test_human_readable_number_negative(self):
        assert human_readable_number(-12345) == -12300
        assert human_readable_number(-123.45) == -123
        assert human_readable_number(-1.2345) == -1.23
        assert human_readable_number(-0.012345) == -0.0123

    def test_human_readable_number_zero(self):
        assert human_readable_number(0) == 0

    def test_human_readable_number_not_finite(self):
        assert math.isnan(human_readable_number(float("nan")))
        assert human_readable_number(float("inf")) == float("inf")
        assert human_readable_number(float("-inf")) == float("-inf")

    def test_human_readable_number_string(self):
        assert human_readable_number("123") == "123"

    def test_human_readable_number_digits_zero(self):
        assert human_readable_number(123, digits=0) == 123
        assert human_readable_number(123, digits=-1) == 123


    def test_human_readable_number_positive_more_digits_varied(self):
        assert human_readable_number(98765, digits=4) == 98770
        assert human_readable_number(456789, digits=5) == 456790
        assert human_readable_number(11111, digits=4) == 11110
        assert human_readable_number(10000, digits=4) == 10000
        assert human_readable_number(10000, digits=3) == 10000
        assert human_readable_number(99999, digits=3) == 100000
        assert human_readable_number(99999, digits=4) == 100000
        assert human_readable_number(99999, digits=5) == 99999
        assert human_readable_number(123456, digits=6) == 123456
        assert human_readable_number(765432, digits=6) == 765432
        assert human_readable_number(123456, digits=7) == 123456.0
        assert human_readable_number(765432, digits=7) == 765432.0
        assert human_readable_number(54321, digits=3) == 54300
        assert human_readable_number(12355, digits=4) == 12360
        assert human_readable_number(54321, digits=5) == 54321
        assert human_readable_number(12355, digits=5) == 12355
        assert human_readable_number(54321, digits=6) == 54321.0
        assert human_readable_number(12355, digits=6) == 12355.0

    def test_human_readable_number_negative_more_digits_varied(self):
        assert human_readable_number(-98765, digits=4) == -98770
        assert human_readable_number(-456789, digits=5) == -456790
        assert human_readable_number(-11111, digits=4) == -11110
        assert human_readable_number(-10000, digits=4) == -10000
        assert human_readable_number(-10000, digits=3) == -10000
        assert human_readable_number(-99999, digits=3) == -100000
        assert human_readable_number(-99999, digits=4) == -100000
        assert human_readable_number(-99999, digits=5) == -99999
        assert human_readable_number(-123456, digits=6) == -123456
        assert human_readable_number(-765432, digits=6) == -765432
        assert human_readable_number(-123456, digits=7) == -123456.0
        assert human_readable_number(-765432, digits=7) == -765432.0
        assert human_readable_number(-54321, digits=3) == -54300
        assert human_readable_number(-12355, digits=4) == -12360
        assert human_readable_number(-54321, digits=5) == -54321
        assert human_readable_number(-12355, digits=5) == -12355
        assert human_readable_number(-54321, digits=6) == -54321.0
        assert human_readable_number(-12355, digits=6) == -12355.0

    def test_human_readable_number_positive_small_numbers_varied(self):
        assert human_readable_number(0.98765, digits=3) == 0.988
        assert human_readable_number(0.12345, digits=4) == 0.1235
        assert human_readable_number(0.12345) == 0.123
        assert human_readable_number(0.098765, digits=4) == 0.09877
        assert human_readable_number(0.012345) == 0.0123
        assert human_readable_number(0.0098765, digits=4) == 0.009877
        assert human_readable_number(0.0012345) == 0.00123
        assert human_readable_number(0.00098765, digits=4) == 0.0009877
        assert human_readable_number(0.00012345, digits=3) == 0.000123
        assert human_readable_number(0.000012345, digits=3) == 1.23e-05

    def test_human_readable_number_negative_small_numbers_varied(self):
        assert human_readable_number(-0.98765, digits=3) == -0.988
        assert human_readable_number(-0.12345, digits=4) == -0.1235
        assert human_readable_number(-0.12345) == -0.123
        assert human_readable_number(-0.098765, digits=4) == -0.09877
        assert human_readable_number(-0.012345) == -0.0123
        assert human_readable_number(-0.0098765, digits=4) == -0.009877
        assert human_readable_number(-0.0012345) == -0.00123
        assert human_readable_number(-0.00098765, digits=4) == -0.0009877
        assert human_readable_number(-0.00012345, digits=3) == -0.000123
        assert human_readable_number(-0.000012345, digits=3) == -1.23e-05

    def test_human_readable_number_positive_large_numbers_varied(self):
        assert human_readable_number(987654321) == 988000000
        assert human_readable_number(1234567890, digits=4) == 1235000000
        assert human_readable_number(123456789, digits=5) == 123460000
        assert human_readable_number(123456789, digits=6) == 123457000
        assert human_readable_number(123456789, digits=7) == 123456800
        assert human_readable_number(987654321, digits=8) == 987654320
        assert human_readable_number(123456789, digits=9) == 123456789
        assert human_readable_number(987654321, digits=10) == 987654321.0
        assert human_readable_number(1234567890, digits=10) == 1234567890.0
        assert human_readable_number(1234567890) == 1230000000
        assert human_readable_number(12345678900) == 12300000000
        assert human_readable_number(999999999) == 1000000000

    def test_human_readable_number_negative_large_numbers_varied(self):
        assert human_readable_number(-987654321) == -988000000
        assert human_readable_number(-1234567890, digits=4) == -1235000000
        assert human_readable_number(-123456789, digits=5) == -123460000
        assert human_readable_number(-123456789, digits=6) == -123457000
        assert human_readable_number(-123456789, digits=7) == -123456800
        assert human_readable_number(-987654321, digits=8) == -987654320
        assert human_readable_number(-123456789, digits=9) == -123456789
        assert human_readable_number(-987654321, digits=10) == -987654321.0
        assert human_readable_number(-1234567890, digits=10) == -1234567890.0
        assert human_readable_number(-1234567890) == -1230000000
        assert human_readable_number(-12345678900) == -12300000000
        assert human_readable_number(-999999999) == -1000000000








class TestHumanReadableNumberShortcuts:
    def test_human_readable_number_shortcut(self):
        assert human_readable_number_1(123.45) == 100
        assert human_readable_number_2(123.45) == 120
        assert human_readable_number_3(123.45) == 123
        assert human_readable_number_4(123.45) == 123.5


class TestHumanReadableSeconds:
    def test_human_readable_seconds(self):
        assert human_readable_seconds(0) == "0 secs"
        assert human_readable_seconds(1) == "1 secs"
        assert human_readable_seconds(59) == "59 secs"
        assert human_readable_seconds(60) == "1 min"
        assert human_readable_seconds(120) == "2 mins"
        assert human_readable_seconds(3600) == "1 hour"
        assert human_readable_seconds(3661) == "1 hour, 1 min, 1 sec"
        assert human_readable_seconds(86400) == "1 day"
        assert human_readable_seconds(86400 * 2) == "2 days"
        assert human_readable_seconds(604800) == "1 week"
        assert human_readable_seconds(604800 * 2) == "2 weeks"
        assert human_readable_seconds(604800 + 86400 + 3600 + 60) == "1 week, 1 day, 1 hour, 1 min"

    def test_human_readable_seconds_float(self):
        assert human_readable_seconds(0.5) == '0.5 secs'
        assert human_readable_seconds(60.5) == '1 min'
        assert human_readable_seconds(120.5) == '2 mins'


class TestHumanReadableBytes:
    def test_human_readable_bytes(self):
        assert human_readable_bytes(0) == "0.0 B"
        assert human_readable_bytes(1023) == "1023.0 B"
        assert human_readable_bytes(1024) == "1.0 KB"
        assert human_readable_bytes(1024 ** 2) == "1.0 MB"
        assert human_readable_bytes(1024 ** 3) == "1.0 GB"
        assert human_readable_bytes(1024 ** 4) == "1.0 TB"
        assert human_readable_bytes(1024 ** 5) == "1.0 PB"
        assert human_readable_bytes(1024 ** 6) == "1.0 EB"
        assert human_readable_bytes(1024 ** 7) == "1.0 ZB"
        assert human_readable_bytes(1024 ** 8) == "1.0 YB"
        assert human_readable_bytes(1024 ** 9) == "1024.0 YB"

    def test_human_readable_bytes_suffix(self):
        assert human_readable_bytes(1024, suffix="b") == "1.0 Kb"
        assert human_readable_bytes(1024 ** 2, suffix="byte") == "1.0 Mbyte"