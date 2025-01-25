"use client";

import React from "react";
import NFTBadge from "@/assets/NFTBadge";

export default function ExamplePage() {
  const imageURIs = [
    "https://images.unsplash.com/photo-1557672199-6e8c8b2b8fff?ixlib=rb-1.2.1&auto=format&fit=crop&w=934&q=80",
    "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-1.2.1&auto=format&fit=crop&w=934&q=80",
    "https://images.unsplash.com/photo-1557672199-6e8c8b2b8fff?ixlib=rb-1.2.1&auto=format&fit=crop&w=934&q=80",
    "https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?ixlib=rb-1.2.1&auto=format&fit=crop&w=934&q=80",
  ];

  return (
    <>
      <div className="container">
        <h1>NFT Badges</h1>
        <p>Here is a collection of NFT Badges. Hover over a badge to explore more!</p>
        <div className="grid">
          {imageURIs.map((uri, index) => (
            <NFTBadge key={index} imageURI={uri} />
          ))}
        </div>
      </div>
    </>
  );
}
