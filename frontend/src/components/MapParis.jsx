import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import { useEffect, useState } from "react";
import API from "../services/api";

function MapParis({ selectedArrondissement, setSelectedArrondissement }) {
  const [geoData, setGeoData] = useState(null);

  useEffect(() => {
    API.get("/geojson")
      .then((res) => {
        setGeoData(res.data);
      })
      .catch(console.error);
  }, []);

  const styleFeature = () => {
    return {
      fillColor: "#4f46e5",
      weight: 2,
      opacity: 1,
      color: "white",
      fillOpacity: 0.5,
    };
  };

  const onEachFeature = (feature, layer) => {
    const arrondissement = Number(feature.properties.c_ar);

    layer.bindPopup(`<h3>${arrondissement}e arrondissement</h3>`);

    layer.on("click", () => {
      setSelectedArrondissement(arrondissement);
    });
  };

  return (
    <MapContainer
      center={[48.8566, 2.3522]}
      zoom={11}
      scrollWheelZoom={true}
      style={{
        height: "600px",
        width: "100%",
      }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {geoData && (
        <GeoJSON
          data={geoData}
          style={styleFeature}
          onEachFeature={onEachFeature}
        />
      )}
    </MapContainer>
  );
}

export default MapParis;
