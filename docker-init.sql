-- Script de inicialización de la base de datos ComPuter
-- Este script se ejecuta automáticamente cuando se crea el contenedor de PostgreSQL

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS computer_db;

-- Conectar a la base de datos
\c computer_db;

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Crear usuario de aplicación con permisos limitados
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'computer_user') THEN
        CREATE ROLE computer_user WITH LOGIN PASSWORD 'computer_password';
    END IF;
END
$$;

-- Otorgar permisos al usuario
GRANT CONNECT ON DATABASE computer_db TO computer_user;
GRANT USAGE ON SCHEMA public TO computer_user;
GRANT CREATE ON SCHEMA public TO computer_user;

-- Configurar permisos por defecto para tablas futuras
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO computer_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO computer_user;

-- Configuración de performance
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Configurar logging para desarrollo
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_duration = on;
ALTER SYSTEM SET log_min_duration_statement = 1000;

-- Crear índices para búsqueda de texto
-- Estos se crearán después de que las tablas sean creadas por la aplicación

COMMENT ON DATABASE computer_db IS 'Base de datos principal para la aplicación ComPuter - Sistema de recomendación de componentes de PC';