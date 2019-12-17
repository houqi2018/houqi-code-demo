-- description: Every time bid amount must be higher than current price.

PRAGMA foreign_keys = ON;

drop trigger if exists trigger10;

create trigger trigger10
	before insert on Bids
	for each row when (New.Amount <= (Select i.Currently from Items i WHERE New.ItemID = Items.ItemID))
	begin
		SELECT raise(rollback, "Trigger10_Failed, Bid amount must be higher than current price.");
	end;