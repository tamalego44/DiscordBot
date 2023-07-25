import random

wins = 0
rounds = 100_000
for i in range(rounds):
    a_guess = random.randint(0, 2)
    # Remove erroneous finger actions
    a_keepFinger = True if a_guess == 2 else False if a_guess == 0 else bool(random.randint(0,1))
    b_keepFinger = bool(random.randint(0,1))

    wins += (int(a_keepFinger) + int(b_keepFinger) == a_guess)

print("Win rate: %.4f" % (wins/rounds))
