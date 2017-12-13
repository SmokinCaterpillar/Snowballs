from ethereum.tester import TransactionFailed
import pytest
from prompt_toolkit.renderer import _TokenToAttrsCache

dev_supply = 99999
gold_unit = 100000000
dev_gold = 33333*gold_unit

ether = int(1e18)
finney = int(ether/1000)


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

    base, deploy_txn_hash2 = provider.get_or_deploy_contract(
       'SnowballUserbase',
       deploy_args=[engine_address]
    )


    chain.wait.for_receipt(engine.transact().setDependencies(balls.address,
                                                             gold.address,
                                                             base.address))

    return engine, balls, gold, base


def set_debug_settings(chain, engine):
    chain.wait.for_receipt(engine.transact().setRules(40, 4, 2, 1, 3))
    chain.wait.for_receipt(engine.transact().setMinBalance(1*finney))


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


def test_deploy(chain, accounts):
    provider = chain.provider
    engine, deploy_txn_hash2 = provider.get_or_deploy_contract(
       'SnowballEngine'
    )
    assert engine.call().owner() == accounts[0]


def test_first_throw(chain, accounts):
    engine, balls, gold, base = deploy_all_the_stuff(chain)

    set_debug_settings(chain, engine)

    stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[1]))

    assert engine.call().owner() == accounts[0]

    assert base.call().totalHits() == 1
    assert base.call().getLevelLogEntry(0) == 1
    assert base.call().getLevelLogEntry(1) == 1
    assert base.call().getLevelLogEntry(2) == 0
    assert base.call().getUserId(accounts[0]) == 1
    assert base.call().getUserId(accounts[1]) == 2
    assert base.call().getUserId(accounts[3]) == 0

    assert base.call().getAddressById(1) == accounts[0]
    assert base.call().getAddressById(2) == accounts[1]

    assert base.call().getUserLevel(1) == 1
    assert base.call().getUserLevel(2) == 0
    assert base.call().getHitsTaken(2) == 1
    assert base.call().getHitsGiven(1) == 1
    assert base.call().getHitsTaken(1) == 0
    assert base.call().getHitsGiven(2) == 0
    assert base.call().getLastHit(1) == 0
    assert base.call().getLastHit(2) > 0
    assert base.call().getLastHitBy(1) == 0
    assert base.call().getLastHitBy(2) == 1

    assert base.call().getHitLogEntry(1) == [1, 2]

    assert balls.call().balanceOf(accounts[1]) == 1
    assert balls.call().balanceOf(accounts[0]) == dev_supply - 1 + 4
    assert balls.call().totalSupply() == dev_supply + 4

    # should fail because paralyzed
    with pytest.raises((TransactionFailed)):
        stuff = chain.wait.for_receipt(engine.transact({'from': accounts[1]}).throwBall(accounts[2]))


def test_min_balance(chain, accounts):
    engine, balls, gold, base = deploy_all_the_stuff(chain)

    set_debug_settings(chain, engine)

    web3 = chain.web3
    balance = web3.eth.getBalance(accounts[1])
    balance = balance - finney + 10
    chain.wait.for_receipt(web3.eth.sendTransaction({'value':balance,
                                                     'from':accounts[1],
                                                     'to': engine.address,
                                                     'gas':200000}))

    stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[1]))

    assert base.call().totalHits() == 0
    assert base.call().getLevelLogEntry(0) == 2
    assert base.call().getLevelLogEntry(1) == 0
    assert balls.call().balanceOf(accounts[0]) == dev_supply - 1
    assert balls.call().balanceOf(accounts[1]) == 1

    with pytest.raises(TransactionFailed):
        # fails because of minBalance
        chain.wait.for_receipt(engine.transact({'from': accounts[1]}).throwBall(accounts[2]))


