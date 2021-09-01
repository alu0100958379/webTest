# -*- coding: utf-8 -*-
import time
import functions 

import pandas as pd
import custom_binance as bn
import utils as ut

from datetime import datetime

    
trading_state = 0


def strategy_scalping_custom (client):
    print("\n")
    print("Custom Strategy")
    market_prices = bn.bn_get_market_prices(client)

    vuelta = 0
    while vuelta < 3:
        init = time.time()
        
        for i in market_prices:
            #print(trading_state)
           
            if trading_state == 1:
                break
            
            info = client.get_symbol_info(i["symbol"])
            if info["status"] == 'TRADING' and float(i["price"]) < 25.0 and not i["symbol"] == 'ADAUSDT':
                rsi_result = ut.check_rsi(bn.bn_get_rsi(client, sym = i["symbol"]))
                macd, signal, diff = bn.bn_get_macd(client, sym = i["symbol"])
                macd_result = ut.check_macd(diff)
                up, mid, low = bn.bn_get_boll(client, sym = i["symbol"])
                boll_result = ut.check_boll(up, mid, low)
                
                if rsi_result == True and macd_result == True and boll_result == True:
                    print("\n")
                    print(i["symbol"])
                    
                    print(str(datetime.now()))


                    
                    #INSERTAR EN LA BASE DE DATOS
                    functions.insert_new_strategy(i["symbol"])
                        
                        
                    actual_price = float((client.get_symbol_ticker(symbol = i["symbol"]))["price"])
                    
                    buy_order = bn.bn_make_buy_limit_order(client, i["symbol"], actual_price)
                    
                    if buy_order is not None:
                        
                        time.sleep(1)
                        custom_buy_init = time.time()
                        custom_buy_time = 0
                        ok = False
                        open_orders = client.get_open_orders(symbol = i["symbol"])
                        
                        while custom_buy_time < 4 and ok == False:
                            if pd.Series(open_orders).empty == True:
                                ok = True
                            open_orders = client.get_open_orders(symbol = i["symbol"])
                            custom_buy_time = time.time() - custom_buy_init
                        
                        if ok == True:
                            sell_order = bn.bn_make_sell_oco_order(client, i["symbol"], actual_price, 0.2, 0.6)
                            #print(sell_order)
                                
                            if sell_order is not None:
                                check_sell = bn.bn_check_open_orders(client, i["symbol"])
                                #check_sell = bn.bn_check_order_by_id(client, sell_order["orders"][0]['orderId'], i["symbol"])
                                    
                                if check_sell == True:    
                                    custom_sell_init = time.time()
                                    custom_sell_time = 0
                                    ok = False
                                    time.sleep(1)
                                    open_orders = client.get_open_orders(symbol = i["symbol"])
                                    print(open_orders)
                                    while custom_sell_time < 900 and ok == False:
                                        if pd.Series(open_orders).empty == True:
                                            ok = True
                                        open_orders = client.get_open_orders(symbol = i["symbol"])
                                        custom_sell_time = time.time() - custom_sell_init
                                        
                                    if ok == False:
                                        print("PASÓ EL TIEMPO DE ESPERA Y NUNCA SE CUMPLIÓ")
                                        bn.bn_cancel_open_orders(client, i["symbol"])
                                        actual_price = float((client.get_symbol_ticker(symbol = i["symbol"]))["price"])
                                        check_limit = bn.bn_make_sell_limit_order(client, i["symbol"], actual_price)
                                        while check_limit is None:
                                            check_limit = bn.bn_make_sell_limit_order(client, i["symbol"], actual_price)
                                               
                                    else:
                                        print(client.get_open_orders(symbol = i["symbol"]))
                                        print("SE CUMPLIÓ")
                                        functions.update_strategy()
                                            
                                else:
                                    print("NO SE GENERÓ LA ORDEN DE VENTA OCO Y SE COLOCA ORDEN DE VENTA LIMIT")
                                    bn.bn_cancel_open_orders(client, i["symbol"])
                                    actual_price = float((client.get_symbol_ticker(symbol = i["symbol"]))["price"])
                                    check_limit = bn.bn_make_sell_limit_order(client, i["symbol"], actual_price)
                                    while check_limit is None:
                                        check_limit = bn.bn_make_sell_limit_order(client, i["symbol"], actual_price)
                                        
                            else:
                                print("JAMAS SE REALIZÓ LA VENTA OCO")
                                actual_price = float((client.get_symbol_ticker(symbol = i["symbol"]))["price"])
                                check_limit = bn.bn_make_sell_limit_order(client, i["symbol"], actual_price)
                                while check_limit is None:
                                   check_limit = bn.bn_make_sell_limit_order(client, i["symbol"], actual_price)
                                   time.sleep(1)
                        else:
                            print("JAMAS SE CUMPLIÓ LA ORDEN DE COMPRA")
                            bn.bn_cancel_open_orders(client, i["symbol"])

                       
                    functions.update_strategy()

                    coin = i["symbol"]
                    coin = coin.replace("USDT","")
                    #print(coin)
                    #print(client.get_asset_balance(asset=coin))
                    free = float(client.get_asset_balance(asset=coin)['free'])
                    actual_price = float((client.get_symbol_ticker(symbol = i["symbol"]))["price"])            
    
                    if free * actual_price > 10.0:
                        actual_price = float((client.get_symbol_ticker(symbol = i["symbol"]))["price"])            
                        finish_check = bn.bn_make_sell_limit_order(client, i["symbol"], actual_price)
                        
                        while finish_check is None:
                            actual_price = float((client.get_symbol_ticker(symbol = i["symbol"]))["price"])            
                            finish_check = bn.bn_make_sell_limit_order(client, i["symbol"], actual_price)
    
                        open_orders = client.get_open_orders(symbol = i["symbol"])
                        
                        while pd.Series(open_orders).empty == False:
                            open_orders = client.get_open_orders(symbol = i["symbol"])

                    
        elapsed_time = time.time() - init
        print(elapsed_time)
        vuelta = vuelta + 1
        print("VUELTA NUMERO: ", vuelta)

    return True


