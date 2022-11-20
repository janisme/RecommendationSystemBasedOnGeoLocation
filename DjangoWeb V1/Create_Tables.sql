-- create table mergedtables2 (
--     id integer primary key autoincrement, 
--     ID_ANO TEXT , PRG TEXT , 
--     ANNEE_SCOLAIRE TEXT , SITE TEXT , ADR_CP INT , 
--     ADR_VILLE TEXT , ADR_PAYS TEXT , ANNEE TEXT , 
--     ENTREPRISE TEXT , CODE_POSTAL INT , VILLE TEXT ,
--     PAYS TEXT , SUJET TEXT , REMUNERATION DECIMAL,
--     idCSV int
-- );

-- ALTER TABLE "PRG_STUDENT_SITE" ADD COLUMN idCSV int;

-- DELETE FROM PRG_STUDENT_SITE WHERE  idCSV=3; 
-- DELETE FROM STUDENT_INTERNSHIP WHERE  idCSV=3; 
-- DELETE FROM "ADR_STUDENTS" WHERE  idCSV=3; 
-- DELETE FROM mergedtables WHERE  mergedtables.idCSV>2;

-- DELETE FROM mergedtables WHERE  mergedtables.idCSV>2; 
-- select distinct idCSV FROM mergedtables; 
-- select distinct idCSV FROM ADR_STUDENTS; 

-- DELETE FROM "FORECAST_WEIGHTS" where idCSV>=2; 
-- select * from FORECAST_WEIGHTS;

VACUUM;

-- ALTER TABLE "mergedtables" ADD COLUMN ENT_LAT REAL;
-- ALTER TABLE "mergedtables" ADD COLUMN ENT_LON REAL;
-- ALTER TABLE "mergedtables" ADD COLUMN ADR_LAT REAL;
-- ALTER TABLE "mergedtables" ADD COLUMN ADR_LON REAL;
-- ALTER TABLE "mergedtables" ADD COLUMN SITE_LAT REAL;
-- ALTER TABLE "mergedtables" ADD COLUMN SITE_LON REAL;
-- ALTER TABLE "mergedtables" ADD COLUMN home_campus REAL;
-- ALTER TABLE "mergedtables" ADD COLUMN home_entreprise REAL;
-- ALTER TABLE "mergedtables" ADD COLUMN campus_entreprise REAL;

-- INSERT INTO mergedtables (
--     ID_ANO , PRG , 
--     ANNEE_SCOLAIRE , SITE , ADR_CP  , 
--     ADR_VILLE , ADR_PAYS  , ANNEE , 
--     ENTREPRISE , CODE_POSTAL , VILLE  ,
--     PAYS , SUJET , REMUNERATION, idCSV )

--     SELECT     ID_ANO , PRG , 
--     ANNEE_SCOLAIRE , SITE , ADR_CP  , 
--     ADR_VILLE , ADR_PAYS  , ANNEE , 
--     ENTREPRISE , CODE_POSTAL , VILLE  ,
--     PAYS , SUJET , REMUNERATION, 1
    
--     FROM mergedtables;

    /* SELECT COUNT(*) FROM mergedtables; */

--     ALTER TABLE mergedtables RENAME TO mergedtables_OLD;

-- create table ADR_STUDENTS (
--     id integer primary key autoincrement, 
--     ADR_CP TEXT,
--     ADR_VILLE TEXT,
--     ADR_PAYS TEXT,
--     ID_ANO TEXT,
--     idCSV int
-- );

-- drop table "adr_students_temp";

-- INSERT INTO "ADR_STUDENTS" (
--     ADR_CP, ADR_VILLE ,
--     ADR_PAYS ,   ID_ANO ,
--     idCSV
-- )
--     SELECT 
--     ADR_CP, ADR_VILLE ,
--     ADR_PAYS ,   ID_ANO ,
--     1
--     FROM "adr_students_temp1";

-- create table STUDENT_INTERNSHIP (
--     id integer primary key autoincrement,
--     ANNEE TEXT,
--     ANNEE_SCOLAIRE TEXT,
--     ENTREPRISE TEXT,
--     CODE_POSTAL TEXT,
--     VILLE TEXT,
--     PAYS TEXT,
--     SUJET TEXT,
--     REMUNERATION TEXT,
--     ID_ANO TEXT,
--     idCSV int
-- );

