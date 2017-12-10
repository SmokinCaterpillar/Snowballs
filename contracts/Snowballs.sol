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
    }

}


contract TakesEther {

    address public owner;

    function TakesEther(){
        owner = msg.sender;
    }

    function withdraw() public{
        // send donations to owner
        require(msg.sender == owner);
        owner.transfer(this.balance);
    }

    function changeOwnership(address _owner) public{
        require(msg.sender == owner);
        owner = _owner;
    }

    function () public payable{
        // just take donations
    }

}


contract HasEngine is TakesEther {

    // address of game enigne, i.e. game rules
    address public engine;

    function HasEngine(address _engine){
        engine = _engine;
    }

    // Can update or change the game Engine
    function changeEngine(address _engine) public{
        require(msg.sender == owner);
        engine = _engine;
    }
}





contract SnowGold is MintableToken, HasEngine {
    string public constant version = '0.1.0';

    // Token symbol
    string public symbol = 'SGC';

    // Name of token
    string public name = 'Snow Gold';

    // Gold = BTC
    uint8 public decimals = 8;

    uint256 public unit = 100000000;

    function SnowGold(address _engine)
        HasEngine(_engine){
        // dev supply
        internalSupply = 33333 * unit;
        balances[owner] = internalSupply;
        Transfer(this, owner, internalSupply);
    }

    function mintBars(address _to, uint256 _amount){
        // this can only be triggered by the game
        require(msg.sender == engine);

        mint(_to, _amount * unit);

    }
}


