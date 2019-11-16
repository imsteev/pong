if __name__ == "__main__":
    from round_robin import construct_matchups, round_robin
    import pandas as pd
    import random
    from models.player import Player

    with open('./files/the_office.csv') as f:
        df = pd.read_csv(f, delimiter=',')

    pool = [Player(**p) for _, p in df.iterrows()]

    # get 5 random players
    random.shuffle(pool)
    players = pool[:5]

    num_players = len(players)
    for i, round in enumerate(round_robin(num_players), 1):
        print("ROUND {}".format(i))
        matchups = construct_matchups(round, players)
        for ((p1, p1_seed), (p2, p2_seed)) in matchups:
            print("{0} ({1}) v. {2} ({3})".format(p1.name, p1_seed, p2.name, p2_seed))
        print()
