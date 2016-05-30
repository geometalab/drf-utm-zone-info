INSERT INTO osmaxx.nonop_l
  SELECT osm_line.osm_id as osm_id,
    osm_timestamp as lastchange ,
-- R=Relation & W=Way --
    CASE
     WHEN osm_line.osm_id<0 THEN 'R' -- Relation
     ELSE 'W'                        -- Way
    END AS geomtype,

    ST_Multi(way) AS geom,
-- Differentiating between Highway and Railway --
    case
    when osm_line.highway is not null then 'highway'
    when railway is not null then 'railway'
    end as type,
    case
      when osmaxx.lifecycle_l.highway='track' then
        case
          when tracktype in ('grade1','grade2','grade3','grade4','grade5') then tracktype
          else 'track'
        end
      when osmaxx.lifecycle_l.highway in ('motorway','trunk','primary','secondary','tertiary',
            'unclassified','residential','living_street','pedestrian',
            'motorway_link','trunk_link','primary_link','secondary_link',
            'service','track','bridleway','cycleway','footway',
            'path','steps') then osmaxx.lifecycle_l.highway
      else 'road'
    end as sub_type,
    name as name,
    "name:en" as name_en,
    "name:fr" as name_fr,
    "name:es" as name_es,
    "name:de" as name_de,
    int_name as name_int,
    case
        when name is not null AND name = transliterate(name) then name
        when "name:en" is not null then "name:en"
        when "name:fr" is not null then "name:fr"
        when "name:es" is not null then "name:es"
        when "name:de" is not null then "name:de"
        when name is not null then transliterate(name)
        else NULL
    end as label,
    cast(tags as text) as tags,
    ref as ref,
-- Checking for bridges with different tags associated to bridges --
    case
    when bridge in ('split_log' , 'beam', 'culvert', 'low_water_crossing', 'yes', 'suspension', 'viaduct', 'aqueduct', 'covered') then TRUE
    else FALSE
    end as bridge,
-- Checking for tunnels with different tags associated to tunnels --
    case
    when tunnel in ('passage', 'culvert', 'noiseprotection galerie', 'gallery', 'building_passage', 'avalanche_protector','teilweise', 'viaduct', 'tunnel', 'yes') then TRUE
    else FALSE
    end as tunnel,

    z_order as z_order,
-- Differentiating the different types of transport --
    case
     when osm_line.highway='planned' or railway='planned' then 'P'
     when osm_line.highway='disused'  or railway='disused' then 'D'
     when osm_line.highway='construction'  or railway='construction' then 'C'
     when osm_line.highway='abandoned'  or railway='abandoned' then 'A'
     end as status
 FROM osm_line
   JOIN osmaxx.lifecycle_l ON osm_line.osm_id = osmaxx.lifecycle_l.osm_id;
