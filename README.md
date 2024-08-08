Requirements:
* Python 3.12.4

The command to run the script is in the format:
- python3 cron_parser.py 'cron_to_parse'

Example command to run script: 
- python3 cron_parser.py '*/15 0 1,15 * 1-5 /usr/bin/find'

To run tests:
- python3 -m unittest tests/test_cron_parser.py

To run this program, please first ensure you have Python 3.12.4 installed on your system.
Then, open up a terminal and run a command following the example structure above, replacing the cron command with one you would like to parse.
