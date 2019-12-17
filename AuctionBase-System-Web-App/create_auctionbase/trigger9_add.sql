-- description: A bidder wins the auction immediately when price is higher than Buy_Price. No more auction allowed after that.

PRAGMA foreign_keys = ON;

drop trigger if exists trigger9;

create trigger trigger9
	before insert on Bids
	for each row when ((Select i.Currently from Items i WHERE New.ItemID = Items.ItemID) > (Select i.Buy_Price from Items i WHERE New.ItemID = Items.ItemID))
	begin
		SELECT raise(rollback, "Trigger9_Failed, Bid was already finished since someone offered a price higher than buy price.");
	end;