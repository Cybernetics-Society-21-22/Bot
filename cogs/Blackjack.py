import random
from discord.ext import commands
import black


class Card:  # Makes and Shows a Card
    def __init__(self, value, suit):
        self.cost = value
        self.value = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"][
            value - 1
        ]  # All possible values of the card
        self.suit = "♥♦♣♠"[suit]  # 4 possible suits, purely for decoration

    def show(self):
        return f"```┌─────────┐ \
               \n| {self.value:<2}      | \
               \n|         | \
               \n|    {self.suit}    | \
               \n|         | \
               \n|      {self.value:>2} | \
               \n└─────────┘```"  # This just prints a nice ascii representation of the card

    def price(self):
        if self.cost >= 10:
            return 10  # Jack Queen King get converted to 10
        elif self.cost == 1:
            return 11  # Ace gets converted to 11
        return self.cost


class Deck:  # Makes a Deck of Cards using the Card class
    def __init__(self):
        self.cards = []

    def generate(self):
        self.cards = []
        for i in range(1, 14):
            for j in range(4):
                self.cards.append(Card(i, j))

    def draw(self, iteration):
        cards = []
        for i in range(iteration):
            card = random.choice(self.cards)
            self.cards.remove(card)
            cards.append(card)
        return cards

    def count(self):
        return len(self.cards)


class Player:  # A class that has a deck and can either be set to player or dealer
    def __init__(self, isdealer, deck):
        self.cards = []
        self.isdealer = isdealer
        self.deck = deck
        self.score = 0

    def hit(self):
        self.cards.extend(self.deck.draw(1))  # Draws another card
        self.check_score()
        if self.score > 21:
            return 1
        return 0

    def deal(self):
        self.cards.extend(self.deck.draw(2))  # Gives the Player 2 cards
        self.check_score()
        if self.score == 21:
            return 1
        return 0

    def check_score(self):  # Updates the score while accounting for ace being 1 or 11
        a_counter = 0
        self.score = 0
        for card in self.cards:
            if card.price() == 11:
                a_counter += 1  # If 1, ace's value is 11, otherwise its value is 1
            self.score += card.price()  # Adds the price of the cards to the score

        while a_counter != 0 and self.score > 21: # If ace is considered 11 and score is more than 21
            a_counter -= 1  # Sets Ace's value is 1
            self.score -= 10
        return self.score

    def show(self):
        return self.cards


class Game(commands.Cog): # The actual cog, all other classes can be moved to another file if needed
    def __init__(self, client):
        self.client = client
        self.deck = Deck()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)

    @commands.command()
    async def blackjack(self, ctx):
        # This resets the deck so you can play more than once
        self.player = Player(False, Deck())
        self.dealer = Player(True, Deck())
        self.deck = Deck()
        self.deck.generate()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)

        p_status = self.player.deal()
        d_status = self.dealer.deal()
        await ctx.send("Player's Cards")
        for n in self.player.show():
            await ctx.send(n.show())
        await ctx.send(f"score: {self.player.check_score()}")

        if p_status == 1:
            await ctx.send("Player got Blackjack! Congrats!")
            if d_status == 1:
                await ctx.send("Dealer and Player got Blackjack! It's a push. (Tie)")
                # Indicator that game has ended
            await ctx.send("─────────────────────────────────────────────────────────")
            return 1

        cmd = ""

        while not (cmd.lower() == "stand" or cmd.lower() == "s"):
            bust = 0
            await ctx.send("Hit or Stand: ")
            message = await self.client.wait_for(
                "message",
                check=lambda m: m.author.id == ctx.author.id
                and m.channel == ctx.channel,
            )

            if message:
                cmd = message.content

            if cmd.lower() == "hit" or cmd.lower() == "h":
                bust = self.player.hit()
                await ctx.send("Player's Cards")
                for n in self.player.show():
                    await ctx.send(n.show())
                await ctx.send(f"score: {self.player.check_score()}")
                if self.player.check_score() == 21:
                    break

            if bust == 1:
                await ctx.send("Player busted. You lose")
                # Indicator that game has ended
                await ctx.send(
                    "─────────────────────────────────────────────────────────"
                )
                return 1

        while self.dealer.check_score() < 17:
            if self.dealer.hit() == 1:
                await ctx.send("Dealer busted. You win.")
                # Indicator that game has ended
                await ctx.send(
                    "─────────────────────────────────────────────────────────"
                )
                return 1

        if self.dealer.check_score() == self.player.check_score():
            await ctx.send("It's a Push (Tie). Better luck next time!")

        elif (
                self.player.check_score() < self.dealer.check_score() <= 21
        ):
            await ctx.send("Dealer wins. Good Game!")

        elif (
                self.dealer.check_score() < self.player.check_score() <= 21
        ):
            await ctx.send("Player wins. Congratulations!")

        await ctx.send("Dealer's Cards")
        for n in self.dealer.show():
            await ctx.send(n.show())

        await ctx.send(f"score: {self.dealer.check_score()}")

        if self.dealer.check_score() == 21:
            await ctx.send("Dealer got Blackjack! Better luck next time!")

        # Indicator that game has ended
        await ctx.send("─────────────────────────────────────────────────────────")


def setup(client):
    client.add_cog(Game(client))
