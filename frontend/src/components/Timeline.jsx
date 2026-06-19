import { useEffect, useState } from "react";
import API from "../services/api";

import { LineChart, Line, ResponsiveContainer, Tooltip } from "recharts";

function Timeline({ selectedArrondissement, annee, setAnnee }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    if (!selectedArrondissement || selectedArrondissement === "all") {
      setData([]);
      return;
    }

    API.get("/prix-median")
      .then((res) => {
        const row = res.data.find(
          (item) =>
            Number(item.arrondissement) === Number(selectedArrondissement),
        );

        if (!row) {
          setData([]);
          return;
        }

        setData([
          {
            year: 2021,
            value: Number(row["2021"]),
          },
          {
            year: 2022,
            value: Number(row["2022"]),
          },
          {
            year: 2023,
            value: Number(row["2023"]),
          },
          {
            year: 2024,
            value: Number(row["2024"]),
          },
          {
            year: 2025,
            value: Number(row["2025"]),
          },
        ]);
      })
      .catch(console.error);
  }, [selectedArrondissement]);

  if (!selectedArrondissement || selectedArrondissement === "all") {
    return (
      <div className="timeline-mini">
        <h3>Évolution des prix</h3>

        <p
          style={{
            textAlign: "center",
            color: "#666",
          }}
        >
          Sélectionnez un arrondissement
        </p>
      </div>
    );
  }

  const firstPrice = data[0]?.value || 0;
  const lastPrice = data[data.length - 1]?.value || 0;

  const evolution =
    firstPrice > 0 ? ((lastPrice - firstPrice) / firstPrice) * 100 : 0;

  const selectedPrice = data.find((item) => item.year === annee)?.value || 0;

  return (
    <div className="timeline-mini">
      <h3>Évolution des prix</h3>

      <div className="timeline-summary">
        <div className={evolution >= 0 ? "timeline-up" : "timeline-down"}>
          {evolution >= 0 ? "↗" : "↘"} {Math.abs(evolution).toFixed(1)}% depuis
          2021
        </div>
      </div>

      <ResponsiveContainer width="100%" height={100}>
        <LineChart data={data}>
          <Tooltip
            content={({ active, payload }) => {
              if (!active || !payload?.length) return null;

              const point = payload[0].payload;

              return (
                <div
                  style={{
                    background: "white",
                    border: "1px solid #ddd",
                    padding: "10px",
                    borderRadius: "8px",
                  }}
                >
                  <div style={{ fontWeight: 600 }}>Année {point.year}</div>

                  <div style={{ color: "#2563eb" }}>
                    Prix : {point.value.toLocaleString()} €/m²
                  </div>
                </div>
              );
            }}
          />

          <Line
            type="monotone"
            dataKey="value"
            stroke="#2563eb"
            strokeWidth={3}
            dot={{
              r: 4,
            }}
            activeDot={{
              r: 6,
            }}
          />
        </LineChart>
      </ResponsiveContainer>

      <div className="year-selector">
        <span>2021</span>

        <input
          type="range"
          min="2021"
          max="2025"
          step="1"
          value={annee}
          onChange={(e) => setAnnee(Number(e.target.value))}
        />

        <span>2025</span>
      </div>

      <div className="selected-year-card">
        <div className="selected-year-label">Prix en {annee}</div>

        <div className="selected-year-price">
          {selectedPrice.toLocaleString()} €/m²
        </div>
      </div>
    </div>
  );
}

export default Timeline;
