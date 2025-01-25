"use client";

import React, { useRef, useState } from "react";

export default function SimpleRefExample() {
  const textRef = useRef<HTMLParagraphElement | null>(null); // Crea un ref
  const [count, setCount] = useState(0);

  function change() {
    if (count == 0) setCount(1);
    if (count == 1) setCount(0);
  }

  const handleClick = () => {
    if (textRef.current) {
      if (count == 0) {
        textRef.current.textContent = "Il testo è stato cambiato!"; // Modifica il testo
        change();
      } else {
        textRef.current.textContent = "TEsto 2!"; // Modifica il testo
        change();
      }
    }
  };

  return (
    <div>
      <p ref={textRef}>Questo è il testo originale.</p> {/* Collega il ref */}
      <button onClick={handleClick}>Cambia il testo</button>
    </div>
  );
}
