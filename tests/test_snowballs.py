from ethereum.tester import TransactionFailed
import pytest

dev_supply = 99999
gold_unit = 100000000
dev_gold = 33333*gold_unit
dev_medals = 42


def deploy_all_the_stuff(chain):
    provider = chain.provider
    engine, deploy_txn_hash2 = provider.get_or_deploy_contract(
       'SnowballEngine'
    )

    engine_address = engine.address

    balls, deploy_txn_hash2 = provider.get_or_deploy_contract(
       'Snowballs',
       deploy_args=[engine_address]
    )

    gold, deploy_txn_hash2 = provider.get_or_deploy_contract(
       'SnowGold',
       deploy_args=[engine_address]
    )

    medals, deploy_txn_hash2 = provider.get_or_deploy_contract(
       'SnowGodMedals',
       deploy_args=[engine_address]
    )

    base, deploy_txn_hash2 = provider.get_or_deploy_contract(
       'SnowballUserbase',
       deploy_args=[engine_address]
    )

    rules, deploy_txn_hash2 = provider.get_or_deploy_contract(
       'SnowballRules',
       deploy_args=[engine_address]
    )

    chain.wait.for_receipt(engine.transact().setDependencies(balls.address,
                                                             gold.address,
                                                             medals.address,
                                                             base.address,
                                                             rules.address))

    return engine, balls, gold, medals, base, rules


def set_debug_settings(chain, rules):
    chain.wait.for_receipt(rules.transact().setMaxLevel(2))
    chain.wait.for_receipt(rules.transact().setExpPerLevel(2))
    chain.wait.for_receipt(rules.transact().setLevelUpGold(1, 1))
    chain.wait.for_receipt(rules.transact().setLevelUpGold(2, 2))
    chain.wait.for_receipt(rules.transact().setLevelWaitingTime(0, 30))
    chain.wait.for_receipt(rules.transact().setLevelWaitingTime(1, 30))


def test_token_transfer(chain, accounts):
    provider = chain.provider

    soul_token, deploy_txn_hash2 = provider.get_or_deploy_contract(
       'Snowballs',
       deploy_args=[accounts[0]]
    )

    assert soul_token.call().balanceOf(accounts[0]) == dev_supply

    # does nothing because of insufficient funds
    chain.wait.for_receipt(soul_token.transact().transfer(accounts[1], int(199925)))
    assert soul_token.call().balanceOf(accounts[0]) == dev_supply

    # transfer the tokens
    chain.wait.for_receipt(soul_token.transact().transfer(accounts[1], int(25)))

    # check that transfer worled
    assert soul_token.call().balanceOf(accounts[0]) == dev_supply - int(25)
    assert soul_token.call().balanceOf(accounts[1]) == int(25)

    # approve some future transfers
    chain.wait.for_receipt(soul_token.transact().approve(accounts[2], int(50)))

    # check for to large sending
    chain.wait.for_receipt(soul_token.transact({'from': accounts[2]}).transferFrom(accounts[0],
                                                                                 accounts[1],
                                                                                 int(51)))

    # there should be no transfer because the amount was too large
    assert soul_token.call().balanceOf(accounts[0]) == dev_supply - int(25)
    assert soul_token.call().balanceOf(accounts[1]) == int(25)

    # this should be allowed
    chain.wait.for_receipt(soul_token.transact({'from': accounts[2]}).transferFrom(accounts[0],
                                                                                 accounts[1],
                                                                                 int(25)))

    assert soul_token.call().balanceOf(accounts[0]) == dev_supply - int(50)
    assert soul_token.call().balanceOf(accounts[1]) == int(50)
    assert soul_token.call().allowance(accounts[0], accounts[2]) == int(25)

    # this should be allowed
    chain.wait.for_receipt(soul_token.transact({'from': accounts[2]}).transferFrom(accounts[0],
                                                                                 accounts[1],
                                                                                 int(25)))

    assert soul_token.call().balanceOf(accounts[0]) == dev_supply - int(75)
    assert soul_token.call().balanceOf(accounts[1]) == int(75)
    assert soul_token.call().allowance(accounts[0], accounts[2]) == 0


