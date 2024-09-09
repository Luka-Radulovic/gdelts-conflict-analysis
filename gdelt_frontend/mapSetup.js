var map = L.map('map').setView([20, 10], 2.2);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    minZoom: 2.0,
    noWrap: true
}).addTo(map);

map.setMaxBounds([[-60,-180], [80,180]])

let geoRaw = await fetch('./assets/countries.geo.json')
let geoJson = await geoRaw.json()

L.geoJson(geoJson).addTo(map)