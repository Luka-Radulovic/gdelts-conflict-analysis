export function dateToIso(date: Date) {
    return date.toISOString().slice(0,10)
}

export function dateFromIso(iso: string) {
    return new Date(iso)
}