pragma solidity ^0.4.2;


contract TransferTokensToParticipant {

	mapping (address => uint) tokens;

	//event Transfer(address indexed _from, address indexed _to, uint256 _value);

	function TransferTokensToParticipant() {
		tokens[tx.origin] = 10000;
	}

	function sendTokens(address participant, uint amount) returns(bool sufficient) {
		if (tokens[msg.sender] < amount) return false;
		tokens[msg.sender] -= amount;
		tokens[participant] += amount;
		//tokens(msg.sender, participant, amount);
		return true;
	}

	/*function getBalanceInEth(address addr) returns(uint){
		return ConvertLib.convert(getBalance(addr),2);
	}*/

	function getTokens(address addr) constant returns(uint) {
		return tokens[addr];
	}
}