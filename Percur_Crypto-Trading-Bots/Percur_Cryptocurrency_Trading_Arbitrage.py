def run():

    arbitrage()
    time.sleep(20)
    initialize()
    portfolio = 10

    while 1:
        ActiveTrader()

def arbitrage(cycle_num=5, cycle_time=240):

    print("Arbitrage Function Running")
    fee_percentage = 0.001
    coins = ['BTC', 'LTC', 'ETH']

    for exch in ccxt.exchanges:
        exchange1 = getattr (ccxt, exch) ()
        symbols = exchange1.symbols
        if symbols is None:
            print("Skipping Exchange ", exch)
            print("\n-----------------\nNext Exchange\n-----------------")
        elif len(symbols)<15:
            print("\n-----------------\nNeed more Pairs (Next Exchange)\n-----------------")
        else:
            print(exchange1)

            exchange1_info = dir(exchange1)
            print("------------Exchange: ", exchange1.id)

            print(exchange1.symbols)
            time.sleep(5)

            pairs = []
            for sym in symbols:
                for symbol in coins:
                    if symbol in sym:
                        pairs.append(sym)
            print(pairs)

            arb_list = ['ETH/BTC'] #, 'ETH/LTC', 'BTC/LTC']
            j=0
            while 1:
                if j == 1:
                            final = arb_list[0][-3:]  + '/' + str(arb_list[1][-3:])
                            print(final)

                            arb_list.append(final)
                            break
                for sym in symbols:
                    if sym in arb_list:
                        pass
                    else:
                        if j % 2 == 0:
                            if arb_list[j][0:3] == sym[0:3]:
                                if arb_list[j] == sym:
                                    pass
                                else:
                                    arb_list.append(sym)
                                    print(arb_list)
                                    j+=1
                                    break
                        if j % 2 == 1:
                            if arb_list[j][-3:] == sym[-3:]:
                                if arb_list[j] == sym:
                                    pass
                                else:
                                    arb_list.append(sym)
                                    print(arb_list)
                                    j+=1
                                    break


            print("List of Arbitrage Symbols:", arb_list)

            list_exch_rate_list = []

            for k in range(0,cycle_num):
                i=0
                exch_rate_list = []
                print("Cycle Number: ", k)
                for sym in arb_list:
                    print(sym)
                    if sym in symbols:
                        depth = exchange1.fetch_order_book(symbol=sym)

                        if i % 2 == 0:
                            exch_rate_list.append(depth['bids'][0][0])
                        else:
                            exch_rate_list.append(depth['asks'][0][0])
                        i+=1
                    else:
                        exch_rate_list.append(0)

                exch_rate_list.append(time.time())
                print(exch_rate_list)

                if exch_rate_list[0]<exch_rate_list[1]/exch_rate_list[2]:
                    print("Arbitrage Possibility")
                else:
                    print("No Arbitrage Possibility")

                list_exch_rate_list.append(exch_rate_list)
                time.sleep(cycle_time)
            print(list_exch_rate_list)

            rateA = []
            rateB = []
            rateB_fee = []
            price1 = []
            price2 = []
            time_list = []

            for rate in list_exch_rate_list:
                rateA.append(rate[0])
                rateB.append(rate[1]/rate[2])
                rateB_fee.append((rate[1]/rate[2])*(1-fee_percentage)*(1-fee_percentage))
                price1.append(rate[1])
                price2.append(rate[2])
                #profit.append((rateB[-1]-rateA[-1])/rateA[-1])
                time_list.append(rate[3])
            print("Rate A: {} \n Rate B: {} \n Rate C: {} \n".format(rateA, rateB, rateB_fee))

            fig, host = plt.subplots()
            fig.subplots_adjust(right=0.75)

            par1 = host.twinx()
            par2 = host.twinx()
            par2.spines["right"].set_position(("axes", 1.2))
            make_patch_spines_invisible(par2)
            par2.spines["right"].set_visible(True)

            p1, = host.plot(time_list, rateA, "k", label = "{}".format(arb_list[0]))
            p1, = host.plot(time_list, rateB, "k+", label = "{} / {}".format(arb_list[1], arb_list[2]))
            p2, = par1.plot(time_list, price1, "b-", label="Price - {}".format(arb_list[1]))
            p3, = par2.plot(time_list, price2, "g-", label="Price - {}".format(arb_list[2]))


            host.set_xlabel("Time")
            host.set_ylabel("Exchange Rate")
            par1.set_ylabel("Price - {}".format(arb_list[1]))
            par2.set_ylabel("Price - {}".format(arb_list[2]))
            host.yaxis.label.set_color(p1.get_color())
            tkw = dict(size=4, width=1.5)
            host.tick_params(axis='y', colors=p1.get_color(), **tkw)
            par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
            par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
            host.tick_params(axis='x', **tkw)
            lines = [p1, p2, p3]
            host.legend(lines, [l.get_label() for l in lines])
            plt.show()

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

