drop table if exists Player;
create table Player (
	uID 		integer	primary key autoincrement,	--user id
	privlege	integer	default 0,					--1 for elevated privleges
	username	text	not null,
	password	text	not null,					--stored in plain text for purpose of project, proof of concept
	platform	text	default 'PC'				--can be PC, XB1, or PS4
);

drop table if exists Item;
create table Item (
	iID 		integer	primary key autoincrement,	--item id
	name 		text	not null,					--every item must have a name
	--next attributes only apply to equippable items
	type		text,	
	quality		text,
	collection	text,
	painted		text,
	certified	text
);

drop table if exists Wants;
create table Wants (
	wID			integer primary key autoincrement,
	userID 		integer,
	itemID 		integer,
	quantity	integer default 1,
	foreign key(userID) references Player(uID),
	foreign key(itemID) references Item(iID)
);

drop table if exists Has;
create table Has (
	hID			integer primary key autoincrement,
	userID 		integer,
	itemID 		integer,
	quantity	integer default 1,
	foreign key(userID) references Player(uID),
	foreign key(itemID) references Item(iID)
);
