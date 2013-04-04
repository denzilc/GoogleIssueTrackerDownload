DROP DATABASE IF EXISTS `android`;
CREATE DATABASE `android`;

USE android;

DROP TABLE IF EXISTS `issues`;
CREATE TABLE `issues` (
  `issue_id` int(11) NOT NULL,
  `title` text,
  `state` text,
  `content` longtext,
  `stars` int(11) DEFAULT NULL,
  `owner` text,
  `blocking` text,
  `blockedOn` text,
  `updated` datetime DEFAULT NULL,
  `status` text,
  `closedDate` datetime DEFAULT NULL,
  `mergedInto` text,
  `cc` text,
  `author` text,
  `published` datetime DEFAULT NULL,
  `restricted` text, 
  `target` text, 
  `securityProblem` TINYINT(1), 
  `reportedBy` text, 
  `component` text, 
  `cat` text, 
  `priority` text, 
  `version` text, 
  `subcomponentopengl` TINYINT(1), 
  `subcomponent` text, 
  `bugtype` text, 
  `regression` TINYINT(1), 
  `num_comments` int(11) DEFAULT NULL,
  PRIMARY KEY (`issue_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `issue_id` int(11) NOT NULL,
  `comment_id` int(11) NOT NULL,
  `published` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  `title` text,
  `content` longtext,
  `author` text,
  `issue_status` text,
  PRIMARY KEY (`issue_id`,`comment_id`),
  KEY `issue_id` (`issue_id`),
  CONSTRAINT `issue_id` FOREIGN KEY (`issue_id`) REFERENCES `issues` (`issue_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
