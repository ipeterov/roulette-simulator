import random

import matplotlib.pyplot as plt


class Player:
    def __init__(self, starting_balance: int):
        self.balance = starting_balance

    def make_a_bet(self) -> tuple[str, int]:
        raise NotImplementedError()

    def record_result(self, payoff: int):
        pass


class AHundredOnBlack(Player):
    def make_a_bet(self) -> tuple[str, int]:
        return "black", 100


class Doubler(Player):
    MINIMAL_BET = 100
    MAXIMUM_BET = 10000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_bet = self.MINIMAL_BET

    def make_a_bet(self) -> tuple[str, int]:
        return "black", self.current_bet

    def record_result(self, payoff: int):
        if not payoff:
            new_bet = self.current_bet * 2
        else:
            new_bet = self.MINIMAL_BET

        new_bet = min(self.MAXIMUM_BET, new_bet)
        self.current_bet = min(self.balance, new_bet)


class RouletteGame:
    CHOICES_WITH_PROBABILITIES = {
        "red": 18 / 37,
        "black": 18 / 37,
        "green": 1 / 37,
    }
    PAYOFF_MULTIPLIERS = {
        "red": 2,
        "black": 2,
        "green": 35,
    }

    def run_simulation(self, player: Player, n_rounds: int) -> list[int]:
        """
        Run the simulation and return the graph of the player's balance over time.
        """

        balance_history = []
        for _ in range(n_rounds):
            bet, amount = player.make_a_bet()

            if player.balance < amount:
                print("Player tried to bet more than they had")
                break
            elif player.balance == 0:
                print("Player spent all their money")
                break

            player.balance -= amount
            payoff = self.evaluate_bet(bet, amount)
            player.balance += payoff
            balance_history.append(player.balance)

            player.record_result(payoff)

        return balance_history

    def evaluate_bet(self, bet: str, amount: int) -> int:
        assert bet in self.CHOICES_WITH_PROBABILITIES

        # Pick a random result according to the probability distribution
        result = random.choices(
            list(self.CHOICES_WITH_PROBABILITIES.keys()),
            list(self.CHOICES_WITH_PROBABILITIES.values()),
        )[0]

        if result == bet:
            return amount * self.PAYOFF_MULTIPLIERS[bet]
        else:
            return 0


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    BALANCE = 1000000

    player = Doubler(starting_balance=BALANCE)
    game = RouletteGame()

    balance_history = game.run_simulation(player, n_rounds=10000)

    fig, ax = plt.subplots()
    ax.plot(balance_history)
    ax.set_ylim(ymin=0)
    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
