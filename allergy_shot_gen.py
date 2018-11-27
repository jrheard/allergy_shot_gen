"""This is a little program that generates taskwarrior tasks to help me keep track of
when I need to go downtown for allergy shots.
"""
import argparse
import datetime

# TODO give allergy tag high urgency


# let's start by writing code to figure out the relevant days, and later on we can figure out taskwarrior stuff

def parse_args():
    parser = argparse.ArgumentParser(description='Generate a taskwarrior task that tells me when to get allergy shots.')
    parser.add_argument('--dry-run', action='store_true')
    return parser.parse_args()


def weekday_to_string(weekday_int):
    """Takes a number between 0 and 6, returns a string like "Wednesday"."""
    assert weekday_int in range(0, 7)

    return [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ][weekday_int]


def format_date(a_datetime):
    return a_datetime.strftime('%Y-%m-%d')


def main():
    args = parse_args()

    # TODO implement most_recent_shot_date arg
    today = datetime.datetime.today()

    # The allergy clinic is only open on weekdays,
    # so `earliest_possible` will always be a weekday.
    earliest_possible = today + datetime.timedelta(days=7)

    # `latest_possible` may not be a weekday, though:
    # if I got a shot on a Monday, then `latest_possible` will be a Sunday.
    latest_possible = today + datetime.timedelta(days=13)

    # The clinic's closed on Sundays, though, so let's round `latest_possible`
    # down to the nearest weekday.

    # a_datetime.weekday() returns an int 0 through 6, 5-6 are sat+sun.
    #
    # If latest_possible.weekday() is 6 (sunday), then we'll want to subtract 2 days
    # in order to clamp it to the previous friday. If it's 5 (saturday), we'll want to
    # subtract 1 day to clamp it to that same friday.
    days_to_subtract = latest_possible.weekday() - 4
    if days_to_subtract > 0:
        latest_possible = latest_possible - datetime.timedelta(days=days_to_subtract)

    if args.dry_run:
        print(
            'task add +ALLERGY pri:H wait:{wait} due:{due} get allergy shots, earliest day is {weekday} {date}'.format(
                wait=format_date(earliest_possible - datetime.timedelta(days=2)),
                due=format_date(latest_possible),
                weekday=weekday_to_string(earliest_possible.weekday()),
                date=earliest_possible.strftime('%m/%d')
            )
        )
    else:
        # TODO
        assert False



if __name__ == '__main__':
    main()
