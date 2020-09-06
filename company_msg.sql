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

 Date: 19/08/2020 12:27:12
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for company_msg
-- ----------------------------
DROP TABLE IF EXISTS `company_msg`;
CREATE TABLE `company_msg`  (
  `company_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `company_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`company_name`) USING BTREE,
  UNIQUE INDEX `company_url`(`company_url`) USING BTREE,
  UNIQUE INDEX `company_name`(`company_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of company_msg
-- ----------------------------
INSERT INTO `company_msg` VALUES (' 黔西南州骏腾智能科技服务有限公司 ', '/firm/000044c9f9cf4a21b3930f6f25fccceb.html');
INSERT INTO `company_msg` VALUES (' 沈阳徐氏房屋开发有限公司 ', '/firm/000055b9df9ef0deb3af175c25d94027.html');
INSERT INTO `company_msg` VALUES (' 厦门市佳胜体育推广有限公司 ', '/firm/0000d16cb7f32ce56ccc229cc3034e0d.html');

SET FOREIGN_KEY_CHECKS = 1;
