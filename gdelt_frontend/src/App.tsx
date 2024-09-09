import { useEffect, useState } from 'react';
import './App.css';
import { MapContainer, Marker, Popup, TileLayer, GeoJSON } from 'react-leaflet'

function App() {
  const [geoJSONCountries, setGeoJSONCountries] = useState({})

  useEffect(() => {
    fetch('../assets/countries.json').then(countries => countries.json().then(data => {
      ;
    }))
  })
  return (
    <MapContainer center={[51.505, -0.09]} zoom={13} scrollWheelZoom={false} id="map">
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[51.505, -0.09]}>
        <Popup>
          A pretty CSS3 popup. <br /> Easily customizable.
        </Popup>
      </Marker>
      {/* <GeoJSON data={ } /> */}
    </MapContainer>
  );
}

export default App;
