"use client";

import { useState } from "react";

export default function CounterPage() {
  const [count, setCount] = useState(0);

  function increment() {
    setCount(count + 1);
  }

  return (
    <div>
      <p>Il contatore è: {count}</p>
      <button onClick={increment}>Incrementa</button>
    </div>
  );
}
