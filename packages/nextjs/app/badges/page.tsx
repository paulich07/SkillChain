"use client";

import React from "react";
import NFTBadge from "@/components/assets/NFTBadge";

export default function ExamplePage() {
  const imageURIs = [
    "https://red-worthy-chimpanzee-652.mypinata.cloud/ipfs/QmcnzzB37EomSPt9RvRD2eTDhj5mYwpxMaQFKaAT65ha7L",
    "https://red-worthy-chimpanzee-652.mypinata.cloud/ipfs/QmdVLT3u585o4vCSMQ4CmKEaJpRtzdqBeX6Z4PbubMF2eV",
  ];

  return (
    <>
      <div className="container">
        <h2>NFT Badges</h2>
        <p>Eventi a cui hai partecipato</p>
        <div className="grid">
          {imageURIs.map((uri, index) => (
            <NFTBadge key={index} imageURI={uri} />
          ))}
        </div>
        <h1>NFT Awards</h1>
        <p>Premi che hai vinto</p>
        <div className="grid">
          {imageURIs.map((uri, index) => (
            <NFTAward key={index} imageURI={uri} />
          ))}
        </div>
      </div>
    </>
  );
}
