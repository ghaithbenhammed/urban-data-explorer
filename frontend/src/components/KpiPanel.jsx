import { useEffect, useState } from "react";
import API from "../services/api";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import ComparisonPanel from "./ComparisonPanel";
function KpiPanel({ selectedArrondissement, compareArrondissement, annee }) {
  const [prix, setPrix] = useState(null);
  const [social, setSocial] = useState(null);
  const [accessibilite, setAccessibilite] = useState(null);
  const [parc, setParc] = useState([]);

  useEffect(() => {
    if (!selectedArrondissement || selectedArrondissement === "all") {
      setPrix(null);
      setSocial(null);
      setAccessibilite(null);
      setParc([]);
      return;
    }

    Promise.all([
      API.get("/prix-median"),
      API.get("/logements-sociaux"),
      API.get("/accessibilite"),
      API.get("/repartition-parc"),
    ])
      .then(([prixRes, socialRes, accesRes, parcRes]) => {
        const arr = Number(selectedArrondissement);

        const prixData = prixRes.data.find(
          (item) => Number(item.arrondissement) === arr,
        );

        const socialData = socialRes.data.find(
          (item) => Number(item.arrondissement) === arr,
        );

        const accesData = accesRes.data.find(
          (item) => Number(item.arrondissement) === arr,
        );

        const parcData = parcRes.data.filter(
          (item) => Number(item.arrondissement) === arr,
        );

        setPrix(prixData);
        setSocial(socialData);
        setAccessibilite(accesData);
        setParc(parcData);
      })
      .catch(console.error);
  }, [selectedArrondissement]);

  const getLabel = (categorie) => {
    if (categorie === "petit") return "< 40 m²";
    if (categorie === "moyen") return "40 - 80 m²";
    if (categorie === "grand") return "> 80 m²";

    return categorie;
  };

  const getColor = (categorie) => {
    if (categorie === "grand") return "#2563eb";
    if (categorie === "moyen") return "#60a5fa";
    if (categorie === "petit") return "#93c5fd";

    return "#d1d5db";
  };
  let analyse = [];

  if (prix) {
    const prixActuel = Number(prix[String(annee)]);

    if (prixActuel > 11000) {
      analyse.push("• Prix immobiliers très élevés");
    } else if (prixActuel > 9000) {
      analyse.push("• Prix immobiliers intermédiaires");
    } else {
      analyse.push("• Prix immobiliers accessibles");
    }
  }

  if (social) {
    const taux = Number(social.taux_logement_social);

    if (taux > 25) {
      analyse.push("• Forte présence de logements sociaux");
    } else if (taux > 10) {
      analyse.push("• Mixité sociale équilibrée");
    } else {
      analyse.push("• Faible part de logements sociaux");
    }
  }

  if (accessibilite) {
    const score = Number(accessibilite.accessibilite);

    if (score > 2) {
      analyse.push("• Très bonne accessibilité");
    } else if (score > 1) {
      analyse.push("• Accessibilité correcte");
    } else {
      analyse.push("• Accessibilité limitée");
    }
  }

  let profil = "";

  if (prix && Number(prix[String(annee)]) > 11000) {
    profil = "Profil adapté à un achat patrimonial.";
  } else if (social && social.taux_logement_social > 20) {
    profil = "Profil adapté à une résidence principale.";
  } else {
    profil = "Profil équilibré pour habiter ou investir.";
  }
  return (
    <div className="kpi-panel">
      {compareArrondissement !== "all" &&
        compareArrondissement !== selectedArrondissement && (
          <ComparisonPanel
            selectedArrondissement={selectedArrondissement}
            compareArrondissement={compareArrondissement}
            annee={annee}
          />
        )}
      <div className="card">
        <h3>Typologie des logements</h3>

        {parc.length === 0 ? (
          <p>--</p>
        ) : (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: "16px",
              marginTop: "10px",
            }}
          >
            <div
              style={{
                width: "110px",
                height: "110px",
                flexShrink: 0,
              }}
            >
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={parc}
                    dataKey="pourcentage"
                    nameKey="categorie_surface"
                    innerRadius={28}
                    outerRadius={48}
                    paddingAngle={3}
                    stroke="none"
                  >
                    {parc.map((item) => (
                      <Cell
                        key={item.categorie_surface}
                        fill={getColor(item.categorie_surface)}
                      />
                    ))}
                  </Pie>

                  <Tooltip
                    formatter={(value) => `${Number(value).toFixed(1)} %`}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div style={{ flex: 1 }}>
              {parc.map((item) => (
                <div
                  key={item.categorie_surface}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: "12px",
                    fontSize: "14px",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "8px",
                    }}
                  >
                    <div
                      style={{
                        width: "10px",
                        height: "10px",
                        borderRadius: "50%",
                        backgroundColor: getColor(item.categorie_surface),
                      }}
                    />

                    <span>{getLabel(item.categorie_surface)}</span>
                  </div>

                  <strong>{item.pourcentage.toFixed(1)}%</strong>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
      <div className="card">
        <h3>Analyse rapide</h3>

        {selectedArrondissement === "all" ? (
          <p
            style={{
              fontSize: "14px",
              color: "#64748b",
            }}
          >
            Sélectionnez un arrondissement pour obtenir une analyse.
          </p>
        ) : (
          <>
            {analyse.map((item) => (
              <div
                key={item}
                style={{
                  marginBottom: "8px",
                  fontSize: "14px",
                }}
              >
                {item}
              </div>
            ))}

            <div
              style={{
                marginTop: "12px",
                padding: "10px",
                background: "#eff6ff",
                borderRadius: "8px",
                fontSize: "13px",
                color: "#1e3a8a",
                fontWeight: "600",
              }}
            >
              {profil}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default KpiPanel;
