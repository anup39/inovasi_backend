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
            ST_AsMVTGeom(ST_Transform(ST_CurveToLine(geom), 3857), ST_TileEnvelope(z, x, y), 4096, 64, true) AS geom ,id, id_estate
            ownership_plot, subsidiary,  estate ,agriplot_id ,type_of_supplier ,village ,sub_district ,district ,province ,country , planted_area , year_update , risk_assess ,ghg_luc , status_of_plot 
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


CREATE OR REPLACE FUNCTION function_zxy_query_app_agriplot_by_estateids_and_wkt(
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

    SELECT INTO mvt ST_AsMVT(tile, 'function_zxy_query_app_agriplot_by_estateids_and_wkt', 4096, 'geom') FROM (
        SELECT
            ST_AsMVTGeom(ST_Transform(ST_CurveToLine(geom), 3857), ST_TileEnvelope(z, x, y), 4096, 64, true) AS  geom ,id, id_estate 
            ownership_plot, subsidiary,  estate ,agriplot_id ,type_of_supplier ,village ,sub_district ,district ,province ,country , planted_area , year_update , risk_assess ,ghg_luc , status_of_plot 
        FROM app_agriplot 
        WHERE id_estate = ANY(estateids) AND ST_Intersects(geom, ST_Transform(ST_GeomFromText(query_params->>'geometry_wkt', 4326), 4326))
    ) AS tile WHERE geom IS NOT NULL;

    RETURN mvt;
END
$$
LANGUAGE plpgsql
STABLE
PARALLEL SAFE;
COMMENT ON FUNCTION function_zxy_query_app_agriplot_by_estateids_and_wkt IS 'Filters the Agriplot table by estateids and wkt geometry and renders 2D geometries ';


CREATE OR REPLACE FUNCTION function_zxy_query_app_mill_by_millid(
    z integer, x integer, y integer,
    query_params json)
RETURNS bytea
AS $$
DECLARE
    mvt bytea;
    millid text;
BEGIN
    millid := trim((query_params::jsonb) ->> 'millid');
    SELECT INTO mvt ST_AsMVT(tile, 'function_zxy_query_app_mill_by_millid', 4096, 'geom') FROM (
        SELECT
            ST_AsMVTGeom(ST_Transform(ST_CurveToLine(geom), 3857), ST_TileEnvelope(z, x, y), 4096, 64, true) AS geom ,id,
            mill_eq_id, mill_name, mill_uml_id , mill_company_name ,mill_company_group_id, mill_company_group ,mill_country, mill_province , mill_district ,mill_address ,mill_type ,mill_lat , mill_long , 
            mill_rspo , mill_mspo , mill_capacity , mill_methane_capture ,mill_deforestation_risk , mill_legal_prf_risk , mill_legal_production_forest,
            mill_legal_conservation_area , mill_legal_landuse_risk , mill_complex_supplybase_risk , mill_date_update
            
        FROM app_mill 
        WHERE mill_eq_id::text=millid
    ) AS tile WHERE geom IS NOT NULL;

    RETURN mvt;
END
$$
LANGUAGE plpgsql
STABLE
PARALLEL SAFE;
COMMENT ON FUNCTION function_zxy_query_app_mill_by_millid IS 'Filters the Mill Table table by mill  and renders 2D geometries';



CREATE OR REPLACE FUNCTION function_zxy_query_app_agriplot_by_mill_eq_id(
    z integer, x integer, y integer,
    query_params json)
RETURNS bytea
AS $$
DECLARE
    mvt bytea;
    mill_eq_id text;
    statusplot text;
BEGIN
    mill_eq_id := trim((query_params::jsonb) ->> 'mill_eq_id');
    statusplot := trim((query_params::jsonb) ->> 'status_of_plot');
    SELECT INTO mvt ST_AsMVT(tile, 'function_zxy_query_app_agriplot_by_mill_eq_id', 4096, 'geom') FROM (
        SELECT
            ST_AsMVTGeom(ST_Transform(ST_CurveToLine(app_agriplot.geom), 3857), ST_TileEnvelope(z, x, y), 4096, 64, true) AS geom,
            app_agriplot.id, app_agriplot.id_estate, 
            app_agriplot.ownership_plot, app_agriplot.subsidiary, app_agriplot.estate, app_agriplot.agriplot_id,
            app_agriplot.type_of_supplier, app_agriplot.village, app_agriplot.sub_district, app_agriplot.district,
            app_agriplot.province, app_agriplot.country, app_agriplot.planted_area, app_agriplot.year_update,
            app_agriplot.risk_assess, app_agriplot.ghg_luc, app_agriplot.status_of_plot
        FROM public.app_agriplot
        WHERE public.app_agriplot.millideq::text = mill_eq_id AND public.app_agriplot.status_of_plot::text = statusplot
    ) AS tile WHERE geom IS NOT NULL;

    RETURN mvt;
END
$$
LANGUAGE plpgsql
STABLE
PARALLEL SAFE;
COMMENT ON FUNCTION function_zxy_query_app_agriplot_by_mill_eq_id IS 'Filters the Agriplot Table table by mill_eq_id  and renders 2D geometries';



CREATE OR REPLACE FUNCTION function_zxy_query_app_agriplot_by_wkt_and_status(
    z integer, x integer, y integer,
    query_params json)
RETURNS bytea
AS $$
DECLARE
    mvt bytea;
    statusplot text;
BEGIN
    statusplot := trim((query_params::jsonb) ->> 'status_of_plot');
    
    SELECT INTO mvt ST_AsMVT(tile, 'function_zxy_query_app_agriplot_by_wkt_and_status', 4096, 'geom') FROM (
        SELECT
            ST_AsMVTGeom(ST_Transform(ST_CurveToLine(geom), 3857), ST_TileEnvelope(z, x, y), 4096, 64, true) AS  geom , app_agriplot.id, app_agriplot.id_estate, 
            app_agriplot.ownership_plot, app_agriplot.subsidiary, app_agriplot.estate, app_agriplot.agriplot_id,
            app_agriplot.type_of_supplier, app_agriplot.village, app_agriplot.sub_district, app_agriplot.district,
            app_agriplot.province, app_agriplot.country, app_agriplot.planted_area, app_agriplot.year_update,
            app_agriplot.risk_assess, app_agriplot.ghg_luc, app_agriplot.status_of_plot
        FROM public.app_agriplot 
        WHERE public.app_agriplot.status_of_plot::text = statusplot AND ST_Intersects(geom, ST_Transform(ST_GeomFromText(query_params->>'geometry_wkt', 4326), 4326))
    ) AS tile WHERE geom IS NOT NULL;

    RETURN mvt;
END
$$
LANGUAGE plpgsql
STABLE
PARALLEL SAFE;
COMMENT ON FUNCTION function_zxy_query_app_agriplot_by_wkt_and_status IS 'Filters the Agriplot table by satatus  and wkt geometry and renders 2D geometries ';


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
