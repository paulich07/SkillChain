/// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract BadgeNFT is ERC1155Burnable, Ownable {

    constructor(string memory baseURI) ERC1155(baseURI) Ownable(msg.sender) {}

    uint256 public currentTokenId;    
    
    struct Badge {
        string name;
        string eventName;
        uint256 mintDate;
        string cid; // IPFS CID dei metadati
    }

    mapping(uint256 => Badge) public badgeMetadata;

    event BadgeMinted(uint256 indexed tokenId, string name, string cid, address[] recipients);

    error TokenNotFound();
    error NoRecipient();

    /// @notice Mint dello stesso NFT a più utenti
    function mintBadge(string memory name, string memory eventName, address[] memory recipients, string memory cid) public onlyOwner {
        if (recipients.length == 0) {
            revert NoRecipient();
        }

        uint256 tokenId = currentTokenId++;
        badgeMetadata[tokenId] = Badge(name, eventName, block.timestamp, cid);

        uint256[] memory ids = new uint256[](recipients.length);
        uint256[] memory amounts = new uint256[](recipients.length);

        for (uint256 i = 0; i < recipients.length; i++) {
            ids[i] = tokenId;
            amounts[i] = 1; // Ogni utente riceve 1 NFT
        }

        _mintBatch(msg.sender, ids, amounts, ""); // Minta tutti gli NFT all'admin

        for (uint256 i = 0; i < recipients.length; i++) {
            safeTransferFrom(msg.sender, recipients[i], tokenId, 1, "");
        }

        emit BadgeMinted(tokenId, name, cid, recipients);
    }

    /// @notice Recupera i metadati di un NFT
    function getBadgeInfo(uint256 tokenId) public view returns (Badge memory) {
        if (tokenId >= currentTokenId) {
            revert TokenNotFound();
        }
        return badgeMetadata[tokenId];
    }

    /// @notice Ottiene tutti i token posseduti da un utente
    function getOwnedTokens(address owner) public view returns (uint256[] memory) {
        uint256 count = 0;
        for (uint256 i = 0; i < currentTokenId; i++) {
            if (balanceOf(owner, i) > 0) {
                count++;
            }
        }

        uint256[] memory tokens = new uint256[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < currentTokenId; i++) {
            if (balanceOf(owner, i) > 0) {
                tokens[index] = i;
                index++;
            }
        }
        return tokens;
    }
}