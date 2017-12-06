
dev_supply = 99999
gold_unit = 100000000
dev_gold = 33333*gold_unit
dev_medals = 42


def test_token_transfer(chain, accounts):
    provider = chain.provider

    soul_token, deploy_txn_hash2 = provider.get_or_deploy_contract(
       'Snowballs',
       deploy_args=[accounts[0], accounts[1]]
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
       deploy_args=[accounts[0], accounts[1]]
    )

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
       deploy_args=[accounts[0], accounts[1]]
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