import web
import sys
import sqlite3

reload(sys)
sys.setdefaultencoding('utf-8')

db = web.database(dbn='sqlite',
        db='AuctionBase.db'
    )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()

# returns the current time from your database
def getTime():
    try:
        query_string = 'select Time from CurrentTime'
        results = query(query_string)
    except:
        print 'There is an error. Please try it again or contact admin.'
    return results[0].Time

# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemById(item_id):
    query_string = 'select * from Items where item_ID = $itemID'
    result = query(query_string, {'itemID': item_id})
    if len(result) == 0:
        exit(-1)
    return result[0]

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
# Note: we didn't use this wrapper method
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

#####################END HELPER METHODS#####################

def updateTime(selected_time):
    ''' This method updates the time '''

    try:
        query_string = 'update CurrentTime set Time = $time'
        db.query(query_string, {'time': selected_time})
    except:
        print 'There is an error. Please try it again or contact admin.'

def addBid(itemID, userID, price):
    ''' This method adds a bid to Bids '''

    returnValue = []
    add_result = False
    msg = "Bid is not added. Please enter correct information."
    check_item_flag = True
    check_user_flag = True

    try:
        # First search itemID and time
        query_search = 'select count(*) from Items where ItemID = $itemID'
        count = list(db.query(query_search, {'itemID': itemID}))
        if len(count) > 0 and count[0].get('count(*)') > 0:
            count = count[0].get('count(*)')
        else:
            count = 0
            msg = "Bid is not added. Please enter a valid Item ID."
            check_item_flag = False

        # Second search userID
        if check_item_flag:
            query_user = 'select count(*) from Users where UserID = $userID'
            count_user = list(db.query(query_user, {'userID': userID}))
            if len(count_user) > 0 and count_user[0].get('count(*)') > 0:
                count_user = count_user[0].get('count(*)')
            else:
                count_user = 0
                msg = "Bid is not added. Please enter a valid User ID."
                check_user_flag = False

            # Third check if given price is below Currently (and implicitly check double bidding)
            if check_user_flag:
                low_price_flag = False
                low_price_query = 'select Currently from Items where ItemID = $itemID'
                low_price = list(db.query(low_price_query, {'itemID': int(itemID)}))
                if len(low_price) > 0 and float(price) <= low_price[0].get('Currently'):
                    low_price_flag = True
                    msg = "Bid is not added. You need a price higher than current price: " + str(low_price[0].get('Currently'))

                # Fourth check if item is close
                if low_price_flag == False:
                    close_flag = False
                    close_query = 'select Ends from Items where ItemID = $itemID'
                    close_check = list(db.query(close_query, {'itemID': int(itemID)}))
                    if len(close_check) > 0 and getTime() > close_check[0].get('Ends'):
                        close_flag = True
                        msg = "Bid is not added. This bid is closed already."

                    # If all checks are passed, insert this bid to Bids, and update Items
                    if count == 1 and count_user == 1 and low_price_flag == False and close_flag == False:
                        query_string = 'insert into Bids values ($itemID, $userID, $price, $time)'
                        db.query(query_string,
                                 {'itemID': int(itemID), 'userID': userID, 'price': float(price), 'time': getTime()})
                        add_result = True

                        # Check if this bid close the item, i.e., if price >= Buy_Price
                        Buy_Price_query = 'select Buy_Price from Items where ItemID = $itemID'
                        Buy_Price = list(db.query(Buy_Price_query, {'itemID': int(itemID)}))
                        close_bid_flag = False
                        buy_price_null_flag = True
                        print Buy_Price[0].get('Buy_Price')
                        # If buyer does not specify Buy_Price, then only close it when time reaches Ends
                        if Buy_Price[0].get('Buy_Price') == None:
                            buy_price_null_flag = False
                        else:
                            if float(price) >= Buy_Price[0].get('Buy_Price'):
                                close_bid_flag = True
                                msg = "One bid is added successfully and this bid closes the item"
                            else:
                                msg = "One bid is added successfully"

                        # Also update Buy_Price, Number_of_Bids and Ends (if necessary) in Items
                        update_price_query = 'update Items set Currently = $price where ItemID = $itemID'
                        db.query(update_price_query, {'price': float(price), 'itemID': int(itemID)})
                        new_num_query = 'select Number_of_Bids from Items where ItemID = $itemID'
                        new_num = list(db.query(new_num_query, {'itemID': int(itemID)}))
                        if len(new_num) > 0:
                            new_num = new_num[0].get('Number_of_Bids')
                            new_num = int(new_num) + 1
                            Number_of_Bids_query = 'update Items set Number_of_Bids = $new_num where ItemID = $itemID'
                            db.query(Number_of_Bids_query, {'new_num': new_num, 'itemID': int(itemID)})
                            if close_bid_flag and buy_price_null_flag:
                                close_bid_query = 'update Items set Ends = $time where ItemID = $itemID'
                                db.query(close_bid_query, {'time': getTime(), 'itemID': int(itemID)})

                            # Update successful message
                            msg = "Bid is added. Good luck."
                    else:
                        add_result = False
    except:
        print 'There is an error. Please try it again or contact admin.'

    returnValue.append(msg)
    returnValue.append(add_result)
    return returnValue


def search_helper(A_list):
    ''' Bulk inserting data to a new table called A_table '''

    items_list = []
    for each in A_list:
        temp = ( each.get('ItemID'), each.get('Name'), each.get('Category'), each.get('Currently'),
                  each.get('Started'), each.get('Ends'), each.get('Description') )
        items_list.append(temp)

    try:
        # Code below uses bulk loading and commit after all items are inserted, which can be much faster
        con = sqlite3.connect("Auctionbase.db")
        con.execute('drop table if exists A_table')
        con.execute('create table A_table (ItemID INTEGER, Name TEXT, Category TEXT, Currently REAL, \
                    Started TEXT, Ends TEXT, Description TEXT)')
        con.executemany("insert into A_table values (?,?,?,?,?,?,?)", items_list)
        con.commit()
    except:
        print 'There is an error. Please try it again or contact admin.'


