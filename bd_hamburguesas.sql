-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 10-12-2025 a las 02:08:27
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bd_hamburguesas`
--
CREATE DATABASE IF NOT EXISTS `bd_hamburguesas` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `bd_hamburguesas`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_venta`
--

CREATE TABLE `detalle_venta` (
  `id_detalle` int(6) NOT NULL,
  `id_venta` int(5) NOT NULL,
  `id_menu` int(5) NOT NULL,
  `cantidad` int(3) UNSIGNED NOT NULL,
  `subtotal` decimal(6,2) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_venta`
--

INSERT INTO `detalle_venta` (`id_detalle`, `id_venta`, `id_menu`, `cantidad`, `subtotal`) VALUES
(2, 52, 1, 2, 180.00),
(3, 52, 4, 1, 25.00),
(4, 52, 6, 2, 40.00),
(5, 53, 3, 1, 55.00),
(6, 54, 1, 3, 270.00),
(7, 54, 5, 2, 50.00),
(8, 55, 2, 2, 120.00),
(13, 57, 2, 1, 60.00),
(14, 57, 5, 1, 25.00),
(15, 57, 7, 1, 3.00),
(16, 58, 2, 2, 120.00),
(17, 58, 5, 1, 25.00),
(18, 58, 7, 1, 3.00),
(19, 59, 2, 1, 60.00),
(20, 60, 4, 1, 25.00),
(21, 60, 6, 1, 20.00),
(22, 61, 1, 3, 270.00),
(23, 61, 2, 1, 60.00),
(24, 61, 6, 1, 20.00),
(25, 62, 1, 2, 180.00),
(26, 63, 4, 2, 50.00),
(27, 63, 6, 1, 20.00),
(28, 64, 2, 3, 180.00),
(29, 64, 5, 1, 25.00),
(30, 64, 7, 1, 3.00),
(31, 65, 3, 2, 110.00),
(32, 65, 5, 1, 25.00),
(33, 66, 1, 3, 270.00),
(34, 66, 5, 1, 25.00),
(35, 66, 7, 1, 3.00),
(36, 67, 3, 1, 55.00),
(37, 67, 5, 1, 25.00),
(38, 68, 1, 2, 180.00),
(39, 68, 7, 3, 9.00),
(40, 69, 4, 1, 25.00),
(41, 70, 3, 2, 110.00),
(42, 71, 3, 3, 165.00),
(43, 72, 2, 1, 60.00),
(44, 72, 5, 1, 25.00),
(45, 72, 7, 3, 9.00),
(46, 73, 1, 2, 180.00),
(47, 73, 2, 1, 60.00),
(48, 74, 3, 1, 55.00),
(49, 75, 1, 3, 270.00),
(50, 75, 6, 2, 40.00),
(51, 76, 2, 2, 120.00),
(52, 76, 7, 1, 3.00),
(53, 77, 1, 3, 270.00),
(54, 77, 7, 3, 9.00),
(55, 78, 4, 3, 75.00),
(56, 79, 1, 2, 180.00),
(57, 79, 7, 5, 15.00),
(58, 80, 6, 2, 40.00),
(59, 81, 3, 2, 110.00),
(60, 81, 5, 1, 25.00),
(61, 81, 7, 3, 9.00),
(62, 82, 1, 3, 270.00),
(63, 82, 3, 1, 55.00),
(64, 83, 2, 1, 60.00),
(65, 83, 6, 2, 40.00),
(66, 84, 1, 2, 180.00),
(67, 84, 6, 2, 40.00),
(68, 85, 2, 1, 60.00),
(69, 85, 7, 1, 3.00),
(70, 86, 1, 3, 270.00),
(71, 86, 6, 1, 20.00),
(72, 87, 3, 2, 110.00),
(73, 87, 7, 1, 3.00),
(74, 88, 1, 2, 180.00),
(75, 88, 2, 1, 60.00),
(76, 88, 6, 1, 20.00),
(77, 89, 2, 1, 60.00),
(78, 89, 5, 1, 25.00),
(79, 90, 1, 2, 180.00),
(80, 90, 5, 1, 25.00),
(81, 91, 4, 2, 50.00),
(82, 92, 3, 2, 110.00),
(83, 92, 5, 1, 25.00),
(84, 92, 6, 1, 20.00),
(85, 93, 1, 3, 270.00),
(86, 93, 2, 1, 60.00),
(87, 93, 7, 1, 3.00),
(88, 94, 2, 1, 60.00),
(89, 94, 5, 1, 25.00),
(90, 94, 6, 1, 20.00),
(91, 95, 1, 2, 180.00),
(92, 95, 4, 2, 50.00),
(93, 96, 4, 2, 50.00),
(94, 96, 6, 1, 20.00),
(95, 97, 1, 3, 270.00),
(96, 97, 5, 1, 25.00),
(97, 97, 7, 3, 9.00),
(98, 98, 2, 2, 120.00),
(99, 98, 7, 3, 9.00),
(100, 99, 1, 3, 270.00),
(101, 100, 2, 1, 60.00),
(102, 100, 5, 1, 25.00),
(103, 100, 7, 1, 3.00),
(104, 101, 1, 2, 180.00),
(105, 101, 5, 1, 25.00),
(106, 101, 7, 3, 9.00),
(107, 102, 2, 1, 60.00),
(108, 103, 3, 3, 165.00),
(109, 103, 7, 1, 3.00),
(110, 104, 1, 3, 270.00),
(111, 104, 2, 1, 60.00),
(112, 104, 7, 3, 9.00),
(113, 105, 3, 2, 110.00),
(114, 106, 1, 2, 180.00),
(115, 106, 2, 1, 60.00),
(116, 106, 7, 1, 3.00),
(117, 107, 4, 3, 75.00),
(118, 108, 1, 3, 270.00),
(119, 108, 5, 1, 25.00),
(120, 108, 6, 1, 20.00),
(121, 109, 2, 2, 120.00),
(122, 109, 6, 1, 20.00),
(123, 110, 1, 3, 270.00),
(124, 110, 7, 5, 15.00),
(125, 111, 3, 1, 55.00),
(126, 111, 5, 1, 25.00),
(127, 111, 7, 5, 15.00),
(128, 112, 1, 2, 180.00),
(129, 112, 4, 1, 25.00),
(130, 112, 6, 1, 20.00),
(131, 113, 3, 1, 55.00),
(132, 114, 2, 2, 120.00),
(133, 114, 3, 1, 55.00),
(134, 115, 1, 3, 270.00),
(135, 115, 2, 1, 60.00),
(136, 115, 6, 1, 20.00),
(137, 116, 3, 2, 110.00),
(138, 116, 7, 1, 3.00),
(139, 117, 1, 2, 180.00),
(140, 117, 2, 1, 60.00),
(141, 117, 7, 3, 9.00),
(142, 118, 2, 1, 60.00),
(143, 118, 6, 1, 20.00),
(144, 119, 1, 3, 270.00),
(145, 119, 4, 2, 50.00),
(146, 120, 2, 2, 120.00),
(147, 120, 5, 1, 25.00),
(148, 121, 1, 3, 270.00),
(149, 121, 6, 1, 20.00),
(150, 122, 3, 1, 55.00),
(151, 122, 5, 1, 25.00),
(152, 122, 6, 1, 20.00),
(153, 123, 1, 2, 180.00),
(154, 123, 3, 1, 55.00),
(155, 124, 4, 2, 50.00),
(156, 124, 7, 5, 15.00),
(157, 125, 2, 3, 180.00),
(158, 125, 7, 1, 3.00),
(159, 126, 1, 4, 360.00),
(160, 127, 2, 2, 120.00),
(163, 129, 3, 1, 55.00),
(164, 129, 5, 1, 25.00),
(165, 129, 7, 1, 3.00),
(192, 141, 3, 2, 110.00),
(193, 141, 6, 1, 20.00),
(194, 142, 1, 1, 90.00),
(195, 143, 4, 4, 100.00),
(196, 143, 5, 2, 50.00),
(197, 144, 2, 2, 120.00),
(198, 145, 1, 3, 270.00),
(199, 145, 4, 2, 50.00),
(200, 142, 2, 3, 180.00),
(201, 142, 3, 1, 55.00),
(202, 142, 6, 1, 20.00),
(203, 146, 2, 2, 120.00),
(204, 146, 3, 2, 110.00),
(205, 146, 6, 1, 20.00),
(206, 58, 1, 2, 180.00),
(207, 58, 4, 1, 25.00),
(208, 148, 1, 2, 180.00),
(209, 149, 1, 2, 180.00),
(210, 149, 5, 1, 25.00),
(211, 153, 1, 2, 180.00),
(212, 153, 2, 1, 60.00),
(213, 154, 2, 2, 120.00),
(214, 154, 5, 1, 25.00),
(215, 156, 1, 1, 90.00),
(216, 156, 6, 1, 20.00),
(217, 157, 1, 2, 180.00),
(218, 158, 6, 1, 20.00),
(219, 159, 5, 1, 25.00),
(220, 159, 2, 2, 120.00),
(221, 160, 1, 2, 180.00),
(222, 160, 4, 3, 75.00),
(223, 161, 1, 7, 630.00),
(224, 161, 3, 3, 165.00),
(225, 161, 5, 5, 125.00),
(226, 162, 3, 3, 165.00),
(227, 162, 4, 2, 50.00),
(228, 162, 7, 4, 12.00),
(229, 163, 1, 3, 270.00),
(230, 163, 2, 1, 60.00),
(231, 164, 1, 2, 180.00),
(232, 164, 6, 2, 40.00),
(233, 164, 7, 1, 3.00),
(234, 165, 1, 11, 990.00),
(235, 166, 3, 2, 110.00),
(236, 167, 1, 2, 180.00),
(237, 168, 1, 4, 360.00),
(238, 168, 6, 1, 20.00),
(239, 169, 1, 4, 360.00),
(240, 169, 2, 5, 300.00),
(241, 169, 4, 3, 75.00),
(242, 59, 4, 4, 100.00),
(245, 169, 6, 2, 40.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ingredientes`
--

CREATE TABLE `ingredientes` (
  `id_producto` int(5) NOT NULL,
  `nombre` text NOT NULL,
  `descripcion` text NOT NULL,
  `cantidad` decimal(5,2) UNSIGNED NOT NULL,
  `unidad` text NOT NULL,
  `precio` decimal(6,2) UNSIGNED NOT NULL,
  `fecha_caducidad` date NOT NULL,
  `id_proveedor` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ingredientes`
--

INSERT INTO `ingredientes` (`id_producto`, `nombre`, `descripcion`, `cantidad`, `unidad`, `precio`, `fecha_caducidad`, `id_proveedor`) VALUES
(7, 'leshuga', 'nose w', 12.00, 'piezas', 12.00, '2025-11-30', 4),
(8, 'Pan hamburguesa', 'pan', 10.00, 'piezas', 200.00, '2025-12-17', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_menu` int(5) NOT NULL,
  `nombre` text NOT NULL,
  `precio` decimal(5,2) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_menu`, `nombre`, `precio`) VALUES
(1, 'Hamburguesa doble', 90.00),
(2, 'Hamburguesa especial', 60.00),
(3, 'Hamburguesa sencilla', 55.00),
(4, 'Hot dog', 25.00),
(5, 'Refresco ', 25.00),
(6, 'Agua', 20.00),
(7, 'Ingrediente extra', 3.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `id_proveedor` int(5) NOT NULL,
  `nombre_empresa` text NOT NULL,
  `nombre_contacto` text NOT NULL COMMENT 'Nombre del contacto',
  `telefono` varchar(15) NOT NULL,
  `direccion` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id_proveedor`, `nombre_empresa`, `nombre_contacto`, `telefono`, `direccion`) VALUES
(1, 'Bimbo', 'via wasap', '738193123', 'Colombia'),
(4, 'Empresa', 'juan', '8', '909i');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(2) NOT NULL,
  `nombre` text NOT NULL,
  `apellido_paterno` text NOT NULL,
  `apellido_materno` text NOT NULL,
  `correo` varchar(30) NOT NULL,
  `password` char(64) NOT NULL,
  `fecha_registro` datetime NOT NULL DEFAULT current_timestamp(),
  `Rol` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `apellido_paterno`, `apellido_materno`, `correo`, `password`, `fecha_registro`, `Rol`) VALUES
