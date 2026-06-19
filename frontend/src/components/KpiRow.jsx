import { useEffect, useState } from "react";
import API from "../services/api";

function KpiRow({ selectedArrondissement, annee }) {
  const [prix, setPrix] = useState(null);
  const [social, setSocial] = useState(null);
  const [accessibilite, setAccessibilite] = useState(null);

  useEffect(() => {
    if (!selectedArrondissement || selectedArrondissement === "all") {
      return;
    }

    Promise.all([
      API.get("/prix-median"),
      API.get("/logements-sociaux"),
      API.get("/accessibilite"),
    ]).then(([prixRes, socialRes, accesRes]) => {
      const arr = Number(selectedArrondissement);

      setPrix(prixRes.data.find((x) => Number(x.arrondissement) === arr));

      setSocial(socialRes.data.find((x) => Number(x.arrondissement) === arr));

      setAccessibilite(
        accesRes.data.find((x) => Number(x.arrondissement) === arr),
      );
    });
  }, [selectedArrondissement]);

  return (
    <div className="kpi-row">
      <div className="kpi-mini">
        <span>Arrondissement</span>

        <strong>
          {selectedArrondissement === "all"
            ? "Tous"
            : `${selectedArrondissement}e`}
        </strong>
      </div>

      <div className="kpi-mini">
        <span>Prix médian</span>

        <strong>
          {prix
            ? `${Math.round(prix[String(annee)]).toLocaleString()} €`
            : "--"}
        </strong>
      </div>

      <div className="kpi-mini">
        <span>Logements sociaux</span>

        <strong>{social ? `${social.taux_logement_social}%` : "--"}</strong>
      </div>

      <div className="kpi-mini">
        <span>Accessibilité</span>

        <strong>
          {accessibilite ? accessibilite.accessibilite.toFixed(2) : "--"}
        </strong>
      </div>
    </div>
  );
}

export default KpiRow;
