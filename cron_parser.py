"""
Python3 script for parsing a cron command into its respective elements (minute, hour, day of month, month, day of week, command)

Example input: 
*/15 0 1,15 * 1-5 /usr/bin/find

Example output:
minute 0 15 30 45
hour 0
day of month 1 15
month 1 2 3 4 5 6 7 8 9 10 11 12
day of week 1 2 3 4 5
command /usr/bin/find


Field	            Accepted Values
minute	            0-59
hour	            0-23
day of the month	1-31
month	            1-12 or names (see below)
day of the week	    0-7 (Sunday is 0 or 7) or names

All fields may contain an asterisk (*) which stands for any value.
Lists are allowed, and are numbers or ranges separated by commas e.g. 1,3,5,7, or 0-7,16-23.

@TODO
The output should be formatted as a table with the field name taking the first 14 columns and
the times as a space-separated list following it.
"""
import argparse

# dictionary of max allowed values in the format cron_position: (min_value, max_value)
MINMAX_VALUE_CONFIG = {
    # minutes
    0: (0, 59),
    # hours
    1: (0, 23),
    # day of the month
    2: (1, 31),
    # month
    3: (1, 12),
    # day of the week
    4: (0, 7)
}

CRON_POSITION_CONFIG = {
    0: 'minutes',
    1: 'hours',
    2: 'month_day',
    3: 'month',
    4: 'week_day'
}

def main():
    """
    Main function to parse arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('cron_command', type=str, help='The cron command to be parsed')
    args = parser.parse_args()

    cron_command = args.cron_command
    
    parse_cron_command(cron_command)
    
    return

def is_asterisk(value):
    return True if value == '*' else False

def is_single_number(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_dash_range(value):
    start, end = None, None
    if '-' in value:
        start, end = value.split('-')
        if is_single_number(start) and is_single_number(end) and int(start) <= int(end):
            return True
        else:
            raise ValueError('Invalid range values supplied')
    return start, end

def is_interval(value):
    interval = None
    if value.startswith('*/'):
        interval_list = value.split('/')
        interval = interval_list[-1]
        print(interval_list)
    return interval

def is_comma_range(value):
    value_list = None
    if ',' in value:
        value_list = value.split(',')
    return value_list


def parse_cron_command(cron_command: str):
    """
    Function to parse command string into separate elements
    """
    output_dict = {
        'minutes': [],
        'hours': [],
        'month_day': [],
        'month': [],
        'week_day': [],
        'command': ''
    }

    try:
        cron_list = cron_command.split(' ')

        for idx, cron_value in enumerate(cron_list):
            # print(idx, cron_value)
            current_cron_value = CRON_POSITION_CONFIG[idx]
            min_value = MINMAX_VALUE_CONFIG[idx][0]
            max_value = MINMAX_VALUE_CONFIG[idx][1]
            if idx == 5:
                output_dict['command'] = cron_value
            else:
                start, end = is_dash_range(cron_value)
                comma_range_list = is_comma_range(cron_value)
                # check if asterisk (all values)
                if is_asterisk(cron_value):
                    print('is asterisk')
                    for i in range(min_value, max_value + 1):
                        output_dict[current_cron_value].append(i)

                # check if single digit format
                elif is_single_number(cron_value):
                    output_dict[current_cron_value].append(int(cron_value))

                # check if range x-y format
                elif start and end:
                    for i in range(start, end + 1):
                        output_dict[current_cron_value].append(i)

                # check if range x,y,z format
                elif comma_range_list:
                    for i in comma_range_list:
                        output_dict[current_cron_value].append(i)
    
                else:
                    raise ValueError(f'Invalid format provided for {CRON_POSITION_CONFIG[idx]}, please try again')

                # TODO month and week day can be day/month names ?



    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

