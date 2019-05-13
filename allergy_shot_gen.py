"""This is a little program that generates taskwarrior tasks to help me keep track of
when I need to go downtown for allergy shots.
"""
import argparse
import datetime
import os

import taskw


def parse_args():
    parser = argparse.ArgumentParser(description='Generate a taskwarrior task that tells me when to get allergy shots.')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--most-recent-shot-date')
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

    if args.most_recent_shot_date:
        today = datetime.datetime.strptime(args.most_recent_shot_date, '%m/%d/%Y')
    else:
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
        latest_possible -= datetime.timedelta(days=days_to_subtract)

    # In taskwarrior, if you mark a task as due on a Tuesday, that means that it's due
    # at midnight Tuesday morning, and during the day on Tuesday the task will display
    # as due in eg -12h. I don't want that behavior to happen until I'm _overdue_,
    # so we'll add a day to latest_possible in order to get this due-display behavior
    # working the way I want.
    due = latest_possible + datetime.timedelta(days=1)

    # I want the task to be hidden until a couple of days before earliest_possible.
    wait_until = earliest_possible - datetime.timedelta(days=2)

    task_description = 'get allergy shots between {earliest_weekday} {earliest_date} and {latest_weekday} {latest_date}'.format(
        earliest_weekday=weekday_to_string(earliest_possible.weekday()),
        earliest_date=earliest_possible.strftime('%m/%d'),
        latest_weekday=weekday_to_string(latest_possible.weekday()),
        latest_date=latest_possible.strftime('%m/%d'),
    )

    task_command = 'task add +ALLERGY pri:H wait:{wait} due:{due} {description} && task sync'.format(
        wait=format_date(wait_until),
        due=format_date(due),
        description=task_description,
    )

    if args.dry_run:
        print(task_command)
    else:
        w = taskw.TaskWarrior()

        preexisting_tasks = w.filter_tasks({'status': 'pending', 'tags': 'ALLERGY'}) + w.filter_tasks({'status': 'waiting', 'tags': 'ALLERGY'})
        assert len(preexisting_tasks) in [0, 1]

        if not preexisting_tasks:
            os.system(task_command)



if __name__ == '__main__':
    main()
