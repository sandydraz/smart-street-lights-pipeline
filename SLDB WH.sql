CREATE DATABASE SmartLightsDW;
USE SmartLightsDW;


-- ── Dimensions ──────────────────────────────────────

CREATE TABLE Dim_Date (
    Date_id    INT PRIMARY KEY,
    FullDate   DATETIME,
    Hour       INT,
    Day        INT,
    Month      INT,
    Year       INT,
    DayName    VARCHAR(20),
    IsWeekend  BIT,
    TimeOfDay  VARCHAR(20)  -- 'Morning','Afternoon','Evening','Night'
);

CREATE TABLE Dim_Light (
    Li_id         VARCHAR(10) PRIMARY KEY,
    Location         VARCHAR(200),
    Brightness_level INT,
    Status           VARCHAR(20),
    Install_date     DATETIME
);

CREATE TABLE Dim_Sensor (
    S_id     VARCHAR(10) PRIMARY KEY,
    Type     VARCHAR(30),
    Li_id VARCHAR(10),
    Status   VARCHAR(20)
);

CREATE TABLE Dim_Technician (
    Tech_id      VARCHAR(10) PRIMARY KEY,
    Name      VARCHAR(100),
    Phone     VARCHAR(20),
    Specialty VARCHAR(50)
);

CREATE TABLE Dim_Admin (
    Adm_id  VARCHAR(10) PRIMARY KEY,
    Name  VARCHAR(100),
    Phone VARCHAR(20),
    Email VARCHAR(100)
);

-- ── Fact Tables ─────────────────────────────────────

CREATE TABLE Fact_Sensor_Readings (
    Reading_id       VARCHAR(10) PRIMARY KEY,
    S_id             VARCHAR(10) FOREIGN KEY REFERENCES Dim_Sensor(S_id),
    Li_id         VARCHAR(10) FOREIGN KEY REFERENCES Dim_Light(Li_id),
    Date_id          INT         FOREIGN KEY REFERENCES Dim_Date(Date_id),
    Motion_detection BIT,
    Light_level      FLOAT
);
alter table Fact_Sensor_Readings
alter column Motion_detection varchar(10);

CREATE TABLE Fact_Maintenance (
    Task_id        VARCHAR(10) PRIMARY KEY,
    Tech_id           VARCHAR(10) FOREIGN KEY REFERENCES Dim_Technician(Tech_id),
    Li_id       VARCHAR(10) FOREIGN KEY REFERENCES Dim_Light(Li_id),
    Date_id        INT         FOREIGN KEY REFERENCES Dim_Date(Date_id),
    Description    VARCHAR(200),
    Duration_hours FLOAT,
    Status         VARCHAR(20)
);

CREATE TABLE Fact_Commands (
    C_id     VARCHAR(10) PRIMARY KEY,
    Adm_id     VARCHAR(10) FOREIGN KEY REFERENCES Dim_Admin(Adm_id),
    Li_id VARCHAR(10) FOREIGN KEY REFERENCES Dim_Light(Li_id),
    Date_id  INT         FOREIGN KEY REFERENCES Dim_Date(Date_id),
    C_type   VARCHAR(50),
    Status   VARCHAR(20)
);




SELECT 'Dim_Admin' as TableName, COUNT(*) as Records FROM Dim_Admin
UNION ALL
SELECT 'Dim_Technician', COUNT(*) FROM Dim_Technician
UNION ALL
SELECT 'Dim_Light', COUNT(*) FROM Dim_Light
UNION ALL
SELECT 'Dim_Sensor', COUNT(*) FROM Dim_Sensor
UNION ALL
SELECT 'Dim_Date', COUNT(*) FROM Dim_Date
UNION ALL
SELECT 'Fact_Sensor_Readings', COUNT(*) FROM Fact_Sensor_Readings
UNION ALL
SELECT 'Fact_Commands', COUNT(*) FROM Fact_Commands
UNION ALL
SELECT 'Fact_Maintenance', COUNT(*) FROM Fact_Maintenance;


USE SmartLightsDW;
select top 5 * from Fact_Sensor_Readings order by Reading_id DESC;