contract SnowGodMedals is MintableToken, HasEngine {

    string public constant version = '0.1';

    // Token symbol
    string public symbol = 'GOD';

    // Name of token
    string public name = 'Snow God Medals';

    // Gold = BTC
    uint8 public decimals = 0;

    function SnowGodMedals(address _engine)
        HasEngine(_engine){
        // dev supply
        internalSupply = 42;
        balances[owner] = internalSupply;
        Transfer(this, owner, internalSupply);
    }

    function mintMedal(address _to){
        // this can only be triggered by the game
        require(msg.sender == engine);

        mint(_to, 1);

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
        HasEngine( _engine){
        // dev supply
        internalSupply = 99999;
        balances[owner] = internalSupply;
        Transfer(this, owner, internalSupply);
    }

    function throwBall(address _from, address _to) public returns(bool){
        // this can only be triggered by the game
        require(msg.sender == engine);
        return executeTransfer(_from, _to, 1);
    }

    function rollBalls(address _to, uint256 _amount){
        // this can only be triggered by the game
        require(msg.sender == engine);

        mint(_to, _amount);

    }

}


contract SnowballUserbase is HasEngine{

    string public constant version = '0.1';

    struct User{
        string name;
        address useraddress;
        uint16 experience;
        uint256 lastHit;
        uint256 lastHitBy;
        uint256 hitsTaken;
        uint256 hitsGiven;
    }

    struct hit{
        uint256 userId;
        uint256 enemyId;
    }

    function SnowballUserbase(address _engine)
        HasEngine(_engine){

    }

    uint256 public totalHits;

    uint256 public nUsers;

    uint256 public usernamePrice = 0;

    mapping(uint256 => User) private users;

    mapping(address => uint256) private userIds;

    mapping(string => uint256) private usernames;

    mapping(uint256 => hit) private hitLog;

    mapping(uint16 => uint256) private experienceLog;

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

    function getUserExp(uint256 _id) public constant returns (uint16){
        return users[_id].experience;
    }

    function getHitsTaken(uint256 _id) public constant returns (uint256){
        return users[_id].hitsTaken;
    }

    function getHitsGiven(uint256 _id) public constant returns (uint256){
        return users[_id].hitsGiven;
    }

    function getFullUserInfo(uint256 _id) public constant returns(string name,
                                                                    address useraddress,
                                                                    uint16 experience,
                                                                    uint256 lastHit,
                                                                    uint256 lastHitBy,
                                                                    uint256 hitsTaken,
                                                                    uint256 hitsGiven){
        return(
            getUsername(_id),
            getAddressById(_id),
            getUserExp(_id),
            getLastHit(_id),
            getLastHitBy(_id),
            getHitsTaken(_id),
            getHitsGiven(_id)
        );

    }

    function getHitLogEntry(uint256 _entry) public constant returns(uint256, uint256){
        return (hitLog[_entry].userId, hitLog[_entry].enemyId);
    }

    function getExperiencLogEntry(uint16 _entry) public constant returns(uint256){
        return experienceLog[_entry];
    }

    function setUsernamePrice(uint256 _amount) public{
        require(msg.sender == owner);
        usernamePrice = _amount;
    }

    function setUsername(string _name) public payable{
        require(msg.value >= usernamePrice);
        // username must be unique and should not be taken
        require(getAddressByUsername(_name) == address(0));
        uint256 userId = userIds[msg.sender];

        // must be existing user;
        require(userId > 0);

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

        // count experiences
        experienceLog[0] += 1;

        // add user to user ids
        userIds[_user] = nUsers;
        users[nUsers].useraddress = _user;
    }

    function addHit(uint256 _by, uint256 _to) {
        require(msg.sender == engine);
        users[_to].lastHitBy = _by;
        users[_to].lastHit = now;
        users[_to].hitsTaken += 1;
        users[_by].hitsGiven += 1;

        totalHits += 1;

        hitLog[totalHits].userId = _by;
        hitLog[totalHits].enemyId = _to;
    }

    function setExp(uint256 _id, uint16 _exp) public{
        require(msg.sender == engine);
        uint16 oldExp = users[_id].experience;
        experienceLog[oldExp] -= 1;
        users[_id].experience = _exp;
        experienceLog[_exp] += 1;
    }

    function resetHitBy(uint256 _id) public{
        require(msg.sender == engine);
        users[_id].lastHitBy = 0;
        users[_id].lastHit = 0;
    }

}


contract SnowballRules is HasEngine{

    string public constant version = '0.1';

    uint16 public maxLevel = 9;
    uint16 public expPerLevel = 3;

    bool public gameActive = true;

    mapping (uint16 => uint256) public level2balls;
    mapping (uint16 => uint256) public level2gold;
    mapping (uint16 => uint256) public level2time;
    mapping (uint16 => string) public level2rank;

    function SnowballRules(address _engine)
        HasEngine(_engine){
        setBallsPerLevel();
        setGoldPerLevelUp();
        setWaitingTimePerLevel();
        setLevelNames();
    }

    function setBallsPerLevel() private{
        level2balls[0] = 2;
        level2balls[1] = 4;
        level2balls[2] = 8;
        level2balls[3] = 16;
        level2balls[4] = 32;
        level2balls[5] = 64;
        level2balls[6] = 128;
        level2balls[7] = 256;
        level2balls[8] = 512;
        level2balls[9] = 2048;
    }

    function setGoldPerLevelUp() private{
        level2gold[2] = 1;
        level2gold[3] = 2;
        level2gold[4] = 4;
        level2gold[5] = 8;
        level2gold[6] = 16;
        level2gold[7] = 32;
        level2gold[8] = 64;
        level2gold[9] = 293;
    }

    function setWaitingTimePerLevel() private{
        level2time[0] = 48 hours;
        level2time[1] = 40 hours;
        level2time[2] = 36 hours;
        level2time[3] = 32 hours;
        level2time[4] = 28 hours;
        level2time[5] = 24 hours;
        level2time[6] = 20 hours;
        level2time[7] = 16 hours;
        level2time[8] = 12 hours;
    }

    function setLevelNames() private{
        level2rank[0] = 'Snow White';
        level2rank[1] = 'Snow Cadet';
        level2rank[2] = 'Snow Officer';
        level2rank[3] = 'Snow Lieutenant';
        level2rank[4] = 'Snow Commander';
        level2rank[5] = 'Snow Captain';
        level2rank[6] = 'Snow General';
        level2rank[7] = 'Snow High Priest';
        level2rank[8] = 'Snow Demigod';
        level2rank[9] = 'Snow God';
    }

    function getLevel(uint16 _experience) public constant returns(uint16){
        return _experience / expPerLevel;
    }

    function allowedToThrow(uint16 _level, uint256 _lastHit) public returns(bool){
        return gameActive && (now > _lastHit + level2time[_level]);
    }

    function setGameState(bool _state) public{
        require(msg.sender == owner);
        gameActive = _state;
    }

    function setMaxLevel(uint16 _level) public {
        require(msg.sender == owner);
        maxLevel = _level;
    }

    function setExpPerLevel(uint16 _exp) public {
        require(msg.sender == owner);
        expPerLevel = _exp;
    }

    function setLevelName(uint16 _level, string _name) public {
        require(msg.sender == owner);
        level2rank[_level] = _name;
    }

    function setLevelWaitingTime(uint16 _level, uint256 _time) public {
        require(msg.sender == owner);
        level2time[_level] = _time;
    }

    function setLevelUpGold(uint16 _level, uint256 _gold) public {
        require(msg.sender == owner);
        level2gold[_level] = _gold;
    }

    function setLevelBalls(uint16 _level, uint256 _balls) public {
        require(msg.sender == owner);
        level2balls[_level] = _balls;
    }

}

contract SnowRelics is HasEngine{

    string public constant version = '0.0';

    function SnowRelics(address _engine)
        HasEngine(_engine){}

    function huntRelic(uint256 _userId, uint256 _enemyId){
        require(msg.sender == engine);
        // TODO create relic game logic!
    }
}


contract SnowballEngine is TakesEther {

    string public constant version = '0.1';

    address public balls;
    address public gold;
    address public medals;
    address public base;
    address public rules;
    address public relics;

    uint256 throwPrice = 0;

    function setDependencies(address _balls,
                            address _gold,
                            address _medals,
                            address _base,
                            address _rules,
                            address _relics) public{
        require(msg.sender == owner);
        balls = _balls;
        gold = _gold;
        medals = _medals;
        base = _base;
        rules = _rules;
        relics = _relics;
    }

    function setThrowPrice(uint256 _price){
        require(msg.sender == owner);
        throwPrice = _price;
    }

    function throwBall(address _enemy) public payable{
        require(_enemy != msg.sender);
        require(msg.value >= throwPrice);

        Snowballs snowballs = Snowballs(balls);
        SnowballUserbase userbase = SnowballUserbase(base);
        SnowballRules snowrules = SnowballRules(rules);
        SnowRelics snowrelics = SnowRelics(relics);

        uint256 enemyId = userbase.getUserId(_enemy);
        uint256 userId = userbase.getUserId(msg.sender);
        uint256 enemyHityById = 0;
        uint256 userLastHit = userbase.getLastHit(userId);

        uint16 enemyLevel = 0;
        uint16 enemyExp = 0;
        uint16 userLevel = 0;
        uint16 userExp = 0;

        // user got some snow via transfer and throws for the first time
        if (userId == 0){
            userbase.addNewUser(msg.sender);
            userId = userbase.getUserId(msg.sender);
        } else{
            userExp = userbase.getUserExp(userId);
            userLevel = snowrules.getLevel(userExp);
        }

        require(snowrules.allowedToThrow(userLevel, userLastHit));
        require(snowballs.throwBall(msg.sender, _enemy));

        if (enemyId == 0){
            userbase.addNewUser(_enemy);
            enemyId = userbase.getUserId(_enemy);
        } else {
            enemyExp = userbase.getUserExp(enemyId);
            enemyLevel = snowrules.getLevel(enemyExp);
            enemyHityById = userbase.getLastHitBy(enemyId);
        }

        // check if ball throwing actually has an effect
        if (enemyLevel < snowrules.maxLevel() && enemyLevel <= userLevel){
            // throw counts
            Hit(msg.sender, _enemy);
            userbase.addHit(userId, enemyId);
            snowrelics.huntRelic(userId, enemyId);

            if (enemyLevel == userLevel && enemyHityById == 0){
                gatherExperience(userId, userExp, userLevel);
            }
        }
    }

    function gatherExperience(uint256 _userId,
                              uint16 _userExp,
                              uint16 _userLevel) internal {
        SnowballUserbase userbase = SnowballUserbase(base);
        SnowballRules snowrules = SnowballRules(rules);
        Snowballs snowballs = Snowballs(balls);

        assert(_userLevel < snowrules.maxLevel());

        uint16 newExp = _userExp += 1;
        uint16 newLevel = snowrules.getLevel(newExp);
        uint256 newBalls = snowrules.level2balls(_userLevel);

        snowballs.rollBalls(msg.sender, newBalls);
        userbase.setExp(_userId, newExp);

        Experience(msg.sender);

        if (newLevel > _userLevel){
            SnowGold snowGold = SnowGold(gold);
            uint256 newgold = snowrules.level2gold(newLevel);
            snowGold.mintBars(msg.sender, newgold);

            userbase.resetHitBy(_userId);

            LevelUp(msg.sender);

            if (newLevel == snowrules.maxLevel()){
                SnowGodMedals snowMedals = SnowGodMedals(medals);
                snowMedals.mintMedal(msg.sender);

                newBalls = snowrules.level2balls(newLevel);
                snowballs.rollBalls(msg.sender, newBalls);

                BecameGod(msg.sender);
            }
        }
    }

     // Triggered when tokens are transferred.
    event Hit(address indexed _from, address indexed _to);

    // Triggered whenever approve(address _spender, uint256 _value) is called.
    event Experience(address indexed _user);

    event LevelUp(address indexed _user);

    event BecameGod(address indexed _user);

}