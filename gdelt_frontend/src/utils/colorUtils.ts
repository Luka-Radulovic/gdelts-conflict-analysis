function interpolateColor(hex1: string, hex2: string, factor: number) {
    factor = Math.max(0, Math.min(1, factor));

    const hexToRgb = (hex: string) => {
        const bigint = parseInt(hex.slice(1), 16);
        return {
            r: (bigint >> 16) & 255,
            g: (bigint >> 8) & 255,
            b: bigint & 255
        };
    };

    const rgbToHex = (r: number, g: number, b: number) => {
        const componentToHex = (c: number) => c.toString(16).padStart(2, '0');
        return `#${componentToHex(r)}${componentToHex(g)}${componentToHex(b)}`;
    };

    const color1 = hexToRgb(hex1);
    const color2 = hexToRgb(hex2);

    const r = Math.round(color1.r + factor * (color2.r - color1.r));
    const g = Math.round(color1.g + factor * (color2.g - color1.g));
    const b = Math.round(color1.b + factor * (color2.b - color1.b));

    return rgbToHex(r, g, b);
}

function clampToUnitRange(value: number, a: number, b: number) {
    if (a > b) [a, b] = [b, a];
    const clampedValue = (value - a) / (b - a);
    return Math.max(0, Math.min(1, clampedValue));
}

export function relationsToColor(value: number) {
    let multiplier = clampToUnitRange(value, -100, 100)
    return interpolateColor('#ff0000','#00ff00',multiplier)
}