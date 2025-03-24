CREATE TABLE Players (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Telegram_First_Name TEXT,
    Telegram_Last_Name TEXT,
    Telegram_Login TEXT,
    Telegram_ID BIGINT,
    Friendly_First_Name TEXT,
    Friendly_Last_Name TEXT,
    Informal_Friendly_First_Name TEXT
);

CREATE TABLE Matchday (
   id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
   Matchday_Date DATE,
   Type TEXT,
   Player_ID INTEGER,
   Time_Stamp TIMESTAMP WITH TIME ZONE,
   CONSTRAINT constraint_1 FOREIGN KEY (Player_ID) REFERENCES public.Players (id) ON UPDATE NO ACTION ON DELETE NO ACTION,
)