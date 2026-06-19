import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import { useEffect, useState, useMemo } from "react";
import API from "../services/api";
import { INDICATEURS } from "../config/indicateurs";

function MapParis({
  indicateur,
  annee,
  selectedArrondissement,
  setSelectedArrondissement,
}) {
  const [geoData, setGeoData] = useState(null);
  const [dataMap, setDataMap] = useState([]);

  const config = useMemo(() => {
    return INDICATEURS[indicateur];
  }, [indicateur]);
  const activeField =
    indicateur === "prix-median" ? String(annee) : config.field;
  // =========================
  // GEOJSON
  // =========================

  useEffect(() => {
    API.get("/geojson")
      .then((res) => {
        setGeoData(res.data);
      })
      .catch(console.error);
  }, []);

  // =========================
  // DONNÉES INDICATEUR
  // =========================

  useEffect(() => {
    if (!config) return;

    setDataMap([]);

    API.get(`/${config.api}`)
      .then((res) => {
        setDataMap(Array.isArray(res.data) ? res.data : []);
      })
      .catch((err) => {
        console.error(err);
        setDataMap([]);
      });
  }, [config]);

  // =========================
  // MIN / MAX
  // =========================

  const { min, max } = useMemo(() => {
    const values = dataMap
      .map((item) => Number(item?.[activeField]))
      .filter((v) => !isNaN(v));

    if (values.length === 0) {
      return {
        min: 0,
        max: 1,
      };
    }

    return {
      min: Math.min(...values),
      max: Math.max(...values),
    };
  }, [dataMap, config]);

  // =========================
  // COULEURS
  // =========================

  const getColor = (value) => {
    if (value === null || value === undefined || isNaN(value)) {
      return "#cccccc";
    }

    if (max === min) {
      return "#4f46e5";
    }

    const ratio = (value - min) / (max - min);

    // =========================
    // QUALITÉ / SÉCURITÉ / AIR
    // =========================

    if (config.palette === "goodbad") {
      if (ratio < 0.2) return "#d73027";
      if (ratio < 0.4) return "#fc8d59";
      if (ratio < 0.6) return "#fee08b";
      if (ratio < 0.8) return "#91cf60";

      return "#1a9850";
    }

    // =========================
    // RISQUE VIEILLISSEMENT
    // =========================

    if (config.palette === "risk") {
      if (ratio < 0.2) return "#1a9850";
      if (ratio < 0.4) return "#91cf60";
      if (ratio < 0.6) return "#fee08b";
      if (ratio < 0.8) return "#fc8d59";

      return "#d73027";
    }

    // =========================
    // BLEU
    // =========================

    if (config.palette === "blue") {
      if (ratio < 0.2) return "#dbeafe";
      if (ratio < 0.4) return "#93c5fd";
      if (ratio < 0.6) return "#60a5fa";
      if (ratio < 0.8) return "#2563eb";

      return "#1e3a8a";
    }

    // =========================
    // VIOLET
    // =========================

    if (config.palette === "purple") {
      if (ratio < 0.2) return "#ede9fe";
      if (ratio < 0.4) return "#c4b5fd";
      if (ratio < 0.6) return "#a78bfa";
      if (ratio < 0.8) return "#7c3aed";

      return "#4c1d95";
    }

    // =========================
    // ORANGE
    // =========================

    if (config.palette === "orange") {
      if (ratio < 0.2) return "#ffedd5";
      if (ratio < 0.4) return "#fdba74";
      if (ratio < 0.6) return "#fb923c";
      if (ratio < 0.8) return "#ea580c";

      return "#9a3412";
    }

    return "#6366f1";
  };

  // =========================
  // STYLE ARRONDISSEMENT
  // =========================

  const styleFeature = (feature) => {
    const arrondissement = Number(feature.properties.c_ar);

    const row = dataMap.find(
      (item) => Number(item.arrondissement) === arrondissement,
    );

    const value = row?.[activeField];

    return {
      fillColor: getColor(Number(value)),

      weight: String(arrondissement) === String(selectedArrondissement) ? 3 : 2,

      color:
        String(arrondissement) === String(selectedArrondissement)
          ? "#111827"
          : "#ffffff",
      opacity: 1,

      fillOpacity: 0.75,
    };
  };

  // =========================
  // POPUP
  // =========================

  const onEachFeature = (feature, layer) => {
    const arrondissement = Number(feature.properties.c_ar);

    const row = dataMap.find(
      (item) => Number(item.arrondissement) === arrondissement,
    );

    let value = "N/A";

    if (row && row[activeField] !== undefined && row[activeField] !== null) {
      value = row[activeField];
    }

    layer.bindPopup(`
      <div>
        <h3>${arrondissement}e arrondissement</h3>
        <strong>${config.label}</strong>
        <br/>
        ${value} ${config.unite}
      </div>
    `);

    layer.on({
      mouseover: (e) => {
        e.target.setStyle({
          weight: 2.5,
          color: "#ffffff",
          fillOpacity: 1,
        });

        e.target.openPopup();
      },

      mouseout: (e) => {
        e.target.closePopup();

        if (String(arrondissement) !== String(selectedArrondissement)) {
          e.target.setStyle({
            weight: 2,
            color: "#ffffff",
            fillOpacity: 0.75,
          });
        }
      },

      click: () => {
        setSelectedArrondissement(String(arrondissement));
      },
    });
  };

  // =========================
  // RENDER
  // =========================

  return (
    <MapContainer
      center={[48.8566, 2.3522]}
      zoom={11}
      scrollWheelZoom={true}
      style={{
        height: "480px",
        width: "100%",
      }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {geoData && config && dataMap.length > 0 && (
        <GeoJSON
          key={`${indicateur}-${dataMap.length}`}
          data={geoData}
          style={styleFeature}
          onEachFeature={onEachFeature}
        />
      )}
    </MapContainer>
  );
}

export default MapParis;
