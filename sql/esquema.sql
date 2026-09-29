-- ============================================
-- BASE DE DATOS: SISTEMA DE REGISTRO DE VEHÍCULOS
-- ESQUEMA MYSQL - SEMANA 13
-- ============================================

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS parqueadero;

USE parqueadero;


-- ============================================
-- 1. TABLA PRODUCTOS
-- ============================================

CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(150) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    disponible BOOLEAN NOT NULL
);


-- ============================================
-- 2. TABLA CLIENTES
-- ============================================

CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    cedula VARCHAR(10) NOT NULL,
    telefono VARCHAR(10) NOT NULL,
    placa VARCHAR(8) NOT NULL
);


-- ============================================
-- 3. TABLA PROVEEDORES
-- ============================================

CREATE TABLE IF NOT EXISTS proveedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    servicio VARCHAR(100) NOT NULL,
    telefono VARCHAR(10) NOT NULL
);


-- ============================================
-- 4. TABLA FACTURACION
-- ============================================

CREATE TABLE IF NOT EXISTS facturacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(10) NOT NULL,
    id_cliente INT NOT NULL,
    id_producto INT NOT NULL,
    placa VARCHAR(8) NOT NULL,
    servicio VARCHAR(100) NOT NULL,
    horas INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_facturacion_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id),

    CONSTRAINT fk_facturacion_producto
        FOREIGN KEY (id_producto)
        REFERENCES productos(id)
);

-- ============================================
-- 5. TABLA USUARIOS
-- ============================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);