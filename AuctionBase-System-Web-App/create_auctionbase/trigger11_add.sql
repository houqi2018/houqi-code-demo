-- description: Bids on closed auctions are not accepted.

PRAGMA foreign_keys = ON;

drop trigger if exists trigger11;

create trigger trigger11
	before insert on Bids
	for each row when (NULL <> (Select i.Ends from Items i WHERE New.ItemID = Items.ItemID))
	begin
		SELECT raise(rollback, "Trigger11_Failed, Bids on closed auctions are not accepted.");
	end;