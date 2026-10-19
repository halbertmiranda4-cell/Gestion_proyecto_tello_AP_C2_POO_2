-- Script de inserción para la tabla tablero
-- Regla: un proyecto tiene un solo tablero.

INSERT INTO tablero (NOMTAB, ID_PROYECTO) VALUES
('Tablero principal', (SELECT ID_PROYECTO FROM proyecto WHERE NOMPRO = 'Sitio web Cafetería'));