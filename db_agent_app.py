import sqlite3
import json
import os
import re
from openai import OpenAI
from typing import List, Dict, Any


DB_PATH = os.path.join(os.path.dirname(__file__), "sample_data.db")

def create_sample_db(db_path: str = DB_PATH) -> None:
    """
    Create a sample SQLite database with one table and a few rows if it doesn't exist.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""DROP TABLE IF EXISTS AMLcase;""")
    cur.execute("""
    CREATE TABLE AMLcase (
        CASE_ID         VARCHAR(100) PRIMARY KEY,
        customer        VARCHAR(255) NOT NULL,
        create_date     DATETIME NOT NULL,
        AAA_Status      VARCHAR(30),
        CASE_Status     VARCHAR(50),
        Event_Country   VARCHAR(100),
        Analyst         VARCHAR(100),
        Source_System   VARCHAR(100)
    );
    """)
    cur.execute("SELECT COUNT(*) FROM AMLcase")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO AMLcase (CASE_ID, customer, create_date, AAA_Status, CASE_Status, Event_Country, Analyst, Source_System) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ('1000001', 'Nelson Shaun, Jim Terry', '2019-01-01 10:10:00', 'ASSESS', 'CLOSED-RISK RELEVANT', 'India', 'Channel Winston', 'SYS001'),
                ('1000002', 'Steve Morgan, Ian Strong, Franci McCoy', '2019-02-15 14:30:00', 'OPEN', 'IN-PROGRESS', 'USA', 'Alice Johnson', 'SYS002'),
                ('1000003', 'Emily Davis, Jonathan Lee', '2019-03-20 09:45:00', 'CLOSED', 'RESOLVED', 'UK', 'Bob Smith', 'SYS003'),
                ('1000004', 'Michael Brown, Olivier Marshall', '2019-04-25 11:20:00', 'PENDING', 'ON-HOLD', 'Canada', 'Charlie Lee', 'SYS004'),
                ('1000005', 'Sarah Wilson', '2019-05-30 16:50:00', 'ESCALATED', 'ESCALATED-URGENT', 'Australia', 'Diana Prince', 'SYS005'),
                ('1000006', 'David Clark, Indiana Marry', '2019-06-10 13:15:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Germany', 'Ethan Hunt', 'SYS006'),
                ('1000007', 'Laura Martinez', '2019-07-22 08:05:00', 'OPEN', 'NEW CASE', 'France', 'Fiona Gallagher', 'SYS007'),
                ('1000008', 'James Taylor', '2019-08-18 12:40:00', 'ASSESS', 'CLOSED-RISK RELEVANT', 'India', 'Channel Winston', 'SYS001'),
                ('1000009', 'Olivia Anderson, Thomas Hugh', '2019-09-05 15:25:00', 'PENDING', 'IN-PROGRESS', 'Italy', 'George Clooney', 'SYS008'),
                ('1000010', 'Daniel Thomas', '2019-10-12 10:55:00', 'CLOSED-RISK RELEVANT', 'RESOLVED', '', '', ''),
                ('1000011', 'Chris Evans', '2019-11-20 14:10:00', 'ESCALATED', 'ESCALATED-URGENT', 'Spain', 'Hannah Baker', 'SYS009'),
                ('1000012', 'Sophia Moore', '2019-12-15 09:30:00', 'CLOSED', 'CLOSED-NOT RISK RELEVANT', 'Netherlands', 'Ian Somerhalder', 'SYS010'),
                ('1000013', 'Jessica Miller', '2020-01-10 08:20:00', 'OPEN', 'IN-PROGRESS', 'USA', 'Jack Black', 'SYS011'),
                ('1000014', 'Matthew Harris', '2020-01-15 09:30:00', 'ASSESS', 'NEW CASE', 'UK', 'Karen White', 'SYS012'),
                ('1000015', 'Ashley Young', '2020-01-20 10:40:00', 'CLOSED', 'RESOLVED', 'Canada', 'Liam Neeson', 'SYS013'),
                ('1000016', 'Joshua King', '2020-01-25 11:50:00', 'PENDING', 'ON-HOLD', 'Australia', 'Mia Wong', 'SYS014'),
                ('1000017', 'Amanda Scott', '2020-02-01 12:00:00', 'ESCALATED', 'ESCALATED-URGENT', 'Germany', 'Noah Kim', 'SYS015'),
                ('1000018', 'Brian Adams', '2020-02-05 13:10:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'France', 'Olivia Lee', 'SYS016'),
                ('1000019', 'Emily Clark', '2020-02-10 14:20:00', 'OPEN', 'IN-PROGRESS', 'Italy', 'Paul Walker', 'SYS017'),
                ('1000020', 'David Lewis', '2020-02-15 15:30:00', 'ASSESS', 'NEW CASE', 'Spain', 'Quinn Parker', 'SYS018'),
                ('1000021', 'Sarah Hall', '2020-02-20 16:40:00', 'CLOSED', 'RESOLVED', 'Netherlands', 'Rachel Green', 'SYS019'),
                ('1000022', 'James Allen', '2020-02-25 17:50:00', 'PENDING', 'ON-HOLD', 'India', 'Sam Carter', 'SYS020'),
                ('1000023', 'Megan Wright', '2020-03-01 08:05:00', 'ESCALATED', 'ESCALATED-URGENT', 'USA', 'Tina Brown', 'SYS021'),
                ('1000024', 'Christopher Hill', '2020-03-05 09:15:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'UK', 'Uma Thurman', 'SYS022'),
                ('1000025', 'Jessica Green', '2020-03-10 10:25:00', 'OPEN', 'IN-PROGRESS', 'Canada', 'Victor Hugo', 'SYS023'),
                ('1000026', 'Daniel Baker', '2020-03-15 11:35:00', 'ASSESS', 'NEW CASE', 'Australia', 'Wendy Adams', 'SYS024'),
                ('1000027', 'Laura Nelson', '2020-03-20 12:45:00', 'CLOSED', 'RESOLVED', 'Germany', 'Xander Cage', 'SYS025'),
                ('1000028', 'Kevin Carter', '2020-03-25 13:55:00', 'PENDING', 'ON-HOLD', 'France', 'Yara Shahidi', 'SYS026'),
                ('1000029', 'Emily Turner', '2020-04-01 15:05:00', 'ESCALATED', 'ESCALATED-URGENT', 'Italy', 'Zane Malik', 'SYS027'),
                ('1000030', 'Michael Phillips', '2020-04-05 16:15:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Spain', 'Abby Lee', 'SYS028'),
                ('1000031', 'Olivia Evans', '2020-04-10 17:25:00', 'OPEN', 'IN-PROGRESS', 'Netherlands', 'Ben Stiller', 'SYS029'),
                ('1000032', 'William Collins', '2020-04-15 08:35:00', 'ASSESS', 'NEW CASE', 'India', 'Cara Delevingne', 'SYS030'),
                ('1000033', 'Sophia Stewart', '2020-04-20 09:45:00', 'CLOSED', 'RESOLVED', 'USA', 'Derek Shepherd', 'SYS031'),
                ('1000034', 'Benjamin Morris', '2020-04-25 10:55:00', 'PENDING', 'ON-HOLD', 'UK', 'Ella Fitzgerald', 'SYS032'),
                ('1000035', 'Grace Foster', '2020-05-01 12:05:00', 'ESCALATED', 'ESCALATED-URGENT', 'Canada', 'Finn Wolfhard', 'SYS033'),
                ('1000036', 'Samuel Reed', '2020-05-05 13:15:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Australia', 'Gina Rodriguez', 'SYS034'),
                ('1000037', 'Chloe Bennett', '2020-05-10 14:25:00', 'OPEN', 'IN-PROGRESS', 'Germany', 'Harry Styles', 'SYS035'),
                ('1000038', 'Jack Russell', '2020-05-15 15:35:00', 'ASSESS', 'NEW CASE', 'France', 'Isla Fisher', 'SYS036'),
                ('1000039', 'Lily Brooks', '2020-05-20 16:45:00', 'CLOSED', 'RESOLVED', 'Italy', 'Jake Gyllenhaal', 'SYS037'),
                ('1000040', 'Ryan Wood', '2020-05-25 17:55:00', 'PENDING', 'ON-HOLD', 'Spain', 'Kylie Jenner', 'SYS038'),
                ('1000041', 'Zoe Adams', '2020-06-01 08:10:00', 'ESCALATED', 'ESCALATED-URGENT', 'Netherlands', 'Liam Hemsworth', 'SYS039'),
                ('1000042', 'Luke Perry', '2020-06-05 09:20:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'India', 'Mila Kunis', 'SYS040'),
                ('1000043', 'Ella James', '2020-06-10 10:30:00', 'OPEN', 'IN-PROGRESS', 'USA', 'Nina Dobrev', 'SYS041'),
                ('1000044', 'Henry Clark', '2020-06-15 11:40:00', 'ASSESS', 'NEW CASE', 'UK', 'Oscar Isaac', 'SYS042'),
                ('1000045', 'Victoria Lee', '2020-06-20 12:50:00', 'CLOSED', 'RESOLVED', 'Canada', 'Penelope Cruz', 'SYS043'),
                ('1000046', 'Mason Wright', '2020-06-25 14:00:00', 'PENDING', 'ON-HOLD', 'Australia', 'Quentin Tarantino', 'SYS044'),
                ('1000047', 'Ava Harris', '2020-07-01 15:10:00', 'ESCALATED', 'ESCALATED-URGENT', 'Germany', 'Rita Ora', 'SYS045'),
                ('1000048', 'Ethan Lewis', '2020-07-05 16:20:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'France', 'Sophie Turner', 'SYS046'),
                ('1000049', 'Madison King', '2020-07-10 17:30:00', 'OPEN', 'IN-PROGRESS', 'Italy', 'Tom Holland', 'SYS047'),
                ('1000050', 'Jacob Scott', '2020-07-15 08:40:00', 'ASSESS', 'NEW CASE', 'Spain', 'Uma Thurman', 'SYS048'),
                ('1000051', 'Mia Young', '2020-07-20 09:50:00', 'CLOSED', 'RESOLVED', 'Netherlands', 'Vin Diesel', 'SYS049'),
                ('1000052', 'Logan Hall', '2020-07-25 11:00:00', 'PENDING', 'ON-HOLD', 'India', 'Will Smith', 'SYS050'),
                ('1000053', 'Harper Allen', '2020-08-01 12:10:00', 'ESCALATED', 'ESCALATED-URGENT', 'USA', 'Xavier Dolan', 'SYS051'),
                ('1000054', 'Sebastian Nelson', '2020-08-05 13:20:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'UK', 'Yvonne Strahovski', 'SYS052'),
                ('1000055', 'Layla Stewart', '2020-08-10 14:30:00', 'OPEN', 'IN-PROGRESS', 'Canada', 'Zachary Levi', 'SYS053'),
                ('1000056', 'Carter Morris', '2020-08-15 15:40:00', 'ASSESS', 'NEW CASE', 'Australia', 'Alicia Keys', 'SYS054'),
                ('1000057', 'Natalie Foster', '2020-08-20 16:50:00', 'CLOSED', 'RESOLVED', 'Germany', 'Brad Pitt', 'SYS055'),
                ('1000058', 'Owen Reed', '2020-08-25 18:00:00', 'PENDING', 'ON-HOLD', 'France', 'Cate Blanchett', 'SYS056'),
                ('1000059', 'Brooklyn Bennett', '2020-09-01 08:15:00', 'ESCALATED', 'ESCALATED-URGENT', 'Italy', 'Daniel Craig', 'SYS057'),
                ('1000060', 'Gabriel Russell', '2020-09-05 09:25:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Spain', 'Emma Watson', 'SYS058'),
                ('1000061', 'Savannah Turner', '2020-09-10 10:35:00', 'OPEN', 'IN-PROGRESS', 'Netherlands', 'Freddie Mercury', 'SYS059'),
                ('1000062', 'Anthony Phillips', '2020-09-15 11:45:00', 'ASSESS', 'NEW CASE', 'India', 'Gal Gadot', 'SYS060'),
                ('1000063', 'Hailey Evans', '2020-09-20 12:55:00', 'CLOSED', 'RESOLVED', 'USA', 'Hugh Jackman', 'SYS061'),
                ('1000064', 'Isaac Collins', '2020-09-25 14:05:00', 'PENDING', 'ON-HOLD', 'UK', 'Idris Elba', 'SYS062'),
                ('1000065', 'Avery Stewart', '2020-10-01 15:15:00', 'ESCALATED', 'ESCALATED-URGENT', 'Canada', 'Jennifer Lawrence', 'SYS063'),
                ('1000066', 'Elijah Foster', '2020-10-05 16:25:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Australia', 'Keanu Reeves', 'SYS064'),
                ('1000067', 'Scarlett Reed', '2020-10-10 17:35:00', 'OPEN', 'IN-PROGRESS', 'Germany', 'Leonardo DiCaprio', 'SYS065'),
                ('1000068', 'Julian Bennett', '2020-10-15 08:45:00', 'ASSESS', 'NEW CASE', 'France', 'Margot Robbie', 'SYS066'),
                ('1000069', 'Stella Morris', '2020-10-20 09:55:00', 'CLOSED', 'RESOLVED', 'Italy', 'Natalie Portman', 'SYS067'),
                ('1000070', 'Hudson King', '2020-10-25 11:05:00', 'PENDING', 'ON-HOLD', 'Spain', 'Octavia Spencer', 'SYS068'),
                ('1000071', 'Penelope Wright', '2020-11-01 12:15:00', 'ESCALATED', 'ESCALATED-URGENT', 'Netherlands', 'Paul Rudd', 'SYS069'),
                ('1000072', 'Lincoln Harris', '2020-11-05 13:25:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'India', 'Queen Latifah', 'SYS070'),
                ('1000073', 'Paisley Lewis', '2020-11-10 14:35:00', 'OPEN', 'IN-PROGRESS', 'USA', 'Robert Downey Jr.', 'SYS071'),
                ('1000074', 'Grayson Hall', '2020-11-15 15:45:00', 'ASSESS', 'NEW CASE', 'UK', 'Sandra Bullock', 'SYS072'),
                ('1000075', 'Aurora Lee', '2020-11-20 16:55:00', 'CLOSED', 'RESOLVED', 'Canada', 'Tom Hanks', 'SYS073'),
                ('1000076', 'Easton Wright', '2020-11-25 18:05:00', 'PENDING', 'ON-HOLD', 'Australia', 'Uma Thurman', 'SYS074'),
                ('1000077', 'Genesis Harris', '2020-12-01 08:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Germany', 'Vin Diesel', 'SYS075'),
                ('1000078', 'Kennedy Lewis', '2020-12-05 09:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'France', 'Will Smith', 'SYS076'),
                ('1000079', 'Sadie Hall', '2020-12-10 10:40:00', 'OPEN', 'IN-PROGRESS', 'Italy', 'Xavier Dolan', 'SYS077'),
                ('1000080', 'Blake Lee', '2020-12-15 11:50:00', 'ASSESS', 'NEW CASE', 'Spain', 'Yvonne Strahovski', 'SYS078'),
                ('1000081', 'Piper Wright', '2020-12-20 13:00:00', 'CLOSED', 'RESOLVED', 'Netherlands', 'Zachary Levi', 'SYS079'),
                ('1000082', 'Jayden Harris', '2020-12-25 14:10:00', 'PENDING', 'ON-HOLD', 'India', 'Alicia Keys', 'SYS080'),
                ('1000083', 'Riley Lewis', '2021-01-01 15:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'USA', 'Brad Pitt', 'SYS081'),
                ('1000084', 'Peyton Hall', '2021-01-05 16:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'UK', 'Cate Blanchett', 'SYS082'),
                ('1000085', 'Ariana Lee', '2021-01-10 17:40:00', 'OPEN', 'IN-PROGRESS', 'Canada', 'Daniel Craig', 'SYS083'),
                ('1000086', 'Sawyer Wright', '2021-01-15 08:50:00', 'ASSESS', 'NEW CASE', 'Australia', 'Emma Watson', 'SYS084'),
                ('1000087', 'Camila Harris', '2021-01-20 10:00:00', 'CLOSED', 'RESOLVED', 'Germany', 'Freddie Mercury', 'SYS085'),
                ('1000088', 'Roman Lewis', '2021-01-25 11:10:00', 'PENDING', 'ON-HOLD', 'France', 'Gal Gadot', 'SYS086'),
                ('1000089', 'Delilah Hall', '2021-02-01 12:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Italy', 'Hugh Jackman', 'SYS087'),
                ('1000090', 'Maddox Lee', '2021-02-05 13:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Spain', 'Idris Elba', 'SYS088'),
                ('1000091', 'Jade Wright', '2021-02-10 14:40:00', 'OPEN', 'IN-PROGRESS', 'Netherlands', 'Jennifer Lawrence', 'SYS089'),
                ('1000092', 'Emery Harris', '2021-02-15 15:50:00', 'ASSESS', 'NEW CASE', 'India', 'Keanu Reeves', 'SYS090'),
                ('1000093', 'Reagan Lewis', '2021-02-20 17:00:00', 'CLOSED', 'RESOLVED', 'USA', 'Leonardo DiCaprio', 'SYS091'),
                ('1000094', 'Sienna Hall', '2021-02-25 08:10:00', 'PENDING', 'ON-HOLD', 'UK', 'Margot Robbie', 'SYS092'),
                ('1000095', 'Adeline Lee', '2021-03-01 09:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Canada', 'Natalie Portman', 'SYS093'),
                ('1000096', 'Finn Wright', '2021-03-05 10:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Australia', 'Octavia Spencer', 'SYS094'),
                ('1000097', 'Valentina Harris', '2021-03-10 11:40:00', 'OPEN', 'IN-PROGRESS', 'Germany', 'Paul Rudd', 'SYS095'),
                ('1000098', 'Elliott Lewis', '2021-03-15 12:50:00', 'ASSESS', 'NEW CASE', 'France', 'Queen Latifah', 'SYS096'),
                ('1000099', 'Brooks Hall', '2021-03-20 14:00:00', 'CLOSED', 'RESOLVED', 'Italy', 'Robert Downey Jr.', 'SYS097'),
                ('1000100', 'Alina Lee', '2021-03-25 15:10:00', 'PENDING', 'ON-HOLD', 'Spain', 'Sandra Bullock', 'SYS098'),
                ('1000101', 'Graham Wright', '2021-04-01 16:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Netherlands', 'Tom Hanks', 'SYS099'),
                ('1000102', 'Juliette Harris', '2021-04-05 17:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'India', 'Uma Thurman', 'SYS100'),
                ('1000103', 'Morgan Lee', '2021-04-10 08:40:00', 'OPEN', 'IN-PROGRESS', 'USA', 'Victor Hugo', 'SYS001'),
                ('1000104', 'Harper Scott', '2021-04-15 09:50:00', 'ASSESS', 'NEW CASE', 'UK', 'Wendy Adams', 'SYS002'),
                ('1000105', 'Aiden Harris', '2021-04-20 11:00:00', 'CLOSED', 'RESOLVED', 'Canada', 'Xander Cage', 'SYS003'),
                ('1000106', 'Layla Wright', '2021-04-25 12:10:00', 'PENDING', 'ON-HOLD', 'Australia', 'Yara Shahidi', 'SYS004'),
                ('1000107', 'Eli Bennett', '2021-05-01 13:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Germany', 'Zane Malik', 'SYS005'),
                ('1000108', 'Aurora Stewart', '2021-05-05 14:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'France', 'Abby Lee', 'SYS006'),
                ('1000109', 'Mila Foster', '2021-05-10 15:40:00', 'OPEN', 'IN-PROGRESS', 'Italy', 'Ben Stiller', 'SYS007'),
                ('1000110', 'Leo Collins', '2021-05-15 16:50:00', 'ASSESS', 'NEW CASE', 'Spain', 'Cara Delevingne', 'SYS008'),
                ('1000111', 'Ruby Evans', '2021-05-20 18:00:00', 'CLOSED', 'RESOLVED', 'Netherlands', 'Derek Shepherd', 'SYS009'),
                ('1000112', 'Henry Phillips', '2021-05-25 08:10:00', 'PENDING', 'ON-HOLD', 'India', 'Ella Fitzgerald', 'SYS010'),
                ('1000113', 'Sadie Morris', '2021-06-01 09:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'USA', 'Finn Wolfhard', 'SYS011'),
                ('1000114', 'Jaxon Reed', '2021-06-05 10:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'UK', 'Gina Rodriguez', 'SYS012'),
                ('1000115', 'Paisley Turner', '2021-06-10 11:40:00', 'OPEN', 'IN-PROGRESS', 'Canada', 'Harry Styles', 'SYS013'),
                ('1000116', 'Everly Russell', '2021-06-15 12:50:00', 'ASSESS', 'NEW CASE', 'Australia', 'Isla Fisher', 'SYS014'),
                ('1000117', 'Lincoln Bennett', '2021-06-20 14:00:00', 'CLOSED', 'RESOLVED', 'Germany', 'Jake Gyllenhaal', 'SYS015'),
                ('1000118', 'Ellie Harris', '2021-06-25 15:10:00', 'PENDING', 'ON-HOLD', 'France', 'Kylie Jenner', 'SYS016'),
                ('1000119', 'Gabriel Wright', '2021-07-01 16:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Italy', 'Liam Hemsworth', 'SYS017'),
                ('1000120', 'Penelope Lee', '2021-07-05 17:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Spain', 'Mila Kunis', 'SYS018'),
                ('1000121', 'Hudson Scott', '2021-07-10 08:40:00', 'OPEN', 'IN-PROGRESS', 'Netherlands', 'Nina Dobrev', 'SYS019'),
                ('1000122', 'Savannah Hall', '2021-07-15 09:50:00', 'ASSESS', 'NEW CASE', 'India', 'Oscar Isaac', 'SYS020'),
                ('1000123', 'Levi Young', '2021-07-20 11:00:00', 'CLOSED', 'RESOLVED', 'USA', 'Penelope Cruz', 'SYS021'),
                ('1000124', 'Stella Allen', '2021-07-25 12:10:00', 'PENDING', 'ON-HOLD', 'UK', 'Quentin Tarantino', 'SYS022'),
                ('1000125', 'Nathan Stewart', '2021-08-01 13:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Canada', 'Rita Ora', 'SYS023'),
                ('1000126', 'Brooklyn Foster', '2021-08-05 14:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Australia', 'Sophie Turner', 'SYS024'),
                ('1000127', 'Zachary Collins', '2021-08-10 15:40:00', 'OPEN', 'IN-PROGRESS', 'Germany', 'Tom Holland', 'SYS025'),
                ('1000128', 'Ariana Evans', '2021-08-15 16:50:00', 'ASSESS', 'NEW CASE', 'France', 'Uma Thurman', 'SYS026'),
                ('1000129', 'Mason Phillips', '2021-08-20 18:00:00', 'CLOSED', 'RESOLVED', 'Italy', 'Vin Diesel', 'SYS027'),
                ('1000130', 'Hailey Morris', '2021-08-25 08:10:00', 'PENDING', 'ON-HOLD', 'Spain', 'Will Smith', 'SYS028'),
                ('1000131', 'Ethan Reed', '2021-09-01 09:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Netherlands', 'Xavier Dolan', 'SYS029'),
                ('1000132', 'Lillian Turner', '2021-09-05 10:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'India', 'Yvonne Strahovski', 'SYS030'),
                ('1000133', 'Wyatt Russell', '2021-09-10 11:40:00', 'OPEN', 'IN-PROGRESS', 'USA', 'Zachary Levi', 'SYS031'),
                ('1000134', 'Madeline Harris', '2021-09-15 12:50:00', 'ASSESS', 'NEW CASE', 'UK', 'Alicia Keys', 'SYS032'),
                ('1000135', 'Carter Lee', '2021-09-20 14:00:00', 'CLOSED', 'RESOLVED', 'Canada', 'Brad Pitt', 'SYS033'),
                ('1000136', 'Aubrey Scott', '2021-09-25 15:10:00', 'PENDING', 'ON-HOLD', 'Australia', 'Cate Blanchett', 'SYS034'),
                ('1000137', 'Isaac Young', '2021-10-01 16:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Germany', 'Daniel Craig', 'SYS035'),
                ('1000138', 'Elena Allen', '2021-10-05 17:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'France', 'Emma Watson', 'SYS036'),
                ('1000139', 'Julian Stewart', '2021-10-10 08:40:00', 'OPEN', 'IN-PROGRESS', 'Italy', 'Freddie Mercury', 'SYS037'),
                ('1000140', 'Piper Foster', '2021-10-15 09:50:00', 'ASSESS', 'NEW CASE', 'Spain', 'Gal Gadot', 'SYS038'),
                ('1000141', 'Roman Collins', '2021-10-20 11:00:00', 'CLOSED', 'RESOLVED', 'Netherlands', 'Hugh Jackman', 'SYS039'),
                ('1000142', 'Aurora Evans', '2021-10-25 12:10:00', 'PENDING', 'ON-HOLD', 'India', 'Idris Elba', 'SYS040'),
                ('1000143', 'Eli Phillips', '2021-11-01 13:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'USA', 'Jennifer Lawrence', 'SYS041'),
                ('1000144', 'Layla Morris', '2021-11-05 14:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'UK', 'Keanu Reeves', 'SYS042'),
                ('1000145', 'Aiden Reed', '2021-11-10 15:40:00', 'OPEN', 'IN-PROGRESS', 'Canada', 'Leonardo DiCaprio', 'SYS043'),
                ('1000146', 'Ruby Turner', '2021-11-15 16:50:00', 'ASSESS', 'NEW CASE', 'Australia', 'Margot Robbie', 'SYS044'),
                ('1000147', 'Henry Russell', '2021-11-20 18:00:00', 'CLOSED', 'RESOLVED', 'Germany', 'Natalie Portman', 'SYS045'),
                ('1000148', 'Sadie Harris', '2021-11-25 08:10:00', 'PENDING', 'ON-HOLD', 'France', 'Octavia Spencer', 'SYS046'),
                ('1000149', 'Jaxon Lee', '2021-12-01 09:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Italy', 'Paul Rudd', 'SYS047'),
                ('1000150', 'Paisley Scott', '2021-12-05 10:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Spain', 'Queen Latifah', 'SYS048'),
                ('1000151', 'Everly Young', '2021-12-10 11:40:00', 'OPEN', 'IN-PROGRESS', 'Netherlands', 'Robert Downey Jr.', 'SYS049'),
                ('1000152', 'Lincoln Allen', '2021-12-15 12:50:00', 'ASSESS', 'NEW CASE', 'India', 'Sandra Bullock', 'SYS050'),
                ('1000153', 'Ellie Stewart', '2021-12-20 14:00:00', 'CLOSED', 'RESOLVED', 'USA', 'Tom Hanks', 'SYS051'),
                ('1000154', 'Gabriel Foster', '2021-12-25 15:10:00', 'PENDING', 'ON-HOLD', 'UK', 'Uma Thurman', 'SYS052'),
                ('1000155', 'Penelope Collins', '2022-01-01 16:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Canada', 'Vin Diesel', 'SYS053'),
                ('1000156', 'Hudson Evans', '2022-01-05 17:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Australia', 'Will Smith', 'SYS054'),
                ('1000157', 'Savannah Phillips', '2022-01-10 08:40:00', 'OPEN', 'IN-PROGRESS', 'Germany', 'Xavier Dolan', 'SYS055'),
                ('1000158', 'Levi Morris', '2022-01-15 09:50:00', 'ASSESS', 'NEW CASE', 'France', 'Yvonne Strahovski', 'SYS056'),
                ('1000159', 'Stella Reed', '2022-01-20 11:00:00', 'CLOSED', 'RESOLVED', 'Italy', 'Zachary Levi', 'SYS057'),
                ('1000160', 'Nathan Turner', '2022-01-25 12:10:00', 'PENDING', 'ON-HOLD', 'Spain', 'Alicia Keys', 'SYS058'),
                ('1000161', 'Brooklyn Russell', '2022-02-01 13:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Netherlands', 'Brad Pitt', 'SYS059'),
                ('1000162', 'Zachary Harris', '2022-02-05 14:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'India', 'Cate Blanchett', 'SYS060'),
                ('1000163', 'Ariana Lee', '2022-02-10 15:40:00', 'OPEN', 'IN-PROGRESS', 'USA', 'Daniel Craig', 'SYS061'),
                ('1000164', 'Mason Scott', '2022-02-15 16:50:00', 'ASSESS', 'NEW CASE', 'UK', 'Emma Watson', 'SYS062'),
                ('1000165', 'Hailey Young', '2022-02-20 18:00:00', 'CLOSED', 'RESOLVED', 'Canada', 'Freddie Mercury', 'SYS063'),
                ('1000166', 'Ethan Allen', '2022-02-25 08:10:00', 'PENDING', 'ON-HOLD', 'Australia', 'Gal Gadot', 'SYS064'),
                ('1000167', 'Lillian Stewart', '2022-03-01 09:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Germany', 'Hugh Jackman', 'SYS065'),
                ('1000168', 'Wyatt Foster', '2022-03-05 10:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'France', 'Idris Elba', 'SYS066'),
                ('1000169', 'Madeline Collins', '2022-03-10 11:40:00', 'OPEN', 'IN-PROGRESS', 'Italy', 'Jennifer Lawrence', 'SYS067'),
                ('1000170', 'Carter Evans', '2022-03-15 12:50:00', 'ASSESS', 'NEW CASE', 'Spain', 'Keanu Reeves', 'SYS068'),
                ('1000171', 'Aubrey Phillips', '2022-03-20 14:00:00', 'CLOSED', 'RESOLVED', 'Netherlands', 'Leonardo DiCaprio', 'SYS069'),
                ('1000172', 'Isaac Morris', '2022-03-25 15:10:00', 'PENDING', 'ON-HOLD', 'India', 'Margot Robbie', 'SYS070'),
                ('1000173', 'Elena Reed', '2022-04-01 16:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'USA', 'Natalie Portman', 'SYS071'),
                ('1000174', 'Julian Turner', '2022-04-05 17:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'UK', 'Octavia Spencer', 'SYS072'),
                ('1000175', 'Piper Russell', '2022-04-10 08:40:00', 'OPEN', 'IN-PROGRESS', 'Canada', 'Paul Rudd', 'SYS073'),
                ('1000176', 'Roman Harris', '2022-04-15 09:50:00', 'ASSESS', 'NEW CASE', 'Australia', 'Queen Latifah', 'SYS074'),
                ('1000177', 'Aurora Lee', '2022-04-20 11:00:00', 'CLOSED', 'RESOLVED', 'Germany', 'Robert Downey Jr.', 'SYS075'),
                ('1000178', 'Eli Scott', '2022-04-25 12:10:00', 'PENDING', 'ON-HOLD', 'France', 'Sandra Bullock', 'SYS076'),
                ('1000179', 'Layla Young', '2022-05-01 13:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Italy', 'Tom Hanks', 'SYS077'),
                ('1000180', 'Aiden Allen', '2022-05-05 14:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Spain', 'Uma Thurman', 'SYS078'),
                ('1000181', 'Ruby Stewart', '2022-05-10 15:40:00', 'OPEN', 'IN-PROGRESS', 'Netherlands', 'Vin Diesel', 'SYS079'),
                ('1000182', 'Henry Foster', '2022-05-15 16:50:00', 'ASSESS', 'NEW CASE', 'India', 'Will Smith', 'SYS080'),
                ('1000183', 'Sadie Collins', '2022-05-20 18:00:00', 'CLOSED', 'RESOLVED', 'USA', 'Xavier Dolan', 'SYS081'),
                ('1000184', 'Jaxon Evans', '2022-05-25 08:10:00', 'PENDING', 'ON-HOLD', 'UK', 'Yvonne Strahovski', 'SYS082'),
                ('1000185', 'Paisley Phillips', '2022-06-01 09:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Canada', 'Zachary Levi', 'SYS083'),
                ('1000186', 'Everly Morris', '2022-06-05 10:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Australia', 'Alicia Keys', 'SYS084'),
                ('1000187', 'Lincoln Reed', '2022-06-10 11:40:00', 'OPEN', 'IN-PROGRESS', 'Germany', 'Brad Pitt', 'SYS085'),
                ('1000188', 'Ellie Turner', '2022-06-15 12:50:00', 'ASSESS', 'NEW CASE', 'France', 'Cate Blanchett', 'SYS086'),
                ('1000189', 'Gabriel Russell', '2022-06-20 14:00:00', 'CLOSED', 'RESOLVED', 'Italy', 'Daniel Craig', 'SYS087'),
                ('1000190', 'Penelope Harris', '2022-06-25 15:10:00', 'PENDING', 'ON-HOLD', 'Spain', 'Emma Watson', 'SYS088'),
                ('1000191', 'Hudson Lee', '2022-07-01 16:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Netherlands', 'Freddie Mercury', 'SYS089'),
                ('1000192', 'Savannah Scott', '2022-07-05 17:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'India', 'Gal Gadot', 'SYS090'),
                ('1000193', 'Levi Young', '2022-07-10 08:40:00', 'OPEN', 'IN-PROGRESS', 'USA', 'Hugh Jackman', 'SYS091'),
                ('1000194', 'Stella Allen', '2022-07-15 09:50:00', 'ASSESS', 'NEW CASE', 'UK', 'Idris Elba', 'SYS092'),
                ('1000195', 'Nathan Stewart', '2022-07-20 11:00:00', 'CLOSED', 'RESOLVED', 'Canada', 'Jennifer Lawrence', 'SYS093'),
                ('1000196', 'Brooklyn Foster', '2022-07-25 12:10:00', 'PENDING', 'ON-HOLD', 'Australia', 'Keanu Reeves', 'SYS094'),
                ('1000197', 'Zachary Collins', '2022-08-01 13:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Germany', 'Leonardo DiCaprio', 'SYS095'),
                ('1000198', 'Ariana Evans', '2022-08-05 14:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'France', 'Margot Robbie', 'SYS096'),
                ('1000199', 'Mason Phillips', '2022-08-10 15:40:00', 'OPEN', 'IN-PROGRESS', 'Italy', 'Natalie Portman', 'SYS097'),
                ('1000200', 'Hailey Morris', '2022-08-15 16:50:00', 'ASSESS', 'NEW CASE', 'Spain', 'Octavia Spencer', 'SYS098'),
                ('1000201', 'Ethan Reed', '2022-08-20 18:00:00', 'CLOSED', 'RESOLVED', 'Netherlands', 'Paul Rudd', 'SYS099'),
                ('1000202', 'Lillian Turner', '2022-08-25 08:10:00', 'PENDING', 'ON-HOLD', 'India', 'Queen Latifah', 'SYS001'),
                ('1000203', 'Wyatt Russell', '2022-09-01 09:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'USA', 'Robert Downey Jr.', 'SYS002'),
                ('1000204', 'Madeline Harris', '2022-09-05 10:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'UK', 'Sandra Bullock', 'SYS003'),
                ('1000205', 'Carter Lee', '2022-09-10 11:40:00', 'OPEN', 'IN-PROGRESS', 'Canada', 'Tom Hanks', 'SYS004'),
                ('1000206', 'Aubrey Scott', '2022-09-15 12:50:00', 'ASSESS', 'NEW CASE', 'Australia', 'Uma Thurman', 'SYS005'),
                ('1000207', 'Isaac Young', '2022-09-20 14:00:00', 'CLOSED', 'RESOLVED', 'Germany', 'Vin Diesel', 'SYS006'),
                ('1000208', 'Elena Allen', '2022-09-25 15:10:00', 'PENDING', 'ON-HOLD', 'France', 'Will Smith', 'SYS007'),
                ('1000209', 'Julian Stewart', '2022-10-01 16:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Italy', 'Xavier Dolan', 'SYS008'),
                ('1000210', 'Piper Foster', '2022-10-05 17:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Spain', 'Yvonne Strahovski', 'SYS009'),
                ('1000211', 'Roman Collins', '2022-10-10 08:40:00', 'OPEN', 'IN-PROGRESS', 'Netherlands', 'Zachary Levi', 'SYS010'),
                ('1000212', 'Aurora Evans', '2022-10-15 09:50:00', 'ASSESS', 'NEW CASE', 'India', 'Alicia Keys', 'SYS011'),
                ('1000213', 'Eli Phillips', '2022-10-20 11:00:00', 'CLOSED', 'RESOLVED', 'USA', 'Brad Pitt', 'SYS012'),
                ('1000214', 'Layla Morris', '2022-10-25 12:10:00', 'PENDING', 'ON-HOLD', 'UK', 'Cate Blanchett', 'SYS013'),
                ('1000215', 'Aiden Reed', '2022-11-01 13:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Canada', 'Daniel Craig', 'SYS014'),
                ('1000216', 'Ruby Turner', '2022-11-05 14:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Australia', 'Emma Watson', 'SYS015'),
                ('1000217', 'Henry Russell', '2022-11-10 15:40:00', 'OPEN', 'IN-PROGRESS', 'Germany', 'Freddie Mercury', 'SYS016'),
                ('1000218', 'Sadie Harris', '2022-11-15 16:50:00', 'ASSESS', 'NEW CASE', 'France', 'Gal Gadot', 'SYS017'),
                ('1000219', 'Jaxon Lee', '2022-11-20 18:00:00', 'CLOSED', 'RESOLVED', 'Italy', 'Hugh Jackman', 'SYS018'),
                ('1000220', 'Paisley Scott', '2022-11-25 08:10:00', 'PENDING', 'ON-HOLD', 'Spain', 'Idris Elba', 'SYS019'),
                ('1000221', 'Everly Young', '2022-12-01 09:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Netherlands', 'Jennifer Lawrence', 'SYS020'),
                ('1000222', 'Lincoln Allen', '2022-12-05 10:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'India', 'Keanu Reeves', 'SYS021'),
                ('1000223', 'Ellie Stewart', '2022-12-10 11:40:00', 'OPEN', 'IN-PROGRESS', 'USA', 'Leonardo DiCaprio', 'SYS022'),
                ('1000224', 'Gabriel Foster', '2022-12-15 12:50:00', 'ASSESS', 'NEW CASE', 'UK', 'Margot Robbie', 'SYS023'),
                ('1000225', 'Penelope Collins', '2022-12-20 14:00:00', 'CLOSED', 'RESOLVED', 'Canada', 'Natalie Portman', 'SYS024'),
                ('1000226', 'Hudson Evans', '2022-12-25 15:10:00', 'PENDING', 'ON-HOLD', 'Australia', 'Octavia Spencer', 'SYS025'),
                ('1000227', 'Savannah Phillips', '2023-01-01 16:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Germany', 'Paul Rudd', 'SYS026'),
                ('1000228', 'Levi Morris', '2023-01-05 17:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'France', 'Queen Latifah', 'SYS027'),
                ('1000229', 'Stella Reed', '2023-01-10 08:40:00', 'OPEN', 'IN-PROGRESS', 'Italy', 'Robert Downey Jr.', 'SYS028'),
                ('1000230', 'Nathan Turner', '2023-01-15 09:50:00', 'ASSESS', 'NEW CASE', 'Spain', 'Sandra Bullock', 'SYS029'),
                ('1000231', 'Brooklyn Russell', '2023-01-20 11:00:00', 'CLOSED', 'RESOLVED', 'Netherlands', 'Tom Hanks', 'SYS030'),
                ('1000232', 'Zachary Harris', '2023-01-25 12:10:00', 'PENDING', 'ON-HOLD', 'India', 'Uma Thurman', 'SYS031'),
                ('1000233', 'Ariana Lee', '2023-02-01 13:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'USA', 'Vin Diesel', 'SYS032'),
                ('1000234', 'Mason Scott', '2023-02-05 14:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'UK', 'Will Smith', 'SYS033'),
                ('1000235', 'Hailey Young', '2023-02-10 15:40:00', 'OPEN', 'IN-PROGRESS', 'Canada', 'Xavier Dolan', 'SYS034'),
                ('1000236', 'Ethan Allen', '2023-02-15 16:50:00', 'ASSESS', 'NEW CASE', 'Australia', 'Yvonne Strahovski', 'SYS035'),
                ('1000237', 'Lillian Stewart', '2023-02-20 18:00:00', 'CLOSED', 'RESOLVED', 'Germany', 'Zachary Levi', 'SYS036'),
                ('1000238', 'Wyatt Foster', '2023-02-25 08:10:00', 'PENDING', 'ON-HOLD', 'France', 'Alicia Keys', 'SYS037'),
                ('1000239', 'Madeline Collins', '2023-03-01 09:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Italy', 'Brad Pitt', 'SYS038'),
                ('1000240', 'Carter Evans', '2023-03-05 10:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Spain', 'Cate Blanchett', 'SYS039'),
                ('1000241', 'Aubrey Phillips', '2023-03-10 11:40:00', 'OPEN', 'IN-PROGRESS', 'Netherlands', 'Daniel Craig', 'SYS040'),
                ('1000242', 'Isaac Morris', '2023-03-15 12:50:00', 'ASSESS', 'NEW CASE', 'India', 'Emma Watson', 'SYS041'),
                ('1000243', 'Elena Reed', '2023-03-20 14:00:00', 'CLOSED', 'RESOLVED', 'USA', 'Freddie Mercury', 'SYS042'),
                ('1000244', 'Julian Turner', '2023-03-25 15:10:00', 'PENDING', 'ON-HOLD', 'UK', 'Gal Gadot', 'SYS043'),
                ('1000245', 'Piper Russell', '2023-04-01 16:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Canada', 'Hugh Jackman', 'SYS044'),
                ('1000246', 'Roman Harris', '2023-04-05 17:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Australia', 'Idris Elba', 'SYS045'),
                ('1000247', 'Aurora Lee', '2023-04-10 08:40:00', 'OPEN', 'IN-PROGRESS', 'Germany', 'Jennifer Lawrence', 'SYS046'),
                ('1000248', 'Eli Scott', '2023-04-15 09:50:00', 'ASSESS', 'NEW CASE', 'France', 'Keanu Reeves', 'SYS047'),
                ('1000249', 'Layla Young', '2023-04-20 11:00:00', 'CLOSED', 'RESOLVED', 'Italy', 'Leonardo DiCaprio', 'SYS048'),
                ('1000250', 'Aiden Allen', '2023-04-25 12:10:00', 'PENDING', 'ON-HOLD', 'Spain', 'Margot Robbie', 'SYS049'),
                ('1000251', 'Ruby Stewart', '2023-05-01 13:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Netherlands', 'Natalie Portman', 'SYS050'),
                ('1000252', 'Henry Foster', '2023-05-05 14:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'India', 'Octavia Spencer', 'SYS051'),
                ('1000253', 'Sadie Collins', '2023-05-10 15:40:00', 'OPEN', 'IN-PROGRESS', 'USA', 'Paul Rudd', 'SYS052'),
                ('1000254', 'Jaxon Evans', '2023-05-15 16:50:00', 'ASSESS', 'NEW CASE', 'UK', 'Queen Latifah', 'SYS053'),
                ('1000255', 'Paisley Phillips', '2023-05-20 18:00:00', 'CLOSED', 'RESOLVED', 'Canada', 'Robert Downey Jr.', 'SYS054'),
                ('1000256', 'Everly Morris', '2023-05-25 08:10:00', 'PENDING', 'ON-HOLD', 'Australia', 'Sandra Bullock', 'SYS055'),
                ('1000257', 'Lincoln Reed', '2023-06-01 09:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Germany', 'Tom Hanks', 'SYS056'),
                ('1000258', 'Ellie Turner', '2023-06-05 10:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'France', 'Uma Thurman', 'SYS057'),
                ('1000259', 'Gabriel Russell', '2023-06-10 11:40:00', 'OPEN', 'IN-PROGRESS', 'Italy', 'Vin Diesel', 'SYS058'),
                ('1000260', 'Penelope Harris', '2023-06-15 12:50:00', 'ASSESS', 'NEW CASE', 'Spain', 'Will Smith', 'SYS059'),
                ('1000261', 'Hudson Lee', '2023-06-20 14:00:00', 'CLOSED', 'RESOLVED', 'Netherlands', 'Xavier Dolan', 'SYS060'),
                ('1000262', 'Savannah Scott', '2023-06-25 15:10:00', 'PENDING', 'ON-HOLD', 'India', 'Yvonne Strahovski', 'SYS061'),
                ('1000263', 'Levi Young', '2023-07-01 16:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'USA', 'Zachary Levi', 'SYS062'),
                ('1000264', 'Stella Allen', '2023-07-05 17:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'UK', 'Alicia Keys', 'SYS063'),
                ('1000265', 'Nathan Stewart', '2023-07-10 08:40:00', 'OPEN', 'IN-PROGRESS', 'Canada', 'Brad Pitt', 'SYS064'),
                ('1000266', 'Brooklyn Foster', '2023-07-15 09:50:00', 'ASSESS', 'NEW CASE', 'Australia', 'Cate Blanchett', 'SYS065'),
                ('1000267', 'Zachary Collins', '2023-07-20 11:00:00', 'CLOSED', 'RESOLVED', 'Germany', 'Daniel Craig', 'SYS066'),
                ('1000268', 'Ariana Evans', '2023-07-25 12:10:00', 'PENDING', 'ON-HOLD', 'France', 'Emma Watson', 'SYS067'),
                ('1000269', 'Mason Phillips', '2023-08-01 13:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Italy', 'Freddie Mercury', 'SYS068'),
                ('1000270', 'Hailey Morris', '2023-08-05 14:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Spain', 'Gal Gadot', 'SYS069'),
                ('1000271', 'Ethan Reed', '2023-08-10 15:40:00', 'OPEN', 'IN-PROGRESS', 'Netherlands', 'Hugh Jackman', 'SYS070'),
                ('1000272', 'Lillian Turner', '2023-08-15 16:50:00', 'ASSESS', 'NEW CASE', 'India', 'Idris Elba', 'SYS071'),
                ('1000273', 'Wyatt Russell', '2023-08-20 18:00:00', 'CLOSED', 'RESOLVED', 'USA', 'Jennifer Lawrence', 'SYS072'),
                ('1000274', 'Madeline Harris', '2023-08-25 08:10:00', 'PENDING', 'ON-HOLD', 'UK', 'Keanu Reeves', 'SYS073'),
                ('1000275', 'Carter Lee', '2023-09-01 09:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Canada', 'Leonardo DiCaprio', 'SYS074'),
                ('1000276', 'Aubrey Scott', '2023-09-05 10:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Australia', 'Margot Robbie', 'SYS075'),
                ('1000277', 'Isaac Young', '2023-09-10 11:40:00', 'OPEN', 'IN-PROGRESS', 'Germany', 'Natalie Portman', 'SYS076'),
                ('1000278', 'Elena Allen', '2023-09-15 12:50:00', 'ASSESS', 'NEW CASE', 'France', 'Octavia Spencer', 'SYS077'),
                ('1000279', 'Julian Stewart', '2023-09-20 14:00:00', 'CLOSED', 'RESOLVED', 'Italy', 'Paul Rudd', 'SYS078'),
                ('1000280', 'Piper Foster', '2023-09-25 15:10:00', 'PENDING', 'ON-HOLD', 'Spain', 'Queen Latifah', 'SYS079'),
                ('1000281', 'Roman Collins', '2023-10-01 16:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Netherlands', 'Robert Downey Jr.', 'SYS080'),
                ('1000282', 'Aurora Evans', '2023-10-05 17:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'India', 'Sandra Bullock', 'SYS081'),
                ('1000283', 'Eli Phillips', '2023-10-10 08:40:00', 'OPEN', 'IN-PROGRESS', 'USA', 'Tom Hanks', 'SYS082'),
                ('1000284', 'Layla Morris', '2023-10-15 09:50:00', 'ASSESS', 'NEW CASE', 'UK', 'Uma Thurman', 'SYS083'),
                ('1000285', 'Aiden Reed', '2023-10-20 11:00:00', 'CLOSED', 'RESOLVED', 'Canada', 'Vin Diesel', 'SYS084'),
                ('1000286', 'Ruby Turner', '2023-10-25 12:10:00', 'PENDING', 'ON-HOLD', 'Australia', 'Will Smith', 'SYS085'),
                ('1000287', 'Henry Russell', '2023-11-01 13:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Germany', 'Xavier Dolan', 'SYS086'),
                ('1000288', 'Sadie Harris', '2023-11-05 14:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'France', 'Yvonne Strahovski', 'SYS087'),
                ('1000289', 'Jaxon Lee', '2023-11-10 15:40:00', 'OPEN', 'IN-PROGRESS', 'Italy', 'Zachary Levi', 'SYS088'),
                ('1000290', 'Paisley Scott', '2023-11-15 16:50:00', 'ASSESS', 'NEW CASE', 'Spain', 'Alicia Keys', 'SYS089'),
                ('1000291', 'Everly Young', '2023-11-20 18:00:00', 'CLOSED', 'RESOLVED', 'Netherlands', 'Brad Pitt', 'SYS090'),
                ('1000292', 'Lincoln Allen', '2023-11-25 08:10:00', 'PENDING', 'ON-HOLD', 'India', 'Cate Blanchett', 'SYS091'),
                ('1000293', 'Ellie Stewart', '2023-12-01 09:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'USA', 'Daniel Craig', 'SYS092'),
                ('1000294', 'Gabriel Foster', '2023-12-05 10:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'UK', 'Emma Watson', 'SYS093'),
                ('1000295', 'Penelope Collins', '2023-12-10 11:40:00', 'OPEN', 'IN-PROGRESS', 'Canada', 'Freddie Mercury', 'SYS094'),
                ('1000296', 'Hudson Evans', '2023-12-15 12:50:00', 'ASSESS', 'NEW CASE', 'Australia', 'Gal Gadot', 'SYS095'),
                ('1000297', 'Savannah Phillips', '2023-12-20 14:00:00', 'CLOSED', 'RESOLVED', 'Germany', 'Hugh Jackman', 'SYS096'),
                ('1000298', 'Levi Morris', '2023-12-25 15:10:00', 'PENDING', 'ON-HOLD', 'France', 'Idris Elba', 'SYS097'),
                ('1000299', 'Stella Reed', '2024-01-01 16:20:00', 'ESCALATED', 'ESCALATED-URGENT', 'Italy', 'Jennifer Lawrence', 'SYS098'),
                ('1000300', 'Nathan Turner', '2024-01-05 17:30:00', 'CLOSED-RISK RELEVANT', 'CLOSED-NOT RISK RELEVANT', 'Spain', 'Keanu Reeves', 'SYS099'),
            ],
        )
    
    cur.execute("""DROP TABLE IF EXISTS AMLevent;""")
    cur.execute("""
    CREATE TABLE AMLevent (
        EVENT_ID         VARCHAR(100) PRIMARY KEY,
        create_date      DATETIME NOT NULL,
        event_Status      VARCHAR(30),
        event_description VARCHAR(50)  
    );
    """)
    cur.execute("SELECT COUNT(*) FROM AMLevent")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO AMLevent (EVENT_ID, create_date, event_Status, event_description) VALUES (?, ?, ?, ?);",
            [
                ('EVT0001','2024-01-01 09:00:00','OPEN','Large deposit detected'),
                ('EVT0002','2024-01-02 09:00:00','PENDING','Wire transfer flagged'),
                ('EVT0003','2024-01-03 09:00:00','CLOSED','Multiple failed logins'),
                ('EVT0004','2024-01-04 09:00:00','REVIEW','Account mismatch'),
                ('EVT0005','2024-01-05 09:00:00','ESCALATED','Unusual cash withdrawal'),
                ('EVT0006','2024-01-06 09:00:00','OPEN','KYC documents required'),
                ('EVT0007','2024-01-07 09:00:00','PENDING','Suspicious merchant activity'),
                ('EVT0008','2024-01-08 09:00:00','CLOSED','Sanctions list hit'),
                ('EVT0009','2024-01-09 09:00:00','REVIEW','High-risk country transfer'),
                ('EVT0010','2024-01-10 09:00:00','ESCALATED','Automated rule triggered'),
                ('EVT0011','2024-01-11 09:00:00','OPEN','Large deposit detected'),
                ('EVT0012','2024-01-12 09:00:00','PENDING','Wire transfer flagged'),
                ('EVT0013','2024-01-13 09:00:00','CLOSED','Multiple failed logins'),
                ('EVT0014','2024-01-14 09:00:00','REVIEW','Account mismatch'),
                ('EVT0015','2024-01-15 09:00:00','ESCALATED','Unusual cash withdrawal'),
                ('EVT0016','2024-01-16 09:00:00','OPEN','KYC documents required'),
                ('EVT0017','2024-01-17 09:00:00','PENDING','Suspicious merchant activity'),
                ('EVT0018','2024-01-18 09:00:00','CLOSED','Sanctions list hit'),
                ('EVT0019','2024-01-19 09:00:00','REVIEW','High-risk country transfer'),
                ('EVT0020','2024-01-20 09:00:00','ESCALATED','Automated rule triggered'),
                ('EVT0021','2024-01-21 09:00:00','OPEN','Large deposit detected'),
                ('EVT0022','2024-01-22 09:00:00','PENDING','Wire transfer flagged'),
                ('EVT0023','2024-01-23 09:00:00','CLOSED','Multiple failed logins'),
                ('EVT0024','2024-01-24 09:00:00','REVIEW','Account mismatch'),
                ('EVT0025','2024-01-25 09:00:00','ESCALATED','Unusual cash withdrawal'),
                ('EVT0026','2024-01-26 09:00:00','OPEN','KYC documents required'),
                ('EVT0027','2024-01-27 09:00:00','PENDING','Suspicious merchant activity'),
                ('EVT0028','2024-01-28 09:00:00','CLOSED','Sanctions list hit'),
                ('EVT0029','2024-01-29 09:00:00','REVIEW','High-risk country transfer'),
                ('EVT0030','2024-01-30 09:00:00','ESCALATED','Automated rule triggered'),
                ('EVT0031','2024-01-31 09:00:00','OPEN','Large deposit detected'),
                ('EVT0032','2024-02-01 09:00:00','PENDING','Wire transfer flagged'),
                ('EVT0033','2024-02-02 09:00:00','CLOSED','Multiple failed logins'),
                ('EVT0034','2024-02-03 09:00:00','REVIEW','Account mismatch'),
                ('EVT0035','2024-02-04 09:00:00','ESCALATED','Unusual cash withdrawal'),
                ('EVT0036','2024-02-05 09:00:00','OPEN','KYC documents required'),
                ('EVT0037','2024-02-06 09:00:00','PENDING','Suspicious merchant activity'),
                ('EVT0038','2024-02-07 09:00:00','CLOSED','Sanctions list hit'),
                ('EVT0039','2024-02-08 09:00:00','REVIEW','High-risk country transfer'),
                ('EVT0040','2024-02-09 09:00:00','ESCALATED','Automated rule triggered'),
                ('EVT0041','2024-02-10 09:00:00','OPEN','Large deposit detected'),
                ('EVT0042','2024-02-11 09:00:00','PENDING','Wire transfer flagged'),
                ('EVT0043','2024-02-12 09:00:00','CLOSED','Multiple failed logins'),
                ('EVT0044','2024-02-13 09:00:00','REVIEW','Account mismatch'),
                ('EVT0045','2024-02-14 09:00:00','ESCALATED','Unusual cash withdrawal'),
                ('EVT0046','2024-02-15 09:00:00','OPEN','KYC documents required'),
                ('EVT0047','2024-02-16 09:00:00','PENDING','Suspicious merchant activity'),
                ('EVT0048','2024-02-17 09:00:00','CLOSED','Sanctions list hit'),
                ('EVT0049','2024-02-18 09:00:00','REVIEW','High-risk country transfer'),
                ('EVT0050','2024-02-19 09:00:00','ESCALATED','Automated rule triggered'),
                ('EVT0051','2024-02-20 09:00:00','OPEN','Large deposit detected'),
                ('EVT0052','2024-02-21 09:00:00','PENDING','Wire transfer flagged'),
                ('EVT0053','2024-02-22 09:00:00','CLOSED','Multiple failed logins'),
                ('EVT0054','2024-02-23 09:00:00','REVIEW','Account mismatch'),
                ('EVT0055','2024-02-24 09:00:00','ESCALATED','Unusual cash withdrawal'),
                ('EVT0056','2024-02-25 09:00:00','OPEN','KYC documents required'),
                ('EVT0057','2024-02-26 09:00:00','PENDING','Suspicious merchant activity'),
                ('EVT0058','2024-02-27 09:00:00','CLOSED','Sanctions list hit'),
                ('EVT0059','2024-02-28 09:00:00','REVIEW','High-risk country transfer'),
                ('EVT0060','2024-02-29 09:00:00','ESCALATED','Automated rule triggered'),
                ('EVT0061','2024-03-01 09:00:00','OPEN','Large deposit detected'),
                ('EVT0062','2024-03-02 09:00:00','PENDING','Wire transfer flagged'),
                ('EVT0063','2024-03-03 09:00:00','CLOSED','Multiple failed logins'),
                ('EVT0064','2024-03-04 09:00:00','REVIEW','Account mismatch'),
                ('EVT0065','2024-03-05 09:00:00','ESCALATED','Unusual cash withdrawal'),
                ('EVT0066','2024-03-06 09:00:00','OPEN','KYC documents required'),
                ('EVT0067','2024-03-07 09:00:00','PENDING','Suspicious merchant activity'),
                ('EVT0068','2024-03-08 09:00:00','CLOSED','Sanctions list hit'),
                ('EVT0069','2024-03-09 09:00:00','REVIEW','High-risk country transfer'),
                ('EVT0070','2024-03-10 09:00:00','ESCALATED','Automated rule triggered'),
                ('EVT0071','2024-03-11 09:00:00','OPEN','Large deposit detected'),
                ('EVT0072','2024-03-12 09:00:00','PENDING','Wire transfer flagged'),
                ('EVT0073','2024-03-13 09:00:00','CLOSED','Multiple failed logins'),
                ('EVT0074','2024-03-14 09:00:00','REVIEW','Account mismatch'),
                ('EVT0075','2024-03-15 09:00:00','ESCALATED','Unusual cash withdrawal'),
                ('EVT0076','2024-03-16 09:00:00','OPEN','KYC documents required'),
                ('EVT0077','2024-03-17 09:00:00','PENDING','Suspicious merchant activity'),
                ('EVT0078','2024-03-18 09:00:00','CLOSED','Sanctions list hit'),
                ('EVT0079','2024-03-19 09:00:00','REVIEW','High-risk country transfer'),
                ('EVT0080','2024-03-20 09:00:00','ESCALATED','Automated rule triggered'),
                ('EVT0081','2024-03-21 09:00:00','OPEN','Large deposit detected'),
                ('EVT0082','2024-03-22 09:00:00','PENDING','Wire transfer flagged'),
                ('EVT0083','2024-03-23 09:00:00','CLOSED','Multiple failed logins'),
                ('EVT0084','2024-03-24 09:00:00','REVIEW','Account mismatch'),
                ('EVT0085','2024-03-25 09:00:00','ESCALATED','Unusual cash withdrawal'),
                ('EVT0086','2024-03-26 09:00:00','OPEN','KYC documents required'),
                ('EVT0087','2024-03-27 09:00:00','PENDING','Suspicious merchant activity'),
                ('EVT0088','2024-03-28 09:00:00','CLOSED','Sanctions list hit'),
                ('EVT0089','2024-03-29 09:00:00','REVIEW','High-risk country transfer'),
                ('EVT0090','2024-03-30 09:00:00','ESCALATED','Automated rule triggered'),
                ('EVT0091','2024-03-31 09:00:00','OPEN','Large deposit detected'),
                ('EVT0092','2024-04-01 09:00:00','PENDING','Wire transfer flagged'),
                ('EVT0093','2024-04-02 09:00:00','CLOSED','Multiple failed logins'),
                ('EVT0094','2024-04-03 09:00:00','REVIEW','Account mismatch'),
                ('EVT0095','2024-04-04 09:00:00','ESCALATED','Unusual cash withdrawal'),
                ('EVT0096','2024-04-05 09:00:00','OPEN','KYC documents required'),
                ('EVT0097','2024-04-06 09:00:00','PENDING','Suspicious merchant activity'),
                ('EVT0098','2024-04-07 09:00:00','CLOSED','Sanctions list hit'),
                ('EVT0099','2024-04-08 09:00:00','REVIEW','High-risk country transfer'),
                ('EVT0100','2024-04-09 09:00:00','ESCALATED','Automated rule triggered'),
            ]
        )
    conn.commit()
    conn.close()

def rows_to_json(column_names: List[str], rows: List[tuple]) -> str:
    results: List[Dict[str, Any]] = []
    for row in rows:
        results.append({col: val for col, val in zip(column_names, row)})
    return json.dumps({"rows": results}, default=str)

def run_safe_select(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> str:
    """
    Run a SELECT query and return results as JSON. Only allows SELECT statements.
    """
    sql_strip = sql.strip().lower()
    if not sql_strip.startswith("select"):
        return json.dumps({"error": "Only SELECT statements are allowed for safety."})
    cur = conn.cursor()
    cur.execute(sql, params)
    col_names = [d[0] for d in cur.description] if cur.description else []
    rows = cur.fetchall()
    return rows_to_json(col_names, rows)

def query_db_from_llm(prompt: str, db_path: str = DB_PATH) -> str:
    create_sample_db(db_path)
    conn = sqlite3.connect(db_path)
    try:
        sql = prompt.strip().replace('\n', ' ')
        return run_safe_select(conn, sql)
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        conn.close()

def query_db_from_prompt(prompt: str, db_path: str = DB_PATH) -> str:
    """
    Interpret the user prompt and return matching database rows as a JSON string.

    Supported prompt formats:
    - "sql: SELECT ...": runs the SELECT (only SELECT allowed)
    - "table:<table_name> term:<search_text>": searches common text columns for the term using LIKE

    Returns:
        str: JSON-formatted string with query results or error.
    """
    create_sample_db(db_path)
    conn = sqlite3.connect(db_path)

    try:
        p = prompt.strip()
        if p.lower().startswith("sql:"):
            sql = p[4:].strip()
            return run_safe_select(conn, sql)
        # parse simple table search: table:<name> term:<text>
        table = None
        term = None
        parts = [part.strip() for part in p.split()]  # simple split parser
        for part in parts:
            if part.lower().startswith("table:"):
                table = part.split(":", 1)[1]
            if part.lower().startswith("case_id:"):
                term = part.split(":", 1)[1]
        if table:
            # For safety, only allow known table names (extendable)
            allowed_tables = {"amlcase"}
            if table not in allowed_tables:
                return json.dumps({"error": f"Table '{table}' is not permitted."})
            if term:
                # search in name, email, description columns
                sql = f"SELECT * FROM {table} WHERE case_id LIKE ? "
                like_term = f"%{term}%"
                return run_safe_select(conn, sql, (like_term, ))
            else:
                sql = f"SELECT * FROM {table} LIMIT 100"
                return run_safe_select(conn, sql)
        return json.dumps({"error": "Unrecognized prompt format. Use 'sql:' or 'table:<name> case_id:<text>'."})
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        conn.close()

def answer_with_openai(query, context, model_name="gpt-4o", max_tokens=1000):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    client = OpenAI(api_key=api_key)
    prompt = (
        f"Use the following context to answer the question:\n\n"
        f"""Context:\nCREATE TABLE AMLcase (
            CASE_ID         VARCHAR(100) PRIMARY KEY,
            customer        VARCHAR(255) NOT NULL,
            create_date     DATETIME NOT NULL,
            AAA_Status      VARCHAR(30),
            CASE_Status     VARCHAR(50),
            Event_Country   VARCHAR(100),
            Analyst         VARCHAR(100),
            Source_System   VARCHAR(100)
        )\n\nCREATE TABLE AMLevent (
            EVENT_ID         VARCHAR(100) PRIMARY KEY,
            create_date      DATETIME NOT NULL,
            event_Status      VARCHAR(30),
            event_description VARCHAR(50)  
        )\n\n"""
        f"Question: {query}\n"
        f"Answer:"
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

def get_user_prompt(user_prompt) -> str:
    answer = answer_with_openai(user_prompt, "")
    #print("Answer from OpenAI:")
    #print(answer)

    # Extract SQL between triple single-quotes that start with 'sql'
    # Captures across newlines and trims surrounding whitespace.
    pattern = re.compile(r"```sql\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)
    sql_matches = pattern.findall(answer)

    #print("Extracted SQL queries:")
    #print(sql_matches)

    result_json2 = query_db_from_llm(sql_matches[0])
    #print("Query result (JSON):")
    #print(result_json2)
    return result_json2

if __name__ == "__main__":
    
    user_prompt = input("Please enter your query > ")

    result_json2 = get_user_prompt(user_prompt)
    print(result_json2)