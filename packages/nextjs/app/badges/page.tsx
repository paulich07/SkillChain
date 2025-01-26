"use client";

import React from "react";
import NFTBadge from "@/components/assets/NFTBadge";
import NFTAward from "@/components/assets/NFTAward";

export default function ExamplePage() {
  const imageURIs2 = [
    "https://red-worthy-chimpanzee-652.mypinata.cloud/ipfs/QmdVLT3u585o4vCSMQ4CmKEaJpRtzdqBeX6Z4PbubMF2eV",
    "https://red-worthy-chimpanzee-652.mypinata.cloud/ipfs/Qma6iGxgTC6PtAbj9jEHY5x6SRiyj2iGNr9RTWk3ixx3G3",
  ];

  return (
    <>
      <div className="container">
        <h1>NFT Badges</h1>
        <div>
          <p>Eventi a cui hai partecipato</p>
          <div className="grid">
            {imageURIs2.map((uri, index) => (
              <NFTBadge key={index} imageURI={uri} />
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
