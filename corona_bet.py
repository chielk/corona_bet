import csv
import datetime
from typing import Iterable, List


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
        return (f'Bet("{self.person}", ' \
                f'"{datetime.datetime.strftime(self.min_time, "%d/%m/%Y")}")')


def sort_closest(now: datetime.datetime, bets: Iterable[Bet]) -> List[Bet]:
    return sorted(bets, key=lambda b: b.timedelta(now))


def print_winner():
    bets = []
    with open('bets.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for person, date in reader:
            bets.append(Bet(person, date))


    # Bets sorted chronologically
    bets_sorted = sorted(bets, key=lambda b: b.min_time)

    # TODO: allow for user-specified time
    now = datetime.datetime.now()

    bets_sorted_closest = sort_closest(now, bets)
    winning_bet = bets_sorted_closest[0]
    print(f"Closest: {winning_bet}, distance: {winning_bet.timedelta(now)}")

    winner_index = bets_sorted.index(winning_bet)
    if winner_index > 0:
        print("No longer elegible to win:")
        for bet in bets_sorted[:winner_index]:
            print(bet)


if __name__ == "__main__":
    print_winner()

