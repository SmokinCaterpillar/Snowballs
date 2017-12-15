var Eth = require('ethjs-query');
var EthContract = require('ethjs-contract');
var BigNumber = require('bignumber.js');


var Web3 = require('web3');


const engineAddress = '0x7d63d05a9f4c70d5c5ae1e61f74cd8b343f6d082';
const engineABI = [{"constant":true,"inputs":[],"name":"active","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_enemy","type":"address"}],"name":"throwBall","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"maxBalls","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_time","type":"uint256"}],"name":"noFreeze","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_owner","type":"address"}],"name":"changeOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"usernameBonus","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_bonus","type":"uint256"}],"name":"setUsernameBonus","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_state","type":"bool"}],"name":"setGameState","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"base","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"throwPrice","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"version","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"balls","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"usernamePrice","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"newPlayerBonus","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_price","type":"uint256"}],"name":"setThrowPrice","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"minGoldLevel","outputs":[{"name":"","type":"uint16"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_balls","type":"address"},{"name":"_gold","type":"address"},{"name":"_base","type":"address"}],"name":"setDependencies","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"minBalance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_balance","type":"uint256"}],"name":"setMinBalance","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_time","type":"uint256"},{"name":"_balls","type":"uint256"},{"name":"_gold","type":"uint256"},{"name":"_exp","type":"uint16"},{"name":"_bonus","type":"uint256"}],"name":"setRules","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_name","type":"string"}],"name":"setUsername","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"maxGold","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_amount","type":"uint256"}],"name":"setUsernamePrice","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"gold","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"freezeTime","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"}],"name":"Hit","type":"event"}]
var engine;