def ema_strategy (client):
    print("\n")
    print("EMA strategy")
    
    market_prices = bn.bn_get_market_prices(client)

    while trading_state == 0:
        for i in market_prices:
            #print(trading_state)

            if trading_state == 1:
                break
                
            info = client.get_symbol_info(i["symbol"])
            
            if info["status"] == 'TRADING' and float(i["price"]) < 500.0 and not i["symbol"] == 'ADAUSDT':
                timeperiod = 25
                ema25 = bn.bn_get_ema(client, i["symbol"], timeperiod)
                
                timeperiod = 50
                ema50 = bn.bn_get_ema(client, i["symbol"], timeperiod)
                
                timeperiod = 100
                ema100 = bn.bn_get_ema(client, i["symbol"], timeperiod)
                
                check_ema = ut.check_ema(ema25, ema50, ema100)
                
                if (check_ema == True):
                    check_close = ut.check_close_ema(ema25, bn.bn_get_close_prices(client, i["symbol"], 1))
                                    
                    if (check_close == True):
                        print(i["symbol"]);
                        buy_process_init = time.time()
                        buy_process_time = 0
                        check = False
                        
                        while buy_process_time < 900 and check == False:
                            close_price = bn.bn_get_close_prices(client, i["symbol"], 1).pop()
                            ema25 = bn.bn_get_ema(client, i["symbol"], 25).tolist().pop()

                            if (close_price < ema25):
                                print("Por debajo de ema25")
                                check = True
                            
                            buy_process_time = time.time() - buy_process_init
                            
                        if check == True:
                            action = 0
                            action_init = time.time()
                            action_time = 0
                            
                            while action_time < 900 and action == 0:
                                close_price = bn.bn_get_close_prices(client, i["symbol"], 1).pop()
                                ema25 = bn.bn_get_ema(client, i["symbol"], 25).tolist().pop()
                                ema100 = bn.bn_get_ema(client, i["symbol"], 100).tolist().pop()
                                
                                if close_price > ema25:
                                    action = 1
                                elif close_price < ema100:
                                    action = -1
                                    
                                action_time = time.time() - action_init

                                
                            if action == 1:
                                #COMPRAR
                                print("COMPRAR")
                                print(i["symbol"])


                                #INSERTAR EN LA BASE DE DATOS
                                functions.insert_new_strategy(i["symbol"])
                            
                            
                                actual_price = float((client.get_symbol_ticker(symbol = i["symbol"]))["price"])
                                
                                buy_order = bn.bn_make_buy_limit_order(client, i["symbol"], actual_price)
                                
                                if buy_order is not None:
                                    
                                    time.sleep(1)
                                    custom_buy_init = time.time()
                                    custom_buy_time = 0
                                    ok = False
                                    open_orders = client.get_open_orders(symbol = i["symbol"])
                                    
                                    while custom_buy_time < 4 and ok == False:
                                        if pd.Series(open_orders).empty == True:
                                            ok = True
                                        open_orders = client.get_open_orders(symbol = i["symbol"])
                                        custom_buy_time = time.time() - custom_buy_init
                                    
                                    if ok == True:
                                        time.sleep(0.5)
                                        stop_per = (100*(actual_price - bn.bn_get_ema(client, i["symbol"], 50).tolist().pop()))/actual_price
                                        limit_per = stop_per * 1.5

                                        #if limit_per > 0.2: #Ganancias minimas para rentabilidad
                                        sell_order = bn.bn_make_sell_oco_order(client, i["symbol"], actual_price, limit_per, stop_per)
                                            
                                        if sell_order is not None:
                                            check_sell = bn.bn_check_open_orders(client, i["symbol"])
                                            #check_sell = bn.bn_check_order_by_id(client, sell_order["orders"][0]['orderId'], i["symbol"])
                                                
                                            if check_sell == True:  
                                                ok = False
                                                time.sleep(0.5)
                                                print(client.get_open_orders(symbol = i["symbol"]))
                                                while ok == False:
                                                    if len(client.get_open_orders(symbol = i["symbol"])) == 0:
                                                        ok = True
                                                    #custom_buy_time = time.time() - custom_buy_init
                                            
                                            else:
                                                bn.bn_cancel_open_orders(client, i["symbol"])

                                    else:
                                        bn.bn_cancel_open_orders(client, i["symbol"])
                                                                
                        functions.update_strategy()
                        
                        print("Termino con la moneda, compruebo si me queda dinero en esa moneda")
                        time.sleep(0.5)
                        bn.bn_cancel_open_orders(client, i["symbol"])
                        coin = i["symbol"]
                        coin = coin.replace("USDT","")
                        free = float(client.get_asset_balance(asset=coin)['free'])
                        actual_price = float((client.get_symbol_ticker(symbol = i["symbol"]))["price"])            
            
                        if free * actual_price > 10.0:
                            actual_price = float((client.get_symbol_ticker(symbol = i["symbol"]))["price"])            
                            finish_check = bn.bn_make_sell_limit_order(client, i["symbol"], actual_price)
                            
                            while finish_check is None:
                                actual_price = float((client.get_symbol_ticker(symbol = i["symbol"]))["price"])            
                                finish_check = bn.bn_make_sell_limit_order(client, i["symbol"], actual_price)
            
                            open_orders = client.get_open_orders(symbol = i["symbol"])
                            
                            while pd.Series(open_orders).empty == False:
                                open_orders = client.get_open_orders(symbol = i["symbol"])

    return True
    '''
    
        - Esperar a que el precio caiga por debajo de la ema 25 o ema 50
            - En caso de que pase por debajo de ema100, salir de la moneda
        
        - Cuando caiga, comprar en la siguiente vela que el cierre supere la ema 25
        
        - Una vez comprada, poner stop loss en ema50 y limit en 1,5*diferencia al stop loss
        
    '''
            
            
