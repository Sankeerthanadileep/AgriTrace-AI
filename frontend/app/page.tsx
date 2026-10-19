"use client";

import { useEffect, useState } from "react";

type ActivityHistory = {
  moving_seconds?: number;
  stationary_seconds?: number;
  feeding_seconds?: number;
  drinking_seconds?: number;
  resting_seconds?: number;
  herd_interaction_seconds?: number;
  separated_seconds?: number;
};

type Alert = {
  timestamp?: string;
  message?: string;
  status?: string;
};

type Event = {
  timestamp?: string;
  activity?: string;
  zone?: string;
};

type Animal = {
  activity_history?: ActivityHistory;
  alerts?: Alert[];
  events?: Event[];
  last_updated?: string;
};

type AnimalsResponse = {
  count: number;
  animals: Record<string, Animal>;
};

export default function Home() {
  const [animals, setAnimals] = useState<Record<string, Animal>>({});
  const [loading, setLoading] = useState(true);
  const [apiStatus, setApiStatus] = useState("Connecting...");

  useEffect(() => {
    fetchAnimals();

    const interval = setInterval(() => {
      fetchAnimals();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  async function fetchAnimals() {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/animals"
      );

      if (!response.ok) {
        throw new Error("Backend request failed");
      }

      const data: AnimalsResponse = await response.json();

      setAnimals(data.animals || {});
      setApiStatus("Connected");
      setLoading(false);
    } catch (error) {
      console.error("Backend error:", error);

      setApiStatus("Backend unavailable");
      setLoading(false);
    }
  }

  const animalEntries = Object.entries(animals);

  const feedingCount = animalEntries.filter(
    ([, animal]) =>
      (animal.activity_history?.feeding_seconds || 0) > 0
  ).length;

  const drinkingCount = animalEntries.filter(
    ([, animal]) =>
      (animal.activity_history?.drinking_seconds || 0) > 0
  ).length;

  const alerts = animalEntries.flatMap(
    ([animalId, animal]) =>
      (animal.alerts || []).map((alert) => ({
        animalId,
        ...alert,
      }))
  );

  const events = animalEntries.flatMap(
    ([animalId, animal]) =>
      (animal.events || []).map((event) => ({
        animalId,
        ...event,
      }))
  );

  return (
    <main className="min-h-screen bg-slate-950 text-white">

      {/* HEADER */}
      <header className="border-b border-slate-800 bg-slate-900">
        <div className="mx-auto max-w-7xl px-6 py-5">

          <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">

            <div>
              <h1 className="text-3xl font-bold">
                AgriTrace AI
              </h1>

              <p className="mt-1 text-sm text-slate-400">
                Intelligent Livestock Video & Digital Record System
              </p>
            </div>

            <div className="flex items-center gap-2 rounded-full border border-slate-700 bg-slate-800 px-4 py-2 text-sm">

              <span
                className={
                  "h-2.5 w-2.5 rounded-full " +
                  (
                    apiStatus === "Connected"
                      ? "bg-green-400"
                      : "bg-yellow-400"
                  )
                }
              />

              <span>
                {apiStatus}
              </span>

            </div>

          </div>

        </div>
      </header>


      {/* MAIN */}
      <div className="mx-auto max-w-7xl space-y-6 px-6 py-6">

        {/* STAT CARDS */}
        <section className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">

          <StatCard
            title="Animals Detected"
            value={animalEntries.length}
            description="Video-based animal identities"
          />

          <StatCard
            title="Feeding"
            value={feedingCount}
            description="Animals observed feeding"
          />

          <StatCard
            title="Drinking"
            value={drinkingCount}
            description="Animals observed drinking"
          />

          <StatCard
            title="Alerts"
            value={alerts.length}
            description="Behavioral observations"
          />

        </section>


        {/* MONITORING + ACTIVITIES */}
        <section className="grid grid-cols-1 gap-6 xl:grid-cols-3">

          {/* AI MONITORING */}
          <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900 xl:col-span-2">

            <div className="flex items-center justify-between border-b border-slate-800 px-5 py-4">

              <div>
                <h2 className="text-lg font-semibold">
                  Live AI Livestock Monitoring
                </h2>

                <p className="text-sm text-slate-400">
                  AI-annotated farm observation
                </p>
              </div>

              <div className="flex items-center gap-2 rounded-full bg-red-500/10 px-3 py-1.5 text-xs text-red-400">

                <span className="h-2 w-2 rounded-full bg-red-400" />

                AI MONITORING

              </div>

            </div>


            {/* WORKING IMAGE INSTEAD OF VIDEO */}
            <div className="flex aspect-video items-center justify-center bg-black">

              <img
                src="/agritrace_preview.jpg"
                alt="AgriTrace AI livestock monitoring"
                className="h-full w-full object-contain"
              />

            </div>


            {/* VIDEO INFORMATION */}
            <div className="border-t border-slate-800 px-5 py-4">

              <div className="grid grid-cols-2 gap-4 md:grid-cols-4">

                <InfoItem
                  label="Source"
                  value="Farm Video"
                />

                <InfoItem
                  label="Resolution"
                  value="1024 × 576"
                />

                <InfoItem
                  label="Frame Rate"
                  value="30 FPS"
                />

                <InfoItem
                  label="Duration"
                  value="40 seconds"
                />

              </div>

            </div>

          </div>


          {/* CURRENT ACTIVITIES */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900">

            <div className="border-b border-slate-800 px-5 py-4">

              <h2 className="text-lg font-semibold">
                Animal Activity
              </h2>

              <p className="text-sm text-slate-400">
                Current digital observations
              </p>

            </div>


            <div className="max-h-[500px] overflow-y-auto">

              {loading ? (

                <div className="p-5 text-sm text-slate-400">
                  Loading animal records...
                </div>

              ) : animalEntries.length === 0 ? (

                <div className="p-5 text-sm text-slate-400">
                  No animals detected.
                </div>

              ) : (

                animalEntries.map(
                  ([animalId, animal]) => {

                    const activity =
                      getCurrentActivity(animal);

                    return (

                      <div
                        key={animalId}
                        className="border-b border-slate-800 px-5 py-4 last:border-b-0"
                      >

                        <div className="flex items-center justify-between">

                          <span className="font-medium">
                            {animalId}
                          </span>


                          <span
                            className={
                              "rounded-full px-2.5 py-1 text-xs font-medium " +
                              activityStyle(activity)
                            }
                          >
                            {activity}
                          </span>

                        </div>


                        <div className="mt-2 text-xs text-slate-500">
                          Digital behavior record
                        </div>

                      </div>

                    );
                  }
                )

              )}

            </div>

          </div>

        </section>


        {/* ALERTS */}
        <section className="rounded-2xl border border-slate-800 bg-slate-900">

          <div className="border-b border-slate-800 px-5 py-4">

            <h2 className="text-lg font-semibold">
              Alerts & Behavioral Observations
            </h2>

            <p className="text-sm text-slate-400">
              Significant behavioral deviations identified by the prototype
            </p>

          </div>


          <div className="p-5">

            {alerts.length === 0 ? (

              <div className="rounded-xl border border-slate-800 bg-slate-950 p-5 text-sm text-slate-400">

                No behavioral deviations currently recorded.

              </div>

            ) : (

              <div className="space-y-3">

                {alerts.map((alert, index) => (

                  <div
                    key={index}
                    className="rounded-xl border border-yellow-900/50 bg-yellow-950/20 p-4"
                  >

                    <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">

                      <div>

                        <div className="font-semibold text-yellow-300">
                          {alert.animalId}
                        </div>

                        <div className="mt-1 text-sm text-slate-300">
                          {alert.message ||
                            "Behavioral deviation detected."}
                        </div>

                      </div>


                      <div className="text-xs text-yellow-400">
                        {alert.status ||
                          "Inspection recommended"}
                      </div>

                    </div>


                    {alert.timestamp && (

                      <div className="mt-2 text-xs text-slate-500">
                        {alert.timestamp}
                      </div>

                    )}

                  </div>

                ))}

              </div>

            )}

          </div>

        </section>


        {/* DIGITAL RECORDS */}
        <section className="rounded-2xl border border-slate-800 bg-slate-900">

          <div className="border-b border-slate-800 px-5 py-4">

            <h2 className="text-lg font-semibold">
              Digital Animal Records
            </h2>

            <p className="text-sm text-slate-400">
              Individual livestock behavior profiles
            </p>

          </div>


          <div className="overflow-x-auto">

            <table className="w-full text-left text-sm">

              <thead className="border-b border-slate-800 text-xs uppercase text-slate-500">

                <tr>

                  <th className="px-5 py-4">
                    Animal ID
                  </th>

                  <th className="px-5 py-4">
                    Moving
                  </th>

                  <th className="px-5 py-4">
                    Stationary
                  </th>

                  <th className="px-5 py-4">
                    Feeding
                  </th>

                  <th className="px-5 py-4">
                    Drinking
                  </th>

                  <th className="px-5 py-4">
                    Resting
                  </th>

                </tr>

              </thead>


              <tbody>

                {animalEntries.map(
                  ([animalId, animal]) => (

                    <tr
                      key={animalId}
                      className="border-b border-slate-800 last:border-b-0"
                    >

                      <td className="px-5 py-4 font-medium">
                        {animalId}
                      </td>

                      <td className="px-5 py-4 text-slate-300">
                        {formatSeconds(
                          animal.activity_history?.moving_seconds
                        )}
                      </td>

                      <td className="px-5 py-4 text-slate-300">
                        {formatSeconds(
                          animal.activity_history?.stationary_seconds
                        )}
                      </td>

                      <td className="px-5 py-4 text-slate-300">
                        {formatSeconds(
                          animal.activity_history?.feeding_seconds
                        )}
                      </td>

                      <td className="px-5 py-4 text-slate-300">
                        {formatSeconds(
                          animal.activity_history?.drinking_seconds
                        )}
                      </td>

                      <td className="px-5 py-4 text-slate-300">
                        {formatSeconds(
                          animal.activity_history?.resting_seconds
                        )}
                      </td>

                    </tr>

                  )
                )}

              </tbody>

            </table>

          </div>

        </section>


        {/* TIMESTAMPED EVENTS */}
        <section className="rounded-2xl border border-slate-800 bg-slate-900">

          <div className="border-b border-slate-800 px-5 py-4">

            <h2 className="text-lg font-semibold">
              Timestamped Events
            </h2>

            <p className="text-sm text-slate-400">
              Recorded livestock activities and observations
            </p>

          </div>


          <div className="p-5">

            {events.length === 0 ? (

              <div className="text-sm text-slate-400">
                No timestamped events available.
              </div>

            ) : (

              <div className="grid grid-cols-1 gap-3 md:grid-cols-2">

                {events.slice(0, 12).map(
                  (event, index) => (

                    <div
                      key={index}
                      className="rounded-xl border border-slate-800 bg-slate-950 p-4"
                    >

                      <div className="flex items-center justify-between">

                        <span className="font-medium">
                          {event.animalId}
                        </span>

                        <span className="text-xs text-slate-500">
                          {event.timestamp || "--"}
                        </span>

                      </div>


                      <div className="mt-2 text-sm text-slate-300">

                        Activity:{" "}

                        <span className="font-medium">
                          {event.activity || "Unknown"}
                        </span>

                      </div>


                      <div className="mt-1 text-xs text-slate-500">
                        Zone: {event.zone || "general_area"}
                      </div>

                    </div>

                  )
                )}

              </div>

            )}

          </div>

        </section>


        {/* SYSTEM INFORMATION */}
        <section className="grid grid-cols-1 gap-4 md:grid-cols-3">

          <SystemCard
            title="Animal Detection"
            value="YOLO"
            description="Computer vision detection and tracking"
          />

          <SystemCard
            title="Tracking"
            value="ByteTrack"
            description="Video-based temporary tracking IDs"
          />

          <SystemCard
            title="Behavior Analysis"
            value="AI Rules"
            description="Individual activity and deviation analysis"
          />

        </section>


        {/* FOOTER */}
        <footer className="border-t border-slate-800 py-6 text-center text-xs text-slate-500">

          AgriTrace AI • Intelligent Livestock Video & Digital Record System

          <br />

          Behavioral deviation alerts are intended for inspection support,
          not disease diagnosis.

        </footer>

      </div>

    </main>
  );
}


/* STAT CARD */

function StatCard({
  title,
  value,
  description,
}: {
  title: string;
  value: number;
  description: string;
}) {
  return (

    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

      <div className="text-sm text-slate-400">
        {title}
      </div>

      <div className="mt-2 text-3xl font-bold">
        {value}
      </div>

      <div className="mt-1 text-xs text-slate-500">
        {description}
      </div>

    </div>

  );
}


/* INFO ITEM */

function InfoItem({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (

    <div>

      <div className="text-xs uppercase tracking-wide text-slate-500">
        {label}
      </div>

      <div className="mt-1 text-sm font-medium text-slate-200">
        {value}
      </div>

    </div>

  );
}


/* SYSTEM CARD */

function SystemCard({
  title,
  value,
  description,
}: {
  title: string;
  value: string;
  description: string;
}) {
  return (

    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

      <div className="text-xs uppercase tracking-wide text-slate-500">
        {title}
      </div>

      <div className="mt-2 text-xl font-bold">
        {value}
      </div>

      <div className="mt-1 text-sm text-slate-400">
        {description}
      </div>

    </div>

  );
}


/* FORMAT SECONDS */

function formatSeconds(value?: number) {

  if (value === undefined || value === null) {
    return "0.00 s";
  }

  return value.toFixed(2) + " s";
}


/* CURRENT ACTIVITY */

function getCurrentActivity(animal: Animal) {

  const history = animal.activity_history;

  if (!history) {
    return "Unknown";
  }

  const activities = [

    {
      name: "Feeding",
      value: history.feeding_seconds || 0,
    },

    {
      name: "Drinking",
      value: history.drinking_seconds || 0,
    },

    {
      name: "Resting",
      value: history.resting_seconds || 0,
    },

    {
      name: "Moving",
      value: history.moving_seconds || 0,
    },

    {
      name: "Stationary",
      value: history.stationary_seconds || 0,
    },

  ];

  activities.sort(
    (a, b) => b.value - a.value
  );

  if (activities[0].value > 0) {
    return activities[0].name;
  }

  return "Unknown";
}


/* ACTIVITY STYLE */

function activityStyle(activity: string) {

  switch (activity) {

    case "Feeding":
      return "bg-green-500/10 text-green-400";

    case "Drinking":
      return "bg-blue-500/10 text-blue-400";

    case "Moving":
      return "bg-purple-500/10 text-purple-400";

    case "Resting":
      return "bg-orange-500/10 text-orange-400";

    case "Stationary":
      return "bg-slate-700 text-slate-300";

    default:
      return "bg-slate-800 text-slate-400";

  }

}