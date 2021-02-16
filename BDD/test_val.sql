--Ajout de capteurs pour la rose dans ChambreBen
INSERT INTO SENSORACTION(Name, Unit, PlantReference) VALUES("Temperature", "°C", 1);
INSERT INTO SENSORACTION(Name, Unit, PlantReference) VALUES("Humidity", "%", 1);
INSERT INTO SENSORACTION(Name, Unit, PlantReference) VALUES("Luminosity", "Lux", 1);
INSERT INTO SENSORACTION(Name, Unit, PlantReference) VALUES("GroundQuality", "%", 1);

--Ajout MEASUREs
--Thermometre
INSERT INTO MEASURE(value, SensoractionReference) VALUES(25, 1);
INSERT INTO MEASURE(value, SensoractionReference) VALUES(26, 1);
INSERT INTO MEASURE(value, SensoractionReference) VALUES(27, 1);

-- Humidite
INSERT INTO MEASURE(value, SensoractionReference) VALUES(30, 2);
INSERT INTO MEASURE(value, SensoractionReference) VALUES(40, 2);
INSERT INTO MEASURE(value, SensoractionReference) VALUES(50, 2);

-- Luminosité
INSERT INTO MEASURE(value, SensoractionReference) VALUES(30, 3);
INSERT INTO MEASURE(value, SensoractionReference) VALUES(40, 3);
INSERT INTO MEASURE(value, SensoractionReference) VALUES(50, 3);

--Modification des dates pour le graph