def engulfing_strategy (client):
    print("\n")
    print("Engulfing Strategy")

    market_prices = bn.bn_get_market_prices(client)
    vuelta = 0

    while trading_state == 0:
        for i in market_prices:
            #print(trading_state)
            if trading_state == 1:
                break
                
            info = client.get_symbol_info(i["symbol"])
            
            if info["status"] == 'TRADING' and float(i["price"]) < 500.0:
                engulfing = bn.bn_get_engulfing_pattern(client, i["symbol"]) 
                
                if (engulfing.tolist().pop() == 100):
                    timeperiod = 200
                    ema200 = bn.bn_get_ema(client, i["symbol"], timeperiod)
                
                    close = bn.bn_get_close_prices(client, i["symbol"], 1)
                    
                    check_close = ut.check_close_engulfing(ema200, close)
                    
                    if (check_close == True):
                        rsi = bn.bn_get_rsi(client, sym = i["symbol"])
                        
                        if (rsi.tolist().pop() > 50):
                            
                            stop = bn.bn_get_low_prices(client, i["symbol"], 1).pop()
                            print(i["symbol"])
                
                            actual_price = float((client.get_symbol_ticker(symbol = i["symbol"]))["price"])
                            
                            #INSERTAR EN LA BASE DE DATOS
                            functions.insert_new_strategy(i["symbol"])
                            #TO_DO:
                                
                                #COMPROBAR QUE actual_price ES MAYOR QUE stop
                            
                            buy_order = bn.bn_make_buy_limit_order(client, i["symbol"], actual_price)
                            
                            if buy_order is not None:
                                
                                time.sleep(1)
                                custom_buy_init = time.time()
                                custom_buy_time = 0
                                ok = False
                                open_orders = client.get_open_orders(symbol = i["symbol"])
                                
                                while custom_buy_time < 4 and ok == False:
                                    if pd.Series(open_orders).empty == True:
                                        ok = True
                                    open_orders = client.get_open_orders(symbol = i["symbol"])
                                    custom_buy_time = time.time() - custom_buy_init
                                    
                                if ok == True:
                                    stop_per = (100*(actual_price - stop))/actual_price
                                    limit_per = stop_per * 2

                                    #if limit_per > 0.2: #Ganancias minimas para rentabilidad
                                    sell_order = bn.bn_make_sell_oco_order(client, i["symbol"], actual_price, limit_per, stop_per)
                                        
                                    if sell_order is not None:
                                        check_sell = bn.bn_check_open_orders(client, i["symbol"])
                                        #check_sell = bn.bn_check_order_by_id(client, sell_order["orders"][0]['orderId'], i["symbol"])
                                        
                                        if check_sell == True:  
                                            ok = False
                                            time.sleep(0.5)
                                            print(client.get_open_orders(symbol = i["symbol"]))
                                            while ok == False:
                                                if len(client.get_open_orders(symbol = i["symbol"])) == 0:
                                                    ok = True
                                                #custom_buy_time = time.time() - custom_buy_init
                                        
                                        else:
                                            bn.bn_cancel_open_orders(client, i["symbol"])
                                            
                                else:
                                    bn.bn_cancel_open_orders(client, i["symbol"])
                        

                            functions.update_strategy()

                            time.sleep(0.5)
                            bn.bn_cancel_open_orders(client, i["symbol"])
                            coin = i["symbol"]
                            coin = coin.replace("USDT","")
                            free = float(client.get_asset_balance(asset=coin)['free'])
                            actual_price = float((client.get_symbol_ticker(symbol = i["symbol"]))["price"])            
                
                            if free * actual_price > 10.0:
                                actual_price = float((client.get_symbol_ticker(symbol = i["symbol"]))["price"])            
                                finish_check = bn.bn_make_sell_limit_order(client, i["symbol"], actual_price)
                                
                                while finish_check is None:
                                    actual_price = float((client.get_symbol_ticker(symbol = i["symbol"]))["price"])            
                                    finish_check = bn.bn_make_sell_limit_order(client, i["symbol"], actual_price)
                
                                open_orders = client.get_open_orders(symbol = i["symbol"])
                                
                                while pd.Series(open_orders).empty == False:
                                    open_orders = client.get_open_orders(symbol = i["symbol"])
        print("vuelta: ", vuelta)
    return True                    

    
def select_strategy (strategy, client):
    #functions.insert_mode(1, strategy)
    
    if strategy == 1:
        return strategy_scalping_custom(client)
        
    if strategy == 2:
        return ema_strategy(client)
        
    if strategy == 3:
        return engulfing_strategy(client)
        
    
