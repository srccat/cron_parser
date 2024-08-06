"""
Python3 script for parsing a cron command into its respective elements (minute, hour, day of month, month, day of week, command)

Example input: 
*/15 0 1,15 * 1-5 /usr/bin/find

Example output:
minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find


References used for crontab format: 
https://docs.hostdime.com/hd/command-line/working-with-cron-jobs

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

@TODO
Month and day of the week may also take month/day arguments e.g. 'Monday'
"""
import argparse
from functools import reduce
from typing import Optional, Tuple

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

# dictionary of cron tab fields in the format array_idx : field_name
CRON_POSITION_CONFIG = {
    0: 'minute',
    1: 'hour',
    2: 'day of month',
    3: 'month',
    4: 'day of week',
    5: 'command'
}

DEFAULT_HEADER_COL_LENGTH = 14

def main():
    """
    Main function to parse arguments and print output table
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('cron_command', type=str, help='The cron command to be parsed')
    args = parser.parse_args()

    cron_command = args.cron_command
    
    output_data = parse_cron_command(cron_command)

    output_table = format_output_values(output_data)
    
    return

def is_asterisk(value: str) -> bool:
    '''
    Check if cron value is * value (all legal values allowed)
    '''
    return True if value == '*' else False

def is_single_number(value: str) -> bool:
    '''
    Check if cron value is a single integer
    '''
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_dash_range(value: str) -> Tuple[Optional[int], Optional[int]]:
    '''
    Check if cron value is a dash range x-y
    '''
    start_num, end_num = None, None
    if '-' in value:
        start, end = value.split('-')
        start_num, end_num = int(start), int(end)
        if is_single_number(start) and is_single_number(end) and start_num <= end_num:
            return start_num, end_num
        else:
            raise ValueError('Invalid range values supplied')
    return start_num, end_num

def is_interval(value: str) -> Optional[int]:
    '''
    Check if cron value is an interval value */x
    '''
    interval = None
    if value.startswith('*/'):
        interval_list = value.split('/')
        interval = int(interval_list[-1])
    return interval

def is_comma_range(value: str) -> Optional[list]:
    '''
    Check if cron value is a comma range x,y,z
    '''
    value_list = None
    if ',' in value:
        value_list = value.split(',')
    return value_list


def parse_cron_command(cron_command: str) -> dict:
    """
    Function to parse command string into separate elements
    """
    output_dict = {
        'minute': [],
        'hour': [],
        'day of month': [],
        'month': [],
        'day of week': [],
        'command': []
    }

    try:
        cron_list = cron_command.split(' ')

        for idx, cron_value in enumerate(cron_list):
            current_cron_value = CRON_POSITION_CONFIG[idx]
            if current_cron_value == 'command':
                output_dict['command'].append(cron_value)
            else:
                min_value = MINMAX_VALUE_CONFIG[idx][0]
                max_value = MINMAX_VALUE_CONFIG[idx][1]

                start, end = is_dash_range(cron_value)
                comma_range_list = is_comma_range(cron_value)
                interval_value = is_interval(cron_value)

                # check if asterisk *
                if is_asterisk(cron_value):
                    # print('%s is asterisk' % current_cron_value)
                    for i in range(min_value, max_value + 1):
                        output_dict[current_cron_value].append(str(i))

                # check if single digit x format
                elif is_single_number(cron_value):
                    # print('%s is single number' % current_cron_value)
                    output_dict[current_cron_value].append(str(cron_value))

                # check if interval */x format
                elif is_interval(cron_value):
                    # print('%s is interval' % current_cron_value)
                    for i in range(min_value, max_value, interval_value):
                        output_dict[current_cron_value].append(str(i))

                # check if range x-y format
                elif start and end:
                    # print('%s is dash range' % current_cron_value)
                    for i in range(start, end + 1):
                        output_dict[current_cron_value].append(str(i))

                # check if range x,y,z format
                elif comma_range_list:
                    # print('%s is comma range' % current_cron_value)
                    for i in comma_range_list:
                        output_dict[current_cron_value].append(str(i))
    
                else:
                    raise ValueError(f'Invalid format provided for {CRON_POSITION_CONFIG[idx]}, please try again')

    except Exception as e:
        # @TODO error handling
        print(e)

    return output_dict

def format_output_values(output_data: dict) -> str:
    '''
    Format output data into a table with first column length of 14 
    and the values following as a space-separated list
    '''
    for header, values in output_data.items():
        formatted_header = header
        formatted_values = ''
        header_length = len(header)
        if header_length < DEFAULT_HEADER_COL_LENGTH:
            spaces_to_add = ' ' * (DEFAULT_HEADER_COL_LENGTH - header_length)
            formatted_header = f'{header}{spaces_to_add}'
        
        formatted_values = reduce(lambda x,y: x + ' ' + y, values)

    formatted_output = f'{formatted_header}{formatted_values}'
    
    return formatted_output

if __name__ == "__main__":
    main()
