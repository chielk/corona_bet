import csv
import datetime
import argparse
from typing import Iterable, List, Tuple, Union


timespan = Tuple[datetime.datetime, datetime.datetime]


class Bet:
    def __init__(self, person: str, date: str):
        self.person = person
        time = datetime.datetime.strptime(date, "%d-%m-%Y")
        self.min_time = time
        self.max_time = time + datetime.timedelta(days=1)

    def timedelta(self, time: datetime.datetime):
        if self.min_time < time < self.max_time:
            return 0
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decide who wins the Coronavirus bet')
    parser.add_argument('when', help="'dd-mm-yyyyThh:mm' OR now")
    parser.add_argument('--bets-file', default='bets.csv', help="The csv containing bets" )
    args = parser.parse_args()

    if args.when == 'now':
        target = datetime.datetime.now()
    else:
        target = datetime.datetime.strptime(args.when, "%d-%m-%YT%H:%M")

    print_winner(target, args.bets_file)

