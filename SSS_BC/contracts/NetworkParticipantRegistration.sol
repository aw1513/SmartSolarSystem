pragma solidity ^0.4.11;

contract NetworkParticipantRegistration {
    
    address     owner;
    uint public participantID;
    mapping (address => uint) public Participants;
 
	function NetworkParticipantRegistration() {
        owner          = msg.sender; 
	    participantID  = 0;  
	  }


    function setParticipant() returns (bool success){
        Participants[msg.sender] = participantID;
        incrementParticipantID();
        return true;  
      }

    function getParticipant(address participantAddress) constant returns (uint participantID) {
        return Participants[participantAddress];
     }

	function incrementParticipantID() returns (uint _newTxId){
           participantID += 1;
           return participantID;
	  }
   

}
