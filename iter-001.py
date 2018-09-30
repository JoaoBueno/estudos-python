import itertools

horses = [1, 2, 3, 4]
races = itertools.permutations(horses)
print(races)
print(list(races))
print(list(itertools.permutations(horses)))
