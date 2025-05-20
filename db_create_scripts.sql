CREATE TABLE Players (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Telegram_First_Name TEXT,
    Telegram_Last_Name TEXT,
    Telegram_Login TEXT,
    Telegram_ID BIGINT,
    Friendly_First_Name TEXT,
    Friendly_Last_Name TEXT,
    Informal_Friendly_First_Name TEXT,
    Birthday DATE,
    Height SMALLINT,
    CONSTRAINT players_pkey PRIMARY KEY (id)
);

CREATE TABLE Matchday (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Game_ID INTEGER,
    Type TEXT,
    Player_ID INTEGER,
    Time_Stamp TIMESTAMP WITH TIME ZONE,
    Wokeup BOOLEAN DEFAULT FALSE,
    Squad TEXT,
    Goals SMALLINT,
    Assists SMALLINT,
    Own_Goals SMALLINT,
    Money_Given DECIMAL,
    Balance_Change DECIMAL,
    Comment text,
    CONSTRAINT constraint_1 FOREIGN KEY(Player_ID) REFERENCES public.Players (id) ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT constraint_2 FOREIGN KEY(Game_ID) REFERENCES public.Games (id) ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT matchday_pkey1 PRIMARY KEY (id)
    );

CREATE TABLE Games (
  id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  Game_Date date,
  Score_Tomato smallint,
  Score_Corn smallint,
  Paid_for_Pitch decimal,
  Played boolean DEFAULT TRUE,
  CONSTRAINT games_pkey PRIMARY KEY (id)
)