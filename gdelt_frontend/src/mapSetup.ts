declare const L: typeof import('leaflet')

var map = L.map('map').setView([20, 10], 2.2);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    minZoom: 2.0,
    noWrap: true
}).addTo(map);

map.setMaxBounds([[-60,-180], [80,180]])

let geoRaw = await fetch('./assets/countries.json')
let geoJson = await geoRaw.json()


let style = {
    fillColor: "#2c7fb8",
    color: "#f20b0b",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.55
};

L.geoJson(geoJson, {
    style:style,
    onEachFeature:districtData
}).addTo(map)

function districtData(feature, layer){
    layer.bindPopup(feature.properties.ADMIN)
    layer.on('mouseover', function(e) {
        e.target.setStyle({
            fillOpacity: 0.8
        });
    });
    layer.on('mouseout', function(e) {
        e.target.setStyle({
            fillOpacity: 0.55
        });
    });
};

export {}