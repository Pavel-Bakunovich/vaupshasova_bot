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
    Height SMALLINT
);

CREATE TABLE Matchday (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Matchday_Date DATE,
    Type TEXT,
    Player_ID INTEGER,
    Time_Stamp TIMESTAMP WITH TIME ZONE,
    Wokeup BOOLEAN DEFAULT FALSE,
    CONSTRAINT constraint_1 FOREIGN KEY(Player_ID) REFERENCES public.Players (id) ON UPDATE NO ACTION ON DELETE NO ACTION
    );

CREATE TABLE Games (
  Game_ID integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  Game_Date timestamp with time zone,
  Score_Tomato smallint,
  Score_Corn smallint,
  Paid_for_Pitch decimal(2)
)
