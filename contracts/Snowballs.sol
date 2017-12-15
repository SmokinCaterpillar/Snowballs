/*
* This is the source code of the smart contract for the SOUL token, aka Soul Napkins.
* Copyright 2017 and all rights reserved by the owner of the following Ethereum address:
* 0x10E44C6bc685c4E4eABda326c211561d5367EEec
*/

pragma solidity ^0.4.19;

// ERC Token standard #20 Interface
// https://github.com/ethereum/EIPs/issues/20
contract ERC20Interface {

    // Token symbol
    string public symbol;

    // Name of token
    string public name;

    // Decimals of token
    uint8 public decimals;

    // Total token supply
    function totalSupply() public constant returns (uint256 supply);

    // The balance of account with address _owner
    function balanceOf(address _owner) public constant returns (uint256 balance);

    // Send _value tokens to address _to
    function transfer(address _to, uint256 _value) public returns (bool success);

    // Send _value tokens from address _from to address _to
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);

    // Allow _spender to withdraw from your account, multiple times, up to the _value amount.
    // If this function is called again it overwrites the current allowance with _value.
    // this function is required for some DEX functionality
    function approve(address _spender, uint256 _value) public returns (bool success);

    // Returns the amount which _spender is still allowed to withdraw from _owner
    function allowance(address _owner, address _spender) public constant returns (uint256 remaining);

    // Triggered when tokens are transferred.
    event Transfer(address indexed _from, address indexed _to, uint256 _value);

    // Triggered whenever approve(address _spender, uint256 _value) is called.
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}


// Implementation of ERC20Interface
contract ERC20Token is ERC20Interface{

    // account balances
    mapping(address => uint256) internal balances;

    // Owner of account approves the transfer of amount to another account
    mapping(address => mapping (address => uint256)) internal allowed;

    // Function to access acount balances
    function balanceOf(address _owner) public constant returns (uint256) {
        return balances[_owner];
    }

    // Transfer the _amount from msg.sender to _to account
    function transfer(address _to, uint256 _amount) public returns (bool) {
        return executeTransfer(msg.sender, _to, _amount);
    }

    // Send _value amount of tokens from address _from to address _to
    // The transferFrom method is used for a withdraw workflow, allowing contracts to send
    // tokens on your behalf, for example to "deposit" to a contract address and/or to charge
    // fees in sub-currencies; the command should fail unless the _from account has
    // deliberately authorized the sender of the message via some mechanism; we propose
    // these standardized APIs for approval:
    function transferFrom(
        address _from,
        address _to,
        uint256 _amount
    ) public returns (bool) {
        if (balances[_from] >= _amount
            && allowed[_from][msg.sender] >= _amount && _amount > 0
                && balances[_to] + _amount > balances[_to]) {
            balances[_from] -= _amount;
            allowed[_from][msg.sender] -= _amount;
            balances[_to] += _amount;
            Transfer(_from, _to, _amount);
            return true;
        } else {
            return false;
        }
    }

    // Allow _spender to withdraw from your account, multiple times, up to the _value amount.
    // If this function is called again it overwrites the current allowance with _value.
    function approve(address _spender, uint256 _amount) public returns (bool) {
        allowed[msg.sender][_spender] = _amount;
        Approval(msg.sender, _spender, _amount);
        return true;
    }

    // Function to specify how much _spender is allowed to transfer on _owner's behalf
    function allowance(address _owner, address _spender) public constant returns (uint256) {
        return allowed[_owner][_spender];
    }

    // Internal function to execute transfer
    function executeTransfer(address _from, address _to, uint256 _amount) internal returns (bool){
        if (balances[_from] >= _amount && _amount > 0
                && balances[_to] + _amount > balances[_to]) {
            balances[_from] -= _amount;
            balances[_to] += _amount;
            Transfer(_from, _to, _amount);
            return true;
        } else {
            return false;
        }

    }

}


