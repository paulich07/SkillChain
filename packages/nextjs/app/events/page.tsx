"use client";

import React, { useEffect, useState } from "react";

interface Event {
  id: number;
  title: string;
  startDate: string;
  endDate: string;
  description: string;
}

export default function EventDetailsPage() {
  const [event, setEvent] = useState<Event | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchEvent() {
      try {
        const response = await fetch("http://localhost:8000/api/events/1"); // ID = 1
        if (!response.ok) {
          throw new Error("Errore durante il recupero dell'evento");
        }
        const data: Event = await response.json();
        setEvent(data);
      } catch (err) {
        setError(err.message);
      }
    }

    fetchEvent();
  }, []);

  if (error) {
    return <div className="text-red-500">Errore: {error}</div>;
  }

  if (!event) {
    return <div>Caricamento in corso...</div>;
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Dettagli Evento</h1>
      <div className="mt-4">
        <p>
          <strong>ID:</strong> {event.id}
        </p>
        <p>
          <strong>Titolo:</strong> {event.title}
        </p>
        <p>
          <strong>Data di inizio:</strong> {event.startDate}
        </p>
        <p>
          <strong>Data di fine:</strong> {event.endDate}
        </p>
        <p>
          <strong>Descrizione:</strong> {event.description}
        </p>
      </div>
    </div>
  );
}
