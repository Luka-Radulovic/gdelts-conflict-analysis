import countries from './assets/countries.json'

export function getCountriesByIso3Code() {
    let c = countries
    let map: Map<string, typeof c.features[0]> = new Map()
    c.features.forEach((feature) => {
        map.set(feature.properties.ISO_A3, feature)
    })
    return map
}