/*
* This is the source code of the smart contract for the SOUL token, aka Soul Napkins.
* Copyright 2017 and all rights reserved by the owner of the following Ethereum address:
* 0x10E44C6bc685c4E4eABda326c211561d5367EEec
*/

pragma solidity ^0.4.18;

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


contract TakesDonations{

    address private beneficiary;

    function TakesDonations(address _beneficiary){
        beneficiary = _beneficiary;
    }

    function withdraw() public{
        // send donations to owner
        require(msg.sender == beneficiary);
        beneficiary.transfer(this.balance);
    }

    function () public payable{
        // just take donations
    }

}


contract HasEngine is TakesDonations{

    // address of game enigne, i.e. game rules
    address public engine;

    address public owner;

    function HasEngine(address _owner, address _engine)
        TakesDonations(_owner){
        owner = _owner;
        engine = _engine;
    }

    // Can update or change the game Engine
    function changeEngine(address _engine) public{
        require(msg.sender == owner);
        engine = _engine;
    }
}


contract Snowballs is ERC20Token, HasEngine {
    // Token symbol
    string public symbol = 'SNOW';

    // Name of token
    string public name = 'Snowballs';

    // Snowballs cannot be divided
    uint8 public decimals = 0;

    // total supply of tokens
    // increased with every tap
    uint256 private internalSupply;

    function Snowballs(address _owner, address _engine)
        HasEngine(_owner, _engine){
        // dev supply
        internalSupply = 42000;
        balances[owner] = internalSupply;
        Transfer(this, owner, internalSupply);
    }

    function totalSupply() public constant returns (uint256){
        return internalSupply;
    }

    function throwBall(address _from, address _to) public returns(bool){
        // this can only be triggered by the game
        require(msg.sender == engine);
        return executeTransfer(_from, _to, 1);
    }

    function rollBalls(address _to, uint256 _amount){
        // this can only be triggered by the game
        require(msg.sender == engine);

        // check for wrap aroung
        require(balances[_to] + _amount > balances[_to]);
        require(internalSupply + _amount > internalSupply);

        // roll the new balls
        internalSupply += _amount;
        balances[_to] += _amount;
    }

}


contract SnowballUserbase is HasEngine{

    struct user{
        string name;
        uint16 experience;
        uint256 lastHit;
        uint256 hitsTaken;
        uint256 hitsGiven;
        uint256 lastHitBy;
    }

    uint256 public nUsers;

    mapping(uint256 => user) private users;

    mapping(address => uint256) private userIds;

    mapping(string => address) private usernames;

    function getUserId(address _user) public constant returns (uint256){
        return userIds[_user];
    }

    function getAddressByUsername(string _name) public constant returns (address){
        return usernames[_name];
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


    function setUsername(string _name){
        // username must be unique and should not be taken
        require(getAddressByUsername(_name) == address(0));
        uint256 userId = userIds[msg.sender];

        // must be existing user;
        require(userId > 0);

        // store username setting
        users[userId].name = _name;
        usernames[_name] = msg.sender;
    }

    function addNewUser(address _user) public{
        require(msg.sender == engine);

        uint256 _userId = userIds[_user];
        // user needs to be new!
        require(_userId == 0);

        // ad new user
        nUsers += 1;

        // add user to user ids
        userIds[_user] = nUsers;
    }

    function addHit(uint256 _by, uint256 _to) {
        require(msg.sender == engine);
        users[_to].lastHitBy = _by;
        users[_to].lastHit = now;
        users[_to].hitsTaken += 1;
        users[_by].hitsGiven += 1;
    }

    function setExp(uint256 _id, uint16 _exp) public{
        require(msg.sender == engine);
        users[_id].experience = _exp;
    }

    function resetHitBy(uint256 _id) public{
        require(msg.sender == engine);
        users[_id].lastHitBy = 0;
        users[_id].lastHit = 0;
    }

}


contract SnowballRules{

    uint16 public constant maxLevel = 9;
    uint16 public constant expPerLevel = 3;

    function getLevel(uint16 experience) public constant returns(uint16){
        return experience / expPerLevel;
    }

    function allowedToThrow(uint256 _lastHit) public returns(bool){
        return true;
    }

}


contract SnowballEngine is TakesDonations{

    address balls;
    address base;
    address rules;



    function throwBall(address _enemy) public payable{
        Snowballs snowballs = Snowballs(balls);
        SnowballUserbase userbase = SnowballUserbase(base);
        SnowballRules snowrules = SnowballRules(rules);

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
        } else{
            userExp = userbase.getUserExp(userId);
            userLevel = snowrules.getLevel(userExp);
        }

        require(snowrules.allowedToThrow(userLastHit));
        require(snowballs.throwBall(msg.sender, _enemy));

        if (enemyId == 0){
            userbase.addNewUser(_enemy);
        } else {
            enemyExp = userbase.getUserExp(enemyId);
            enemyLevel = snowrules.getLevel(enemyExp);
            enemyHityById = userbase.getLastHitBy(enemyId);
        }

        // check if ball throwing actually has an effect
        if (enemyLevel < snowrules.maxLevel() && enemyLevel <= userLevel){
            // throw counts
            userbase.addHit(userId, enemyId);

            if (enemyLevel == userLevel && enemyHityById == 0){
                gatherExperience(userId, userExp, userLevel);
            }
        }
    }

    function gatherExperience(uint256 userId,
                              uint16 userExp,
                              uint16 userLevel) internal {
        SnowballUserbase userbase = SnowballUserbase(base);
        SnowballRules snowrules = SnowballRules(rules);

        uint16 newExp = userExp += 1;
        uint16 newLevel = snowrules.getLevel(newExp);

        userbase.setExp(userId, newExp);

        if (newLevel > userLevel){
            userbase.resetHitBy(userId);
        }
    }

}