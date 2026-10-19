-- Script de inserción para la tabla tarjeta_etiqueta
-- Relación muchos a muchos: una tarjeta puede tener varias etiquetas.

INSERT INTO tarjeta_etiqueta (ID_TARJETA, ID_ETIQUETA) VALUES
((SELECT ID_TARJETA FROM tarjeta WHERE NOMBTARJ = 'Diseñar logo'), (SELECT ID_ETIQUETA FROM etiqueta WHERE NOMETIQ = 'Diseño')),
((SELECT ID_TARJETA FROM tarjeta WHERE NOMBTARJ = 'Maquetar página de inicio'), (SELECT ID_ETIQUETA FROM etiqueta WHERE NOMETIQ = 'Diseño')),
((SELECT ID_TARJETA FROM tarjeta WHERE NOMBTARJ = 'Maquetar página de inicio'), (SELECT ID_ETIQUETA FROM etiqueta WHERE NOMETIQ = 'Urgente')),
((SELECT ID_TARJETA FROM tarjeta WHERE NOMBTARJ = 'Contratar hosting'), (SELECT ID_ETIQUETA FROM etiqueta WHERE NOMETIQ = 'Urgente')),
((SELECT ID_TARJETA FROM tarjeta WHERE NOMBTARJ = 'Formulario de contacto'), (SELECT ID_ETIQUETA FROM etiqueta WHERE NOMETIQ = 'Backend'));