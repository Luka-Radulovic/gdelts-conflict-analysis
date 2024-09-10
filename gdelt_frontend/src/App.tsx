import { useState } from 'react';
import './App.css';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet'
import countries from './assets/countries.json'

function App() {
  const [countryCodeA, setCountryCodeA] = useState("")
  
  return (
    <div>
      <MapContainer center={[20, 10]} zoom={2.2} id="map" maxBounds={[[-60, -180], [80, 180]]}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          maxZoom={19}
          minZoom={2}
          noWrap={true}
          />
        {/* @ts-ignore */}
        <GeoJSON data={countries as GeoJSON.FeatureCollection} style={function (geoJsonFeature: GeoJSON.Feature) {
          return {
            fillColor: geoJsonFeature.properties && geoJsonFeature.properties.ISO_A3 == countryCodeA ? "#fff" : "#2c7fb8",
            color: "#f20b0b",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.55
          }
        }}

        onEachFeature={(feature, layer) => {
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
          layer.on('click', e => {
            setCountryCodeA(e.target.feature.properties.ISO_A3)
          })
        }}/>
      </MapContainer>
    </div>
  );
}

export default App;
