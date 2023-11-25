CREATE OR REPLACE FUNCTION function_zxy_query_app_agriplot_by_estateids(
    z integer, x integer, y integer,
    query_params json)
RETURNS bytea
AS $$
DECLARE
    mvt bytea;
    estateids text[];
BEGIN
    -- Extracting the array using json_array_elements_text
    SELECT array_agg(value::text) INTO estateids
    FROM json_array_elements_text(query_params -> 'estateids');

    SELECT INTO mvt ST_AsMVT(tile, 'function_zxy_query_app_agriplot_by_estateids', 4096, 'geom') FROM (
        SELECT
            ST_AsMVTGeom(ST_Transform(ST_CurveToLine(geom), 3857), ST_TileEnvelope(z, x, y), 4096, 64, true) AS geom, id_estate
        FROM app_agriplot 
        WHERE id_estate = ANY(estateids)
    ) AS tile WHERE geom IS NOT NULL;

    RETURN mvt;
END
$$
LANGUAGE plpgsql
STABLE
PARALLEL SAFE;
COMMENT ON FUNCTION function_zxy_query_app_agriplot_by_estateids IS 'Filters the Agriplot table by estateids and renders 2D geometries';
