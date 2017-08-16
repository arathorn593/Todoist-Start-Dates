import todoist
from datetime import *
import sys
import calendar

def run_tests():
    passed = True
    now = datetime.today()

    print("Testing get_tag_str...\n")
    inputs_outputs = [("hello \s081217", "\s", "081217"),
                      ("\\b08-1225af hi", "\\b", "08-1225af"),
                      ("test\i52345 hi", "\i", "52345"),
                      ("test \s12345 test", "\s", "12345")]
    for io in inputs_outputs:
        (i0, i1, o) = io
        ao = get_tag_str(i0, i1)
        if (ao != o):
            print("test FAILED: get_tag_str('%s', '%s')" % (i0, i1))
            print("\tExpected: '%s'\n\tActual output: '%s'" % (o, ao))
            passed = False
        else:
            print("pass: get_tag_str('%s', '%s') = '%s'" % (i0, i1, o))
    print("\n\n\n")

    print("Testing parse_sep_date...\n")
    inputs_outputs_sep_date = [("08-17-17", datetime(2017, 8, 17)),
                               ("8-44", (datetime(now.year, 8, 31) if datetime(now.year, 8, 31) > now else datetime(now.year+1, 8, 31))),
                               ("9-31-20", datetime(2020, 9, 30)),
                               ("12-1-18", datetime(2018, 12, 1)),
                               ("12-08", (datetime(now.year, 12, 8) if datetime(now.year, 12, 8) > now else datetime(now.year+1, 12, 8))),
                               ("1-1", datetime(now.year+1, 1, 1)),
                               ("5/6/17", datetime(2017, 5, 6)),
                               ("7/4", (datetime(now.year, 7, 4) if datetime(now.year, 7, 4) > now else datetime(now.year+1, 7, 4)))]
    for io in inputs_outputs_sep_date:
        (i, o) = io
        ao = parse_sep_date(i)
        if (ao != o):
            print("test FAILED: parse_sep_date('%s')" % i)
            print("\tExpectd: '%s'\n\tActual output: '%s'" % (o, ao))
            passed = False
        else:
            print("pass: parse_sep_date('%s') = '%s'" % (i, o))
    print("\n\n\n")

    print("Testing parse_old_date...\n")
    inputs_outputs_old_date = [("081717", datetime(2017, 8, 17)),
                               ("083117", datetime(2017, 8, 31)),
                               ("093020", datetime(2020, 9, 30)),
                               ("120118", datetime(2018, 12, 1)),
                               ("120817", datetime(2017, 12, 8)),
                               ("010118", datetime(2018, 1, 1)),
                               ("050617", datetime(2017, 5, 6)),
                               ("070417", datetime(2017, 7, 4)),
                               ("111117", datetime(2017, 11, 11))]
    for io in inputs_outputs_old_date:
        (i, o) = io
        ao = parse_old_date(i)
        if (ao != o):
            print("test FAILED: parse_old_date('%s')" % i)
            print("\tExpected: '%s'\n\tActual output: '%s'" % (o, ao))
            passed = False
        else:
            print("pass: parse_sep_date('%s') = '%s'" % (i, o))
    print("\n\n\n")

    print("Testing parse_date...\n")
    inputs_outputs = []
    inputs_outputs.extend(inputs_outputs_sep_date)
    inputs_outputs.extend(inputs_outputs_old_date)
    for io in inputs_outputs:
        (i, o) = io
        ao = parse_date(i)
        if (ao != o):
            print("test FAILED: parse_date('%s')" % i)
            print("\tExpected: '%s'\n\tActual output: '%s'" % (o, ao))
            passed = False
        else:
            print("pass: parse_date('%s') = '%s'" % (i, o))
    print("\n\n\n")

    print("Testing parse_duration...\n")
    inputs_outputs = [("", (0, 0, 0)),
                      ("1d", (1, 0, 0)),
                      ("3m", (0, 3, 0)),
                      ("5y", (0, 0, 5)),
                      ("5d3m", (5, 3, 0)),
                      ("60d1y", (60, 0, 1)),
                      ("14m24y", (0, 14, 24)),
                      ("24d9m2y", (24, 9, 2))]
    for io in inputs_outputs:
        (i, o) = io
        ao = parse_duration(i)
        if (ao != o):
            print("test FAILED: parse_duration('%s')" % i)
            print("\tExpected: '%s'\n\tAcutal output: '%s'" % (o, ao))
            passed = False
        else:
            print("pass: parse_duration('%s') = '%s'" % (i, o))
    print("\n\n\n")

    print("Testing parse_duration_after...\n")
    inputs_outputs = [("", datetime(2017, 8, 16), datetime(2017, 8, 16)),
                      ("1d", datetime(2017, 1, 1), datetime(2017, 1, 2)),
                      ("2d", datetime(2017, 1, 29), datetime(2017, 1, 31)),
                      ("2d", datetime(2017, 4, 29), datetime(2017, 5, 1)),
                      ("5d2m", datetime(2017, 11, 27), datetime(2018, 2, 1)),
                      ("3m2y", datetime(2017, 4, 4), datetime(2019, 7, 4)),
                      ("24d3m1y", datetime(2018, 5, 19), datetime(2019, 9, 12))]
    for io in inputs_outputs:
        (i0, i1, o) = io
        ao = parse_duration_after(i0, i1)
        if (ao != o):
            print("test FAILED: parse_duration_after('%s', '%s')" % (i0, i1))
            print("\tExpected: '%s'\nAcutal output: '%s'" % (o, ao))
            passed = False
        else:
            print("pass: parse_duration_after('%s', '%s') = '%s'" % (i0, i1, o))
    print("\n\n\n")

    print("Testing parse_duration_before...\n")
    for io in inputs_outputs:
        (i0, o, i1) = io
        ao = parse_duration_before(i0, i1)
        if (ao != o):
            print("test FAILED: parse_duration_after('%s', '%s')" % (i0, i1))
            print("\tExpected: '%s'\n\tActual output: '%s'" % (o, ao))
            passed = False
        else:
            print("pass: parse_duration_after('%s', '%s') = '%s'" % (i0, i1, o))
    print("\n\n\n")

    if passed:
        print("All tests PASSED!")
        return 0
    else:
        print("Some tests FAILED!")
        return 1