def testLevelUp(chain, accounts):
    engine, balls, gold, base = deploy_all_the_stuff(chain)

    set_debug_settings(chain, engine)

    stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[1]))

    stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[2]))

    assert base.call().totalHits() == 1
    assert base.call().getLevelLogEntry(0) == 2
    assert base.call().getLevelLogEntry(1) == 1
    assert base.call().getLevelLogEntry(2) == 0
    assert base.call().getUserId(accounts[0]) == 1
    assert base.call().getUserId(accounts[1]) == 2
    assert base.call().getUserId(accounts[2]) == 3

    assert base.call().getAddressById(1) == accounts[0]
    assert base.call().getAddressById(2) == accounts[1]

    assert base.call().getUserLevel(1) == 1
    assert base.call().getUserLevel(2) == 0
    assert base.call().getHitsTaken(2) == 1
    assert base.call().getHitsGiven(1) == 1
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
    assert gold.call().balanceOf(accounts[0]) == dev_gold
    assert gold.call().totalSupply() == dev_gold


    # this should be a legitimate hit but give no experience
    # blow some time
    for irun in range(5):
        chain.wait.for_receipt(base.transact().getFullUserInfo(1))

    stuff = chain.wait.for_receipt(engine.transact({'from': accounts[1]}).throwBall(accounts[3]))

    # should fail because paralyzed
    with pytest.raises((TransactionFailed)):
        stuff = chain.wait.for_receipt(engine.transact({'from': accounts[3]}).throwBall(accounts[2]))

    # should fail because no self hit
    with pytest.raises((TransactionFailed)):
        stuff = chain.wait.for_receipt(engine.transact({'from': accounts[0]}).throwBall(accounts[0]))

    assert base.call().totalHits() == 2
    assert base.call().getLevelLogEntry(0) == 2
    assert base.call().getLevelLogEntry(1) == 2
    assert base.call().getLevelLogEntry(2) == 0
    assert base.call().getUserId(accounts[0]) == 1
    assert base.call().getUserId(accounts[1]) == 2
    assert base.call().getUserId(accounts[2]) == 3

    assert base.call().getAddressById(1) == accounts[0]
    assert base.call().getAddressById(2) == accounts[1]

    assert base.call().getUserLevel(1) == 1
    assert base.call().getUserLevel(2) == 1

    assert balls.call().totalSupply() == dev_supply + 8

    stuff = chain.wait.for_receipt(engine.transact({'from': accounts[0]}).throwBall(accounts[1]))

    assert balls.call().balanceOf(accounts[1]) == 5
    assert balls.call().balanceOf(accounts[2]) == 1
    assert balls.call().balanceOf(accounts[0]) == dev_supply - 3 + 4 + 2
    assert balls.call().totalSupply() == dev_supply + 10

    assert base.call().getLevelLogEntry(0) == 3
    assert base.call().getLevelLogEntry(1) == 0
    assert base.call().getLevelLogEntry(2) == 1

    assert base.call().getUserLevel(1) == 2
    assert base.call().getUserLevel(2) == 0
    assert base.call().getMaxLevel(2) == 1
    assert base.call().getMaxLevel(1) == 2

    assert gold.call().balanceOf(accounts[1]) == 0
    assert gold.call().balanceOf(accounts[0]) == dev_gold + 1 * gold_unit
    assert gold.call().totalSupply() == dev_gold + 1 * gold_unit

    for irun in range(5):
        chain.wait.for_receipt(base.transact().getFullUserInfo(1))

    stuff = chain.wait.for_receipt(engine.transact({'from': accounts[1]}).throwBall(accounts[3]))

    assert balls.call().balanceOf(accounts[1]) == 5
    assert balls.call().balanceOf(accounts[2]) == 1
    assert balls.call().balanceOf(accounts[0]) == dev_supply - 3 + 4 + 2
    assert balls.call().totalSupply() == dev_supply + 11

    assert base.call().getLevelLogEntry(0) == 2
    assert base.call().getLevelLogEntry(1) == 1
    assert base.call().getLevelLogEntry(2) == 1

    assert base.call().getUserLevel(1) == 2
    assert base.call().getUserLevel(2) == 1

    assert gold.call().balanceOf(accounts[1]) == 0
    assert gold.call().balanceOf(accounts[0]) == dev_gold + 1 * gold_unit
    assert gold.call().totalSupply() == dev_gold + 1 * gold_unit


def test_ownership_transfer(chain, accounts):

    engine, balls, gold, base = deploy_all_the_stuff(chain)

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(engine.transact({'from': accounts[6]}).changeOwnership(accounts[1]))

    chain.wait.for_receipt(engine.transact({'from': accounts[0]}).changeOwnership(accounts[1]))
    chain.wait.for_receipt(base.transact({'from': accounts[0]}).changeOwnership(accounts[1]))

    assert engine.call().owner() == accounts[1]
    assert base.call().owner() == accounts[1]

    chain.wait.for_receipt(base.transact({'from': accounts[1]}).changeOwnership(accounts[0]))

    assert base.call().owner() == accounts[0]


def test_engine_change(chain, accounts):

    engine, balls, gold, base = deploy_all_the_stuff(chain)

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(balls.transact({'from': accounts[1]}).changeEngine(accounts[1]))

    chain.wait.for_receipt(balls.transact({'from': accounts[0]}).changeEngine(accounts[1]))

    assert balls.call().engine() == accounts[1]

    with pytest.raises(TransactionFailed):
        stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[1]))

    chain.wait.for_receipt(balls.transact({'from': accounts[0]}).changeEngine(engine.address))

    stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[1]))