def test_gold_transfer(chain, accounts):
    provider = chain.provider

    soul_token, deploy_txn_hash2 = provider.get_or_deploy_contract(
       'SnowGold',
       deploy_args=[accounts[0]]
    )

    assert soul_token.call().owner() == accounts[0]

    assert soul_token.call().balanceOf(accounts[0]) == dev_gold

    # does nothing because of insufficient funds
    chain.wait.for_receipt(soul_token.transact().transfer(accounts[1], int(44444*gold_unit)))
    assert soul_token.call().balanceOf(accounts[0]) == dev_gold

    # transfer the tokens
    chain.wait.for_receipt(soul_token.transact().transfer(accounts[1], int(25)))

    # check that transfer worled
    assert soul_token.call().balanceOf(accounts[0]) == dev_gold - int(25)
    assert soul_token.call().balanceOf(accounts[1]) == int(25)

    # approve some future transfers
    chain.wait.for_receipt(soul_token.transact().approve(accounts[2], int(50)))

    # check for to large sending
    chain.wait.for_receipt(soul_token.transact({'from': accounts[2]}).transferFrom(accounts[0],
                                                                                 accounts[1],
                                                                                 int(51)))

    # there should be no transfer because the amount was too large
    assert soul_token.call().balanceOf(accounts[0]) == dev_gold - int(25)
    assert soul_token.call().balanceOf(accounts[1]) == int(25)

    # this should be allowed
    chain.wait.for_receipt(soul_token.transact({'from': accounts[2]}).transferFrom(accounts[0],
                                                                                 accounts[1],
                                                                                 int(25)))

    assert soul_token.call().balanceOf(accounts[0]) == dev_gold - int(50)
    assert soul_token.call().balanceOf(accounts[1]) == int(50)
    assert soul_token.call().allowance(accounts[0], accounts[2]) == int(25)

    # this should be allowed
    chain.wait.for_receipt(soul_token.transact({'from': accounts[2]}).transferFrom(accounts[0],
                                                                                 accounts[1],
                                                                                 int(25)))

    assert soul_token.call().balanceOf(accounts[0]) == dev_gold - int(75)
    assert soul_token.call().balanceOf(accounts[1]) == int(75)
    assert soul_token.call().allowance(accounts[0], accounts[2]) == 0


def test_medal_transfer(chain, accounts):
    provider = chain.provider

    soul_token, deploy_txn_hash2 = provider.get_or_deploy_contract(
       'SnowGodMedals',
       deploy_args=[accounts[0]]
    )

    assert soul_token.call().balanceOf(accounts[0]) == dev_medals

    # does nothing because of insufficient funds
    chain.wait.for_receipt(soul_token.transact().transfer(accounts[1], int(199925)))
    assert soul_token.call().balanceOf(accounts[0]) == dev_medals

    # transfer the tokens
    chain.wait.for_receipt(soul_token.transact().transfer(accounts[1], int(25)))

    # check that transfer worled
    assert soul_token.call().balanceOf(accounts[0]) == dev_medals - int(25)
    assert soul_token.call().balanceOf(accounts[1]) == int(25)

    # approve some future transfers
    chain.wait.for_receipt(soul_token.transact().approve(accounts[2], int(50)))

    # check for to large sending
    chain.wait.for_receipt(soul_token.transact({'from': accounts[2]}).transferFrom(accounts[0],
                                                                                 accounts[1],
                                                                                 int(51)))

    # there should be no transfer because the amount was too large
    assert soul_token.call().balanceOf(accounts[0]) == dev_medals - int(25)
    assert soul_token.call().balanceOf(accounts[1]) == int(25)

    # this should be allowed
    chain.wait.for_receipt(soul_token.transact({'from': accounts[2]}).transferFrom(accounts[0],
                                                                                 accounts[1],
                                                                                 int(17)))

    assert soul_token.call().balanceOf(accounts[0]) == 0
    assert soul_token.call().balanceOf(accounts[1]) == 42
    assert soul_token.call().allowance(accounts[0], accounts[2]) == 33

    # this cannot work in this case
    chain.wait.for_receipt(soul_token.transact({'from': accounts[2]}).transferFrom(accounts[0],
                                                                                 accounts[1],
                                                                                 int(25)))

    assert soul_token.call().balanceOf(accounts[0]) == 0
    assert soul_token.call().balanceOf(accounts[1]) == 42
    assert soul_token.call().allowance(accounts[0], accounts[2]) == 33


def test_deploy(chain, accounts):
    provider = chain.provider
    engine, deploy_txn_hash2 = provider.get_or_deploy_contract(
       'SnowballEngine'
    )
    assert engine.call().owner() == accounts[0]

def test_deploy_rules(chain, accounts):
    provider = chain.provider
    rules, deploy_txn_hash2 = provider.get_or_deploy_contract(
       'SnowballRules',
        deploy_args=[accounts[0]]
    )
    pass