API_TOKEN='1d585b7f68e32d1a22290dbf11a91c7884bde7b8'

# tag format: $TAGddmmyy_hhmm
#   ex: \s061517_2130 -> start date of June 15th 2017 at 9:30 pm
#   time is 24 hour and is optional. Thus \s061517 is also valid
START_TAG='\\s'
BEFORE_TAG='\\b'
IN_TAG='\\i'

MON_OFFSET=0        # offset from start of tag to month
MON_LEN=2           # number of chars for month
DAY_OFFSET=2        # offset from start of tag to day
DAY_LEN=2           # number of chars for day
YEAR_OFFSET=4       # offset from start of tag to year
YEAR_LEN=2          # number of chars for year

LABEL_NAME="Started"

'''
constrains value to the range [min_val, max_val]

@param val value to constrain
@param min_val inclusive lower bound of range
@param max_val inclusive upper bound of range
@returns constrained value
'''
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

'''
Finds the date or duration string in an item name

@param name the item name to look for the date/duration string in
@param the tag that signals the start of the date/duration string
@returns the date/duration string right after the tag in the item name
'''
def get_tag_str(item_name, tag):
    tag_start = item_name.find(tag)

    tag_end = item_name.find(" ", tag_start, -1)

    if tag_end == -1:
        tag_str = item_name[(tag_start + len(tag)):]
    else:
        tag_str = item_name[(tag_start + len(tag)):tag_end]

    return tag_str

'''
Takes a string with a date and returns a date object (next date not passed
assumed if year ommitted)

@param str the string containing a date
@return datetime object with the same date as the string
'''
def parse_date(str):
    if ('-' in str or '/' in str):
        return parse_sep_date(str)
    else:
        return parse_old_date(str)

