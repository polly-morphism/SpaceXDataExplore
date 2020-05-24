CREATE TABLE country (
    countryid  INTEGER NOT NULL,
    name       CHAR(60 CHAR)
);

ALTER TABLE country ADD CONSTRAINT country_pk PRIMARY KEY ( countryid );

CREATE TABLE customer (
    name                         CHAR(40 CHAR),
    customertype_customertypeid  INTEGER NOT NULL,
    country_countryid            INTEGER NOT NULL,
    customerid                   INTEGER NOT NULL
);

ALTER TABLE customer ADD CONSTRAINT customer_pk PRIMARY KEY ( customerid );

CREATE TABLE customertype (
    customertypeid  INTEGER NOT NULL,
    name            CHAR(40 CHAR)
);

ALTER TABLE customertype ADD CONSTRAINT customertype_pk PRIMARY KEY ( customertypeid );

CREATE TABLE landingtype (
    landingtypeid  INTEGER NOT NULL,
    name           CHAR(40 CHAR)
);

ALTER TABLE landingtype ADD CONSTRAINT landingtype_pk PRIMARY KEY ( landingtypeid );

CREATE TABLE mission (
    missionid                  INTEGER NOT NULL,
    launchdate                 DATE,
    launchsite                 VARCHAR2(128 CHAR),
    missionoutcome             CHAR(20 CHAR),
    falurereason               CHAR(40 CHAR),
    landingoutcome             CHAR(50 CHAR),
    flightnumber               CHAR(5 CHAR),
    orbit                      CHAR(40 CHAR),
    payload_payloadid          INTEGER NOT NULL,
    landingtype_landingtypeid  INTEGER NOT NULL,
    vehicletype_vehicletypeid  INTEGER NOT NULL,
    customer_customerid        INTEGER NOT NULL
);

ALTER TABLE mission ADD CONSTRAINT mission_pk PRIMARY KEY ( missionid );

CREATE TABLE payload (
    payloadid                  INTEGER NOT NULL,
    name                       CHAR(50 CHAR),
    masskg                     FLOAT,
    payloadtype_payloadtypeid  INTEGER NOT NULL
);

ALTER TABLE payload ADD CONSTRAINT payload_pk PRIMARY KEY ( payloadid );

CREATE TABLE payloadtype (
    payloadtypeid  INTEGER NOT NULL,
    name           CHAR(40 CHAR)
);

ALTER TABLE payloadtype ADD CONSTRAINT payloadtype_pk PRIMARY KEY ( payloadtypeid );

CREATE TABLE vehicletype (
    vehicletypeid  INTEGER NOT NULL,
    name           CHAR(40 CHAR)
);

ALTER TABLE vehicletype ADD CONSTRAINT vehicletype_pk PRIMARY KEY ( vehicletypeid );

ALTER TABLE customer
    ADD CONSTRAINT customer_country_fk FOREIGN KEY ( country_countryid )
        REFERENCES country ( countryid )
            ON DELETE CASCADE;

ALTER TABLE customer
    ADD CONSTRAINT customer_customertype_fk FOREIGN KEY ( customertype_customertypeid )
        REFERENCES customertype ( customertypeid )
            ON DELETE CASCADE;

ALTER TABLE mission
    ADD CONSTRAINT mission_customer_fk FOREIGN KEY ( customer_customerid )
        REFERENCES customer ( customerid )
            ON DELETE CASCADE;

ALTER TABLE mission
    ADD CONSTRAINT mission_landingtype_fk FOREIGN KEY ( landingtype_landingtypeid )
        REFERENCES landingtype ( landingtypeid )
            ON DELETE CASCADE;

ALTER TABLE mission
    ADD CONSTRAINT mission_payload_fk FOREIGN KEY ( payload_payloadid )
        REFERENCES payload ( payloadid )
            ON DELETE CASCADE;

ALTER TABLE mission
    ADD CONSTRAINT mission_vehicletype_fk FOREIGN KEY ( vehicletype_vehicletypeid )
        REFERENCES vehicletype ( vehicletypeid )
            ON DELETE CASCADE;

ALTER TABLE payload
    ADD CONSTRAINT payload_payloadtype_fk FOREIGN KEY ( payloadtype_payloadtypeid )
        REFERENCES payloadtype ( payloadtypeid )
            ON DELETE CASCADE;
