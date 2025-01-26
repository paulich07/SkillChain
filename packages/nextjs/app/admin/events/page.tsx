import { Event } from "@/types/event";

export default async function EventsPage() {
  // Recupera gli eventi dall'APIs
  const response = await fetch("http://localhost:3001/api/events", {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error("Errore durante il recupero degli eventi.");
  }

  const events: Event[] = await response.json();

  // Data attuale
  const currentDate = new Date();

  // Filtra eventi programmati e terminati
  const upcomingEvents = events.filter(
    (event) => new Date(event.startDate) > currentDate
  );
  const pastEvents = events.filter(
    (event) => new Date(event.endDate) < currentDate
  );

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Gestione Eventi</h1>
        <button
          className="btn btn-primary transition-transform transform hover:-translate-x-1"
          onClick={() => {
            window.location.href = "/admin/create-events";
          }}
        >
          + Crea Evento
        </button>
      </div>

      {/* Eventi Programmati */}
      <div className="bg-base-200 p-4 rounded-lg shadow-lg mb-4">
        <h2 className="text-lg font-bold mb-2">Eventi Programmati</h2>
        <ul>
          {upcomingEvents.map((event) => (
            <li key={event.id}>
              {event.title} - {event.startDate}
            </li>
          ))}
        </ul>
      </div>

      {/* Eventi Terminati */}
      <div className="bg-base-200 p-4 rounded-lg shadow-lg">
        <h2 className="text-lg font-bold mb-2">Eventi Terminati</h2>
        <ul>
          {pastEvents.map((event) => (
            <li key={event.id}>
              {event.title} - {event.endDate}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
