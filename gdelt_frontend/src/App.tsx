import { useEffect, useState } from 'react';
import './App.css';
import { MapContainer, Marker, Popup, TileLayer, GeoJSON } from 'react-leaflet'
import countries from './assets/countries.json'

function App() {
  return (
    <MapContainer center={[20, 10]} zoom={2.2} id="map" maxBounds={[[-60, -180], [80, 180]]}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        maxZoom={19}
        minZoom={2}
        noWrap={true}
      />
      <GeoJSON data={countries as GeoJSON.FeatureCollection} style={{
        fillColor: "#2c7fb8",
        color: "#f20b0b",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.55
      }}
       onEachFeature={(feature, layer) => {
        layer.bindPopup(feature.properties.ADMIN)
        layer.on('mouseover', function (e) {
          e.target.setStyle({
            fillOpacity: 0.8
          });
        });
        layer.on('mouseout', function (e) {
          e.target.setStyle({
            fillOpacity: 0.55
          });
        });
      }}/>
    </MapContainer>
  );
}

export default App;
