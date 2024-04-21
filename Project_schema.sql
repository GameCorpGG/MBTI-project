#Create database
CREATE DATABASE `project` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

#Create Tables
CREATE TABLE `personality_questions` (
  `questionid` int NOT NULL,
  `questiondesc` varchar(1000) NOT NULL,
  `personal_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`questionid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='deatils of question related to personality';
CREATE TABLE `personqa` (
  `personqaid` int NOT NULL AUTO_INCREMENT,
  `person_name` varchar(100) DEFAULT NULL,
  `questionoptionid` int DEFAULT NULL,
  `questionid` int DEFAULT NULL,
  `age` int DEFAULT NULL,
  `phone_no` bigint NOT NULL,
  PRIMARY KEY (`personqaid`),
  KEY `questionoptionid_fk_idx` (`questionoptionid`),
  KEY `questionid_fk_idx` (`questionid`),
  CONSTRAINT `question_fk` FOREIGN KEY (`questionid`) REFERENCES `personality_questions` (`questionid`),
  CONSTRAINT `questionoptionid_fk` FOREIGN KEY (`questionoptionid`) REFERENCES `questionoptions` (`questionoptionid`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `questionoptions` (
  `questionoptionid` int NOT NULL,
  `optiondescription` varchar(100) NOT NULL,
  `optionmarks` int DEFAULT NULL,
  `questionid` int NOT NULL,
  PRIMARY KEY (`questionoptionid`),
  KEY `questionid_fk_idx` (`questionid`),
  CONSTRAINT `questionid_fk` FOREIGN KEY (`questionid`) REFERENCES `personality_questions` (`questionid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='stores options for questions';

#Create Views
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_getperson` AS select distinct concat(`personqa`.`person_name`,' | ',`personqa`.`phone_no`) AS `person` from `personqa`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_getquestionoption` AS select concat(`a`.`questiondesc`,'(',`a`.`questionid`,')') AS `questiondesc`,max((case when (`b`.`optiondescription` = 'Strongly Agree') then concat(`b`.`optiondescription`,'(',`b`.`questionoptionid`,')') else NULL end)) AS `Option1`,max((case when (`b`.`optiondescription` = 'Agree') then concat(`b`.`optiondescription`,'(',`b`.`questionoptionid`,')') else NULL end)) AS `Option2`,max((case when (`b`.`optiondescription` = 'Disagree') then concat(`b`.`optiondescription`,'(',`b`.`questionoptionid`,')') else NULL end)) AS `Option3`,max((case when (`b`.`optiondescription` = 'Strongly Disagree') then concat(`b`.`optiondescription`,'(',`b`.`questionoptionid`,')') else NULL end)) AS `Option4` from (`personality_questions` `a` left join `questionoptions` `b` on((`a`.`questionid` = `b`.`questionid`))) group by `a`.`questionid`;
