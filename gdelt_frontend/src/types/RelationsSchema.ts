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
    return 1 / (1 + Math.exp(-(z-300)));
}

export function relationsToScore(relations: RelationsSchema) {
    // return relations.relations_score * 10

    let total = relations.num_verbal_coop +
        relations.num_material_coop +
        relations.num_verbal_conf +
        relations.num_material_conf

    let MATERIAL_MULTIPLIER = 5
    return 10 * sigmoid(total) * (relations.num_verbal_coop + MATERIAL_MULTIPLIER * relations.num_material_coop
        - relations.num_verbal_conf - MATERIAL_MULTIPLIER * relations.num_material_conf) /
        (relations.num_verbal_coop + MATERIAL_MULTIPLIER * relations.num_material_coop
            + relations.num_verbal_conf + MATERIAL_MULTIPLIER * relations.num_material_conf)
}