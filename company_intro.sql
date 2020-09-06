/*
 Navicat MySQL Data Transfer

 Source Server         : Localhost_Root
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : localhost:3306
 Source Schema         : qcc_crawler

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : 65001

 Date: 19/08/2020 12:28:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for company_intro
-- ----------------------------
DROP TABLE IF EXISTS `company_intro`;
CREATE TABLE `company_intro`  (
  `company_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `company_intro` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`company_name`) USING BTREE,
  CONSTRAINT `fk_name` FOREIGN KEY (`company_name`) REFERENCES `company_detail` (`company_name`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