'''
Takes a string with a date with separators (- or /) and returns a datetime obj
    Expected form: "8-13-17" or "8-13" (year optional) Aug. 13th 2017
                   "8/13/17" or "8/13" (year optional) Aug. 13th 2017
(next date not passed assumed if year ommitted)

@param date_str the string containing the date with dashes or slashes
@returns datetime object with the same date as the string
'''
def parse_sep_date(date_str):
    now = datetime.today()

    nums = []
    if ('-' in date_str):
        nums = date_str.split('-')
    else:
        nums = date_str.split('/')

    (day, month, year) = (0, 0, 0)
    no_year = False
    try:
        if (len(nums) >= 1):
            month = int(nums[0])
        else:
            month = now.month
        if (len(nums) >= 2):
            day = int(nums[1])
        else:
            day = now.day
        if (len(nums) >= 3):
            year = int(nums[2]) + 2000
        else:
            no_year = True
            year = now.year
    except(ValueError):
        return now

    year = constrain(year, MINYEAR, MAXYEAR)
    month = constrain(month, 1, 12)

    (weekday, max_day) = calendar.monthrange(year, month)
    day = constrain(day, 1, max_day)

    result = datetime(year, month, day)
    # make sure date is in the future
    if (no_year and result < now):
        result = datetime(year + 1, month, day)

    return result

'''
Takes a string with a date in the old format and returns a datetime object
    Expected form: "%02d%02d%02d" % (month, day, year)

@param date_str the string containing the date
@returns datetime object with the same date as the string
'''
def parse_old_date(date_str):
    now = datetime.today()
    (day, month, year) = (0, 0, 0)

    try:
        month = int(date_str[MON_OFFSET:(MON_OFFSET + MON_LEN)])
        day = int(date_str[DAY_OFFSET:(DAY_OFFSET + DAY_LEN)])
        year = int(date_str[YEAR_OFFSET:(YEAR_OFFSET + YEAR_LEN)]) + 2000
    except(ValueError):
        return now

    year = constrain(year, MINYEAR, MAXYEAR)
    month = constrain(month, 1, 12)

    (weekday, max_day) = calendar.monthrange(year, month)
    day = constrain(day, 1, max_day)

    result = datetime(year, month, day)

    return result

'''
Takes a string and returns the days, months, and years specified by the string
    Ex: 5d1m2y = 5 days 1 month 2 years
        Month, day, and/or years may be ommitted. An empty string will return
        a timedelta object of zero

@param dur_str the duration string to parse
@returns a tuple with the day, month, and year of the duration str: (d, m, y)
'''
def parse_duration(dur_str):
    (days, months, years) = (0, 0, 0)

    num_str = ""
    for c in dur_str:
        try:
            if c.isdigit():
                num_str += c
            elif c == 'd':
                days = int(num_str)
                num_str = ""
            elif c == 'm':
                months = int(num_str)
                num_str = ""
            elif c == 'y':
                years = int(num_str)
                num_str = ""
            else:
                num_str = ""
        except(ValueError):
            pass

    return (days, months, years)

'''
Takes a string with a time duration and returns a datetime object that duration
before the other datetime object passed in

@param str the string with the duration to convert
@param date the datetime object the result is based off
@returns a datetime object the given duration before the given date
'''
def parse_duration_before(dur_str, date):
    return datetime.min

'''
Takes a string with a time duration and a date and returns a datetime object
that duration after the date

@param str the duration string
@param date datetime object for the starting point of the duration
@returns the datetime object the given duration after the given date
'''
def parse_duration_after(dur_str, date):
    return datetime.min

# ------------- MAIN PROGRAM ----------------
if __name__ == "__main__":
    if (len(sys.argv) > 1 and sys.argv[1] == 'test'):
        result = run_tests()
        sys.exit(result)

    api = todoist.TodoistAPI(API_TOKEN)

    # make sure we reset so sync will grab everything
    api.reset_state()

    response = api.sync()

    items = response['items']

    labels = response['labels']
    start_label_id = 0;
    for label in labels:
        if label['name'] == LABEL_NAME:
            start_label_id = label['id']
            break

    for item in items:
        name = item['content']

        try:
            error_str = ""
            tag_str = ""
            add_label = False

            if START_TAG in name:
                now = datetime.today()
                tag_str = get_tag_str(name, START_TAG)

                item_date = parse_date(tag_str)

                add_label = item_date < now
            elif DURATION_TAG in name:
                print("huh, this task has a delay tag... wish I could help: %s" %
                      name)

            # Update tag if need be
            item_id = item['id']
            item_labels = item['labels']
            if add_label:
                item_labels.append(start_label_id)
                name = name.replace(tag_str, "")
                api.items.update(item_id, labels=item_labels, content=name)
            else:
                if start_label_id in item_labels:
                    item_labels.remove(start_label_id)
                    api.items.update(item_id, labels=item_labels)
        except:
            print("task: %s has an invalid start date string" % name)
            print("error str = \n%s" % error_str)

    api.commit()