def test_first_throw(chain, accounts):
    engine, balls, gold, medals, base, rules = deploy_all_the_stuff(chain)

    set_debug_settings(chain, rules)

    stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[1]))

    assert base.call().totalHits() == 1
    assert base.call().getExperiencLogEntry(0) == 1
    assert base.call().getExperiencLogEntry(1) == 1
    assert base.call().getExperiencLogEntry(2) == 0
    assert base.call().getUserId(accounts[0]) == 1
    assert base.call().getUserId(accounts[1]) == 2
    assert base.call().getUserId(accounts[3]) == 0

    assert base.call().getAddressById(1) == accounts[0]
    assert base.call().getAddressById(2) == accounts[1]

    assert base.call().getUserExp(1) == 1
    assert base.call().getUserExp(2) == 0
    assert base.call().getHitsTaken(2) == 1
    assert base.call().getHitsGiven(1) == 1
    assert base.call().getHitsTaken(1) == 0
    assert base.call().getHitsGiven(2) == 0
    assert base.call().getLastHit(1) == 0
    assert base.call().getLastHit(2) > 0
    assert base.call().getLastHitBy(1) == 0
    assert base.call().getLastHitBy(2) == 1

    assert balls.call().balanceOf(accounts[1]) == 1
    assert balls.call().balanceOf(accounts[0]) == dev_supply + 1
    assert balls.call().totalSupply() == dev_supply + 2

    # should fail because paralyzed
    with pytest.raises((TransactionFailed)):
        stuff = chain.wait.for_receipt(engine.transact({'from': accounts[1]}).throwBall(accounts[2]))


def testLevelUp(chain, accounts):
    engine, balls, gold, medals, base, rules = deploy_all_the_stuff(chain)

    set_debug_settings(chain, rules)

    stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[1]))

    stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[2]))


    assert base.call().totalHits() == 2
    assert base.call().getExperiencLogEntry(0) == 2
    assert base.call().getExperiencLogEntry(1) == 0
    assert base.call().getExperiencLogEntry(2) == 1
    assert base.call().getUserId(accounts[0]) == 1
    assert base.call().getUserId(accounts[1]) == 2
    assert base.call().getUserId(accounts[2]) == 3

    assert base.call().getAddressById(1) == accounts[0]
    assert base.call().getAddressById(2) == accounts[1]

    assert base.call().getUserExp(1) == 2
    assert base.call().getUserExp(2) == 0
    assert base.call().getHitsTaken(2) == 1
    assert base.call().getHitsGiven(1) == 2
    assert base.call().getHitsTaken(1) == 0
    assert base.call().getHitsGiven(2) == 0
    assert base.call().getLastHit(1) == 0
    assert base.call().getLastHit(2) > 0
    assert base.call().getLastHitBy(1) == 0
    assert base.call().getLastHitBy(2) == 1

    assert balls.call().balanceOf(accounts[1]) == 1
    assert balls.call().balanceOf(accounts[2]) == 1
    assert balls.call().balanceOf(accounts[0]) == dev_supply - 2 + 4
    assert balls.call().totalSupply() == dev_supply + 2 + 2

    assert gold.call().balanceOf(accounts[1]) == 0
    assert gold.call().balanceOf(accounts[0]) == dev_gold + 1 * gold_unit
    assert gold.call().totalSupply() == dev_gold + 1 * gold_unit


    # this should be a legitimate hit but give no experience

    previous_last_hit = base.call().getLastHit(3)

    stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[2]))
    stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[3]))

    stuff = chain.wait.for_receipt(engine.transact({'from': accounts[1]}).throwBall(accounts[3]))

    # should fail because paralyzed
    with pytest.raises((TransactionFailed)):
        stuff = chain.wait.for_receipt(engine.transact({'from': accounts[2]}).throwBall(accounts[3]))

    # should fail because no self hit
    with pytest.raises((TransactionFailed)):
        stuff = chain.wait.for_receipt(engine.transact({'from': accounts[0]}).throwBall(accounts[0]))

    assert base.call().totalHits() == 5
    assert base.call().getExperiencLogEntry(0) == 3
    assert base.call().getExperiencLogEntry(1) == 0
    assert base.call().getExperiencLogEntry(2) == 1
    assert base.call().getUserId(accounts[0]) == 1
    assert base.call().getUserId(accounts[1]) == 2
    assert base.call().getUserId(accounts[2]) == 3

    assert base.call().getAddressById(1) == accounts[0]
    assert base.call().getAddressById(2) == accounts[1]

    assert base.call().getUserExp(1) == 2
    assert base.call().getUserExp(2) == 0
    assert base.call().getHitsTaken(2) == 1
    assert base.call().getHitsGiven(1) == 4
    assert base.call().getHitsTaken(3) == 2
    assert base.call().getHitsGiven(2) == 1
    assert base.call().getLastHit(1) == 0
    assert base.call().getLastHit(3) > previous_last_hit
    assert base.call().getLastHitBy(1) == 0
    assert base.call().getLastHitBy(2) == 1

    assert balls.call().balanceOf(accounts[1]) == 0
    assert balls.call().balanceOf(accounts[2]) == 2
    assert balls.call().balanceOf(accounts[0]) == dev_supply - 2 + 4 - 2
    assert balls.call().totalSupply() == dev_supply + 2 + 2

    assert gold.call().balanceOf(accounts[1]) == 0
    assert gold.call().balanceOf(accounts[0]) == dev_gold + 1 * gold_unit
    assert gold.call().totalSupply() == dev_gold + 1 * gold_unit


    # this should not be a legitimate hit and just transfer the ball
    # blow some time
    for irun in range(5):
        chain.wait.for_receipt(base.transact().getFullUserInfo(1))
    stuff = chain.wait.for_receipt(engine.transact({'from': accounts[2]}).throwBall(accounts[0]))

    assert base.call().totalHits() == 5
    assert base.call().getExperiencLogEntry(0) == 3
    assert base.call().getExperiencLogEntry(1) == 0
    assert base.call().getExperiencLogEntry(2) == 1
    assert base.call().getUserId(accounts[0]) == 1
    assert base.call().getUserId(accounts[1]) == 2
    assert base.call().getUserId(accounts[2]) == 3

    assert base.call().getAddressById(1) == accounts[0]
    assert base.call().getAddressById(2) == accounts[1]

    assert base.call().getUserExp(1) == 2
    assert base.call().getUserExp(2) == 0
    assert base.call().getHitsTaken(2) == 1
    assert base.call().getHitsGiven(1) == 4
    assert base.call().getHitsTaken(3) == 2
    assert base.call().getHitsGiven(2) == 1
    assert base.call().getLastHit(1) == 0
    assert base.call().getLastHit(2) > 0
    assert base.call().getLastHitBy(1) == 0
    assert base.call().getLastHitBy(2) == 1

    assert balls.call().balanceOf(accounts[1]) == 0
    assert balls.call().balanceOf(accounts[2]) == 1
    assert balls.call().balanceOf(accounts[0]) == dev_supply - 2 + 4 - 2 + 1
    assert balls.call().totalSupply() == dev_supply + 2 + 2

    assert gold.call().balanceOf(accounts[1]) == 0
    assert gold.call().balanceOf(accounts[0]) == dev_gold + 1 * gold_unit
    assert gold.call().totalSupply() == dev_gold + 1 * gold_unit

    # blow some time
    for irun in range(5):
        chain.wait.for_receipt(base.transact().getFullUserInfo(1))
    stuff = chain.wait.for_receipt(engine.transact({'from': accounts[2]}).throwBall(accounts[3]))


