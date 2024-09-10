import { useState } from 'react';
import './App.css';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet'
import countries from './assets/countries.json'

function App() {
  const [countryCodeA, setCountryCodeA] = useState("")
  const [countryCodeB, setCountryCodeB] = useState("")
  
  return (
    <div onClick={() => {
      setCountryCodeA("")
      setCountryCodeB("")
    }}>
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
          if (!geoJsonFeature.properties) {
            throw Error("GeoJSONFeature properties are null")
          }
          let cc = geoJsonFeature.properties.ISO_A3
          return {
            fillColor: cc == countryCodeA ? "#fff" : cc == countryCodeB ? "#000" : "#2c7fb8",
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
            let cc = e.target.feature.properties.ISO_A3
            setCountryCodeA(prev => {
              if (!prev) {
                return cc;
              } else if (prev !== cc) {
                setCountryCodeB(cc); // Only set countryCodeB if countryCodeA is already set
              }
              return prev; // Keep countryCodeA the same
            });
            e.originalEvent.stopPropagation()
          })
        }}/>
      </MapContainer>
    </div>
  );
}

export default App;
