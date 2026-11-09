-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 09, 2026 at 03:23 AM
-- Server version: 8.4.3
-- PHP Version: 8.3.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pizzeria_julia`
--

-- --------------------------------------------------------

--
-- Table structure for table `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `telefono` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `nombre`, `direccion`, `telefono`) VALUES
(6, 'Julia', 'Real de tijuana', '4771234567');

-- --------------------------------------------------------

--
-- Table structure for table `detalle_pedido`
--

CREATE TABLE `detalle_pedido` (
  `id_detalle` int NOT NULL,
  `id_pedido` int NOT NULL,
  `tamano` varchar(50) NOT NULL,
  `ingredientes` varchar(200) NOT NULL,
  `num_pizzas` int NOT NULL,
  `subtotal` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `detalle_pedido`
--

INSERT INTO `detalle_pedido` (`id_detalle`, `id_pedido`, `tamano`, `ingredientes`, `num_pizzas`, `subtotal`) VALUES
(11, 7, 'Mediana', 'Piña, Jamón', 3, 300.00),
(12, 7, 'Grande', 'Champiñones', 1, 130.00);

-- --------------------------------------------------------

--
-- Table structure for table `detalle_temporal`
--

CREATE TABLE `detalle_temporal` (
  `id_temporal` int NOT NULL,
  `tamano` varchar(50) NOT NULL,
  `ingredientes` varchar(200) NOT NULL,
  `num_pizzas` int NOT NULL,
  `subtotal` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pedido`
--

CREATE TABLE `pedido` (
  `id_pedido` int NOT NULL,
  `id_cliente` int NOT NULL,
  `fecha_pedido` date NOT NULL,
  `total_pedido` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `pedido`
--

INSERT INTO `pedido` (`id_pedido`, `id_cliente`, `fecha_pedido`, `total_pedido`) VALUES
(7, 6, '2026-11-09', 430.00);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`);

--
-- Indexes for table `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `id_pedido` (`id_pedido`);

--
-- Indexes for table `detalle_temporal`
--
ALTER TABLE `detalle_temporal`
  ADD PRIMARY KEY (`id_temporal`);

--
-- Indexes for table `pedido`
--
ALTER TABLE `pedido`
  ADD PRIMARY KEY (`id_pedido`),
  ADD KEY `pedido_ibfk_1` (`id_cliente`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  MODIFY `id_detalle` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `detalle_temporal`
--
ALTER TABLE `detalle_temporal`
  MODIFY `id_temporal` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `pedido`
--
ALTER TABLE `pedido`
  MODIFY `id_pedido` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD CONSTRAINT `detalle_pedido_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`);

--
-- Constraints for table `pedido`
--
ALTER TABLE `pedido`
  ADD CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
