
var NetworkParticipantRegistration = artifacts.require("./NetworkParticipantRegistration.sol");
var TransferTokensToParticipant = artifacts.require("./TransferTokensToParticipant.sol");
var NetworkToken = artifacts.require("./NetworkToken.sol");

module.exports = function(deployer) {
  deployer.deploy(NetworkParticipantRegistration);
  deployer.deploy(TransferTokensToParticipant);
  deployer.deploy(NetworkToken);
};