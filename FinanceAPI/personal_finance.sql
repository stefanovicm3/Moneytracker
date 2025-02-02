-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 02, 2025 at 07:26 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `personal_finance`
--

-- --------------------------------------------------------

--
-- Table structure for table `budzeti`
--

CREATE TABLE `budzeti` (
  `id` int(11) NOT NULL,
  `korisnik_id` int(11) NOT NULL,
  `kategorija` enum('Hrana','Transport','Računi','Štednja','Zabava','Oprema','Putovanja','Zdravlje','Obrazovanje','Pokloni','Ostalo') NOT NULL,
  `iznos` int(11) DEFAULT NULL,
  `mesec` enum('Januar','Februar','Mart','April','Maj','Jun','Jul','Avgust','Septembar','Oktobar','Novembar','Decembar') NOT NULL,
  `godina` year(4) NOT NULL,
  `budzet_id` int(11) DEFAULT NULL,
  `ukupna_potrosnja` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `budzeti`
--

INSERT INTO `budzeti` (`id`, `korisnik_id`, `kategorija`, `iznos`, `mesec`, `godina`, `budzet_id`, `ukupna_potrosnja`) VALUES
(4, 1, 'Hrana', 250, 'Januar', '2025', NULL, 0),
(5, 1, 'Transport', 100, 'Januar', '2025', NULL, 0),
(16, 1, 'Hrana', 250, 'Januar', '2025', NULL, 0),
(17, 1, 'Transport', 100, 'Januar', '2025', NULL, 0),
(18, 1, 'Zdravlje', 150, 'Februar', '2025', NULL, 0),
(19, 1, 'Obrazovanje', 200, 'Mart', '2025', NULL, 0),
(48, 2, 'Pokloni', 9000, 'Februar', '2025', NULL, 19550),
(52, 2, 'Hrana', 14000, 'Mart', '2024', NULL, 31500),
(53, 2, 'Obrazovanje', 85000, 'Oktobar', '2025', NULL, 136234),
(58, 2, 'Hrana', 5595, 'Januar', '2025', NULL, 0),
(61, 6, 'Računi', 25000, 'Maj', '2025', NULL, 20000),
(68, 6, 'Zdravlje', 24000, 'Septembar', '2025', NULL, 15000),
(69, 2, 'Obrazovanje', 5000, 'Maj', '2025', NULL, 0),
(70, 2, 'Transport', 3000, 'April', '2025', NULL, 0),
(71, 2, 'Zdravlje', 8000, 'April', '2025', NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `korisnici`
--

CREATE TABLE `korisnici` (
  `id` int(11) NOT NULL,
  `naziv` varchar(255) DEFAULT NULL,
  `iznos` int(11) DEFAULT NULL,
  `type` enum('prihod','rashod') DEFAULT NULL,
  `datum` timestamp NOT NULL DEFAULT current_timestamp(),
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `korisnici`
--

INSERT INTO `korisnici` (`id`, `naziv`, `iznos`, `type`, `datum`, `user_id`) VALUES
(4, 'Namirnice', -4786, 'rashod', '2025-01-20 12:34:57', NULL),
(7, 'Plata za mesec decembar', 75000, 'prihod', '2025-01-20 12:43:02', NULL),
(9, 'Proba', 15000, 'prihod', '2025-01-20 12:58:46', NULL),
(11, 'Popravka automobila', -22000, 'rashod', '2025-01-20 13:18:26', NULL),
(12, 'Fashion and Friends', -9000, 'rashod', '2025-01-20 13:52:35', NULL),
(13, 'Proba', 100000, 'prihod', '2025-01-22 17:17:13', NULL),
(14, 'Dorucak', 100000, 'prihod', '2025-01-22 17:17:23', NULL),
(15, 'test', 100000, 'prihod', '2025-01-22 17:18:51', NULL),
(21, 'Rashodi', 5000, 'rashod', '2025-01-23 08:02:05', 2),
(22, 'Proba', 5000, 'rashod', '2025-01-23 08:02:29', 2),
(23, 'Plata', 52000, 'prihod', '2025-01-23 08:05:39', 2),
(25, 'Rashodi', 100000, 'rashod', '2025-01-23 08:28:56', 12),
(26, 'Proba', 120000, 'prihod', '2025-01-23 08:29:04', 12),
(27, 'Proba', 5000, 'prihod', '2025-01-30 09:11:25', 6),
(28, 'Test', 5000, 'prihod', '2025-01-30 09:11:36', 6),
(30, 'Proba', 5000, 'prihod', '2025-01-31 10:10:47', 6),
(37, 'Proba', 5000, 'rashod', '2025-01-31 21:20:58', 2),
(39, 'Proba', 5000, 'rashod', '2025-02-01 17:38:02', 6),
(40, 'Test', 5000, 'prihod', '2025-02-02 12:47:11', 14),
(42, 'test', 6000, 'prihod', '2025-02-02 13:54:50', 2);

-- --------------------------------------------------------

--
-- Table structure for table `potrosnja`
--

CREATE TABLE `potrosnja` (
  `id` int(11) NOT NULL,
  `budzet_id` int(11) DEFAULT NULL,
  `iznos` int(11) DEFAULT NULL,
  `korisnik_id` int(11) DEFAULT NULL,
  `kategorija` varchar(255) DEFAULT NULL,
  `mesec` varchar(20) DEFAULT NULL,
  `godina` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `potrosnja`
--

INSERT INTO `potrosnja` (`id`, `budzet_id`, `iznos`, `korisnik_id`, `kategorija`, `mesec`, `godina`) VALUES
(78, 53, 25000, 2, 'Obrazovanje', 'Mart', 2025),
(87, 53, 7000, 2, 'Transport', 'Jul', 2028),
(88, 52, 5000, 2, 'Hrana', 'April', 2025),
(89, 61, 20000, 6, 'Računi', 'April', 2025),
(90, 68, 5000, 6, 'Zdravlje', 'April', 2026),
(91, 68, 10000, 6, 'Zdravlje', 'Maj', 2027),
(92, 53, 5000, 2, 'Obrazovanje', 'Jun', 2025);

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `naziv` varchar(255) NOT NULL,
  `iznos` decimal(10,2) NOT NULL,
  `tip` enum('prihod','rashod') NOT NULL,
  `datum` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `naziv`, `iznos`, `tip`, `datum`) VALUES
(2, 'Dorucak', -5000.00, 'rashod', '2025-01-20 12:02:49');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `lozinka` varchar(255) NOT NULL,
  `datum_registracije` timestamp NOT NULL DEFAULT current_timestamp(),
  `ukupna_potrosnja` int(11) DEFAULT 0,
  `role` enum('user','admin') DEFAULT 'user',
  `reset_token` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `lozinka`, `datum_registracije`, `ukupna_potrosnja`, `role`, `reset_token`) VALUES
(1, 'user1@example.com', 'scrypt:32768:8:1$LML8jM2Tvh1dM4B9$b370a74bf36f02c5c77f05c0b82f87b4dbd7698a254b657a0873416ec0955b56e06c10581c4c831a63fcf712bef22b51f4ece51f8a88f357db1b73af54626e52', '2025-01-20 14:32:26', 0, 'user', NULL),
(2, 'user2@example.com', 'scrypt:32768:8:1$UTZUfNfg7Zwl24o5$d12c60b4126ed06c37fad813e0ffab644f5c116c1d2371293c81b983f332717dae1e1874d0c13aace03451f1a524d9afb0f6c57990b4d9eac6c1dfc8e552e866', '2025-01-20 14:32:26', 4086251, 'user', NULL),
(6, 'admin@example.com', 'scrypt:32768:8:1$m5b39AladrHgJGbU$a2a8a01f6ae412ffb8c736f56476bd66576a9207d824df1f490e41711ef57232422a4bb2a9086826ef048ed82b308be9ad604351823e959e028f674b7c5657c0', '2025-01-22 15:05:11', 35000, 'admin', NULL),
(12, 'user5@example.com', 'scrypt:32768:8:1$7yTNs2EsRqlwwg8C$206ee068b8a989fb602f74474fb1706651b3fca5bc366334a34ed0eaa175081123413e7b5d104c74548c63655807bf6fc5818e085601d9b570401ccb6547a20e', '2025-01-23 08:28:03', 0, 'user', NULL),
(14, 'vtsnis@example.com', 'pbkdf2:sha256:1000000$oJfYYwQLAwvJ271p$23dabdd5dc35085f806389618301e085c93b3c841886480c512e05b6bfb7c472', '2025-02-02 12:45:16', 0, 'user', NULL),
(15, 'novikorisnik@example.com', 'scrypt:32768:8:1$gVXGUHQ21cMDyJW4$40581e81fcc263fb732396d28c22d1bc417b9cf6932c61740602fa078ca01a36dccad4cf463f4a737b319397ff6ad7a6bc47a25e2bf03ecaa5f0947fbd504809', '2025-02-02 16:06:58', 0, 'user', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `budzeti`
--
ALTER TABLE `budzeti`
  ADD PRIMARY KEY (`id`),
  ADD KEY `budzeti_ibfk_1` (`korisnik_id`);

--
-- Indexes for table `korisnici`
--
ALTER TABLE `korisnici`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_korisnik` (`user_id`);

--
-- Indexes for table `potrosnja`
--
ALTER TABLE `potrosnja`
  ADD PRIMARY KEY (`id`),
  ADD KEY `potrosnja_ibfk_2` (`korisnik_id`),
  ADD KEY `potrosnja_ibfk_1` (`budzet_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `budzeti`
--
ALTER TABLE `budzeti`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=72;

--
-- AUTO_INCREMENT for table `korisnici`
--
ALTER TABLE `korisnici`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `potrosnja`
--
ALTER TABLE `potrosnja`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=93;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `budzeti`
--
ALTER TABLE `budzeti`
  ADD CONSTRAINT `budzeti_ibfk_1` FOREIGN KEY (`korisnik_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `korisnici`
--
ALTER TABLE `korisnici`
  ADD CONSTRAINT `FK_korisnik` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `potrosnja`
--
ALTER TABLE `potrosnja`
  ADD CONSTRAINT `potrosnja_ibfk_1` FOREIGN KEY (`budzet_id`) REFERENCES `budzeti` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `potrosnja_ibfk_2` FOREIGN KEY (`korisnik_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