def diversify():
    for exch2 in ccxt.exchanges:
        exch = getattr (ccxt, exch2) ()
        print(exch.fetchBalance())
    pass

def ActiveTrader():
    pass

def initialize():
    all_symbols = []
    micro_cap_coins = []
    print("\n\n---------------------------------------------------------\n\n")
    print("Hello and Welcome to the Percar\nCreated by Fahim (@BlockchainDev)")
    print("A quick 'run-through' of percar arbitrage")
    print("Percar\n\n")

    time.sleep(5)
    i = 0
    try:
            #Get Status of Exchange & Account
        print("Number of Exchanges: ", len(ccxt.exchanges))
        print("\nList of Available Exchanges: \n \n")
        print(ccxt.exchanges)

            #Get Exchange Info For All Listed Exchanges
        for exch1 in ccxt.exchanges:
            list_of_symbols = []        #Reset List of Symbols for Each Exchange
            if i>0:
                break           #Break Out of Statement
            exch = getattr (ccxt, exch1) ()
            print("\n\nExchange: ", exch.id)
            print("Set Exchange Info (Limits): ", exch.rateLimit)
            print("Load Market: ", exch.load_markets)
            #print(list(exchange1.markets.keys()))
            symbols = exch.symbols
            if symbols is None:
                print("\n-----------------\nNo symbols Loaded\n-----------------")
            else:
                print("-----------------------\nNumber of Symbols: ", len(symbols))
                print("Exchange & Symbols:")
                #print(exchange1.id, exchange1.markets.keys())
                print(exch.id,"-      ", symbols)
                print("-----------------------")
                for sym in symbols:
                    list_of_symbols.append(sym) #Create List of Symbols - Each Exchange
                    all_symbols.append(sym)     #Create List of ALL Symbols on ALL Exchanges
                #print("\n\n'Fetch Orders: ", exchange1.fetch_orders())
                currencies = exch.currencies
                #print("Currencies: ", currencies)
                time.sleep(5)
                rand_sym = random.choice(list_of_symbols)
                market_depth(rand_sym, exch)
                visualize_market_depth(sym=rand_sym, exchange=exch)
                scalping_orders(exch, rand_sym)
                i+=1        #Break Out of Initialize Statement
                time.sleep(4)

        print("INITIALIZE SUCCESSFUL")
    except():
        print("\n \n \nATTENTION: NON-VALID CONNECTION WITH PERCAR \n \n \n")

            #Account Withdrawal History Info
        #withdraws = client.get_withdraw_history()
        #print("\nClient Withdraw History: ", withdraws)


def market_depth(sym, exchange=ccxt.binance(), num_entries=20):
    #Get market depth
    #Retrieve and format market depth (order book) including time-stamp
    i=0     #Used as a counter for number of entries
    print("Order Book: ") #convert_time_binance(client.get_server_time()))   #Transfer to CCXT
    exchange.verbose = True
    depth = exchange.fetch_order_book(symbol=sym)               #Transf'd to CCXT
    #pprint(depth)
    print(depth['asks'][0])
    ask_tot=0.0
    ask_price =[]
    ask_quantity = []
    bid_price = []
    bid_quantity = []
    bid_tot = 0.0
    place_order_ask_price = 0
    place_order_bid_price = 0
    max_order_ask = 0
    max_order_bid = 0
    print("\n", sym, "\nDepth     ASKS:\n")         #Edit to work with CCXT
    print("Price     Amount")
    for ask in depth['asks']:
        if i<num_entries:
            if float(ask[1])>float(max_order_ask):
                #Determine Price to place ask order based on highest volume
                max_order_ask=ask[1]
                #print("Max Order ASK: ", max_order_ask)
                place_order_ask_price=round(float(ask[0]),5)-0.0001
            #ask_list.append([ask[0], ask[1]])
            ask_price.append(float(ask[0]))
            ask_tot+=float(ask[1])
            ask_quantity.append(ask_tot)
            #print(ask)
            i+=1
    j=0     #Secondary Counter for Bids
    print("\n", sym, "\nDepth     BIDS:\n")
    print("Price     Amount")
    for bid in depth['bids']:
        if j<num_entries:
            if float(bid[1])>float(max_order_bid):
                #Determine Price to place ask order based on highest volume
                max_order_bid=bid[1]
                #print("Max Order BID: ", max_order_bid)
                place_order_bid_price=round(float(bid[0]),5)+0.0001
            bid_price.append(float(bid[0]))
            bid_tot += float(bid[1])
            bid_quantity.append(bid_tot)
            #print(bid)
            j+=1
    return ask_price, ask_quantity, bid_price, bid_quantity, place_order_ask_price, place_order_bid_price
    #Plot Data

