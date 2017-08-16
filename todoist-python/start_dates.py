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
    pass

'''
Takes a string with a date in the old format and returns a datetime object
    Expected form: "%02d%02d%02d" % (month, day, year)

@param str the string containing the date
@returns datetime object with the same date as the string
'''
def parse_old_date(str):
    pass

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
            if START_TAG in name:
                pos = name.find(START_TAG)
                error_str += "before int conversion\n"
                day = int(name[(pos+DAY_OFFSET):(pos+DAY_OFFSET+DAY_LEN)])
                mon = int(name[(pos+MON_OFFSET):(pos+MON_OFFSET+MON_LEN)])
                year = int(name[(pos+YEAR_OFFSET):(pos+YEAR_OFFSET+YEAR_LEN)])
                hour = 0
                minute = 0
                error_str += "after int conversion\n"

                has_time = ((pos + TIME_TAG_OFFSET) < len(name) and
                            name[pos + TIME_TAG_OFFSET] == TIME_TAG)
                if has_time:
                    error_str += "before time int conversion\n"
                    hour = int(name[(pos+HOUR_OFFSET):(pos+HOUR_OFFSET+HOUR_LEN)])
                    minute = int(name[(pos+MIN_OFFSET):(pos+MIN_OFFSET+MIN_LEN)])
                    error_str += "after time int conversion\n"

                item_id = item['id']
                item_labels = item['labels']
                if has_started(day, mon, year, hour, minute, has_time):
                    item_labels.append(start_label_id)
                    name = name[0:pos]
                    api.items.update(item_id, labels=item_labels, content=name)
                else:
                    if start_label_id in item_labels:
                        item_labels.remove(start_label_id)
                        api.items.update(item_id, labels=item_labels)

            elif DURATION_TAG in name:
                print("huh, this task has a delay tag... wish I could help: %s" %
                      name)
            else:
                item_id = item['id']
                item_labels = item['labels']
                if item_labels.count(start_label_id) == 0:
                    item_labels.append(start_label_id)
                    api.items.update(item_id, labels=item_labels)
        except:
            print("task: %s has an invalid start date string" % name)
            print("error str = \n%s" % error_str)

    api.commit()


def run_tests():
    success = 0

    print()


    return success
