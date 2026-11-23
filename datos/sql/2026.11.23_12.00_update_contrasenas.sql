-- Reemplaza las contraseñas en texto plano de los usuarios de prueba por su hash bcrypt.
-- Contraseña de prueba de los 4 usuarios: Trello#2026
USE PROYECTO_TRELLO_V2;

UPDATE usuarios SET CONTRASENA = '$2b$12$LISCp94BPlGySolJNlmgFerAxjs0vnoczmdonG9gdezCtVNoM4Bf6' WHERE RUT = '11.222.333-9';
UPDATE usuarios SET CONTRASENA = '$2b$12$mzIp2r44QZdi/e4RavV/FevQcI0n6EE1AZpqkvYnoPJwDleXny5iG' WHERE RUT = '15.678.901-1';
UPDATE usuarios SET CONTRASENA = '$2b$12$XcOl38lJDD1qNmk4.zvFauWVjot9b/jVQKI9V93rFxLJA7WeCPif2' WHERE RUT = '18.765.432-7';
UPDATE usuarios SET CONTRASENA = '$2b$12$WzLAoc8X0SxdxlgcepMWJuYmUHPJFSogQtp0VN3Et0ONAcME1onGm' WHERE RUT = '20.111.222-2';