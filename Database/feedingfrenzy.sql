-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th6 01, 2025 lúc 10:56 AM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `feedingfrenzy`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `lichsudau`
--

CREATE TABLE `lichsudau` (
  `name` varchar(255) NOT NULL,
  `level` int(255) NOT NULL,
  `score` int(255) NOT NULL,
  `time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `lichsudau`
--

INSERT INTO `lichsudau` (`name`, `level`, `score`, `time`) VALUES
('Player', 8, 1244, '01:28'),
('Player', 3, 90, '00:11'),
('Player', 4, 375, '00:26'),
('Player', 2, 0, '00:02'),
('Player', 2, 60, '00:12'),
('Player', 5, 1658, '01:41'),
('Player', 12, 1095, '01:44'),
('Player', 10, 0, '00:01'),
('Player', 7, 2407, '01:26'),
('Player', 1, 60, '00:11'),
('Player', 1, 30, '00:06'),
('Player', 2, 300, '00:42'),
('Player', 5, 1065, '02:44'),
('Player', 3, 405, '01:04'),
('Player', 1, 15, '00:13'),
('Player', 1, 75, '00:26'),
('Player', 1, 15, '00:30'),
('Player', 1, 30, '00:14'),
('Player', 1, 15, '00:14'),
('Player', 1, 0, '00:09');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
