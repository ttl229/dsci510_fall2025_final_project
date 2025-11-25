BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "Cast" (
	"id"	INTEGER PRIMARY KEY,
	"name"	TEXT UNIQUE NOT NULL,
	"number_titles"	INTEGER,
	"number_followers"	NUMERIC
);
CREATE TABLE IF NOT EXISTS "Character_Type" (
	"id"	INTEGER PRIMARY KEY,
	"type"	TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS "Genre" (
	"id"	INTEGER PRIMARY KEY,
	"genre"	TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS "Platforms" (
	"id"	INTEGER PRIMARY KEY,
	"name"	TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS "Role" (
	"id"        INTEGER PRIMARY KEY,
	"title_id"	INTEGER NOT NULL,
	"cast_id"	INTEGER NOT NULL,
	"role"      TEXT UNIQUE NOT NULL,  -- name of the character in the show
	"type_id"	INTEGER,  -- type of character ie. male protagonist, villain, etc
	FOREIGN KEY("cast_id") REFERENCES "Cast"("id"),
	FOREIGN KEY("title_id") REFERENCES "Titles"("id"),
	FOREIGN KEY("type_id") REFERENCES "Character_Type"("id")
);
CREATE TABLE IF NOT EXISTS "Titles" (
	"id"	INTEGER PRIMARY KEY,
	"title"	TEXT UNIQUE NOT NULL,
	"release_date"	DATE,  -- date format yyyy-MM-dd
	"episodes"	INTEGER,
	"platform_id"	INTEGER,
	"genre_id"	INTEGER,
	"cast_id"	INTEGER,
	FOREIGN KEY("cast_id") REFERENCES "Cast"("id"),
	FOREIGN KEY("genre_id") REFERENCES "Genre"("id"),
	FOREIGN KEY("platform_id") REFERENCES "Platforms"("id")
);
COMMIT;
