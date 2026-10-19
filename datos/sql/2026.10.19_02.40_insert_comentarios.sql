-- Script de inserción para la tabla comentario

INSERT INTO comentario (TEXTO, ID_USUARIO, ID_TARJETA) VALUES
('Logo aprobado por el cliente.', (SELECT ID_USUARIO FROM usuarios WHERE RUT = '11.222.333-9'), (SELECT ID_TARJETA FROM tarjeta WHERE NOMBTARJ = 'Diseñar logo')),
('Falta la versión móvil.', (SELECT ID_USUARIO FROM usuarios WHERE RUT = '15.678.901-1'), (SELECT ID_TARJETA FROM tarjeta WHERE NOMBTARJ = 'Maquetar página de inicio')),
('El hosting ya está atrasado, priorizar.', (SELECT ID_USUARIO FROM usuarios WHERE RUT = '18.765.432-7'), (SELECT ID_TARJETA FROM tarjeta WHERE NOMBTARJ = 'Contratar hosting'));