CREATE DATABASE `chromium`;

USE chromium;

DROP TABLE IF EXISTS `issues`;
CREATE TABLE `issues` (
  `issue_id` int(11) NOT NULL,
  `title` text,
  `state` text,
  `content` text,
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
  `bugtype` text,
  `priority` text,
  `pri` tinyint(4) DEFAULT NULL,
  `os` text,
  `area` text,
  `feature` text,
  `mstone` text,
  `releaseBlock` text,
  `regression` tinyint(4) DEFAULT NULL,
  `performance` tinyint(4) DEFAULT NULL,
  `cleanup` tinyint(4) DEFAULT NULL,
  `polish` tinyint(4) DEFAULT NULL,
  `usability` tinyint(4) DEFAULT NULL,
  `crash` tinyint(4) DEFAULT NULL,
  `security` tinyint(4) DEFAULT NULL,
  `secSeverity` text,
  `webkit` text,
  `hotlist` text,
  `internals` text,
  `sev` int(11) DEFAULT NULL,
  `secImpacts` text,
  `notLabel` text,
  `action` text,
  `numComments` int(11) DEFAULT NULL,
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
  `owner_update` text,
  PRIMARY KEY (`issue_id`,`comment_id`),
  KEY `issue_id` (`issue_id`),
  CONSTRAINT `issue_id` FOREIGN KEY (`issue_id`) REFERENCES `issues` (`issue_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