contract MintableToken is ERC20Token {
    // total supply of tokens
    // increased with every tap
    uint256 internal internalSupply;

    function totalSupply() public constant returns (uint256){
        return internalSupply;
    }

    function mint(address _beneficiary, uint256 _amount) internal{
        // check for wrap aroung
        require(balances[_beneficiary] + _amount > balances[_beneficiary]);
        require(internalSupply + _amount > internalSupply);

        // roll the new balls
        internalSupply += _amount;
        balances[_beneficiary] += _amount;
        Transfer(this, _beneficiary, _amount);
    }

}


contract TakesEther {

    address public owner;

    function TakesEther() public{
        owner = msg.sender;
    }

    // send donations to owner
    function withdraw() public{
        // send donations to owner
        require(msg.sender == owner);
        owner.transfer(this.balance);
    }

    // one can change the owner
    function changeOwnership(address _owner) public{
        require(msg.sender == owner);
        owner = _owner;
    }

    // accepts donations
    function () public payable{
        // just take donations
    }

}


contract HasEngine is TakesEther {

    // address of game enigne, i.e. game rules
    address public engine;

    function HasEngine(address _engine) public{
        engine = _engine;
    }

    // Can update or change the game Engine
    function changeEngine(address _engine) public{
        require(msg.sender == owner);
        engine = _engine;
    }
}


contract SnowGold is MintableToken, HasEngine {
    string public constant version = '0.1';

    // Token symbol
    string public symbol = 'SGC';

    // Name of token
    string public name = 'Snow Gold';

    // Gold = BTC
    uint8 public decimals = 8;

    // unit = 10**decimals
    uint256 public unit = 100000000;

    function SnowGold(address _engine)
        HasEngine(_engine) public{
        // dev supply
        internalSupply = 33333 * unit;
        balances[owner] = internalSupply;
        Transfer(this, owner, internalSupply);
    }

    // creates new gold
    function mintBars(address _to, uint256 _amount) public{
        // this can only be triggered by the game
        require(msg.sender == engine);
        mint(_to, _amount * unit);

    }
}


contract Snowballs is MintableToken, HasEngine {

    string public constant version = '0.1';

    // Token symbol
    string public symbol = 'SNOW';

    // Name of token
    string public name = 'Snowballs';

    // Snowballs cannot be divided
    uint8 public decimals = 0;


    function Snowballs(address _engine)
        HasEngine( _engine) public{
        // dev supply
        internalSupply = 99999;
        balances[owner] = internalSupply;
        Transfer(this, owner, internalSupply);
    }

    // throws a snow ball at an enemy
    // not triggered by user but by engine
    function throwBall(address _from, address _to) public returns(bool){
        // this can only be triggered by the game
        require(msg.sender == engine);
        return executeTransfer(_from, _to, 1);
    }

    // mints new Snowballs
    function rollBalls(address _to, uint256 _amount)public{
        // this can only be triggered by the game
        require(msg.sender == engine);

        mint(_to, _amount);

    }

}