const ballsAddress ='0xeb567f17cb69c24f9f335a95f249eb498495cbc7';
const ballsABI = [{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_amount","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"}],"name":"throwBall","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_owner","type":"address"}],"name":"changeOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_engine","type":"address"}],"name":"changeEngine","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"rollBalls","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"version","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"engine","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_engine","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}];
var balls;

const goldAddress = '0xd4b92793a48251cf2fba1bc4bed6964f14ca352d';
const goldABI = [{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_amount","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_owner","type":"address"}],"name":"changeOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_engine","type":"address"}],"name":"changeEngine","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"version","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mintBars","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"unit","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"engine","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_engine","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}];
var gold;

const baseAddress = '0x4517176ff148a8fe4b2073439f0334a7728efa52';
const baseABI = [{"constant":true,"inputs":[{"name":"_entry","type":"uint256"}],"name":"getHitLogEntry","outputs":[{"name":"","type":"uint256"},{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_owner","type":"address"}],"name":"changeOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_user","type":"address"}],"name":"getUserId","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_engine","type":"address"}],"name":"changeEngine","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_id","type":"uint256"}],"name":"getUserLevel","outputs":[{"name":"","type":"uint16"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalHits","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"version","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_id","type":"uint256"}],"name":"getHitsTaken","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_id","type":"uint256"}],"name":"getLastHit","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_name","type":"string"}],"name":"getAddressByUsername","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"nUsers","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_id","type":"uint256"}],"name":"getAddressById","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_id","type":"uint256"}],"name":"getMaxLevel","outputs":[{"name":"","type":"uint16"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_entry","type":"uint16"}],"name":"getLevelLogEntry","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_id","type":"uint256"}],"name":"getFullUserInfo","outputs":[{"name":"useraddress","type":"address"},{"name":"level","type":"uint16"},{"name":"maxLevel","type":"uint16"},{"name":"lastHit","type":"uint256"},{"name":"lastHitBy","type":"uint256"},{"name":"hitsTaken","type":"uint256"},{"name":"hitsGiven","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_id","type":"uint256"}],"name":"getLastHitBy","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_user","type":"address"}],"name":"addNewUser","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"engine","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_name","type":"string"}],"name":"getIdByUsername","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_user","type":"address"},{"name":"_name","type":"string"}],"name":"setUsername","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"_by","type":"uint256"},{"name":"_to","type":"uint256"}],"name":"addHit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_id","type":"uint256"}],"name":"getUsername","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_id","type":"uint256"}],"name":"getHitsGiven","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_engine","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]
var base;

const goldUnit = 100000000;
const minTime = 0.5;
const minBalance = 0.001;
const defaultGasLimit = 555000;

var withMeta;
var metaUnlocked;
var account;



const nullAddress = "0x0000000000000000000000000000000000000000";

var ballBalance = 'N/A';
var level = 'N/A';
var maxLevel = 'N/A';
var lastHit = 0;
var lastHitBy = 'N/A';
var hitsTaken = 'N/A';
var hitsGiven = 'N/A';
var goldBalance = 'N/A';
var address = 'N/A';
var userId = 'N/A';
var username = 'N/A';
var ethBalance = 'N/A';


var enemyBallBalance = 'N/A';
var enemyLevel = 'N/A';
var enemyMaxLevel = 'N/A';
var enemyLastHit = 0;
var enemyLastHitBy = 'N/A';
var enemyHitsTaken = 'N/A';
var enemyHitsGiven = 'N/A';
var enemyGoldBalance = 'N/A';
var enemyAccount = 'N/A';
var enemyUserId = 'N/A';
var enemyUsername = 'N/A';
var enemyETHBalance = 'N/A';


var totalUsers = 'N/A';
var totalBalls = 'N/A';
var totalGold = 'N/A';
var totalHits = 'N/A';

var levelLog = {};
const nLevels = 10;
var hitLog = {};
const nHits = 10;

////////////////////////// UTILS ///////////////////////////////////////////

function convertTimestamp(timestamp){
    var now = new BigNumber(Math.floor(Date.now() / 1000));

    var hoursAgo = now.minus(timestamp);
    hoursAgo = hoursAgo.dividedBy(3600).round(2);

    return hoursAgo
}


function createContracts(){
    const eth = new Eth(web3.currentProvider);
    const contract = new EthContract(eth);

    const Engine = contract(engineABI);
    engine = Engine.at(engineAddress);

    const Balls = contract(ballsABI);
    balls = Balls.at(ballsAddress);

    const Gold = contract(goldABI);
    gold = Gold.at(goldAddress);

    const Base = contract(baseABI);
    base = Base.at(baseAddress);

}


function startApp() {

    createContracts();
    listenForEnemyFindClicks();
    listenForThrowClicks();
    listenForNewUsernameClicks();
    checkUser();
    checkStats();


}

function checkStats(){
    collectTotalBalls();
    collectTotalGold();
    collectTotalUsers();
    collectTotalHits();
    collectLeveLog();
}

function checkUser(){
    if (withMeta) {
        getAccount();
        if (metaUnlocked) {
            collectBallBalance();
            collectGoldBalance();
            collectEthBlance();
        }
        collectUserInfo();
    } else {
        metaUnlocked = false;
    }
}


function listenForEnemyFindClicks() {
  var button = document.getElementById('findButton');
  button.addEventListener('click', function() {

      checkUser();
      checkStats();

      var enemy = document.getElementById("enemyID").value;

      console.log('Clicked info about enemy ' +  enemy);
      var isAddress = enemy.startsWith('0x');
      if (isAddress){
          enemyAccount = enemy;
          collectEnemyInfo();
      } else {
          base.getAddressByUsername(enemy).then( function (results){
              enemyAccount = results[0];
              console.log('enemy Account ' + enemyAccount)

              if (enemyAccount == nullAddress){
                  alert('Invalid username!');
              } else {
                  collectEnemyInfo();
              }
          })
      }
  })
}


function listenForThrowClicks() {
  var button = document.getElementById('throwBall');
  button.addEventListener('click', function() {
      if (metaUnlocked) {
          var lastHitinH = convertTimestamp(lastHit);

          if (lastHitinH <= minTime){
              alert('You are still paralzed from the last Hit wait some time!')
          } else if (ballBalance === 0){
              alert('You do not own a single Snowball!')
          } else if (ethBalance < minBalance){
              alert('You have insufficient ETH funds to participate!')
          } else if (enemyAccount === 'N/A') {
              alert('Plese search for a target enemy before throwing')
          } else if (enemyAccount == account){
              alert('You cannot hit yourself? What is wrong with you?')
          } else {
              console.log('Throwing at ' + enemyAccount);
              engine.throwBall(enemyAccount, {
                  from: account,
                  gas: defaultGasLimit
              }).then(function (txHash) {
                  console.log('Transaction sent');
                  console.dir(txHash);
              });
          }
      } else {
          alert('Please install and/or unlock MetaMask!')
      }

  })
}

function listenForNewUsernameClicks() {
  var button = document.getElementById('setUsername');
  button.addEventListener('click', function() {
      if (metaUnlocked) {
          var newUsername = document.getElementById("usernameField").value;

          if (newUsername == '') {
              alert('Your username cannot be empty');
          } else if (ethBalance < minBalance){
              alert('Your account has insufficient funds to participate!');
          } else {
              base.getAddressByUsername(newUsername).then(function (results){
                  var foundUser = results[0];
                  console.log('Username found for ' + foundUser);

                  if (foundUser != nullAddress){
                      alert('Sorry username already taken!')
                  } else {
                      engine.setUsername(newUsername, {
                          from: account,
                          gas: defaultGasLimit / 2
                      }).then(function (txHash) {
                          console.log('Transaction sent');
                          console.dir(txHash);
                      });
                  }
              })
          }
      } else {
          alert('Please install and/or unlock MetaMask!')
      }

  })
}

function getAccount(){
    account = web3.eth.coinbase;
    console.log('Found user account ' + account)
    if (account === null){
        metaUnlocked = false;
    } else {
        metaUnlocked = true;
    }
}


function collectBallBalance(){
    balls.balanceOf(account).then(function (results){
        ballBalance = results[0];
        console.log('ballBalance ' + ballBalance);
        updateUI();

    }).catch(function (error) {
        console.log(error);
    })
}


function collectGoldBalance(){
    gold.balanceOf(account).then(function (results){
        goldBalance = results[0];
        goldBalance = new BigNumber(goldBalance).dividedBy(goldUnit).round(2);
        console.log('goldBalance ' + goldBalance);
        updateUI();

    }).catch(function (error) {
        console.log(error);
    })
}


function collectTotalUsers(){
    base.nUsers().then(function (results){
        totalUsers = results[0];
        console.log('totalUsers ' + totalUsers);
        updateUI();

    }).catch(function (error) {
        console.log(error);
    })
}


function collectTotalBalls(){
    balls.totalSupply().then(function (results){
        totalBalls = results[0];
        console.log('totalBalls ' + totalBalls);
        updateUI();

    }).catch(function (error) {
        console.log(error);
    })
}


function collectTotalGold(){
    gold.totalSupply().then(function (results){
        totalGold = results[0];
        totalGold = new BigNumber(totalGold).dividedBy(goldUnit);
        console.log('totalGold ' + totalGold);
        updateUI();

    }).catch(function (error) {
        console.log(error);
    })
}

function collectTotalHits(){
    base.totalHits().then(function (results){
        totalHits = results[0];
        totalHits = new BigNumber(totalHits);
        console.log('totalHits ' + totalHits);
        updateUI();
        collectHitLog();

    }).catch(function (error) {
        console.log(error);
    })
}

function collectEthBlance(){
    web3.eth.getBalance(account, function (error, result) {
        if (!error) {
            ethBalance = web3.fromWei(result, 'ether');
            ethBalance = new BigNumber(ethBalance).round(5);
            console.log('ETH balance ' + ethBalance);
            updateUI();
        } else {
            console.error(error);
        }
    })
}


function collectEnemyBallBalance(){
    balls.balanceOf(enemyAccount).then(function (results){
        enemyBallBalance = results[0];
        console.log('enemyballBalance ' + enemyBallBalance);
        updateUI();

    }).catch(function (error) {
        console.log(error);
    })
}


function collectEnemyGoldBalance(){
    gold.balanceOf(enemyAccount).then(function (results){
        enemyGoldBalance = results[0];
        enemyGoldBalance = new BigNumber(enemyGoldBalance).dividedBy(goldUnit);
        console.log('enemygoldBalance ' + enemyGoldBalance);
        updateUI();
    }).catch(function (error) {
        console.log(error);
    })
}


function collectEnemyEthBlance(){
    try  {
        web3.eth.getBalance(enemyAccount, function (error, result) {
            if (!error) {
                enemyETHBalance = web3.fromWei(result, 'ether');
                enemyETHBalance = new BigNumber(enemyETHBalance).round(5);
                console.log('enemy ETH balance ' + enemyETHBalance);
                updateUI();
            } else {
                console.error(error);
            }
        })
    } catch(err){
        console.log(err);
        alert('Invalid enemy address!');
    }
}


function collectUserInfo(){

    if (!metaUnlocked){
        updateUI();
    } else {
        base.getUserId(account).then(function (results) {
            userId = results[0];
            console.log('userId ' + userId);
            metaUnlocked = true;

            base.getUsername(userId).then(function (results) {
                username = results[0];
                console.log('username ' + username);
                base.getFullUserInfo(userId).then(function (results) {
                    level = results[1];
                    console.log('level ' + level);
                    maxLevel = results[2];
                    console.log('maxLevel ' + level);
                    lastHit = results[3];
                    console.log('lastHit ' + lastHit);
                    lastHitBy = results[4];
                    console.log('lastHitBy ' + lastHitBy);
                    hitsTaken = results[5];
                    console.log('hitsTaken ' + hitsTaken);
                    hitsGiven = results[6];
                    console.log('hitsGiven ' + hitsGiven);

                    updateUI();
                })
            })
        }).catch(function (error) {
            console.log(error);
        })
    }
}


function collectEnemyInfo(){
    console.log('Looking for ' + enemyAccount);

     collectEnemyBallBalance();
     collectEnemyEthBlance();
     collectEnemyGoldBalance();

     base.getUserId(enemyAccount).then(function (results) {
         enemyUserId = results[0];
         console.log('enemyUserId ' + enemyUserId);

         base.getUsername(enemyUserId).then(function (results) {
             enemyUsername = results[0];
             console.log('enemyUsername ' + username);
             base.getFullUserInfo(enemyUserId).then(function (results) {
                 enemyLevel = results[1];
                 console.log('enemyLevel ' + enemyLevel);
                 enemyMaxLevel = results[2];
                 console.log('enemyMaxLevel ' + enemyMaxLevel);
                 enemyLastHit = results[3];
                 console.log('enemyLastHit ' + enemyLastHit);
                 enemyLastHitBy = results[4];
                 console.log('enemyLastHitBy ' + enemyLastHitBy);
                 enemyHitsTaken = results[5];
                 console.log('enemyHitsTaken ' + enemyHitsTaken);
                 enemyHitsGiven = results[6];
                 console.log('enemyHitsGiven ' + enemyHitsGiven);

                 updateUI();
             });
         });
     });
}


function accessLevelLogEntry(idx){
    levelLog[idx] = 0;
    base.getLevelLogEntry(idx).then(function (results){
        var entry = results[0]
        console.log('Found level log entry ' + idx + ' ' + entry)
        levelLog[idx] = entry
        updateUI();
    })
}


function collectLeveLog(){
    for (var irun = 0; irun < nLevels; irun++){
        accessLevelLogEntry(irun);
    }
}

function addUserLogEntry(userId, idx, logidx){
    base.getUsername(userId).then(function (results){
        var thename = results[0]
        if (thename == ''){
            base.getAddressById(userId).then(function (results){
                var theaddress = results[0];
                hitLog[idx][logidx] = theaddress;
                updateUI();
            })
        } else {
            hitLog[idx][logidx] = thename;
            updateUI();
        }
    })
}


function accessHitLogEntry(idx){
    hitLog[idx] = ['TBA', 'TBA'];
    base.getHitLogEntry(idx).then(function (results){
        var from = results[0];
        var to = results[1];
        console.log('Found hit log entry ' + idx + ' ' + from + ' ' + to);
        addUserLogEntry(from, idx, 0);
        addUserLogEntry(to, idx, 1);
    })
}


function collectHitLog(){
    console.log('Searching hitlog!');
    for (var irun = 0; irun < nHits; irun++){
        var tocheck = totalHits.minus(irun);
        if (tocheck <= 0){
            break;
        }
        accessHitLogEntry(tocheck);
    }
}


function updateUI(){
    updateUserData();
    updateEnemyData();
    updateStats();
}

function updateStats(){
    var statsData = document.getElementById('stats');

    var htmlText = 'Total players: ' + totalUsers + '<br>' +
                   'Total hits: ' + totalHits + '<br>' +
                   'Total Snowball supply: ' + totalBalls + '<br>' +
                   'Total Gold supply: ' + totalGold + '<br><br>' +
                    '<h5>Level Statistics</h5>';

    for (var irun = 0; irun < nLevels; irun++) {
        htmlText += 'Level ' + irun +' players: ' + levelLog[irun] +'<br>'
        if (levelLog[irun] == 0){
            break;
        }
    }

    htmlText += '<br><h5>Recent Snowball Hits</h5>';

    for (var irun = 0; irun < nHits; irun++) {
        if (irun in hitLog) {
            htmlText += hitLog[irun][0] + ' hit ' + hitLog[irun][1] + '<br>';
        }
    }

    statsData.innerHTML = htmlText;
}


function updateUserData(){
    var userData = document.getElementById('userData');
    var htmlText = "Please unlock your MetaMask to see your balance! <br><br>";

    if (metaUnlocked) {
        var lastHitinH = convertTimestamp(lastHit);

        htmlText = 'Hello <b>' + username + '</b> your level is <b>' + level +
             '</b><br><br>' + 'You own <b>' + ballBalance +
            ' Snowballs</b> and <b>' + goldBalance + ' SnowGold</b> <br><br>' +
            'You hit <b>' + hitsGiven + ' enemys</b> and took <b>' + hitsTaken + ' hits</b><br>';

        if (lastHit != 0) {
            htmlText += '(last time was ' + lastHitinH + 'h ago)<br>';
        }
    }

    userData.innerHTML = htmlText;

    if (username !== 'N/A' && username !== ''){
        document.getElementById('usernameSetter').innerHTML = '';
        console.log('Removed username register!')
    }
}


function updateEnemyData(){
    var userData = document.getElementById('enemyData');
    var htmlText;

    if (enemyAccount !== 'N/A') {
        var lastHitinH;

        if (enemyLastHit !== 'N/A') {
            lastHitinH = convertTimestamp(enemyLastHit);
        }

        htmlText = 'Your enemy has level <b>' + enemyLevel +
            '</b><br><br>' + 'She or he owns <b>' + enemyBallBalance +
            ' Snowballs</b> and <b>' + enemyGoldBalance + ' SnowGold</b> and <b>' +
            enemyETHBalance + ' ETH</b><br><br>' +
            'She or he hit <b>' + enemyHitsGiven + ' other enemys</b> and took <b>' + enemyHitsTaken + ' hits</b><br>';

        if (enemyLastHit != 0) {
            htmlText += '(last time was ' + lastHitinH + 'h ago)<br>';
        }

        if (lastHitinH <= minTime){
            htmlText += '<br> <b>Warning</b>: Your enemy is still paralyzed!';
        }

        if (enemyETHBalance < minBalance){
            htmlText += '<br> <b>Warning</b>: Your enemy has insufficient ETH to participate!';
        }

        if (level !== 'N/A' && enemyLevel < level){
            htmlText += '<br> <b>Warning</b>: Your enemy has a lower level than you!';
        }

        enemyData.innerHTML = htmlText;
    }
}



window.addEventListener('load', function() {

  // Check if Web3 has been injected by MetaMask:
  if (typeof web3 !== 'undefined') {
    // You have a web3 plugin, Start the DApp
      web3 = new Web3(web3.currentProvider);
      withMeta = true;
      startApp();
  } else {
      console.log('You need a Web3 plugin like MetaMask for your browser to trade souls on this website.\n' +
          'Visit https://metamask.io/ to install the plugin.');
      web3 = new Web3(new Web3.providers.HttpProvider('https://ropsten.infura.io/RP37rz6ONK5OilQuWaqc'))
      withMeta = false;
      startApp();
  }
});