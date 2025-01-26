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
      ref={cardRef}
      style={{
        fontWeight: "bold",
        padding: "1em",
        textAlign: "right",
        color: "#181a1a",
        width: "200px",
        height: "100px",
        boxShadow: "0 1px 5px #00000099",
        borderRadius: "10px",
        backgroundImage: `url(${imageURI})`,
        backgroundSize: "cover",
        position: "relative",
        transitionDuration: "300ms",
        transitionProperty: "transform, box-shadow",
        transitionTimingFunction: "ease-out",
        transform: "rotate3d(0)",
      }}
      onMouseEnter={() => {
        if (cardRef.current) {
          cardRef.current.style.boxShadow = "0 5px 20px 5px #00000044";
          cardRef.current.style.transitionDuration = "150ms";
        }
      }}
      onMouseLeave={() => {
        if (cardRef.current) {
          cardRef.current.style.boxShadow = "0 1px 5px #00000099";
          cardRef.current.style.transitionDuration = "300ms";
        }
      }}
    >
      <div
        className="glow"
        style={{
          position: "absolute",
          width: "100%",
          height: "100%",
          left: "0",
          top: "0",
          backgroundImage: "radial-gradient(circle at 50% -20%, #ffffff22, #0000000f)",
        }}
      />
    </div>
  );
}
