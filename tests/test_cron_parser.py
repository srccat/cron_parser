import unittest
from cron_parser import parse_cron_command, format_output_values


class TestCronParser(unittest.TestCase):
    def test_parser_succeeds_with_valid_cron(self):
        valid_cron = '*/15 0 1,15 * 1-5 /usr/bin/find'
        expected_output = {
            'minute': ['0', '15', '30', '45'],
            'hour': ['0'],
            'day of month': ['1', '15'],
            'month': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            'day of week': ['1', '2', '3', '4', '5'],
            'command': ['/usr/bin/find']
        }

        output_data = parse_cron_command(valid_cron)

        self.assertEqual(output_data, expected_output)

    def test_parser_fails_with_invalid_format(self):
        invalid_cron = '1/15 0 1,15 * 1-5 /usr/bin/find'
        expected_message = 'Invalid format for minute field'

        with self.assertRaises(ValueError) as error:
            parse_cron_command(invalid_cron)
        self.assertEqual(str(error.exception), expected_message)

    def test_parser_fails_with_invalid_start_end(self):
        # end value of range is lower than start
        invalid_cron = '*/15 0 1,15 * 1-0 /usr/bin/find'
        expected_message = 'Invalid range values supplied'

        with self.assertRaises(ValueError) as error:
            parse_cron_command(invalid_cron)
        self.assertEqual(str(error.exception), expected_message)

    def test_parser_fails_with_invalid_month_day(self):
        invalid_cron = '*/15 0 1-45 * 1-5 /usr/bin/find'
        expected_message = 'day of month end value is outside allowed range'

        with self.assertRaises(ValueError) as error:
            parse_cron_command(invalid_cron)
        self.assertEqual(str(error.exception), expected_message)

    def test_parser_fails_with_invalid_week_day(self):
        invalid_cron = '*/15 0 1-15 * 1-8 /usr/bin/find'
        expected_message = 'day of week end value is outside allowed range'

        with self.assertRaises(ValueError) as error:
            parse_cron_command(invalid_cron)
        self.assertEqual(str(error.exception), expected_message)

    def test_parser_fails_with_invalid_month(self):
        invalid_cron = '*/15 0 1-15 13 1-8 /usr/bin/find'
        expected_message = 'month value is outside allowed range'

        with self.assertRaises(ValueError) as error:
            parse_cron_command(invalid_cron)
        self.assertEqual(str(error.exception), expected_message)

    def test_output_table_format(self):
        test_output_data = {
            'minute': ['0', '15', '30', '45'],
            'hour': ['0'],
            'day of month': ['1', '15'],
            'month': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            'day of week': ['1', '2', '3', '4', '5'],
            'command': ['/usr/bin/find']
        }

        expected_table_output = (
            "minute        0 15 30 45\n"
            "hour          0\n"
            "day of month  1 15\n"
            "month         1 2 3 4 5 6 7 8 9 10 11 12\n"
            "day of week   1 2 3 4 5\n"
            "command       /usr/bin/find\n"
        )

        output_table = format_output_values(test_output_data)

        self.assertEqual(output_table, expected_table_output)