contract SnowballUserbase is HasEngine{

    string public constant version = '0.1';

    struct User{
        string name;  // optional username
        address useraddress;  // eth address
        uint16 level;  // level of user
        uint16 maxLevel;  // maximum level she or he ever achieved
        uint256 lastHit;  // time of last hit
        uint256 lastHitBy;  // user id of last hitter
        uint256 hitsTaken;  // number of times hit by others
        uint256 hitsGiven;  // number of times thrown at others
    }

    struct hit{
        uint256 userId;
        uint256 enemyId;
    }

    function SnowballUserbase(address _engine)
        HasEngine(_engine) public{
    }

    uint256 public totalHits;

    uint256 public nUsers;

    mapping(uint256 => User) private users;

    mapping(address => uint256) private userIds;

    mapping(string => uint256) private usernames;

    mapping(uint256 => hit) private hitLog;

    mapping(uint16 => uint256) private levelLog;

    function getUserId(address _user) public constant returns (uint256){
        return userIds[_user];
    }

    function getAddressById(uint256 _id) public constant returns(address){
        return users[_id].useraddress;
    }

    function getIdByUsername(string _name) public constant returns (uint256){
        address useraddress = getAddressByUsername(_name);
        return getUserId(useraddress);
    }

    function getAddressByUsername(string _name) public constant returns (address){
        return getAddressById(usernames[_name]);
    }

    function getUsername(uint _id) public constant returns (string){
        return users[_id].name;
    }

    function getLastHit(uint256 _id) public constant returns (uint256){
        return users[_id].lastHit;
    }

    function getLastHitBy(uint256 _id) public constant returns (uint256){
        return users[_id].lastHitBy;
    }

    function getUserLevel(uint256 _id) public constant returns (uint16){
        return users[_id].level;
    }

    function getMaxLevel(uint256 _id) public constant returns (uint16){
        return users[_id].maxLevel;
    }

    function getHitsTaken(uint256 _id) public constant returns (uint256){
        return users[_id].hitsTaken;
    }

    function getHitsGiven(uint256 _id) public constant returns (uint256){
        return users[_id].hitsGiven;
    }

    function getFullUserInfo(uint256 _id) public
        constant returns(address useraddress,
                         uint16 level,
                         uint16 maxLevel,
                         uint256 lastHit,
                         uint256 lastHitBy,
                         uint256 hitsTaken,
                         uint256 hitsGiven){
        return(
            getAddressById(_id),
            getUserLevel(_id),
            getMaxLevel(_id),
            getLastHit(_id),
            getLastHitBy(_id),
            getHitsTaken(_id),
            getHitsGiven(_id)
        );

    }

    function getHitLogEntry(uint256 _entry) public constant returns(uint256, uint256){
        return (hitLog[_entry].userId, hitLog[_entry].enemyId);
    }

    function getLevelLogEntry(uint16 _entry) public constant returns(uint256){
        return levelLog[_entry];
    }

    function setUsername(address _user, string _name) public payable{
        require(msg.sender == engine);
        require(bytes(_name).length > 0);
        // username must be unique and should not be taken
        require(getAddressByUsername(_name) == address(0));

        uint256 userId = userIds[_user];
        if (userId == 0){
            addNewUser(_user);
            userId = userIds[_user];
        }

        // store username setting
        users[userId].name = _name;
        usernames[_name] = userId;
    }

    function addNewUser(address _user) public{
        require(msg.sender == engine);

        uint256 _userId = userIds[_user];
        // user needs to be new!
        require(_userId == 0);

        // ad new user
        nUsers += 1;

        // count levels
        levelLog[0] += 1;

        // add user to user ids
        userIds[_user] = nUsers;
        users[nUsers].useraddress = _user;
    }

    // Adds a hit, i.e. a throw `_by` hitting `_to`
    function addHit(uint256 _by, uint256 _to, uint16 _loss) public{
        require(msg.sender == engine);
        uint16 oldLevel;
        uint16 newLevel;

        users[_to].lastHitBy = _by;
        users[_to].lastHit = now;
        users[_to].hitsTaken += 1;
        users[_by].hitsGiven += 1;
        totalHits += 1;

        oldLevel = users[_to].level;
        newLevel = oldLevel - _loss;
        if (newLevel > oldLevel){
            // wrap around
            newLevel = 0;
        }
        changeLevelLog(_to, oldLevel, newLevel);

        oldLevel = users[_by].level;
        newLevel = oldLevel + 1;
        changeLevelLog(_by, oldLevel, newLevel);

        if (newLevel > users[_by].maxLevel){
            users[_by].maxLevel = newLevel;
        }

        hitLog[totalHits].userId = _by;
        hitLog[totalHits].enemyId = _to;
    }

    // internal function to update the log
    // i.e. move one entry higher or lower
    function changeLevelLog(uint256 _id, uint16 _old, uint16 _new) internal{
        users[_id].level = _new;
        levelLog[_old] -= 1;
        levelLog[_new] += 1;
    }
}


