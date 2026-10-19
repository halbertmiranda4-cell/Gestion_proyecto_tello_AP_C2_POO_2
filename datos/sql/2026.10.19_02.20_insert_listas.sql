-- Script de inserción para la tabla lista
-- Listas del tablero del proyecto "Sitio web Cafetería", ordenadas por posición.

INSERT INTO lista (NOMBLIST, ID_TABLERO, POSICION, DESCRIPLIST) VALUES
('Por hacer', (SELECT ID_TABLERO FROM tablero WHERE NOMTAB = 'Tablero principal'), 1, 'Tareas pendientes'),
('En curso', (SELECT ID_TABLERO FROM tablero WHERE NOMTAB = 'Tablero principal'), 2, 'Tareas en desarrollo'),
('Hecho', (SELECT ID_TABLERO FROM tablero WHERE NOMTAB = 'Tablero principal'), 3, 'Tareas terminadas');