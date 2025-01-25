"use client";

import NFTBadge from "@/assets/NFTBadge";

export default function ExamplePage() {
  const imageURI = "https://images.unsplash.com/photo-1557672199-6e8c8b2b8fff?ixlib=rb-1.2.1&auto=format&fit=crop&w=934&q=80";

  return (
    <>
      <h1>Badges</h1>
      <NFTBadge imageURI={imageURI} />
    </>
  );
}
