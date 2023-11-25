CREATE OR REPLACE FUNCTION function_zxy_query_app_agriplot_by_estateids(
    z integer, x integer, y integer,
    query_params json)
RETURNS bytea
AS $$
DECLARE
    mvt bytea;
    estateids text;
    actual_supplier text;
BEGIN
    estateids := trim((query_params::jsonb) ->> 'estateids');
    actual_supplier := trim((query_params::jsonb)->> 'actual_supplier');

    SELECT INTO mvt ST_AsMVT(tile, 'function_zxy_query_app_agriplot_by_estateids', 4096, 'geom') FROM (
        SELECT
            ST_AsMVTGeom(ST_Transform(ST_CurveToLine(geom), 3857), ST_TileEnvelope(z, x, y), 4096, 64, true) AS geom, id_estate ,actual_supplier
        FROM app_agriplot 
        WHERE  actual_supplier::text = actual_supplier AND id_state::text IN estateids 
    ) AS tile WHERE geom IS NOT NULL;

    RETURN mvt;
END;
$$
LANGUAGE plpgsql
STABLE
PARALLEL SAFE;
COMMENT ON FUNCTION function_zxy_query_app_agriplot_by_estateids IS 'Filters the Agriplot table by estateids and actual supplier';