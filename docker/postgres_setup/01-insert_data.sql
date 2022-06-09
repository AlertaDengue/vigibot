\connect "dengue"

INSERT INTO "Dengue_global"."Municipio" (geocodigo, nome, geojson, populacao, uf) 
VALUES (3304557, 'Rio de Janeiro', 'null', 1, 'null');

INSERT INTO "Dengue_global"."Municipio" (geocodigo, nome, geojson, populacao, uf) 
VALUES (4126306, 'sengés', 'null', 2, 'null');

INSERT INTO "Dengue_global"."Municipio" (geocodigo, nome, geojson, populacao, uf) 
VALUES (2312601, 'São Luís do Curu', 'null', 3, 'null');

INSERT INTO "Dengue_global"."Municipio" (geocodigo, nome, geojson, populacao, uf) 
VALUES (3160603, 'santo hipolito', 'null', 4, 'null');

INSERT INTO "Dengue_global"."Municipio" (geocodigo, nome, geojson, populacao, uf) 
VALUES (3303302, 'niteroi', 'null', 5, 'null');

INSERT INTO "Municipio"."Historico_alerta" (id, "data_iniSE", nivel, "SE", municipio_geocodigo) 
VALUES (01, '2022-05-29', 3, 202222, 3304557);