-- INSERT INTO STUDENT_INTERNSHIP (
--     ANNEE  ,    ANNEE_SCOLAIRE  ,    ENTREPRISE  ,    CODE_POSTAL  ,
--     VILLE  ,    PAYS  ,    SUJET  ,    REMUNERATION  ,    ID_ANO  ,
--         idCSV )
--     SELECT 
--     ANNEE  ,    ANNEE_SCOLAIRE  ,    ENTREPRISE  ,    CODE_POSTAL  ,
--     VILLE  ,    PAYS  ,    SUJET  ,    REMUNERATION  ,    ID_ANO  ,
--     3
--     FROM "STUDENT_INTERNSHIP" ;

-- DROP TABLE ADR_LOCATION;

-- CREATE TABLE ADR_LOCATION (
--     id integer primary key autoincrement,
--     CODE_POSTAL TEXT,
--     LAT TEXT,
--     LON TEXT,
--     PAYS TEXT,
--     VILLE TEXT,
--     idCSV int
--   );

-- INSERT INTO
--   "ADR_LOCATION" (CODE_POSTAL, idCSV, LAT, LON, PAYS, VILLE)
-- SELECT CODE_POSTAL, 1, LAT, LON, PAYS, VILLE
--    FROM temp_LOCATION;
  

-- INSERT INTO
--   "PRG_STUDENT_SITE" (ANNE_SCOLAIRE, id, ID_ANO, idCSV, PRG, SITE)
-- SELECT
--   ANNE_SCOLAIRE, id, ID_ANO, 3, PRG, SITE
--   FROM  "PRG_STUDENT_SITE";

-- SELECT DISTINCT idCSV from "PRG_STUDENT_SITE";
/* SELECT DISTINCT idCSV from ADR_STUDENTS; */
/* SELECT DISTINCT idCSV from "STUDENT_INTERNSHIP"; */

-- INSERT INTO
--   "ADR_STUDENTS" (ADR_CP, ADR_PAYS, ADR_VILLE, ID_ANO, idCSV)
-- SELECT
--   ADR_CP, ADR_PAYS, ADR_VILLE, ID_ANO, 1
--   FROM ADR_STUDENTS;

-- CREATE TABLE "PRG_STUDENT_SITE"(
--     id integer primary key autoincrement,
--     ANNE_SCOLAIRE TEXT,
--     ID_ANO TEXT,
--     PRG TEXT,
--     SITE TEXT,
--     idCSV int
--   );

-- INSERT INTO
--   "PRG_STUDENT_SITE" (ANNE_SCOLAIRE, ID_ANO, idCSV, PRG, SITE)
-- SELECT 
--    ANNE_SCOLAIRE, ID_ANO, idCSV, PRG, SITE
-- FROM PRG_STUDENT_SITE2;

-- DROP TABLE PRG_STUDENT_SITE2;

-- DROP TABLE FORECAST_WEIGHTS;

-- create table FORECAST_WEIGHTS (
--     id integer primary key autoincrement,
--     w0 REAL,
--     w1 REAL,
--     w2 REAL,
--     idCSV int
-- );

-- INSERT INTO
--   "FORECAST_WEIGHTS" (idCSV, w0, w1, w2)
-- VALUES
-- (1,0.6411390851115564,0.00995699529048115,0.2993355787543132),
-- (3,0.3833683335255038,0.03745249965275769,0.22946374019113733),
-- (4,0.6454130968379639,0.7055628892611244,0.03323184189739557),
-- (5,0.5275708187649965,0.36851935471907665,0.05518348317144247),
-- (6,0.46386889717894925,0.3959920289332492,0.8630252752900243),
-- (7,0.3361249453413812,0.44996396397868565,0.3977180647783032),
-- (8,0.295189241350076,0.1143489018081086,0.4861927367208909),
-- (9,0.17547350296804282,0.05738630166020678,0.5092936204229007),
-- (11,-0.12265417857601617,0.6536882444296673,0.8694860998917122),
-- (12,0.32942959823090007,0.43087942045379946,0.9318324900236523)
--   ;

/* select * from "PRG_STUDENT_SITE"; */
/* select idCSV, count(*) from "PRG_STUDENT_SITE" group by idCSV; */
/* select count(*)  */
/* delete from PRG_STUDENT_SITE where idCSV is NULL; */
/* delete from PRG_STUDENT_SITE where idCSV=3; */

/* select idCSV, count(*) from "PRG_STUDENT_SITE" group by idCSV; */
/* delete from STUDENT_INTERNSHIP where idCSV is NULL; */
