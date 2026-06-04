import { useState } from "react";

import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import MapParis from "../components/MapParis";
import KpiPanel from "../components/KpiPanel";
import ParcPanel from "../components/ParcPanel";
import Timeline from "../components/Timeline";

function Dashboard() {
  const [mode, setMode] = useState("habiter");

  const [arrondissement, setArrondissement] = useState("all");

  const [annee, setAnnee] = useState(2025);
  const [selectedArrondissement, setSelectedArrondissement] = useState(null);
  const [indicateur, setIndicateur] = useState("qualite-vie");

  return (
    <div className="dashboard">
      <Header />

      <div className="top-section">
        <Sidebar
          mode={mode}
          setMode={setMode}
          indicateur={indicateur}
          setIndicateur={setIndicateur}
          arrondissement={arrondissement}
          setArrondissement={setArrondissement}
          annee={annee}
          setAnnee={setAnnee}
        />
        <div className="map-section">
          <MapParis
            indicateur={indicateur}
            selectedArrondissement={selectedArrondissement}
            setSelectedArrondissement={setSelectedArrondissement}
          />
        </div>
        <KpiPanel selectedArrondissement={selectedArrondissement} />
      </div>

      <ParcPanel />

      <Timeline />
    </div>
  );
}

export default Dashboard;
