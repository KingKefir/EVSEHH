DROP DATABASE IF EXISTS charging_germany;

CREATE DATABASE ev_charging_germany;

DROP TABLE IF EXISTS ladeeinrichtung;

CREATE TABLE ladeeinrichtung (
	ladeeinrichtung_id			int,
    art_der_ladeeinrichung		varchar(225),
    anzahl_ladepunkte			tinyint,
    anschlussleistung			int,
    steckertypen1				varchar(225),
    steckertypen2				varchar(225),
    steckertypen3				varchar(225),
    steckertypen4				varchar(225),
    p1_kw						float,
    p2_kw						float			NULL,
    p3_kw						float			NULL,
    p4_kw						float			NULL,
    inbetriebnahmedatum			date			NULL,
    betreiber_id				int,
    standort_id					int
    
 )
 ;   
 
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\ladeeinrichtung.csv' 
INTO TABLE ladeeinrichtung
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES ; 
 
####################################################
# adresse
 
 DROP TABLE IF EXISTS adresse;
 
 CREATE TABLE adresse (
	adress_id				INT				NOT NULL,
    kreis_kreisfreie_stadt	VARCHAR(255)	NOT NULL,
    ort						VARCHAR(255)	NOT NULL,
    postleitzahl			INT,
    strasse					VARCHAR(255),
    hausnummer				VARCHAR(255)
 )
 ;   


LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\adresse.csv' 
INTO TABLE adresse
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
; 


####################################################
# betreiber

DROP TABLE IF EXISTS betreiber;

 CREATE TABLE betreiber (
	betreiber_id		INT				NOT NULL,
    betreiber			VARCHAR(255)	NOT NULL
    
 )
 ;   
 
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\betreiber.csv' 
INTO TABLE betreiber
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
;  
 
 ####################################################
# standort

DROP TABLE IF EXISTS standort;

 CREATE TABLE standort (
	standort_id		INT				NOT NULL,
    breitengrad		VARCHAR(255),
    laengengrad		VARCHAR(255),
    adress_id		INT				NOT NULL
 )
 ;   
 
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\standort.csv' 
INTO TABLE standort
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
;  
 
############################################################### 

ALTER TABLE ladeeinrichtung
ADD PRIMARY KEY (ladeeinrichtung_id);

ALTER TABLE betreiber
ADD PRIMARY KEY (betreiber_id);

ALTER TABLE standort
ADD PRIMARY KEY (standort_id);

ALTER TABLE adresse
ADD PRIMARY KEY (adress_id);

ALTER TABLE betreiber
ADD PRIMARY KEY (betreiber_id);

ALTER TABLE standort
ADD PRIMARY KEY (standort_id);



ALTER TABLE ladeeinrichtung
ADD CONSTRAINT fk_betreiber_id
FOREIGN KEY (betreiber_id) REFERENCES betreiber(betreiber_id);

ALTER TABLE ladeeinrichtung
ADD CONSTRAINT fk_standort_id
FOREIGN KEY (standort_id) REFERENCES standort(standort_id);

ALTER TABLE standort
ADD CONSTRAINT fk_adress_id
FOREIGN KEY (adress_id) REFERENCES adresse(adress_id);