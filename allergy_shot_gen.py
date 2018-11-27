"""This is a little program that generates taskwarrior tasks to help me keep track of
when I need to go downtown for allergy shots.
"""
import datetime


# let's start by writing code to figure out the relevant days, and later on we can figure out taskwarrior stuff

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



def main():
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


    print('Latest possible is {}'.format(weekday_to_string(latest_possible.weekday())))


if __name__ == '__main__':
    main()
