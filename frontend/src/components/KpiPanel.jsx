import { useEffect, useState } from "react";
import API from "../services/api";

function KpiPanel({ selectedArrondissement }) {
  const [prix, setPrix] = useState(null);
  const [social, setSocial] = useState(null);
  const [accessibilite, setAccessibilite] = useState(null);
  const [parc, setParc] = useState([]);

  useEffect(() => {
    if (!selectedArrondissement) return;

    Promise.all([
      API.get("/prix-median"),
      API.get("/logements-sociaux"),
      API.get("/accessibilite"),
      API.get("/repartition-parc"),
    ])
      .then(([prixRes, socialRes, accesRes, parcRes]) => {
        const prixData = prixRes.data.find(
          (item) => item.arrondissement === selectedArrondissement,
        );

        const socialData = socialRes.data.find(
          (item) => item.arrondissement === selectedArrondissement,
        );

        const accesData = accesRes.data.find(
          (item) => item.arrondissement === selectedArrondissement,
        );

        const parcData = parcRes.data.filter(
          (item) => item.arrondissement === selectedArrondissement,
        );

        setPrix(prixData);
        setSocial(socialData);
        setAccessibilite(accesData);
        setParc(parcData);
      })
      .catch(console.error);
  }, [selectedArrondissement]);

  return (
    <div className="kpi-panel">
      <div className="card">
        <h3>Arrondissement</h3>

        <p>{selectedArrondissement ? `${selectedArrondissement}e` : "--"}</p>
      </div>

      <div className="card">
        <h3>Prix médian</h3>

        <p>
          {prix ? `${Math.round(prix["2025"]).toLocaleString()} €` : "-- €"}
        </p>
      </div>

      <div className="card">
        <h3>Logements sociaux</h3>

        <p>{social ? `${social.taux_logement_social}%` : "-- %"}</p>
      </div>

      <div className="card">
        <h3>Accessibilité</h3>

        <p>{accessibilite ? accessibilite.accessibilite.toFixed(2) : "--"}</p>
      </div>

      <div className="card">
        <h3>Répartition du parc</h3>

        {parc.length === 0 ? (
          <p>--</p>
        ) : (
          parc.map((item) => (
            <div
              key={item.categorie_surface}
              style={{
                display: "flex",
                justifyContent: "space-between",
                marginBottom: "6px",
              }}
            >
              <span>{item.categorie_surface}</span>

              <strong>{item.pourcentage.toFixed(1)}%</strong>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default KpiPanel;
