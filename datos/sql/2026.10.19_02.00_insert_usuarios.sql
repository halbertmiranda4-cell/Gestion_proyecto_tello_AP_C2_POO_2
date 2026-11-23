-- Script de inserción para la tabla usuarios
-- Las contraseñas se guardan como hash bcrypt (nunca en texto plano).
-- Contraseña de prueba de los 4 usuarios: Trello#2026

INSERT INTO usuarios (NOMBRE, CORREO, CONTRASENA, RUT) VALUES
('Ana Torres', 'ana.torres@trello.cl', '$2b$12$LISCp94BPlGySolJNlmgFerAxjs0vnoczmdonG9gdezCtVNoM4Bf6', '11.222.333-9'),
('Bruno Díaz', 'bruno.diaz@trello.cl', '$2b$12$mzIp2r44QZdi/e4RavV/FevQcI0n6EE1AZpqkvYnoPJwDleXny5iG', '15.678.901-1'),
('Carla Muñoz', 'carla.munoz@trello.cl', '$2b$12$XcOl38lJDD1qNmk4.zvFauWVjot9b/jVQKI9V93rFxLJA7WeCPif2', '18.765.432-7'),
('Diego Rojas', 'diego.rojas@trello.cl', '$2b$12$WzLAoc8X0SxdxlgcepMWJuYmUHPJFSogQtp0VN3Et0ONAcME1onGm', '20.111.222-2');