contract SnowballEngine is TakesEther {

    string public constant version = '0.1';

    address public balls;
    address public gold;
    address public base;

    uint256 public usernamePrice = 0;
    uint256 public throwPrice = 0;
    uint256 public minBalance = 1 finney;
    uint256 public maxBalls = 1024;
    uint256 public maxGold = 128;
    uint256 public newPlayerBonus = 3;
    uint256 public usernameBonus = 3;
    uint16 public minGoldLevel = 2;
    uint16 public levelLoss = 2;
    uint256 public freezeTime = 30 minutes;
    bool public active = true;

    function setDependencies(address _balls,
                            address _gold,
                            address _base) public{
        require(msg.sender == owner);
        balls = _balls;
        gold = _gold;
        base = _base;
    }

    function setRules(uint256 _time, uint256 _balls,
                      uint256 _gold, uint16 _exp, uint256 _bonus,
                      uint16 _loss) public {
        require(msg.sender == owner);
        maxGold = _gold;
        maxBalls = _balls;
        freezeTime = _time;
        minGoldLevel = _exp;
        newPlayerBonus = _bonus;
        levelLoss = _loss;
    }

    function setUsernameBonus(uint256 _bonus) public {
        require(msg.sender == owner);
        usernameBonus = _bonus;
    }

    function setUsernamePrice(uint256 _amount) public{
        require(msg.sender == owner);
        usernamePrice = _amount;
    }

    function setThrowPrice(uint256 _price) public {
        require(msg.sender == owner);
        throwPrice = _price;
    }

    function setMinBalance(uint256 _balance) public{
        require(msg.sender == owner);
        minBalance = _balance;
    }

    function setGameState(bool _state) public{
        require(msg.sender == owner);
        active = _state;
    }

    function noFreeze(uint256 _time) public constant returns(bool){
        return now - freezeTime > _time;
    }

    function throwBall(address _enemy) public payable{
        require(active);
        require(_enemy != msg.sender);
        require(msg.sender.balance >= minBalance);
        require(msg.value >= throwPrice);

        SnowballUserbase userbase = SnowballUserbase(base);
        Snowballs snowballs = Snowballs(balls);

        uint256 enemyId = userbase.getUserId(_enemy);
        uint256 userId = userbase.getUserId(msg.sender);
        uint256 userLastHit = userbase.getLastHit(userId);

        uint16 enemyLevel = 0;
        uint16 userLevel = 0;
        uint256 enemyLastHit = 0;

        require(noFreeze(userLastHit));
        require(snowballs.throwBall(msg.sender, _enemy));

        if (userId == 0){
            // user got some snow via transfer and throws for the first time
            userbase.addNewUser(msg.sender);
            userId = userbase.getUserId(msg.sender);
        } else{
            userLevel = userbase.getUserLevel(userId);
        }
        if (enemyId == 0){
            userbase.addNewUser(_enemy);
            enemyId = userbase.getUserId(_enemy);
        } else {
            enemyLevel = userbase.getUserLevel(enemyId);
            enemyLastHit = userbase.getLastHit(enemyId);
        }

        // check if ball throwing actually has an effect
        if ((enemyLevel >= userLevel) &&
                noFreeze(enemyLastHit) &&
                (_enemy.balance >= minBalance)){
            // throw counts
            Hit(msg.sender, _enemy);
            userbase.addHit(userId, enemyId, levelLoss);

            newGoldAndBalls(userLevel, enemyLastHit);
        }
    }

    function setUsername(string _name) public payable{
        require(msg.sender.balance >= minBalance);
        require(msg.value >= usernamePrice);

        SnowballUserbase userbase = SnowballUserbase(base);
        Snowballs snowballs = Snowballs(balls);

        userbase.setUsername(msg.sender, _name);
        snowballs.rollBalls(msg.sender, usernameBonus);
    }

    function newGoldAndBalls(uint16 _userLevel, uint256 _enemyLastHit) internal {
        Snowballs snowballs = Snowballs(balls);

        uint256 newBalls = 2**uint256(_userLevel);
        if (_enemyLastHit == 0){
            // get an extra balls for new players
            newBalls += newPlayerBonus;
        }
        if (newBalls > maxBalls){
            newBalls = maxBalls;
        }

        snowballs.rollBalls(msg.sender, newBalls);

        if (_userLevel >= minGoldLevel){
            SnowGold snowGold = SnowGold(gold);

            uint256 newGold = 2**uint256(_userLevel - minGoldLevel);
            if (newGold > maxGold){
                newGold = maxGold;
            }

            snowGold.mintBars(msg.sender, newGold);
        }
    }

     // Triggered legit hit.
    event Hit(address indexed _from, address indexed _to);

}
