-- Ajustes de restricciones para PROYECTO_TRELLO_V2
-- Ejecutar después de Proyecto_Trello.sql y antes de los inserts
USE PROYECTO_TRELLO_V2;

-- Un proyecto solo puede tener un tablero
ALTER TABLE TABLERO
    ADD CONSTRAINT UQ_TABLERO_PROYECTO UNIQUE (ID_PROYECTO);

-- Solo se permiten los estados definidos en la aplicación
ALTER TABLE TARJETA
    ADD CONSTRAINT CK_TARJETA_ESTADO CHECK (ESTADO IN ('pendiente', 'en progreso', 'completada')); 