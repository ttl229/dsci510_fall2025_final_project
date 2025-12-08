BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "Actors" (
	"id"	INTEGER PRIMARY KEY,
	"name"	TEXT UNIQUE NOT NULL,
	"number_titles"	INTEGER,
	"number_followers"	NUMERIC
);
CREATE TABLE IF NOT EXISTS "Character_Types" (
	"id"	INTEGER PRIMARY KEY,
	"type"	TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS "Genres" (
	"id"	INTEGER PRIMARY KEY,
	"genre"	TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS "Platforms" (
	"id"	INTEGER PRIMARY KEY,
	"name"	TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS "Roles" (
	"id"        INTEGER PRIMARY KEY,
	"title_id"	INTEGER NOT NULL,
	"actor_id"	INTEGER NOT NULL,
	"role"      TEXT NOT NULL,  -- name of the character in the show
	"type_id"	INTEGER,        -- type of character ie. male protagonist, villain, etc
	UNIQUE(title_id, role),      -- avoid duplicate entries of role+title combo (multiple titles okay)
	FOREIGN KEY("actors_id") REFERENCES "Actors"("id"),
	FOREIGN KEY("title_id") REFERENCES "Titles"("id"),
	FOREIGN KEY("type_id") REFERENCES "Character_Types"("id")
);
CREATE TABLE IF NOT EXISTS "Titles" (
	"id"	INTEGER PRIMARY KEY,
	"title"	TEXT UNIQUE NOT NULL,
	"release_date"	DATE,  -- date format yyyy-MM-dd
	"episodes"	INTEGER,
	"platform_id"	INTEGER,
	"genre_id"	INTEGER,
	"views" INTEGER,
	FOREIGN KEY("genre_id") REFERENCES "Genres"("id"),
	FOREIGN KEY("platform_id") REFERENCES "Platforms"("id")
);
COMMIT;
