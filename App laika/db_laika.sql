-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 14-03-2025 a las 02:21:51
-- Versión del servidor: 10.4.27-MariaDB
-- Versión de PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `db_laika`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asesor`
--

CREATE TABLE `asesor` (
  `idf_cliente` varchar(30) NOT NULL,
  `idf_empleado` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `nombre_categoria` varchar(20) NOT NULL,
  `nombre_sucursal` varchar(50) DEFAULT NULL,
  `presupuesto` decimal(20,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`nombre_categoria`, `nombre_sucursal`, `presupuesto`) VALUES
('Accesorios', NULL, NULL),
('Gatos', NULL, NULL),
('Juguetes', NULL, NULL),
('Perros', NULL, NULL),
('Snacks', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` varchar(30) NOT NULL,
  `nombre_cliente` varchar(50) NOT NULL,
  `nombre_categoria` varchar(20) DEFAULT NULL,
  `estado` enum('Activo','Inactivo') NOT NULL DEFAULT 'Activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `nombre_cliente`, `nombre_categoria`, `estado`) VALUES
('10000001', 'Ana García Pérez', 'Accesorios', 'Inactivo'),
('10000002', 'Juan Rodríguez López', 'Accesorios', 'Activo'),
('10000003', 'Sofía Martínez Sánchez', 'Gatos', 'Activo'),
('10000004', 'Pablo Hernández Díaz', 'Gatos', 'Inactivo'),
('10000005', 'Laura Ramírez García', 'Juguetes', 'Activo'),
('10000006', 'Pedro López Fernández', 'Juguetes', 'Activo'),
('10000007', ' Julia Fernández  González', 'Perros', 'Activo'),
('10000008', 'Manuel Torres Romero', 'Perros', 'Inactivo'),
('10000009', 'Camila Sánchez Pérez', 'Snacks', 'Activo'),
('10000010', ' Andrés Álvarez Díaz', 'Snacks', 'Activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleados`
--

CREATE TABLE `empleados` (
  `id_empleado` varchar(30) NOT NULL,
  `nombre_empleado` varchar(50) NOT NULL,
  `nombre_categoria` varchar(20) DEFAULT NULL,
  `salario` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empleados`
--

INSERT INTO `empleados` (`id_empleado`, `nombre_empleado`, `nombre_categoria`, `salario`) VALUES
('1001', 'Ana Sánchez', 'Accesorios', '35.00'),
('1002', 'Lucía Pérez', 'Accesorios', '28.00'),
('1003', 'Javier Gómez', 'Gatos', '50.00'),
('1004', 'María López', 'Gatos', '37.80'),
('1005', 'Pedro Torres', 'Juguetes', '45.20'),
('1006', 'Sofía Díaz', 'Juguetes', '32.50'),
('1007', 'Miguel Fernández', 'Perros', '55.00'),
('1008', 'Isabel Ruiz', 'Perros', '40.00'),
('1009', 'José Herrera', 'Snacks', '48.30'),
('1010', 'Saireth Tovar', 'Snacks', '38.00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lineaproductos`
--

CREATE TABLE `lineaproductos` (
  `id_producto` varchar(30) NOT NULL,
  `sec_id` varchar(8) NOT NULL,
  `forma_pago` varchar(20) NOT NULL,
  `coleccion` decimal(4,0) NOT NULL,
  `nombre_sucursal` varchar(15) DEFAULT NULL,
  `numero_sala` varchar(7) DEFAULT NULL,
  `id_seccionhe` varchar(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id_cliente` varchar(30) NOT NULL,
  `id_producto` varchar(30) NOT NULL,
  `sec_id` varchar(8) NOT NULL,
  `forma_pago` varchar(20) NOT NULL,
  `coleccion` decimal(4,0) NOT NULL,
  `estado_pedido` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` varchar(30) NOT NULL,
  `descripcion` varchar(50) DEFAULT NULL,
  `nombre_categoria` varchar(20) DEFAULT NULL,
  `precio` decimal(50,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `descripcion`, `nombre_categoria`, `precio`) VALUES
('ARP-002', ' Arnés ajustable para perros, ideal para paseos.', 'Accesorios', '30000'),
('Gato-001', 'Pro plan pollo', 'Gatos', '15000'),
('Gato-002', 'Croquetas de atún que son ideales para gatos.', 'Gatos', '16000'),
('Jug-001', 'peluche en forma de hamburguesa', 'Juguetes', '25000'),
('Jug-002', 'Un juguete de goma resistente.', 'Juguetes', '22000'),
('Perro-001', 'Dog Chow Adulto', 'Perros', '20000'),
('Perro-002', 'Still Hills Croquetas cachorro', 'Perros', '18000'),
('RGC-005', 'Rascador de cartón reciclado.', 'Accesorios', '27000'),
('SNP-001', 'Deliciosas galletitas para perros.', 'Snacks', '14500'),
('SNP-002', 'Barras de proteínas para gatos con sabor a atún.', 'Snacks', '11500');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `id_producto` varchar(30) NOT NULL,
  `id_proveedor` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `seccionhe`
--

CREATE TABLE `seccionhe` (
  `id_seccionhe` varchar(4) NOT NULL,
  `dia` varchar(1) NOT NULL,
  `inicio_he` time NOT NULL,
  `fin_he` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `seccionhe`
--

INSERT INTO `seccionhe` (`id_seccionhe`, `dia`, `inicio_he`, `fin_he`) VALUES
('A', 'F', '08:00:00', '08:50:00'),
('A', 'M', '08:00:00', '08:50:00'),
('A', 'W', '08:00:00', '08:50:00'),
('B', 'F', '09:00:00', '09:50:00'),
('B', 'M', '09:00:00', '09:50:00'),
('B', 'W', '09:00:00', '09:50:00'),
('C', 'F', '11:00:00', '11:50:00'),
('C', 'M', '11:00:00', '11:50:00'),
('C', 'W', '11:00:00', '11:50:00'),
('D', 'F', '13:00:00', '13:50:00'),
('D', 'M', '13:00:00', '13:50:00'),
('D', 'W', '13:00:00', '13:50:00'),
('E', 'R', '10:30:00', '11:45:00'),
('E', 'T', '10:30:00', '11:45:00'),
('F', 'R', '14:30:00', '15:45:00'),
('F', 'T', '14:30:00', '15:45:00'),
('G', 'F', '16:00:00', '16:50:00'),
('G', 'M', '16:00:00', '16:50:00'),
('G', 'W', '16:00:00', '16:50:00'),
('H', 'W', '10:00:00', '12:30:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sucursales`
--

CREATE TABLE `sucursales` (
  `nombre_sucursal` varchar(15) NOT NULL,
  `numero_sala` varchar(7) NOT NULL,
  `capacidad` decimal(4,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sucursales`
--

INSERT INTO `sucursales` (`nombre_sucursal`, `numero_sala`, `capacidad`) VALUES
('Guacarí', '2', '149'),
('Viva Sincelejo', '1', '109');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(10) NOT NULL,
  `rol` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `email`, `password`, `rol`) VALUES
(3, 'root@gmail.com', 'root', 'admin'),
(4, '12345', '12345', 'clientes'),
(6, 'jesus@gmail.com', '123456', 'clientes'),
(7, '23121', '23121', 'clientes'),
(8, '44553', '44553', 'clientes'),
(9, '45678', '45678', 'clientes'),
(10, '54321', '54321', 'clientes'),
(11, '55739', '55739', 'clientes'),
(13, '76543', '76543', 'clientes'),
(14, '76653', '76653', 'clientes'),
(15, '98765', '98765', 'clientes'),
(16, '98988', '98988', 'clientes'),
(17, '1131', '1131', 'clientes'),
(21, 'dev@gmail.com', '7777', 'admin'),
(22, 'admin@gmail.com', 'admin', 'admin'),
(26, '2468', '2468', 'clientes'),
(29, '102654273', '102654273', 'clientes'),
(30, '12345678', '12345678', 'clientes'),
(31, '133423423', '133423423', 'clientes'),
(32, '10000001', '10000001', 'clientes'),
(33, '10000002', '10000002', 'clientes'),
(34, '10000003', '10000003', 'clientes'),
(35, '10000004', '10000004', 'clientes'),
(36, '10000005', '10000005', 'clientes'),
(37, '10000006', '10000006', 'clientes'),
(38, '10000007', '10000007', 'clientes'),
(39, '10000008', '10000008', 'clientes'),
(40, '10000009', '10000009', 'clientes'),
(41, '10000010', '10000010', 'clientes');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `id_venta` varchar(30) NOT NULL,
  `id_producto` varchar(30) NOT NULL,
  `sec_id` varchar(8) NOT NULL,
  `forma_pago` varchar(20) NOT NULL,
  `coleccion` decimal(4,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `asesor`
--
ALTER TABLE `asesor`
  ADD PRIMARY KEY (`idf_cliente`),
  ADD KEY `idf_empleado` (`idf_empleado`);

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`nombre_categoria`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`),
  ADD KEY `nombre_categoria` (`nombre_categoria`) USING BTREE;

--
-- Indices de la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD PRIMARY KEY (`id_empleado`),
  ADD KEY `dept_name_inst` (`nombre_categoria`);

--
-- Indices de la tabla `lineaproductos`
--
ALTER TABLE `lineaproductos`
  ADD PRIMARY KEY (`id_producto`,`sec_id`,`forma_pago`,`coleccion`),
  ADD KEY `nombre_sucursal` (`nombre_sucursal`,`numero_sala`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id_cliente`,`id_producto`,`sec_id`,`forma_pago`,`coleccion`),
  ADD KEY `id_producto` (`id_producto`,`sec_id`,`forma_pago`,`coleccion`) USING BTREE;

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `nombre_categoria` (`nombre_categoria`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id_producto`,`id_proveedor`),
  ADD KEY `prereq_id` (`id_proveedor`);

--
-- Indices de la tabla `seccionhe`
--
ALTER TABLE `seccionhe`
  ADD PRIMARY KEY (`id_seccionhe`,`dia`,`inicio_he`);

--
-- Indices de la tabla `sucursales`
--
ALTER TABLE `sucursales`
  ADD PRIMARY KEY (`nombre_sucursal`,`numero_sala`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`) USING BTREE;

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id_venta`,`id_producto`,`sec_id`,`forma_pago`,`coleccion`),
  ADD KEY `id_producto` (`id_producto`,`sec_id`,`forma_pago`,`coleccion`) USING BTREE;

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asesor`
--
ALTER TABLE `asesor`
  ADD CONSTRAINT `asesor_ibfk_1` FOREIGN KEY (`idf_empleado`) REFERENCES `empleados` (`id_empleado`) ON DELETE SET NULL,
  ADD CONSTRAINT `asesor_ibfk_2` FOREIGN KEY (`idf_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE;

--
-- Filtros para la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`nombre_categoria`) REFERENCES `categorias` (`nombre_categoria`) ON DELETE SET NULL;

--
-- Filtros para la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD CONSTRAINT `dept_name_inst` FOREIGN KEY (`nombre_categoria`) REFERENCES `categorias` (`nombre_categoria`) ON DELETE SET NULL;

--
-- Filtros para la tabla `lineaproductos`
--
ALTER TABLE `lineaproductos`
  ADD CONSTRAINT `lineaproductos_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE,
  ADD CONSTRAINT `lineaproductos_ibfk_2` FOREIGN KEY (`nombre_sucursal`,`numero_sala`) REFERENCES `sucursales` (`nombre_sucursal`, `numero_sala`) ON DELETE SET NULL;

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_producto`,`sec_id`,`forma_pago`,`coleccion`) REFERENCES `lineaproductos` (`id_producto`, `sec_id`, `forma_pago`, `coleccion`) ON DELETE CASCADE,
  ADD CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE;

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `dept_name` FOREIGN KEY (`nombre_categoria`) REFERENCES `categorias` (`nombre_categoria`) ON DELETE SET NULL;

--
-- Filtros para la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD CONSTRAINT `proveedores_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE,
  ADD CONSTRAINT `proveedores_ibfk_2` FOREIGN KEY (`id_proveedor`) REFERENCES `productos` (`id_producto`);

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`id_producto`,`sec_id`,`forma_pago`,`coleccion`) REFERENCES `lineaproductos` (`id_producto`, `sec_id`, `forma_pago`, `coleccion`) ON DELETE CASCADE,
  ADD CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`id_venta`) REFERENCES `empleados` (`id_empleado`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
