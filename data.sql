CREATE TABLE `data` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `file_id` varchar(50) NOT NULL DEFAULT '',
  `title` varchar(100) NOT NULL DEFAULT '',
  `image_link` varchar(500) NOT NULL DEFAULT '',
  `vod_link` varchar(500) NOT NULL DEFAULT '',
  `file_link` varchar(500) NOT NULL DEFAULT '',
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=utf8;