def test_become_god(chain, accounts):

    engine, balls, gold, medals, base, rules = deploy_all_the_stuff(chain)

    set_debug_settings(chain, rules)

    stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[1]))

    assert balls.call().balanceOf(accounts[0]) == dev_supply - 1 + 2

    stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[2]))

    assert balls.call().balanceOf(accounts[0]) == dev_supply - 2 + 4

    chain.wait.for_receipt(balls.transact().transfer(accounts[3], 20))
    chain.wait.for_receipt(balls.transact().transfer(accounts[6], 10))

    assert balls.call().balanceOf(accounts[0]) == dev_supply - 2 + 4 - 30

    stuff = chain.wait.for_receipt(engine.transact({'from': accounts[3]}).throwBall(accounts[4]))

    stuff = chain.wait.for_receipt(engine.transact({'from': accounts[3]}).throwBall(accounts[5]))

    stuff = chain.wait.for_receipt(engine.transact({'from': accounts[6]}).throwBall(accounts[7]))

    stuff = chain.wait.for_receipt(engine.transact({'from': accounts[6]}).throwBall(accounts[8]))

    stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[3]))

    assert balls.call().balanceOf(accounts[0]) == dev_supply - 3 + 4 - 30 + 4
    assert base.call().getUserExp(1) == 3

    stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[6]))

    assert base.call().getUserExp(1) == 4
    assert balls.call().balanceOf(accounts[0]) == dev_supply - 4 + 4 - 30 + 8 + 8 ## including god stuff

    assert balls.call().balanceOf(accounts[1]) == 1
    assert balls.call().balanceOf(accounts[2]) == 1

    assert gold.call().balanceOf(accounts[1]) == 0
    assert gold.call().balanceOf(accounts[0]) == dev_gold + 3 * gold_unit
    assert gold.call().balanceOf(accounts[3]) == 1 * gold_unit
    assert gold.call().balanceOf(accounts[6]) == 1 * gold_unit
    assert gold.call().totalSupply() == dev_gold + 5 * gold_unit


    assert medals.call().balanceOf(accounts[0]) == dev_medals + 1
    assert medals.call().balanceOf(accounts[6]) == 0