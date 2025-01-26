"use client";

import React from "react";
import NFTAward from "@/components/assets/NFTAward";

export default function ExamplePage() {
  const imageURIs = [
    "https://red-worthy-chimpanzee-652.mypinata.cloud/ipfs/QmfK5voxj52UsQe4kbkHRhvV1Weu9ZLXrqngKMiznAtzsR",
    "https://red-worthy-chimpanzee-652.mypinata.cloud/ipfs/QmcnzzB37EomSPt9RvRD2eTDhj5mYwpxMaQFKaAT65ha7L",
  ];

  return (
    <>
      <div className="container">
        <h1>NFT Awards</h1>
        <div>
          <p>Premi che hai vinto</p>
          <div className="grid">
            {imageURIs.map((uri, index) => (
              <NFTAward key={index} imageURI={uri} />
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
