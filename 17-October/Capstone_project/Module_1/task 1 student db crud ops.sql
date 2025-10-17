create database Student_capstone; 

use Student_capstone;

create table students(
StudentID int primary key,
name varchar(50),
age int,
course varchar (50));

insert into students (StudentID,name,age,course)  values 
(101, 'Neha', 21, 'AI'),
(102, 'Arjun', 22, 'ML'),
(103, 'Sophia', 20, 'Data Science'),
(104, 'Ravi', 23, 'AI'),
(105, 'Meena', 21, 'ML');

insert into students (StudentID,name,age,course) values
(106,'Aniket',21,'AI');

update students
set course="ML & DL"
where StudentID=102;

delete from students
where StudentID =106;

select * from students 
where course="AI"