def test_payable_throw(chain, accounts):
    engine, balls, gold, base = deploy_all_the_stuff(chain)

    chain.wait.for_receipt(balls.transact({'from': accounts[0]}).transfer(accounts[2], 100))
    chain.wait.for_receipt(engine.transact({'from': accounts[0]}).changeOwnership(accounts[1]))


    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(engine.transact({'from': accounts[0]}).setThrowPrice(100))

    chain.wait.for_receipt(engine.transact({'from': accounts[1]}).setThrowPrice(100))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(engine.transact({'from': accounts[0]}).throwBall(accounts[2]))

    chain.wait.for_receipt(engine.transact({'from': accounts[0], 'value': 1*ether}).throwBall(accounts[2]))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(engine.transact({'from': accounts[0]}).withdraw())

    web3 = chain.web3

    chain.wait.for_receipt(web3.eth.sendTransaction({'value':int(1*ether),
                                                     'from':accounts[3],
                                                     'to': engine.address,
                                                     'gas':200000}))

    assert web3.eth.getBalance(engine.address) == int(2*ether)
    oldBal = web3.eth.getBalance(accounts[1])

    chain.wait.for_receipt(engine.transact({'from': accounts[1]}).withdraw())

    assert web3.eth.getBalance(accounts[1]) > oldBal + 2*ether - 10*finney


def test_register_username(chain, accounts):
    engine, balls, gold, base = deploy_all_the_stuff(chain)

    chain.wait.for_receipt(base.transact({'from': accounts[0]}).setUsernamePrice(100))

    chain.wait.for_receipt(balls.transact({'from': accounts[0]}).transfer(accounts[1], 10))

    chain.wait.for_receipt(engine.transact({'from': accounts[1]}).throwBall(accounts[2]))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(base.transact({'from': accounts[2]}).setUsername('Brian'))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(base.transact({'from': accounts[5], 'value':100}).setUsername('Brian'))

    chain.wait.for_receipt(engine.transact({'from': accounts[0]}).throwBall(accounts[5]))


    chain.wait.for_receipt(base.transact({'from': accounts[2], 'value':100}).setUsername('Brian'))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(base.transact({'from': accounts[5], 'value':100}).setUsername('Brian'))

    chain.wait.for_receipt(base.transact({'from': accounts[5], 'value':100}).setUsername('Mary'))

    web3 = chain.web3

    assert web3.eth.getBalance(base.address) == 200

    chain.wait.for_receipt(base.transact().withdraw())

    assert web3.eth.getBalance(base.address) == 0

    idbrian = base.call().getIdByUsername('Brian')
    idmary = base.call().getIdByUsername('Mary')
    noid = base.call().getIdByUsername('Franke')

    assert idbrian == 2
    assert idmary == 4
    assert noid == 0

    address, exp, max_exp, hit, hitby, taken, given = base.call().getFullUserInfo(2)
    name = base.call().getUsername(2)

    assert name == 'Brian'
    assert address == accounts[2]
    assert exp == 0
    assert max_exp == 0
    assert hit > 0
    assert hitby == 1
    assert taken == 1
    assert given == 0

    address, exp, max_exp, hit, hitby, taken, given = base.call().getFullUserInfo(1)
    name = base.call().getUsername(1)

    assert name == ''
    assert address == accounts[1]
    assert exp == 1
    assert max_exp == 1
    assert hit == 0
    assert hitby == 0
    assert taken == 0
    assert given == 1


def test_game_pause(chain, accounts):
    engine, balls, gold, base = deploy_all_the_stuff(chain)

    stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[1]))

    chain.wait.for_receipt(engine.transact().setGameState(False))

    with pytest.raises(TransactionFailed):
        stuff = chain.wait.for_receipt(engine.transact().throwBall(accounts[1]))

    chain.wait.for_receipt(engine.transact().setGameState(True))

    chain.wait.for_receipt(engine.transact().throwBall(accounts[1]))


def test_security(chain, accounts):
    engine, balls, gold, base = deploy_all_the_stuff(chain)

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(balls.transact({'from': accounts[1]}).changeEngine(accounts[1]))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(balls.transact({'from': accounts[1]}).withdraw())

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(balls.transact({'from': accounts[1]}).changeOwnership(accounts[1]))

    with pytest.raises(ValueError):
        chain.wait.for_receipt(balls.transact({'from': accounts[1]}).mint(accounts[1], 10))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(balls.transact({'from': accounts[1]}).rollBalls(accounts[1], 10))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(gold.transact({'from': accounts[1]}).mintBars(accounts[1], 10))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(base.transact({'from': accounts[1]}).setUsernamePrice(10))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(base.transact({'from': accounts[1]}).addNewUser(accounts[1]))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(base.transact({'from': accounts[1]}).addHit(2,3))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(engine.transact({'from': accounts[1]}).setGameState(True))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(engine.transact({'from': accounts[1]}).setDependencies(balls.address,
                                                             gold.address,
                                                             base.address))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(engine.transact({'from': accounts[1]}).setThrowPrice(11))

