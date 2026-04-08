import random


SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


def build_deck():
    deck = [f"{rank} of {suit}" for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck


def card_value(card):
    rank = card.split(" of ")[0]
    if rank in ("J", "Q", "K"):
        return 10
    if rank == "A":
        return 11
    return int(rank)


def hand_value(hand):
    total = sum(card_value(c) for c in hand)
    aces = sum(1 for c in hand if c.startswith("A"))
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def display_hand(name, hand, hide_second=False):
    print(f"\n{name}'s hand:")
    for i, card in enumerate(hand):
        if hide_second and i == 1:
            print("  [hidden]")
        else:
            print(f"  {card}")
    if not hide_second:
        print(f"  Total: {hand_value(hand)}")


def play():
    print("=" * 40)
    print("       Welcome to Blackjack!")
    print("=" * 40)

    deck = build_deck()

    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]

    # Show initial hands
    display_hand("Dealer", dealer, hide_second=True)
    display_hand("Player", player)

    # Check for immediate blackjack
    player_bj = hand_value(player) == 21
    dealer_bj = hand_value(dealer) == 21

    if player_bj or dealer_bj:
        print("\n--- Revealing dealer's hand ---")
        display_hand("Dealer", dealer)
        if player_bj and dealer_bj:
            print("\nBoth have Blackjack! It's a TIE.")
        elif player_bj:
            print("\nBlackjack! You WIN!")
        else:
            print("\nDealer has Blackjack. You LOSE.")
        return

    # Player's turn
    while True:
        action = input("\nHit or Stand? (h/s): ").strip().lower()
        if action == "h":
            player.append(deck.pop())
            display_hand("Player", player)
            if hand_value(player) > 21:
                print("\nBust! You went over 21. You LOSE.")
                return
            if hand_value(player) == 21:
                break
        elif action == "s":
            break
        else:
            print("Please enter 'h' to hit or 's' to stand.")

    # Dealer's turn
    print("\n--- Dealer reveals hidden card ---")
    display_hand("Dealer", dealer)

    while hand_value(dealer) < 17:
        print("Dealer hits...")
        dealer.append(deck.pop())
        display_hand("Dealer", dealer)

    dealer_total = hand_value(dealer)
    player_total = hand_value(player)

    print("\n" + "=" * 40)
    print(f"  Player: {player_total}   Dealer: {dealer_total}")
    print("=" * 40)

    if dealer_total > 21:
        print("Dealer busts! You WIN!")
    elif player_total > dealer_total:
        print("You WIN!")
    elif player_total < dealer_total:
        print("You LOSE.")
    else:
        print("It's a TIE.")


def main():
    while True:
        play()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("\nThanks for playing. Goodbye!")
            break
        print()


if __name__ == "__main__":
    main()
