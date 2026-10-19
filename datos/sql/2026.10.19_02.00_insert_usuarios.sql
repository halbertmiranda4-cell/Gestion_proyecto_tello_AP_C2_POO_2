-- Script de inserción para la tabla usuarios
-- Usuarios de prueba. La contraseña es texto de relleno: los usuarios reales
-- se registran desde la aplicación, que guarda la contraseña encriptada (bcrypt).

INSERT INTO usuarios (NOMBRE, CORREO, CONTRASENA, RUT) VALUES
('Ana Torres', 'ana.torres@trello.cl', 'SIN_CLAVE', '11.222.333-9'),
('Bruno Díaz', 'bruno.diaz@trello.cl', 'SIN_CLAVE', '15.678.901-1'),
('Carla Muñoz', 'carla.munoz@trello.cl', 'SIN_CLAVE', '18.765.432-7'),
('Diego Rojas', 'diego.rojas@trello.cl', 'SIN_CLAVE', '20.111.222-2');