(11, 'Adrián', 'Rangel', 'Vázquez', 'adrian@gmail.com', '55a9f4f8994b1bbf2058ea38c8efb6c459000814d5f39c087002571639e6230e', '2025-11-30 20:46:31', 'Admin'),
(12, 'Pablo', 'Pablito', 'Pablez', 'pablo@gmail.com', '55a9f4f8994b1bbf2058ea38c8efb6c459000814d5f39c087002571639e6230e', '2025-11-30 20:47:28', 'Colaborador'),
(13, 'ola', 'ola', 'ola', 'ola', '55a9f4f8994b1bbf2058ea38c8efb6c459000814d5f39c087002571639e6230e', '2025-11-30 20:48:31', 'Admin');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `id_venta` int(5) NOT NULL,
  `fecha_venta` date NOT NULL DEFAULT current_timestamp(),
  `hora_venta` time NOT NULL,
  `total_venta` decimal(6,2) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`id_venta`, `fecha_venta`, `hora_venta`, `total_venta`) VALUES
(52, '2025-09-16', '20:15:00', 245.00),
(53, '2025-09-16', '21:45:00', 55.00),
(54, '2025-09-17', '19:10:00', 320.00),
(55, '2025-09-18', '22:00:00', 120.00),
(57, '2025-09-20', '21:15:00', 90.00),
(58, '2025-09-21', '19:45:00', 353.00),
(59, '2025-09-22', '20:00:00', 160.00),
(60, '2025-09-23', '23:10:00', 45.00),
(61, '2025-09-24', '19:20:00', 350.00),
(62, '2025-09-25', '21:00:00', 180.00),
(63, '2025-09-26', '22:30:00', 70.00),
(64, '2025-09-27', '20:45:00', 210.00),
(65, '2025-09-28', '19:50:00', 135.00),
(66, '2025-09-29', '21:20:00', 300.00),
(67, '2025-09-30', '20:10:00', 80.00),
(68, '2025-10-01', '19:05:00', 190.00),
(69, '2025-10-02', '22:15:00', 25.00),
(70, '2025-10-03', '23:00:00', 110.00),
(71, '2025-10-04', '20:25:00', 165.00),
(72, '2025-10-05', '21:40:00', 95.00),
(73, '2025-10-06', '19:35:00', 240.00),
(74, '2025-10-07', '20:50:00', 55.00),
(75, '2025-10-08', '22:45:00', 310.00),
(76, '2025-10-09', '19:15:00', 125.00),
(77, '2025-10-10', '21:10:00', 280.00),
(78, '2025-10-11', '20:40:00', 75.00),
(79, '2025-10-12', '19:55:00', 195.00),
(80, '2025-10-13', '22:20:00', 40.00),
(81, '2025-10-14', '23:30:00', 145.00),
(82, '2025-10-15', '20:05:00', 325.00),
(83, '2025-10-16', '21:35:00', 100.00),
(84, '2025-10-17', '19:25:00', 220.00),
(85, '2025-10-18', '20:55:00', 65.00),
(86, '2025-10-19', '22:50:00', 290.00),
(87, '2025-10-20', '19:40:00', 115.00),
(88, '2025-10-21', '21:05:00', 260.00),
(89, '2025-10-22', '20:35:00', 85.00),
(90, '2025-10-23', '19:10:00', 205.00),
(91, '2025-10-24', '22:00:00', 50.00),
(92, '2025-10-25', '23:15:00', 155.00),
(93, '2025-10-26', '20:15:00', 335.00),
(94, '2025-10-27', '21:45:00', 105.00),
(95, '2025-10-28', '19:30:00', 230.00),
(96, '2025-10-29', '20:45:00', 70.00),
(97, '2025-10-30', '22:30:00', 305.00),
(98, '2025-10-31', '19:50:00', 130.00),
(99, '2025-11-01', '21:20:00', 270.00),
(100, '2025-11-02', '20:25:00', 90.00),
(101, '2025-11-03', '19:05:00', 215.00),
(102, '2025-11-04', '22:15:00', 60.00),
(103, '2025-11-05', '23:00:00', 170.00),
(104, '2025-11-06', '20:40:00', 340.00),
(105, '2025-11-07', '21:55:00', 110.00),
(106, '2025-11-08', '19:20:00', 245.00),
(107, '2025-11-09', '20:30:00', 75.00),
(108, '2025-11-10', '22:45:00', 315.00),
(109, '2025-11-11', '19:45:00', 140.00),
(110, '2025-11-12', '21:10:00', 285.00),
(111, '2025-11-13', '20:15:00', 95.00),
(112, '2025-11-14', '19:35:00', 225.00),
(113, '2025-11-15', '22:20:00', 55.00),
(114, '2025-11-16', '23:30:00', 175.00),
(115, '2025-11-17', '20:55:00', 350.00),
(116, '2025-11-18', '21:30:00', 115.00),
(117, '2025-11-19', '19:10:00', 250.00),
(118, '2025-11-19', '20:45:00', 80.00),
(119, '2025-11-20', '22:00:00', 320.00),
(120, '2025-11-20', '19:50:00', 145.00),
(121, '2025-11-21', '21:25:00', 290.00),
(122, '2025-11-21', '20:35:00', 100.00),
(123, '2025-11-21', '19:15:00', 235.00),
(124, '2025-11-22', '22:30:00', 65.00),
(125, '2025-11-22', '23:15:00', 185.00),
(126, '2025-11-22', '20:20:00', 360.00),
(127, '2025-11-22', '21:40:00', 120.00),
(129, '2025-11-23', '20:50:00', 85.00),
(141, '2025-11-23', '19:00:00', 130.00),
(142, '2025-11-23', '19:00:00', 345.00),
(143, '2025-11-23', '19:00:00', 150.00),
(144, '2025-11-23', '19:00:00', 120.00),
(145, '2025-11-21', '22:16:00', 320.00),
(146, '2025-11-23', '21:20:00', 250.00),
(147, '2025-11-24', '19:00:00', 55.00),
(148, '2025-11-24', '19:04:00', 180.00),
(149, '2025-11-24', '21:34:00', 205.00),
(153, '2025-11-24', '19:12:00', 240.00),
(154, '2025-11-24', '19:00:00', 145.00),
(156, '2025-11-24', '19:11:00', 110.00),
(157, '2025-11-24', '19:00:00', 180.00),
(158, '2025-11-24', '19:00:00', 20.00),
(159, '2025-11-24', '19:00:00', 145.00),
(160, '2025-11-25', '19:00:00', 255.00),
(161, '2025-11-25', '19:00:00', 920.00),
(162, '2025-11-25', '19:00:00', 227.00),
(163, '2025-11-26', '19:00:00', 330.00),
(164, '2025-11-26', '19:00:00', 223.00),
(165, '2025-11-27', '19:00:00', 990.00),
(166, '2025-11-27', '19:00:00', 110.00),
(167, '2025-11-29', '19:00:00', 180.00),
(168, '2025-11-30', '19:00:00', 380.00),
(169, '2025-12-12', '19:06:00', 775.00);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `id_venta` (`id_venta`),
  ADD KEY `id_producto` (`id_menu`);

--
-- Indices de la tabla `ingredientes`
--
ALTER TABLE `ingredientes`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `id_proveedor` (`id_proveedor`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_menu`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id_proveedor`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id_venta`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  MODIFY `id_detalle` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=248;

--
-- AUTO_INCREMENT de la tabla `ingredientes`
--
ALTER TABLE `ingredientes`
  MODIFY `id_producto` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_menu` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `id_proveedor` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id_venta` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=172;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD CONSTRAINT `detalle_venta_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`),
  ADD CONSTRAINT `detalle_venta_ibfk_2` FOREIGN KEY (`id_menu`) REFERENCES `productos` (`id_menu`);

--
-- Filtros para la tabla `ingredientes`
--
ALTER TABLE `ingredientes`
  ADD CONSTRAINT `ingredientes_ibfk_1` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
