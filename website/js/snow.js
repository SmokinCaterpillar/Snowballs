

var Eth = require('ethjs-query');
var EthContract = require('ethjs-contract');
var BigNumber = require('bignumber.js');

var Web3 = require('web3');




















window.addEventListener('load', function() {

  // Check if Web3 has been injected by MetaMask:
  if (typeof web3 !== 'undefined') {
    // You have a web3 plugin, Start the DApp
      web3 = new Web3(web3.currentProvider);
      startApp();
  } else {
      console.log('You need a Web3 plugin like MetaMask for your browser to trade souls on this website.\n' +
          'Visit https://metamask.io/ to install the plugin.');
      web3 = new Web3(new Web3.providers.HttpProvider('https://ropsten.infura.io/RP37rz6ONK5OilQuWaqc'))
      startAppNoWeb3();
  }
});


console.log('Soul Script loaded.');