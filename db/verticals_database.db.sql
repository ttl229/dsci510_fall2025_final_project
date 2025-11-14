BEGIN TRANSACTION;
DROP TABLE IF EXISTS "Cast";
CREATE TABLE "Cast" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"number_titles"	INTEGER,
	"number_followers"	NUMERIC,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "Character_Type";
CREATE TABLE "Character_Type" (
	"id"	INTEGER NOT NULL,
	"type"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "Genre";
CREATE TABLE "Genre" (
	"id"	INTEGER NOT NULL,
	"genre"	TEXT,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "Platforms";
CREATE TABLE "Platforms" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "Role";
CREATE TABLE "Role" (
	"title_id"	INTEGER NOT NULL,
	"cast_id"	INTEGER NOT NULL,
	"type_id"	INTEGER,
	FOREIGN KEY("cast_id") REFERENCES "Cast"("id"),
	FOREIGN KEY("title_id") REFERENCES "Titles"("id"),
	FOREIGN KEY("type_id") REFERENCES "Character_Type"("id")
);
DROP TABLE IF EXISTS "Titles";
CREATE TABLE "Titles" (
	"id"	INTEGER NOT NULL,
	"title"	INTEGER NOT NULL,
	"release_date"	TEXT,
	"episodes"	INTEGER,
	"platform_id"	INTEGER,
	"genre_id"	INTEGER,
	"cast_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("cast_id") REFERENCES "Cast"("id"),
	FOREIGN KEY("genre_id") REFERENCES "Genre"("id"),
	FOREIGN KEY("platform_id") REFERENCES "Platforms"("id")
);
COMMIT;
