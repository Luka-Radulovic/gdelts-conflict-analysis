export default interface RelationsSchema {
    relations_score: number;
    country_code_a: string;
    country_code_b: string;
    date: Date;
    num_verbal_coop: number;
    num_material_coop: number;
    num_verbal_conf: number;
    num_material_conf: number;
}

function sigmoid(z: number) {
    return 1 / (1 + Math.exp(-0.05 * (z - 300)));
}

export function relationsToScore(relations: RelationsSchema) {
    // return relations.relations_score

    let total = relations.num_verbal_coop +
        relations.num_material_coop +
        relations.num_verbal_conf +
        relations.num_material_conf

    const MATERIAL_MULTIPLIER = 5

    let tone = (relations.relations_score + 10) / 20
    let significance = sigmoid(total)
    let eventScore = ((relations.num_verbal_coop + MATERIAL_MULTIPLIER * relations.num_material_coop
        - relations.num_verbal_conf - MATERIAL_MULTIPLIER * relations.num_material_conf) /
        (relations.num_verbal_coop + MATERIAL_MULTIPLIER * relations.num_material_coop
            + relations.num_verbal_conf + MATERIAL_MULTIPLIER * relations.num_material_conf) + 1) / 2

    const toneMultiplier = 2
    const significanceMultiplier = -1
    const eventScoreMultiplier = 10

    // return tone + significance + eventScore
    // return significance
    let baseRelations = 20 * (toneMultiplier * tone + 
        significanceMultiplier * significance + 
        eventScoreMultiplier * eventScore) / (toneMultiplier+significanceMultiplier+eventScoreMultiplier) - 10
    
    return baseRelations * Math.pow(significance, -significanceMultiplier)
}