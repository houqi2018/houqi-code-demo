-- description: Bids from unknown users are not accepted.

PRAGMA foreign_keys = ON;

drop trigger if exists trigger12;

create trigger trigger12
	before insert on Bids
	for each row when (New.UserID not in (Select UserID from User))
	begin
		SELECT raise(rollback, "Trigger12_Failed, Bids from unknown users are not accepted.");
	end;