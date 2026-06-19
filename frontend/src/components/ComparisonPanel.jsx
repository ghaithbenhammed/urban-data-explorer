import { useEffect, useState } from "react";
import API from "../services/api";

function ComparisonPanel({
  selectedArrondissement,
  compareArrondissement,
  annee,
}) {
  const [result, setResult] = useState(null);
  const [details, setDetails] = useState(null);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    if (
      selectedArrondissement === "all" ||
      compareArrondissement === "all" ||
      selectedArrondissement === compareArrondissement
    ) {
      setResult(null);
      setDetails(null);
      return;
    }

    Promise.all([
      API.get("/prix-median"),
      API.get("/rentabilite"),
      API.get("/tension"),
      API.get("/qualite-vie"),
      API.get("/securite"),
      API.get("/air"),
      API.get("/transport"),
      API.get("/vieillissement"),
    ])
      .then(
        ([
          prixRes,
          rentRes,
          tensionRes,
          qualiteRes,
          securiteRes,
          airRes,
          transportRes,
          vieillissementRes,
        ]) => {
          const getRow = (data, arr) =>
            data.find((item) => Number(item.arrondissement) === Number(arr));

          const a = {
            prix: getRow(prixRes.data, selectedArrondissement),
            rent: getRow(rentRes.data, selectedArrondissement),
            tension: getRow(tensionRes.data, selectedArrondissement),
            qualite: getRow(qualiteRes.data, selectedArrondissement),
            securite: getRow(securiteRes.data, selectedArrondissement),
            air: getRow(airRes.data, selectedArrondissement),
            transport: getRow(transportRes.data, selectedArrondissement),
            vieillissement: getRow(
              vieillissementRes.data,
              selectedArrondissement,
            ),
          };

          const b = {
            prix: getRow(prixRes.data, compareArrondissement),
            rent: getRow(rentRes.data, compareArrondissement),
            tension: getRow(tensionRes.data, compareArrondissement),
            qualite: getRow(qualiteRes.data, compareArrondissement),
            securite: getRow(securiteRes.data, compareArrondissement),
            air: getRow(airRes.data, compareArrondissement),
            transport: getRow(transportRes.data, compareArrondissement),
            vieillissement: getRow(
              vieillissementRes.data,
              compareArrondissement,
            ),
          };

          const acheter =
            Number(a.prix?.[String(annee)]) < Number(b.prix?.[String(annee)])
              ? selectedArrondissement
              : compareArrondissement;

          const scoreInvestA =
            Number(a.rent?.rentabilite || 0) + Number(a.tension?.tension || 0);

          const scoreInvestB =
            Number(b.rent?.rentabilite || 0) + Number(b.tension?.tension || 0);

          const investir =
            scoreInvestA > scoreInvestB
              ? selectedArrondissement
              : compareArrondissement;

          const scoreHabiterA =
            Number(a.qualite?.score_qualite_vie || 0) +
            Number(a.securite?.score_securite || 0) +
            Number(a.air?.score_air || 0) +
            Number(a.transport?.nb_arrets || 0);

          const scoreHabiterB =
            Number(b.qualite?.score_qualite_vie || 0) +
            Number(b.securite?.score_securite || 0) +
            Number(b.air?.score_air || 0) +
            Number(b.transport?.nb_arrets || 0);

          const habiter =
            scoreHabiterA > scoreHabiterB
              ? selectedArrondissement
              : compareArrondissement;

          const vieillir =
            Number(a.vieillissement?.score_inadaptation || 0) <
            Number(b.vieillissement?.score_inadaptation || 0)
              ? selectedArrondissement
              : compareArrondissement;

          setResult({
            acheter,
            investir,
            habiter,
            vieillir,
          });

          setDetails({ a, b });
        },
      )
      .catch(console.error);
  }, [selectedArrondissement, compareArrondissement, annee]);

  if (
    compareArrondissement === "all" ||
    selectedArrondissement === "all" ||
    selectedArrondissement === compareArrondissement
  ) {
    return null;
  }

  const ComparisonBar = ({
    label,
    valueA,
    valueB,
    suffix = "",
    reverse = false,
  }) => {
    const max = Math.max(valueA || 0, valueB || 0);

    const winner = reverse
      ? valueA < valueB
        ? selectedArrondissement
        : compareArrondissement
      : valueA > valueB
        ? selectedArrondissement
        : compareArrondissement;

    return (
      <div
        style={{
          marginTop: "14px",
          paddingTop: "12px",
          borderTop: "1px solid #e5e7eb",
        }}
      >
        <div
          style={{
            fontWeight: "600",
            marginBottom: "8px",
          }}
        >
          {label}
        </div>

        <div style={{ marginBottom: "8px" }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              fontSize: "12px",
            }}
          >
            <span>{selectedArrondissement}e</span>
            <span>
              {Number(valueA || 0).toFixed(1)}
              {suffix}
            </span>
          </div>

          <div
            style={{
              height: "6px",
              background: "#e5e7eb",
              borderRadius: "999px",
            }}
          >
            <div
              style={{
                width: `${(valueA / max) * 100}%`,
                height: "100%",
                background: "#2563eb",
                borderRadius: "999px",
              }}
            />
          </div>
        </div>

        <div>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              fontSize: "12px",
            }}
          >
            <span>{compareArrondissement}e</span>
            <span>
              {Number(valueB || 0).toFixed(1)}
              {suffix}
            </span>
          </div>

          <div
            style={{
              height: "6px",
              background: "#e5e7eb",
              borderRadius: "999px",
            }}
          >
            <div
              style={{
                width: `${(valueB / max) * 100}%`,
                height: "100%",
                background: "#93c5fd",
                borderRadius: "999px",
              }}
            />
          </div>
        </div>

        <div
          style={{
            marginTop: "6px",
            fontSize: "12px",
            color: "#16a34a",
            fontWeight: "600",
          }}
        >
          Avantage {winner}e
        </div>
      </div>
    );
  };

  return (
    <div className="card">
      <h3>Comparaison</h3>

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "14px",
        }}
      >
        <strong>{selectedArrondissement}e</strong>
        <strong>{compareArrondissement}e</strong>
      </div>

      {result && (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "8px",
          }}
        >
          <div className="winner-card">
            <span>Acheter</span>
            <strong>{result.acheter}e</strong>
          </div>

          <div className="winner-card">
            <span>Investir</span>
            <strong>{result.investir}e</strong>
          </div>

          <div className="winner-card">
            <span>Habiter</span>
            <strong>{result.habiter}e</strong>
          </div>

          <div className="winner-card">
            <span>Vieillir</span>
            <strong>{result.vieillir}e</strong>
          </div>
        </div>
      )}

      <button
        onClick={() => setShowDetails(!showDetails)}
        style={{
          width: "100%",
          marginTop: "14px",
          padding: "10px",
          border: "none",
          borderRadius: "10px",
          background: "#eff6ff",
          color: "#2563eb",
          fontWeight: "600",
          cursor: "pointer",
        }}
      >
        {showDetails
          ? "▲ Masquer les détails"
          : "▼ Voir la comparaison détaillée"}
      </button>

      {details && showDetails && (
        <>
          <ComparisonBar
            label="Prix médian"
            valueA={details.a.prix?.[String(annee)]}
            valueB={details.b.prix?.[String(annee)]}
            suffix=" €"
            reverse
          />

          <ComparisonBar
            label="Rentabilité"
            valueA={details.a.rent?.rentabilite}
            valueB={details.b.rent?.rentabilite}
            suffix="%"
          />

          <ComparisonBar
            label="Qualité de vie"
            valueA={details.a.qualite?.score_qualite_vie}
            valueB={details.b.qualite?.score_qualite_vie}
          />

          <ComparisonBar
            label="Sécurité"
            valueA={details.a.securite?.score_securite}
            valueB={details.b.securite?.score_securite}
          />

          <ComparisonBar
            label="Qualité de l'air"
            valueA={details.a.air?.score_air}
            valueB={details.b.air?.score_air}
          />

          <ComparisonBar
            label="Transport"
            valueA={details.a.transport?.nb_arrets}
            valueB={details.b.transport?.nb_arrets}
          />

          <ComparisonBar
            label="Inadaptation au vieillissement"
            valueA={details.a.vieillissement?.score_inadaptation}
            valueB={details.b.vieillissement?.score_inadaptation}
            reverse
          />
        </>
      )}
    </div>
  );
}

export default ComparisonPanel;
