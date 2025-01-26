"use client";

import NFTAward from "@/components/assets/NFTAward";

export default function ExamplePageWithWrapper() {
  const nftBadges = [
    "QmTzQ1X1zWKL9K3tQF1PqT3X9BgK9kEZh1r8VcNm1KM2QL", // Badge 1
    "QmbZwZ8xUYN2m1m1NVaY9KGsNmzm5XkGfQ7WXH2A8bZYD4", // Badge 2
    "QmW2T9vJ5KgM5N1JrQYn9YZ6KzF6M1Y8XbVpK7gF8H8D7Z", // Badge 3
  ];

  function generateBadgeURL(cid: string): string {
    return `https://red-worthy-chimpanzee-652.mypinata.cloud/ipfs/${cid}`;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-6">
      {nftBadges.map((cid, index) => (
        <NFTAward key={index} imageURI={generateBadgeURL(cid)} />
      ))}
    </div>
  );
}
