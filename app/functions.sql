CREATE OR REPLACE FUNCTION function_zxy_query_app_mill_by_planted(
    z integer, x integer, y integer,
    query_params json)
RETURNS bytea
AS $$
DECLARE
    mvt bytea;
BEGIN
    SELECT INTO mvt ST_AsMVT(tile, 'function_zxy_query_app_mill_by_planted', 4096, 'geom') FROM (
        SELECT
            ST_AsMVTGeom(ST_Transform(ST_CurveToLine(geom), 3857), ST_TileEnvelope(z, x, y), 4096, 64, true) AS geom ,id,
            mill_eq_id, mill_name, mill_uml_id , mill_company_name ,mill_company_group_id, mill_company_group ,mill_country, mill_province , mill_district ,mill_address ,mill_type ,mill_lat , mill_long , 
            mill_rspo , mill_mspo , mill_capacity , mill_methane_capture ,mill_deforestation_risk , mill_legal_prf_risk , mill_legal_production_forest,
            mill_legal_conservation_area , mill_legal_landuse_risk , mill_complex_supplybase_risk , mill_date_update
            
        FROM app_mill 
        WHERE is_planted::boolean=true
    ) AS tile WHERE geom IS NOT NULL;

    RETURN mvt;
END
$$
LANGUAGE plpgsql
STABLE
PARALLEL SAFE;
COMMENT ON FUNCTION function_zxy_query_app_mill_by_planted IS 'Filters the Mill table by planted  and renders 2D geometries';


CREATE OR REPLACE FUNCTION function_zxy_query_app_mill_by_unplanted(
    z integer, x integer, y integer,
    query_params json)
RETURNS bytea
AS $$
DECLARE
    mvt bytea;
BEGIN
    SELECT INTO mvt ST_AsMVT(tile, 'function_zxy_query_app_mill_by_unplanted', 4096, 'geom') FROM (
        SELECT
            ST_AsMVTGeom(ST_Transform(ST_CurveToLine(geom), 3857), ST_TileEnvelope(z, x, y), 4096, 64, true) AS geom ,id,
            mill_eq_id, mill_name, mill_uml_id , mill_company_name ,mill_company_group_id, mill_company_group ,mill_country, mill_province , mill_district ,mill_address ,mill_type ,mill_lat , mill_long , 
            mill_rspo , mill_mspo , mill_capacity , mill_methane_capture ,mill_deforestation_risk , mill_legal_prf_risk , mill_legal_production_forest,
            mill_legal_conservation_area , mill_legal_landuse_risk , mill_complex_supplybase_risk , mill_date_update
            
        FROM app_mill 
        WHERE is_planted::boolean=false
    ) AS tile WHERE geom IS NOT NULL;

    RETURN mvt;
END
$$
LANGUAGE plpgsql
STABLE
PARALLEL SAFE;
COMMENT ON FUNCTION function_zxy_query_app_mill_by_unplanted IS 'Filters the Mill table by unplanted  and renders 2D geometries';
