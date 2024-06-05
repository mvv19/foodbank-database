/*for needing to alter only one database

drop table if exists VisitorVisited;
Create Table VisitorVisited(
  visitorID varchar(255) not null,
  datevisited date not null,
  hours int not null,
  foodbankaddr varchar(255) not null,
  constraint visSession primary key (visitorID, datevisited),
  foodbankID int
);

*/

/*
drop table if exists Amenities;
Create Table Amenities (
  foodbank_id int primary key,
  description varchar(1024)
);

*/
/* thank u sm!!!!*/
/*ok! lemme drop that from the csv rq
drop table if exists Rating;
Create Table Rating(
  reviewID int not null,
  FoodbankID int not null,
  CONSTRAINT review PRIMARY KEY (reviewID, FoodbankID),
  ReviewerEmail varchar(255) not null,
  foodbank varchar(255) not null,
  numOfStars int not null
);
*/

drop table if exists Owner;
Create Table Owner(
  foodbank_id int not null,
  ownerFirst varchar(255) not null,
  ownerLast varchar(255) not null,
  ownerEmail varchar(255) primary key not null,
  income int
);
