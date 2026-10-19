-- Script de inserción para la tabla etiqueta
-- Cada etiqueta pertenece a un proyecto.

INSERT INTO etiqueta (NOMETIQ, COLOR, ID_PROYECTO) VALUES
('Diseño', 'morado', (SELECT ID_PROYECTO FROM proyecto WHERE NOMPRO = 'Sitio web Cafetería')),
('Urgente', 'rojo', (SELECT ID_PROYECTO FROM proyecto WHERE NOMPRO = 'Sitio web Cafetería')),
('Backend', 'azul', (SELECT ID_PROYECTO FROM proyecto WHERE NOMPRO = 'Sitio web Cafetería'));