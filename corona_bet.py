import csv
import datetime
import argparse
from typing import Iterable, List, Tuple, Union


timespan = Tuple[datetime.datetime, datetime.datetime]


def get_opening_time(date: datetime.datetime):
    """
    Monday	1pm     0
    Tuesday	1pm     1
    Wednesday   1pm     2
    Thursday    1pm     3
    Friday	12pm    4
    Saturday    12pm    5
    Sunday      12pm    6
    """
    day_names = {0: "Monday",
                 1: "Tuesday",
                 2: "Wednesday",
                 3: "Thursday",
                 4: "Friday",
                 5: "Saturday",
                 6: "Sunday"
                }
    if (weekday := date.weekday()) < 4:
        return day_names[weekday], datetime.timedelta(hours=13)
    else:
        return day_names[weekday], datetime.timedelta(hours=12)



class Bet:
    def __init__(self, person: str, date: str):
        self.person = person
        time = datetime.datetime.strptime(date, "%d-%m-%Y")
        self.min_time = time
        self.max_time = time + datetime.timedelta(days=1)

    def timedelta(self, time: datetime.datetime):
        if self.min_time < time < self.max_time:
            return datetime.timedelta()
        if time < self.min_time:
            return self.min_time - time
        return time - self.max_time

    def __str__(self):
        date_str = datetime.datetime.strftime(self.min_time, "%d-%m-%Y")
        return f"{self.person}'s bet on {date_str}"

    def __repr__(self):
        return (f'Bet("{self.person}", ' \
                f'"{datetime.datetime.strftime(self.min_time, "%d-%m-%Y")}")')


def sort_closest(target: datetime.datetime, bets: Iterable[Bet]) -> List[Bet]:
    return sorted(bets, key=lambda b: b.timedelta(target))


def load_bets(bets_filename):
    bets = []
    with open('bets.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for person, date in reader:
            bets.append(Bet(person, date))
    return bets

def print_winner(target, bets_filename):
    bets = load_bets(bets_filename)

    # Bets sorted chronologically
    bets_sorted = sorted(bets, key=lambda b: b.min_time)


    bets_sorted_closest = sort_closest(target, bets)
    winning_bet = bets_sorted_closest[0]
    print(f"Closest: {winning_bet}, with a distance of {winning_bet.timedelta(target)}")

    winner_index = bets_sorted.index(winning_bet)
    if winner_index > 0:
        print("No longer elegible to win:")
        for bet in bets_sorted[:winner_index]:
            print(bet)


def parse_time(when: str):
    formats = [ "%d-%m-%Y",
               "%d/%m/%Y",
              ]
    for date_format in formats:
        try:
            return datetime.datetime.strptime(args.when, date_format)
        except ValueError:
            pass
    raise ValueError(f"Unable to parse date: {when}")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decide who wins the Coronavirus bet')
    parser.add_argument('when', help="'dd-mm-yyyyThh:mm' OR now")
    parser.add_argument('--bets-file', default='bets.csv', help="The csv containing bets" )
    args = parser.parse_args()

    if args.when == 'now':
        target = datetime.datetime.now()
    else:
        target = parse_time(args.when)
        day, opening_time = get_opening_time(target)
        print(f"Opening time on {day} is {opening_time}.")
        target += opening_time
    print_winner(target, args.bets_file)