def search(itemID, category, description, minPrice, maxPrice, status):
    ''' This method search the db by filters user inputs '''

    try:
        select_all = 'select * from Items as I, Categories as C where I.ItemID = C.ItemID'
        A = list(db.query(select_all))
        search_helper(A)

        # Case: when user want to filter items by itemID
        if str(itemID) != "":
            itemID_search = 'select * from A_table where ItemID = $itemID'
            A = list(db.query(itemID_search, {'itemID': int(itemID)}))
            search_helper(A)

        # Case: when user want to filter items by category
        if category != "":
            category_search = 'select * from A_table where Category = $category'
            A = list(db.query(category_search, {'category': category}))
            search_helper(A)

        # Case: when user want to filter items by description
        # We limit the length to 30 chars, because more than 30 chars would result sqlite error.
        # We gracefully check the length to avoid the error.
        if description != "":
            if '\'' in description:
                description = description[0:description.index('\'')]
            description_search = 'select * from A_table where Description like \'%'+ description + '%\''
            A = list(db.query(description_search))
            search_helper(A)

        # Case: when user want to filter items by minPrice
        if str(minPrice) != "":
            minPrice_search = 'select * from A_table where Currently > $minPrice'
            A = list(db.query(minPrice_search, {'minPrice': int(minPrice)}))
            search_helper(A)

        # Case: when user want to filter items by maxPrice
        if str(maxPrice) != "":
            maxPrice_search = 'select * from A_table where Currently < $maxPrice'
            A = list(db.query(maxPrice_search, {'maxPrice': int(maxPrice)}))
            search_helper(A)

        # Case: when user want to filter items by item status
        if status == "open":
            status_search = 'select * from A_table where Started <= $currTime and Ends >= $currTime'
            A = list(db.query(status_search, {'currTime': getTime()}))
            search_helper(A)

        elif status == "close":
            status_search = 'select * from A_table where Ends <= $currTime'
            A = list(db.query(status_search, {'currTime': getTime()}))
            search_helper(A)

        elif status == "notStarted":
            status_search = 'select * from A_table where Started >= $currTime'
            A = list(db.query(status_search, {'currTime': getTime()}))
            search_helper(A)
    except:
        print 'There is an error. Please try it again or contact admin.'

    return A


def getdetail(itemID):
    ''' This method show user details of an item '''

    try:
        itemID_search = 'select * from Items where ItemID = $itemID'
        detail = list(db.query(itemID_search, {'itemID': int(itemID)}))
        if len(detail) == 0:
            ret = []
        else:
            # Get all entries from Table Items
            detail = detail[0]
            ItemID = detail.get('ItemID')
            Name = detail.get('Name')
            Currently = detail.get('Currently')
            First_Bid = detail.get('First_Bid')
            Buy_Price = detail.get('Buy_Price')
            Number_of_Bids = detail.get('Number_of_Bids')
            Started = detail.get('Started')
            Ends = detail.get('Ends')
            Seller_UserID = detail.get('Seller_UserID')
            Description = detail.get('Description')

            # Get category of this item
            category_search = 'select Category from Categories where ItemID = $itemID'
            category = list(db.query(category_search, {'itemID': int(itemID)}))
            multiple_cat = ""
            for i in range(len(category)):
                multiple_cat = multiple_cat + category[i].get('Category') + ", "

            # Get past bidding info of this item, also get a winner if there exists one
            hasWinner = False
            currTime = getTime()
            if Started <= currTime and Ends >= currTime:
                Status = "open"
            elif Ends <= currTime:
                Status = "close"
                hasWinner = True
            elif Started >= currTime:
                Ststus = "notStarted"

            bids_search = 'select * from Bids where ItemID = $itemID'
            bids_info = list(db.query(bids_search, {'itemID': int(itemID)}))
            bids_info_long_string = ""
            UserID = ""
            for i in range(len(bids_info)):
                UserID = bids_info[i].get('UserID')
                Amount = bids_info[i].get('Amount')
                Time = bids_info[i].get('Time')
                bids_info_long_string += "User: " + str(UserID) + " Amount: " + str(Amount) + " Time: " + str(Time) + " // "

            if hasWinner:
                winner = UserID
            else:
                winner = 'nobody'

            # All info:
            #       ItemID, Name, Currently, First_Bid, Buy_Price, Number_of_Bids, Started, Ends, Seller_UserID, Description
            #       multiple_cat, Status, bids_info_long_string, winner
            info_list = [(ItemID, Name, Currently, First_Bid, Buy_Price, Number_of_Bids, Started, Ends, Seller_UserID, Description,
                         multiple_cat, Status, bids_info_long_string, winner),
                        ]

            # Put the details back to a table and finally return an instance from the detail_table
            con = sqlite3.connect("Auctionbase.db")
            con.execute('drop table if exists detail_table')
            con.execute('create table detail_table (ItemID, Name, Currently, First_Bid, Buy_Price, Number_of_Bids, Started, \
                        Ends, Seller_UserID, Description, Category, Status, Bids_info, Winner)'
                        )
            con.executemany("insert into detail_table values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", info_list)
            con.commit()

            status_search = 'select * from detail_table'
            ret = list(db.query(status_search))
    except:
        print 'There is an error. Please try it again or contact admin.'

    return ret