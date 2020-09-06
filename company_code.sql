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

 Date: 19/08/2020 12:27:58
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for company_code
-- ----------------------------
DROP TABLE IF EXISTS `company_code`;
CREATE TABLE `company_code`  (
  `company_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `credit_code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `org_code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `ie_org_code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `reg_num` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`credit_code`) USING BTREE,
  UNIQUE INDEX `company_name`(`company_name`) USING BTREE,
  UNIQUE INDEX `org_code`(`org_code`) USING BTREE,
  CONSTRAINT `fk_company_name` FOREIGN KEY (`company_name`) REFERENCES `company_detail` (`company_name`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_credit_code` FOREIGN KEY (`credit_code`) REFERENCES `company_detail` (`credit_code`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
