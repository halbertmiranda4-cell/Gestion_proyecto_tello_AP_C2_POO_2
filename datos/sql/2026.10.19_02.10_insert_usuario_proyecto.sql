-- Script de inserción para la tabla usuario_proyecto
-- Relación muchos a muchos: Bruno y Ana participan en ambos proyectos.

INSERT INTO usuario_proyecto (ID_USUARIO, ID_PROYECTO, ROL) VALUES
((SELECT ID_USUARIO FROM usuarios WHERE RUT = '11.222.333-9'), (SELECT ID_PROYECTO FROM proyecto WHERE NOMPRO = 'Sitio web Cafetería'), 'administrador'),
((SELECT ID_USUARIO FROM usuarios WHERE RUT = '15.678.901-1'), (SELECT ID_PROYECTO FROM proyecto WHERE NOMPRO = 'Sitio web Cafetería'), 'miembro'),
((SELECT ID_USUARIO FROM usuarios WHERE RUT = '18.765.432-7'), (SELECT ID_PROYECTO FROM proyecto WHERE NOMPRO = 'Sitio web Cafetería'), 'miembro'),
((SELECT ID_USUARIO FROM usuarios WHERE RUT = '15.678.901-1'), (SELECT ID_PROYECTO FROM proyecto WHERE NOMPRO = 'Sistema de inventario'), 'administrador'),
((SELECT ID_USUARIO FROM usuarios WHERE RUT = '11.222.333-9'), (SELECT ID_PROYECTO FROM proyecto WHERE NOMPRO = 'Sistema de inventario'), 'miembro'),
((SELECT ID_USUARIO FROM usuarios WHERE RUT = '20.111.222-2'), (SELECT ID_PROYECTO FROM proyecto WHERE NOMPRO = 'Sistema de inventario'), 'miembro');