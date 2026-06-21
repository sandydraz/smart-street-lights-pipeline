create database SmartLightsDB ;
use SmartLightsDB;

create table Admins(
Adm_id varchar(10) primary key,
Name varchar(100),
Phone varchar(50),
Email varchar(100)
);


create table Technicians(
Tech_id varchar(10) primary key,
Name varchar(100),
Phone varchar(11),
Specialty varchar(50)
);

create table SLights(
Li_id varchar(10) primary key,
Location varchar(200),
Brightness_level int,
Status varchar(50),
Install_date datetime
);

create table Sensors(
S_id varchar(10) primary key,
Type varchar(30),
Li_id varchar(10),
Status varchar(20),
foreign key (Li_id) references SLights(Li_id)
);

create table Faults(
F_id varchar(10) primary key,
Li_id varchar(10),
F_type varchar(100),
Severity varchar(20),
Timestamp datetime,
Resolved bit,
foreign key (Li_id) references SLights(Li_id)
);

create table Commands(
C_id varchar(10) primary key,
Adm_id varchar(10),
Li_id varchar(10),
C_type varchar(50),
Timestamp datetime,
Status varchar(20),
foreign key (Adm_id) references Admins(Adm_id),
foreign key (Li_id) references SLights(Li_id)
);

create table Sensor_readings(
R_id varchar(10) primary key,
S_id varchar(10),
Li_id varchar(10),
Timestamp datetime,
Motion_detection bit,
Light_level float,
foreign key (S_id) references Sensors(S_id),
foreign key (Li_id) references SLights(Li_id)
);

alter table Sensor_readings
alter column Motion_detection varchar(10);

create table Maintenance_tasks(
Task_id varchar(10) primary key,
Tech_id varchar(10),
F_id varchar(10),
Li_id varchar(10),
Description varchar(200),
Start_date datetime,
End_date datetime,
Status varchar(20),
foreign key (Tech_id) references Technicians(Tech_id),
foreign key (F_id) references Faults(F_id),
foreign key (Li_id) references SLights(Li_id)
);


use SmartLightsDB;
select top 5 * from Sensor_readings order by R_id DESC;