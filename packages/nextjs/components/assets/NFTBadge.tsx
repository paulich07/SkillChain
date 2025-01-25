"use client";

import React, { useEffect, useRef } from "react";

interface ExamplePageProps {
  imageURI: string; // Accepts the dynamic URI as a prop
}

export default function ExamplePage({ imageURI }: ExamplePageProps) {
  const cardRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const $card = cardRef.current;

    if (!$card) {
      console.error("Card element not found!");
      return;
    }

    let bounds: DOMRect;

    function rotateToMouse(e: MouseEvent) {
      const mouseX = e.clientX;
      const mouseY = e.clientY;
      const leftX = mouseX - bounds.x;
      const topY = mouseY - bounds.y;
      const center = {
        x: leftX - bounds.width / 2,
        y: topY - bounds.height / 2,
      };
      const distance = Math.sqrt(center.x ** 2 + center.y ** 2);

      $card.style.transform = `
        scale3d(1.07, 1.07, 1.07)
        rotate3d(
          ${center.y / 100},
          ${-center.x / 100},
          0,
          ${Math.log(distance) * 2}deg
        )
      `;

      const glow = $card.querySelector(".glow") as HTMLDivElement | null;
      if (glow) {
        glow.style.backgroundImage = `
          radial-gradient(
            circle at
            ${center.x * 2 + bounds.width / 2}px
            ${center.y * 2 + bounds.height / 2}px,
            #ffffff55,
            #0000000f
          )
        `;
      }
    }

    function handleMouseEnter() {
      bounds = $card.getBoundingClientRect();
      document.addEventListener("mousemove", rotateToMouse);
    }

    function handleMouseLeave() {
      document.removeEventListener("mousemove", rotateToMouse);
      $card.style.transform = "";
      const glow = $card.querySelector(".glow") as HTMLDivElement | null;
      if (glow) {
        glow.style.backgroundImage = "";
      }
    }

    $card.addEventListener("mouseenter", handleMouseEnter);
    $card.addEventListener("mouseleave", handleMouseLeave);

    // Cleanup event listeners
    return () => {
      $card.removeEventListener("mouseenter", handleMouseEnter);
      $card.removeEventListener("mouseleave", handleMouseLeave);
    };
  }, []);

  return (
    <div
      className="card"
      ref={cardRef}
      style={{
        backgroundImage: `url(${imageURI})`, // Dynamically set the background image
        backgroundSize: "cover",
        backgroundPosition: "center",
        margin: "50px auto",
        padding: "20px",
        width: "300px",
        height: "300px",
        textAlign: "center",
        position: "relative",
      }}
    >
      <div
        className="glow"
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          pointerEvents: "none",
        }}
      />
    </div>
  );
}
