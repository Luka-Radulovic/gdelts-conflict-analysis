const baseUrl = "http://localhost:8000"

async function getRelationsByCountryCode(countryCode: string): Promise<RelationsSchema[]> {
    const url = new URL(`${baseUrl}/`);
    url.searchParams.append('country_code', countryCode);
  
    const response = await fetch(url.toString(), { method: 'GET' });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
}
  
async function getRelationsByTwoCountries(countryCodeA: string, countryCodeB: string): Promise<RelationsSchema[]> {
    const url = new URL(`${baseUrl}/`);
    url.searchParams.append('country_code_a', countryCodeA);
    url.searchParams.append('country_code_b', countryCodeB);
  
    const response = await fetch(url.toString(), { method: 'GET' });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
}
  
async function getRelationsByCountryAndDate(countryCode: string, date: string): Promise<RelationsSchema[]> {
    const url = new URL(`${baseUrl}/`);
    url.searchParams.append('country_code', countryCode);
    url.searchParams.append('date', date);
  
    const response = await fetch(url.toString(), { method: 'GET' });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
}
  
async function getRelationsByDateRange(dateFrom: string, dateTo: string): Promise<RelationsSchema[]> {
    const url = new URL(`${baseUrl}/`);
    url.searchParams.append('date_from', dateFrom);
    url.searchParams.append('date_to', dateTo);
  
    const response = await fetch(url.toString(), { method: 'GET' });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
}
  
async function getRelationsByTwoCountriesAndDateRange(countryCodeA: string, countryCodeB: string, dateFrom: string, dateTo: string): Promise<RelationsSchema[]> {
    const url = new URL(`${baseUrl}/`);
    url.searchParams.append('country_code_a', countryCodeA);
    url.searchParams.append('country_code_b', countryCodeB);
    url.searchParams.append('date_from', dateFrom);
    url.searchParams.append('date_to', dateTo);
  
    const response = await fetch(url.toString(), { method: 'GET' });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
}
  
async function getRelationsByCompositeId(countryCodeA: string, countryCodeB: string, date: string): Promise<RelationsSchema> {
    const url = new URL(`${baseUrl}/`);
    url.searchParams.append('country_code_a', countryCodeA);
    url.searchParams.append('country_code_b', countryCodeB);
    url.searchParams.append('date', date);
  
    const response = await fetch(url.toString(), { method: 'GET' });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
}