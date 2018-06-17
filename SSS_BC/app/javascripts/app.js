// Import the page's CSS. Webpack will know what to do with it.
import "../stylesheets/app.css";

// Import libraries we need.
import { default as Web3} from 'web3';
import { default as contract } from 'truffle-contract'

// Import our contract artifacts and turn them into usable abstractions.
import allbet_artifacts from '../../build/contracts/NetworkParticipantRegistration.json'
import allbet_artifacts2 from '../../build/contracts/NetworkToken.json'

var NetworkParticipantRegistration = contract(allbet_artifacts);
var NetworkToken = contract(allbet_artifacts2);
//z var AllBetsOneDay2 = contract(allbet_artifacts2);
var accounts;
var account;
var betN;

window.App = {

  start: function() {
    var self = this;
    NetworkParticipantRegistration.setProvider(web3.currentProvider);
    NetworkToken.setProvider(web3.currentProvider);
    // Get the initial account balance so it can be displayed.
    web3.eth.getAccounts(function(err, accs) {
      if (err != null) {
        alert("There was an error fetching your accounts.");
        return;
      }
      if (accs.length == 0) {
        alert("Couldn't get any accounts! Make sure your Ethereum client is configured correctly.");
        return;
      }
      accounts = accs;
      account = accounts[0];
      self.refreshBalance();
      //self.refreshPotAmount();
      //self.refreshBetNumber();
    });
  },

  registerParticipant: function() {
    var self = this;
    this.setStatus2("Initiating transaction for register participant... (please wait)");
    var meta;
    NetworkParticipantRegistration.deployed().then(function(instance) {
      meta = instance;
      return meta.setParticipant(account, {from: account});
    }).then(function() {
      self.setStatus2("Transaction complete!");
     // self.refreshBalance();
    }).catch(function(e) {
      console.log(e);
      self.setStatus2("Error registering participant");
    });
  },

  getParticipantID: function() {
    var self = this;
    var adr = document.getElementById("adr").value;
    this.setStatus1("Initiating transaction for get participant ID... (please wait)");
    var meta;
    NetworkParticipantRegistration.deployed().then(function(instance) {
      meta = instance;
      return meta.getParticipant(adr);
    }).then(function(value) {
      self.setStatus1("Transaction complete!");

      var idParticipant_element = document.getElementById("idParticipant");
      idParticipant_element.innerHTML = value.valueOf();
    }).catch(function(e) {
      console.log(e);
      self.setStatus1("Error getting participant id");
    });
  },

  refreshBalance: function() {
    var self = this;
    var meta;
    NetworkToken.deployed().then(function(instance) {
      meta = instance;
      return meta.balanceOf.call(account, {from: account});
    }).then(function(value) {
      var balance_element = document.getElementById("balance");
      balance_element.innerHTML = value.valueOf();
    }).catch(function(e) {
      console.log(e);
      self.setStatus("Error getting balance; see log.");
    });
  },

    transfer: function() {
    var self = this;

    var amount = parseInt(document.getElementById("amount").value);
    var receiver = document.getElementById("receiver").value;

    this.setStatus("Initiating transaction... (please wait)");

    var meta;
    NetworkToken.deployed().then(function(instance) {
      meta = instance;
      return meta.transfer(receiver, amount, {from: account});
    }).then(function() {
      self.setStatus("Transaction complete!");
      self.refreshBalance();
    }).catch(function(e) {
      console.log(e);
      self.setStatus("Error sending tokens; see log.");
    });
  },

  setStatus: function(message) {
    var status = document.getElementById("status");
    status.innerHTML = message;
  },

  setStatus1: function(message) {
    var status = document.getElementById("status1");
    status.innerHTML = message;
  },

  setStatus2: function(message) {
    var status = document.getElementById("status2");
    status.innerHTML = message;
  }

};

window.addEventListener('load', function() {
  // Checking if Web3 has been injected by the browser (Mist/MetaMask)
  if (typeof web3 !== 'undefined') {
    console.warn("Using web3 detected from external source. If using MetaMask, see the following link. Feel free to delete this warning. :) http://truffleframework.com/tutorials/truffle-and-metamask")
    // Use Mist/MetaMask's provider
    window.web3 = new Web3(web3.currentProvider);
  } else {
    console.warn("No web3 detected. Falling back to http://localhost:8545. You should remove this fallback when you deploy live, as it's inherently insecure. Consider switching to Metamask for development. More info here: http://truffleframework.com/tutorials/truffle-and-metamask");
    // fallback - use your fallback strategy (local node / hosted node + in-dapp id mgmt / fail)
    window.web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
  }

  App.start();
});
