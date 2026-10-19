-- Script de inserción para la tabla tarjeta
-- Incluye tarjetas en los tres estados, una sin responsable y una vencida.
-- El responsable es un participante del proyecto (usuario_proyecto).

INSERT INTO tarjeta (NOMBTARJ, ID_LISTA, DESCRIPTARJ, FECHA_CREACION, FECHA_VENCIMIENTO, ESTADO, POSICION, ID_RESPONSABLE) VALUES
('Diseñar logo', (SELECT ID_LISTA FROM lista WHERE NOMBLIST = 'Hecho'), 'Propuesta de logo y paleta de colores', '2026-10-05', '2026-10-15', 'completada', 1,
    (SELECT up.ID_USUARIO_PROYECTO FROM usuario_proyecto up JOIN usuarios u ON u.ID_USUARIO = up.ID_USUARIO JOIN proyecto p ON p.ID_PROYECTO = up.ID_PROYECTO WHERE u.RUT = '18.765.432-7' AND p.NOMPRO = 'Sitio web Cafetería')),
('Maquetar página de inicio', (SELECT ID_LISTA FROM lista WHERE NOMBLIST = 'En curso'), 'HTML y CSS de la portada', '2026-10-10', '2026-10-30', 'en progreso', 1,
    (SELECT up.ID_USUARIO_PROYECTO FROM usuario_proyecto up JOIN usuarios u ON u.ID_USUARIO = up.ID_USUARIO JOIN proyecto p ON p.ID_PROYECTO = up.ID_PROYECTO WHERE u.RUT = '15.678.901-1' AND p.NOMPRO = 'Sitio web Cafetería')),
('Cargar carta digital', (SELECT ID_LISTA FROM lista WHERE NOMBLIST = 'Por hacer'), 'Ingresar productos y precios', '2026-10-15', '2026-11-10', 'pendiente', 1,
    (SELECT up.ID_USUARIO_PROYECTO FROM usuario_proyecto up JOIN usuarios u ON u.ID_USUARIO = up.ID_USUARIO JOIN proyecto p ON p.ID_PROYECTO = up.ID_PROYECTO WHERE u.RUT = '11.222.333-9' AND p.NOMPRO = 'Sitio web Cafetería')),
('Formulario de contacto', (SELECT ID_LISTA FROM lista WHERE NOMBLIST = 'Por hacer'), 'Formulario con validación de correo', '2026-10-15', '2026-11-20', 'pendiente', 2,
    NULL),
('Contratar hosting', (SELECT ID_LISTA FROM lista WHERE NOMBLIST = 'Por hacer'), 'Cotizar y contratar el hosting', '2026-10-01', '2026-10-12', 'pendiente', 3,
    (SELECT up.ID_USUARIO_PROYECTO FROM usuario_proyecto up JOIN usuarios u ON u.ID_USUARIO = up.ID_USUARIO JOIN proyecto p ON p.ID_PROYECTO = up.ID_PROYECTO WHERE u.RUT = '11.222.333-9' AND p.NOMPRO = 'Sitio web Cafetería'));