def scalping_orders(exchange = ccxt.binance(), coin='BTC/USDT', wait=1, tot_time=1):
    #Function for placing 'scalp orders'
    #Calls on Visualizing Scalping Orders Function
    ap, aq, bp, bq, place_ask_order, place_bid_order, spread, proj_spread, max_bid, min_ask = visualize_market_depth(wait, tot_time, coin, 5, exchange)
    print("Coin: {}\nPrice to Place Ask Order: {}\nPrice to place Bid Order: {}".format(coin, place_ask_order, place_bid_order))
    print("Spread: {} % Projected Spread {} %".format(spread, proj_spread))
    print("Max Bid: {} Min Ask: {}".format(max_bid, min_ask))
    #Place Orders based on calculated bid-ask orders if projected > 0.05% (transaction fee)
    """
    if proj_spread > 0.05:
        quant1=100          #Determine Code Required to calculate 'minimum' quantity
        #Place Bid Order:
        bid_order1 = client.order_limit_buy(
            symbol=coin,
            quantity=quant1,
            price=place_bid_order)
        #Place Ask Order
        ask_order1 = client.order_limit_sell(
            symbol=coin,
            quantity=quant1,
            price=place_ask_order)


    #Place second order if current spread > 0.05% (transaction fee)

    """


def visualize_market_depth(wait_time_sec='1', tot_time='1', sym='BTC/USDT', precision=5, exchange=ccxt.binance()):
    cycles = int(tot_time)/int(wait_time_sec)
    start_time = time.asctime()         #Trans CCXT
    fig, ax = plt.subplots()
    for i in range(1,int(cycles)+1):
        ask_pri, ask_quan, bid_pri, bid_quan, ask_order, bid_order = market_depth(sym, exchange)

        #print(ask_price)
        plt.plot(ask_pri, ask_quan, color = 'red', label='asks-cycle: {}'.format(i))
        plt.plot(bid_pri, bid_quan, color = 'blue', label = 'bids-cycle: {}'.format(i))

        #ax.plot(depth['bids'][0], depth['bids'][1])
        max_bid = max(bid_pri)
        min_ask = min(ask_pri)
        max_quant = max(ask_quan[-1], bid_quan[-1])
        spread = round(((min_ask-max_bid)/min_ask)*100,5)   #Spread based on market
        proj_order_spread = round(((ask_order-bid_order)/ask_order)*100, precision)
        price=round(((max_bid+min_ask)/2), precision)
        plt.plot([price, price],[0, max_quant], color = 'green', label = 'Price - Cycle: {}'.format(i)) #Vertical Line for Price
        plt.plot([ask_order, ask_order],[0, max_quant], color = 'black', label = 'Ask - Cycle: {}'.format(i))
        plt.plot([bid_order, bid_order],[0, max_quant], color = 'black', label = 'Buy - Cycle: {}'.format(i))
        #plt.plot([min_ask, min_ask],[0, max_quant], color = 'grey', label = 'Min Ask - Cycle: {}'.format(i))
        #plt.plot([max_bid, max_bid],[0, max_quant], color = 'grey', label = 'Max Buy - Cycle: {}'.format(i))
        ax.annotate("Max Bid: {} \nMin Ask: {}\nSpread: {} %\nCycle: {}\nPrice: {}"
                    "\nPlace Bid: {} \nPlace Ask: {}\n Projected Spread: {} %".format(max_bid, min_ask, spread, i, price, bid_order, ask_order, proj_order_spread),
                    xy=(max_bid, ask_quan[-1]), xytext=(max_bid, ask_quan[0]))
        if i==(cycles+1):
            break
        else:
            time.sleep(int(wait_time_sec))
    #end_time = time.asctime()
    ax.set(xlabel='Price', ylabel='Quantity',
       title='{} Order Book: {} \n {}\n Cycle Time: {} seconds - Num Cycles: {}'.format(exchange.id, sym, start_time, wait_time_sec, cycles))
    plt.legend()
    plt.show()
    return ask_pri, ask_quan, bid_pri, bid_quan, ask_order, bid_order, spread, proj_order_spread, max_bid, min_ask


def coin_prices(watch_list):
    #Will print to screen, prices of coins on 'watch list'
    #returns all prices
    prices = client.get_all_tickers()           #Trans CCXT
    print("\nSelected (watch list) Ticker Prices: ")
    for price in prices:
        if price['symbol'] in watch_list:
            print(price)
    return prices


def coin_tickers(watch_list):
    # Prints to screen tickers for 'watch list' coins
    # Returns list of all price tickers
    tickers = client.get_orderbook_tickers()            #Trans CCXT
    print("\nWatch List Order Tickers: \n")
    for tick in tickers:
        if tick['symbol'] in watch_list:
            print(tick)
    return tickers

def portfolio_management(deposit = '10000', withdraw=0, portfolio_amt = '0', portfolio_type='USDT', test_acct='True'):
    """The Portfolio Management Function will be used to track profit/loss of Portfolio in Any Particular Currency (Default: USDT)"""
    #Maintain Portfolio Statistics (Total Profit/Loss) in a file
    pass

def Bollinger_Bands():
    #This Function will calculate Bollinger Bands for Given Time Period
    pass

def buy_sell_bot():
    pass

def position_sizing():
    pass

def trailing_stop_loss():
    pass

if __name__ == "__main__":
    run()
