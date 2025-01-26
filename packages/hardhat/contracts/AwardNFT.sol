// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract AwardNFT is ERC721Enumerable, Ownable {

    constructor() ERC721("AwardNFT", "AWD") Ownable(msg.sender) {}

    struct AwardMetadata {
        string eventName;
        string name;
        address recipient;
        uint256 mintDate;
        string cid; // IPFS CID dei metadati
    }

    uint256 private _tokenIdCounter;
    mapping(uint256 => AwardMetadata) public awardMetadata;

    event AwardMinted(address indexed recipient, uint256 indexed tokenId, string eventName, string awardName);

    error TokenNotFound();
    error NoRecipient();

    /// @notice Mint un NFT e salva i metadati on-chain
    function mintAward(address recipient, string memory eventName, string memory name, string memory cid) public onlyOwner {
        if (recipient == address(0)) {
            revert NoRecipient();
        }

        uint256 tokenId = _tokenIdCounter++;

        _mint(recipient, tokenId);
        emit AwardMinted(recipient, tokenId, eventName, awardName);

        // Salva i metadati prima del minting
        awardMetadata[tokenId] = AwardMetadata({
            eventName: eventName,
            name: name,
            recipient: recipient,
            issuedDate: block.timestamp,
            cid: cid
        });

    }

    /// @notice Recupera i dati di un Award NFT
    function getAwardInfo(uint256 tokenId) public view returns (AwardMetadata memory) {
        if (tokenId >= _tokenIdCounter) {
            revert TokenNotFound();
        }
        return awardMetadata[tokenId];
    }

    /// @notice Ottiene tutti i token posseduti da un indirizzo
    function getOwnedTokens(address owner) public view returns (uint256[] memory) {
        if (owner == address(0)) {
            revert NoRecipient();
        }
        uint256 balance = balanceOf(owner);
        uint256[] memory tokens = new uint256[](balance);
        for (uint256 i = 0; i < balance; i++) {
            tokens[i] = tokenOfOwnerByIndex(owner, i);
        }
        return tokens;
    }
}