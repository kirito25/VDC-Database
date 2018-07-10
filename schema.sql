

CREATE TABLE model (
	"model_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"name" character(255) NOT NULL,
	"file_id" bigint NOT NULL
);

CREATE TABLE file (
	"file_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"filename" character(255) NOT NULL,
	"type" character(255) NOT NULL,
	"catalog" character(255) NOT NULL,
	"weight" bigint NOT NULL,
	"logP" int NOT NULL,
	"charge" int NOT NULL,
	"pH" int NOT NULL,
	"purchasability" character(255) NOT NULL,
	"reactivity" character(255) NOT NULL
);


