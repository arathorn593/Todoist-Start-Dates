import todoist
from datetime import *
import sys

API_TOKEN='1d585b7f68e32d1a22290dbf11a91c7884bde7b8'

# tag format: $TAGddmmyy_hhmm
#   ex: \s061517_2130 -> start date of June 15th 2017 at 9:30 pm
#   time is 24 hour and is optional. Thus \s061517 is also valid
START_TAG='\s'
DURATION_TAG='\d'
IN_DURATION_TAG='\i'

MON_OFFSET=2        # offset from start of tag to month
MON_LEN=2           # number of chars for month
DAY_OFFSET=4        # offset from start of tag to day
DAY_LEN=2           # number of chars for day
YEAR_OFFSET=6       # offset from start of tag to year
YEAR_LEN=2          # number of chars for year
TIME_TAG_OFFSET=8   # offset from start of tag to underscore marking time
TIME_TAG='_'
HOUR_OFFSET=9       # offset from start of (main) tag to hours
HOUR_LEN=2
MIN_OFFSET=11       # offset from start of (main) tag to minutes
MIN_LEN=2
LABEL_NAME="Started"

'''
Finds the date or duration string in an item name

@param name the item name to look for the date/duration string in
@param the tag that signals the start of the date/duration string
@returns the date/duration string right after the tag in the item name
'''
def get_tag_str(item_name, tag):
    tag_start = name.find(tag)
    # if no space before end of line, tag_end=-1 which works
    tag_end = name.find(" ", tag_start, -1)

    tag_str = name[(tag_start + len(tag)):tag_end]

'''
Takes a string with a date and returns a date object

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

@param str the string containing the date with dashes or slashes
@returns datetime object with the same date as the string
'''
def parse_sep_date(str):
    return datetime.min

'''
Takes a string with a date in the old format and returns a datetime object
    Expected form: "%02d%02d%02d" % (month, day, year)

@param str the string containing the date
@returns datetime object with the same date as the string
'''
def parse_old_date(str):
    return datetime.min

'''
Takes a string with a time duration and returns a timedelta object
    Ex: 5d1m2y = 5 days 1 month 2 years
        Month, day, and/or years may be ommitted. An empty string will return
        a timedelta object of zero
@param str the string with the duration to convert
@returns a timedelta object corresponding to the duration given in str
'''
def parse_duration(str):
    return timedelta()

# ------------- MAIN PROGRAM ----------------
if __name__ == "__main__":
    if (len(sys.argv) > 1 and sys.argv[1] == 'test'):
        result = run_tests()
        sys.exit(status=result)

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


def run_tests():
    passed = True

    print("Testing get_tag_str...")
    inputs_outputs = [("hello \s081217", "\s", "081217"),
                      ("\d08-1225af hi", "\d", "08-1225af"),
                      ("test\i52345 hi", "\i", "52345"),
                      ("test \s12345 test", "\s", "12345")]
    for io in inputs_outputs:
        (i0, i1, o) = io
        ao = get_tag_str(i0, i1)
        if (ao != o):
            print("test FAILED: get_tag_str(%s, %s)" % (i0, i1))
            print("Expected: %s\nActual output:%s" % (o, ao))
            passed = False
        else:
            print("pass: get_tag_str(%s, %s) = %s" % (i0, i1, o))
    print("\n\n\n")

    print("Testing parse_sep_date...")
    now = datetime.today()
    inputs_outputs_sep_date = [("08-17-17", datetime(2017, 8, 17)),
                               ("8-44", (datetime(now.year, 8, 31) if datetime(now.year, 8, 31) > now else datetime(now.year+1, 8, 31))),
                               ("9-31-20", datetime(2020, 9, 30)),
                               ("12-1-18", datetime(2018, 12, 1)),
                               ("12-08", (datetime(now.year, 12, 8) if datetime(now.year, 12, 8) > now else datetime(now.year+1, 12, 8))),
                               ("1-1", datetime(now.year+1, 1, 1)),
                               ("5/6/17", datetime(2017, 5, 6)),
                               ("7/4", (datetime(now.year, 7, 4) if datetime(now.year, 7, 4) > now else datetime(now.year+1, 12, 8)))]
    for io in inputs_outputs_sep_date:
        (i, o) = io
        ao = parse_sep_date(i)
        if (ao != o):
            print("test FAILED: parse_sep_date(%s)" % i)
            print("Expectd: %s\nActual output:%s" % (o, ao))
            passed = False
        else:
            print("pass: parse_sep_date(%s) = %s" % (i, o))
    print("\n\n\n")

    print("Testing parse_old_date...")
    print("\n\n\n")

    print("Testing parse_date...")
    print("\n\n\n")

    print("Testing parse_duration...")
    print("\n\n\n")

    if passed:
        return 0
    else:
        return 1
