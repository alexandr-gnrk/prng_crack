import casino_api as api
import lcg_crack as lcg
import mt19937 as mt
import random
import time


def create_new_acc():
    resp = api.createacc(random.randrange(2**32))
    while 'error' in resp:
        resp = api.createacc(random.randrange(2**32))
    return resp

def make_fake_bets(mode, player, num, bet=1):
    nums = list()
    for i in range(num):
        resp = api.play(mode, player, bet, 0)
        player = resp['account']
        nums.append(int(resp["realNumber"]))
    return player, nums

def win_the_game(mode, player, bet_num, gen):
    return api.play(mode, player, bet_num, next(gen))


player = create_new_acc()
print("Making fake bets to crack LCG...")
player, nums = make_fake_bets('Lcg', player, 20)
print("Cracking LCG...")
a, c, m = lcg.crack(nums, 2**33, 2**32)
gen = lcg.get_generator(nums[-1], a, c, m)
print("Winning the game...")
resp = win_the_game('Lcg', player, 100, gen)
print("Win message is:", resp['message'])

# print("============")
# print("Making fake bets to crack MT19937...")
# player, nums = make_fake_bets('Mt', player, mt.MT19937.n)
# print("Cracking MT19937...")
# gen = mt.crack(nums).get_generator()
# print("Winning the game...")
# resp = win_the_game('Mt', player, 100, gen)
# print("Win message is:", resp['message'])


# print("============")
# print("Making fake bets to crack better MT19937...")
# player, nums = make_fake_bets('BetterMt', player, mt.MT19937.n)
# print("Cracking better MT19937...")
# gen = mt.crack(nums).get_generator()
# print("Winning the game...")
# resp = win_the_game('BetterMt', player, 100, gen)
# print("Win message is:", resp['message'])