// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CryptoBetting {
    address public owner;
    address public houseWallet;
    uint256 public houseCut = 5; // 5% house cut
    
    struct Player {
        address payable wallet;
        uint256 bet;
        string guess; // "up" or "down"
    }

    Player[] public players;

    constructor(address _houseWallet) {
        owner = msg.sender;
        houseWallet = _houseWallet;
    }

    function placeBet(string memory guess) external payable {
        require(msg.value > 0, "Bet must be greater than 0");
        require(
            keccak256(abi.encodePacked(guess)) == keccak256("up") ||
            keccak256(abi.encodePacked(guess)) == keccak256("down"),
            "Invalid guess"
        );
        players.push(Player(payable(msg.sender), msg.value, guess));
    }

    function distributeWinnings(uint256 oldPrice, uint256 newPrice) external {
        require(msg.sender == owner, "Only owner can distribute winnings");
        require(players.length > 0, "No players have placed bets");
        
        address[] memory winners;
        address[] memory losers;
        uint256 totalPool;
        uint256 winningPool;
        
        for (uint256 i = 0; i < players.length; i++) {
            totalPool += players[i].bet;
        }
        
        if (newPrice > oldPrice) {
            for (uint256 i = 0; i < players.length; i++) {
                if (keccak256(abi.encodePacked(players[i].guess)) == keccak256("up")) {
                    winners.push(players[i].wallet);
                    winningPool += players[i].bet;
                } else {
                    losers.push(players[i].wallet);
                }
            }
        } else if (newPrice < oldPrice) {
            for (uint256 i = 0; i < players.length; i++) {
                if (keccak256(abi.encodePacked(players[i].guess)) == keccak256("down")) {
                    winners.push(players[i].wallet);
                    winningPool += players[i].bet;
                } else {
                    losers.push(players[i].wallet);
                }
            }
        }
        
        uint256 houseEarnings = (totalPool * houseCut) / 100;
        uint256 remainingPool = totalPool - houseEarnings;
        
        payable(houseWallet).transfer(houseEarnings);
        
        for (uint256 i = 0; i < winners.length; i++) {
            uint256 playerShare = (players[i].bet * remainingPool) / winningPool;
            payable(players[i].wallet).transfer(playerShare);
        }
        
        delete players;
    }
}
