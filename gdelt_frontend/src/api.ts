import RelationsSchema from "./types/RelationsSchema";

const baseUrl = process.env.REACT_APP_BACKEND_BASE_URL ?? "https://gdelt-api-staging.filipovski.net/api/v1"

async function fetchFromApi(method: string, endpoint: string, params: Record<string, string>) {
    const url = new URL(`${baseUrl}/${endpoint}/`)
    Object.entries(params).forEach(([k, v]) => {
        url.searchParams.append(k, v)
    })
    const response = await fetch(url.toString(), { method: method });
    if (!response.ok)
        throw new Error(`Call to ${url.toString()} failed: ${response.status}`);
    return response.json();
}

export async function getRelationsByCountryCode(countryCode: string): Promise<RelationsSchema[]> {
    return await fetchFromApi('GET', 'relations', { country_code: countryCode });
}

export async function getRelationsByTwoCountries(countryCodeA: string, countryCodeB: string): Promise<RelationsSchema[]> {
    return await fetchFromApi('GET', 'relations', { country_code_a: countryCodeA, country_code_b: countryCodeB });
}

export async function getRelationsByCountryAndDate(countryCode: string, date: string): Promise<RelationsSchema[]> {
    return await fetchFromApi('GET', 'relations', { country_code: countryCode, date: date });
}

export async function getRelationsByDateRange(dateFrom: string, dateTo: string): Promise<RelationsSchema[]> {
    return await fetchFromApi('GET', 'relations', { date_from: dateFrom, date_to: dateTo });
}

export async function getRelationsByTwoCountriesAndDateRange(countryCodeA: string, countryCodeB: string, dateFrom: string, dateTo: string): Promise<RelationsSchema[]> {
    return await fetchFromApi('GET', 'relations', {
        country_code_a: countryCodeA,
        country_code_b: countryCodeB,
        date_from: dateFrom,
        date_to: dateTo
    });
}

export async function getRelationsByCompositeId(countryCodeA: string, countryCodeB: string, date: string): Promise<RelationsSchema> {
    return await fetchFromApi('GET', 'relations', {
        country_code_a: countryCodeA,
        country_code_b: countryCodeB,
        date: date
    });
}