drop table if exists FoodTable;
Create Table FoodTable (
  foodbank_ID int primary key not null,
  name varchar(255) not null,
  address varchar(255) not null,
  pplServedMonthly varchar(255),
  DateFounded Date, 
  ownerEmail varchar(255) not null
);

drop table if exists Staff;
Create Table Staff(
  fulltime bool not null,
  firstname varchar(255) not null,
  lastname varchar(255) not null,
  birthday date,
  salary int not null,
  address varchar(255),
  email varchar(255) primary key,
  yearsAtBank varchar(255),
  WorkAddr varchar(255) not null,
  foodbank_ID int not null
);

/*firstName,lastName,phone_number,address,email,hoursVolunteeredWeekly,volunteerID */
  
drop table if exists Volunteer;
Create Table Volunteer(
  firstname varchar(255) not null,
  lastname varchar(255) not null,
  phonenum int not null,
  address varchar(255),
  email varchar(255) primary key,
  hoursvolunteered int
);

drop table if exists VolunteerSession;
Create Table VolunteerSession(
  volunteeremail varchar(255) not null,
  datevolunteered date not null,
  hours int not null,
  foodbankaddr varchar(255) not null,
  constraint volSession primary key (volunteeremail, datevolunteered)
);
/*visitorID,dateVisited,hours,foodbankAddress,foodbankID
*/
drop table if exists VisitorVisited;
Create Table VisitorVisited(
  visitorID varchar(255) not null,
  datevisited date not null,
  hours int not null,
  foodbankaddr varchar(255) not null,
  constraint visSession primary key (visitorID, datevisited)
  foodbankID int,
);

drop table if exists GeoData;
Create Table GeoData (
  percentfoodinsecure float not null,
  city varchar(255) not null primary key,
  state varchar(255) not null,
  population int not null,
  avgincome int not null
);

drop table if exists Ammenities;
Create Table Ammenities (
  FoodBankAddr varchar(255),
  description varchar(1024)
);
/*foodbankID,ownerFirst,ownerLast,ownerEmail,income*/
drop table if exists Owner;
Create Table Owner(
  foodbankID int not null,
  email varchar(255) primary key not null,
  name varchar(255) not null,
  income int
);

drop table if exists Visitors;
Create Table Visitors(
  numOfChildren int not null,
  age int not null,
  firstname varchar(255) not null,
  lastname varchar(255) not null,
  numofvisits int not null,
  visitorid int not null
);
/*reviewerID,foodbankID,reviewerEmail,foodbankName,numberOfStars */
  
drop table if exists Rating;
Create Table Rating(
  ReviewerEmail varchar(255) not null,
  foodbank varchar(255) not null,
  CONSTRAINT review PRIMARY KEY (ReviewerEmail, foodbank),
  numOfStars int not null,
  reviewtext varchar(2048) 
);


drop table if exists foodSupplies;
Create Table foodSupplies(
  menu varchar(255) not null,
  bankaddr varchar(255) not null,
  constraint bankmenu primary key (menu, bankaddr),
  glutenfree bool not null,
  halal bool not null,
  kosher bool not null,
  vegan bool not null,
  amount int not null

); 
