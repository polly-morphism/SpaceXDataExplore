DECLARE
    var_country country.name%TYPE;
BEGIN
    var_country := 'contry';
    FOR i IN 11..21 LOOP
        INSERT INTO country (
        countryid, name)
        VALUES (
        i,
        trim(var_country) || i);
        END LOOP;
    END;
