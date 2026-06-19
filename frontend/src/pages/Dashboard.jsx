import { useState } from "react";

import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import MapParis from "../components/MapParis";
import KpiPanel from "../components/KpiPanel";
import Timeline from "../components/Timeline";
import Legend from "../components/Legend";
import ComparisonPanel from "../components/ComparisonPanel";
import KpiRow from "../components/KpiRow";

function Dashboard() {
  const [mode, setMode] = useState("habiter");

  const [selectedArrondissement, setSelectedArrondissement] = useState("all");
  const [compareArrondissement, setCompareArrondissement] = useState("all");

  const [annee, setAnnee] = useState(2025);

  const [indicateur, setIndicateur] = useState("qualite-vie");

  return (
    <div className="dashboard">
      <Header />
      <div className="top-section">
        <div className="left-column">
          <Sidebar
            mode={mode}
            setMode={setMode}
            indicateur={indicateur}
            setIndicateur={setIndicateur}
            arrondissement={selectedArrondissement}
            setArrondissement={setSelectedArrondissement}
            compareArrondissement={compareArrondissement}
            setCompareArrondissement={setCompareArrondissement}
            annee={annee}
            setAnnee={setAnnee}
          />

          {indicateur === "prix-median" && (
            <Timeline
              selectedArrondissement={selectedArrondissement}
              annee={annee}
              setAnnee={setAnnee}
            />
          )}
        </div>

        {/* CENTRE */}

        <div className="center-panel">
          <KpiRow
            selectedArrondissement={selectedArrondissement}
            annee={annee}
          />

          <div className="map-section">
            <MapParis
              indicateur={indicateur}
              annee={annee}
              selectedArrondissement={selectedArrondissement}
              setSelectedArrondissement={setSelectedArrondissement}
            />

            <Legend indicateur={indicateur} />
          </div>
        </div>

        {/* DROITE */}

        <KpiPanel
          selectedArrondissement={selectedArrondissement}
          compareArrondissement={compareArrondissement}
          annee={annee}
        />
      </div>
    </div>
  );
}

export default Dashboard;
