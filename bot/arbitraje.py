# -*- coding: utf-8 -*-
import custom_binance as bn
import custom_kucoin as kc
import utils as ut
import pandas as pd

import functions 
import smtplib
import time

from binance.exceptions import BinanceAPIException

arbitraje_state = 0


def transfer_arb(binance_client, kucoin_client):
    #qty_aux = 10
    #transfer = kucoin_client.create_inner_transfer('main', 'trade', qty_aux)
    #print(transfer)
    
    #print("\n")
    #deposits = kucoin_client.get_deposits('XEM')
    #print(deposits)
    
    print("\n")
    print("ARBITRAJE CON TRANSFERENCIA ENTRE EXCHANGES")
    
    binance_pairs = bn.bn_get_market_prices(binance_client)
    kucoin_pairs = kc.kc_get_market_info(kucoin_client)
    
    aux_binance_pairs = []
    
    aux_kucoin_pairs = []
    
    for i in binance_pairs:
        aux_binance_pairs.append(i["symbol"].replace("USDT",""))
        
    for i in kucoin_pairs:
        aux_kucoin_pairs.append(i["symbol"].replace("-USDT",""))
    
    crypto_list = list(set(aux_binance_pairs) & set(aux_kucoin_pairs))
    crypto_list.remove("BCHSV")
    bn_fees = bn.bn_get_withdrawal_fees(binance_client)
    #print(bn_fees)
    
    for i in crypto_list:
        
        if arbitraje_state == 1:
            break
            
        if (kucoin_client.get_currency(i)["isDepositEnabled"] == True):
            
            time.sleep(1)
            sym_bn = i + "USDT"
            binance_price = float((binance_client.get_symbol_ticker(symbol = sym_bn))["price"])
            sym_kc = i + "-USDT"
            kucoin_price = float((kucoin_client.get_ticker(symbol = sym_kc))["price"])
            
           
            if (binance_price < kucoin_price):
          
                print("\n")
                print(i)
                
                print("Binance -- KuCoin")
                print(binance_price, " -- ", kucoin_price)
                
                min_withdr = float(bn_fees[i]["minWithdrawAmount"])
                print("MINIMUN WITHDRAWAL : ", min_withdr)
                
                fees = float(bn_fees[i]["withdrawFee"])
                print("FEES : ", fees)

                if fees != 0:

                    #x=(((x/z)*(1-y))-r)*v*(1-w)        Despejamos x para obtener min_usdt
                    min_usdt = abs((fees*kucoin_price*(0.001-1)*binance_price)/(kucoin_price*(0.001-1)*(0.001-1)-binance_price))
                    print("MINIMO DE USDT A GASTAR (contando comision de compra, transferencia y venta): ")
                    print(min_usdt)       
                
                else:
                    #MIRAR QUE PASA SI FEES=0
                    
                    fees = 0.000001
                    min_usdt = abs((fees*kucoin_price*(0.001-1)*binance_price)/(kucoin_price*(0.001-1)*(0.001-1)-binance_price))
                    print("MINIMO DE USDT A GASTAR (contando comision de compra, transferencia y venta): ")
                    print(min_usdt)
                    
                balances = pd.Series(binance_client.get_account()["balances"])
                for i in balances:
                    if i["asset"] == 'USDT':
                        usdt_avaiable = float(i["free"])
                
                if ((usdt_avaiable > (10*min_usdt)) and ((10*min_usdt/binance_price) >= min_withdr) and 10*min_usdt < 100):
                    print("PUEDO COMPRAR MAS MONEDAS DEL MINIMO, Y SUPONE UN GASTO MENOR DE 100$")
                    
                    
                    #INSERTAR EN BASE DE DATOS
                    functions.insert_new_arbitraje(sym_bn)    
                    
                    
                    print("Genero orden de compra en BINANCE")
                    buy_order = bn.bn_make_buy_limit_order(binance_client, sym_bn, binance_price)
                    
                    if buy_order is not None:
                        time.sleep(1)
                        custom_buy_init = time.time()
                        custom_buy_time = 0
                        ok = False
                        open_orders = binance_client.get_open_orders(symbol = sym_bn)
                        
                        while custom_buy_time < 4 and ok == False:
                            if pd.Series(open_orders).empty == True:
                                ok = True
                            open_orders = binance_client.get_open_orders(symbol = sym_bn)
                            custom_buy_time = time.time() - custom_buy_init
                        
                        if ok == True:
                            deposit = kucoin_client.get_deposit_address(i)
                            print("DIRECCION DE DEPOSITO: ", deposit)
                        
                            qty = ut.truncate(float(2*min_usdt), 8)
                            
                            try:
                                #EN MI PC (supongo por version de python o alguna libreria)
                                result = binance_client.withdraw(
                                    asset=i,
                                    address=deposit['address'],
                                    addressTag=deposit['memo'],
                                    amount=qty,
                                    name=i
                                    )
                                
                                '''
                                #EN EL SERVIDOR (supongo por version de python o alguna libreria)
                                result = binance_client.withdraw(
                                    coin='XEM',
                                    address='NDMFF4NCQIJKCQHP6W47WSZF3TNM2YLMRLGPLTXU',
                                    addressTag='1882686335',
                                    amount=15)
                                '''
                                
                                print(result)
                                print("TRANSFIRIENDO FONDOS DE BINANCE A KUCOIN")
                                
                            except BinanceAPIException as e:
                                print(e)
                            else:
                                print("Success")
                           
                            
                            try:
                                result
                            except NameError:
                                print("Error en la TRANSFERENCIA")
                            else:
                                print("COMPROBANDO TRANSFERENCIA")
                               
                                accounts = kucoin_client.get_accounts()
                                if len(accounts) == 0:
                                    while len(accounts) == 0:
                                        time.sleep(20)
                                        accounts = kucoin_client.get_accounts()
                                else:
                                    aux = 0
                                    free = 0
                                    for i in accounts:
                                        if i["currency"] == i:
                                            aux = 1
                                            free = i["balance"]
                                            
                                    if aux == 0:
                                        while aux == 0:
                                            time.sleep(20)
                                            accounts = kucoin_client.get_accounts()
                                            for i in accounts:
                                                if i["currency"] == i:
                                                    aux = 1
                                                    qty_aux = i["balance"]
                                    else:
                                        qty_aux = free
                                        while free == qty_aux:
                                            time.sleep(20)
                                            accounts = kucoin_client.get_accounts()
                                            for i in accounts:
                                                if i["currency"] == i:
                                                    qty_aux = i["balance"]
                                                            
                                
                                
                                #TRANSFERENCIA DE MAIN A TRADING ACCOUNT                                
                                transfer = kucoin_client.create_inner_transfer('main', 'trade', qty_aux)
                                '''
                                OPCIONES PARA PASAR DINERO:
                                    1. ENVIAR MENSAJE Y RECIBIR CONFIRMACIÓN
                                    2. ENCONTRAR ALGUNA SOLUCIÓN PARA PASAR DE MAIN A TRADING ACOUNT
                                    3. PASAR  DE TODO Y COGER OTRA API
                                '''
                                
                                '''
                                #ENVIAR MENSAJE POR CORREO PARA PASAR DINERO DE CUENTA
                                message = 'hola'
                                subject = 'prueba'
                                message = 'Subject: {}\n\n{}'.format(subject, message)
                                server = smtplib.SMTP('smtp.gmail.com', 587)
                                server.starttls()
                                server.login('tester.info.0@gmail.com', 'Test123456789.')
                                server.sendmail('tester.info.0@gmail.com@gmail.com', 'tester.info.0@gmail.com', message)
                                server.quit()
                                '''
                                 
                                time.sleep(60)
                                accounts = kucoin_client.get_accounts()
                                usdt = 0
                                for i in accounts:
                                    if i["currency"] == "USDT":
                                        usdt = i["balance"]
                                
                                print("Genero orden de venta en KUCOIN")         
                                sell_order = kc.kc_make_sell_limit_order(kucoin_client, sym_kc, kucoin_price, qty_aux)
                                if sell_order is not None:
                                    time.sleep(1)
                                
                                    if usdt == 0:
                                        while usdt == 0:
                                            for i in accounts:
                                                if i["currency"] == "USDT":
                                                    usdt = i["balance"]
                                            accounts = kucoin_client.get_accounts()
 
                                    else:
                                        usdt_aux = usdt
                                        while usdt == usdt_aux:
                                            for i in accounts:
                                                if i["currency"] == "USDT":
                                                    usdt_aux = i["balance"]
                                            accounts = kucoin_client.get_accounts()
                        else:
                            print("comprobar cuanto tengo y si compró, vender")
                                            
                    functions.update_arbitraje()              
                    
                else:
                    print("No hay fondos suficientes")
    
    return True     
        

def multi_operation_arb(binance_client, kucoin_client, sym):
    print("\n")
    print("ARBITRAJE HACIENDO COMPRA/VENTA SIN TRANSFERENCIA") 
    
    binance_pairs = bn.bn_get_market_prices(binance_client)
    kucoin_pairs = kc.kc_get_market_info(kucoin_client)
    
    aux_binance_pairs = []
    
    aux_kucoin_pairs = []
    
    for i in binance_pairs:
        aux_binance_pairs.append(i["symbol"].replace("USDT",""))
        
    for i in kucoin_pairs:
        aux_kucoin_pairs.append(i["symbol"].replace("-USDT",""))
    
    crypto_list = list(set(aux_binance_pairs) & set(aux_kucoin_pairs))
    crypto_list.remove("BCHSV")
  
    if sym in crypto_list:
        print("\n")
        print("COMENZANDO ARBITRAJE")

        custom_buy_init = time.time()
        custom_buy_time = 0
       
        while custom_buy_time < 100000 and arbitraje_state == 0:
            
            if arbitraje_state == 1:
                break
            
            sym_bn = sym + "USDT"
            binance_price = float((binance_client.get_symbol_ticker(symbol = sym_bn))["price"])
            sym_kc = sym + "-USDT"
            kucoin_price = float((kucoin_client.get_ticker(symbol = sym_kc))["price"])

        
            functions.insert_new_arbitraje(sym_bn,0)  


            print("Binance -- KuCoin")
            print(binance_price, " -- ", kucoin_price)
            print("\n")
            
            time.sleep(1)
            
            if (binance_price < kucoin_price):
                #COMPRAR EN BINANCE Y VENDER EN KUCOIN
                print("\n")
                print("Menor en BINANCE que en KUCOIN")
                
                usdt = float(binance_client.get_asset_balance(asset='USDT')["free"])
            
                kc_qty = 0
                kc_asset = kucoin_client.get_accounts()
    
                for j in kc_asset:
                    if (j["currency"] == sym):
                        if j["available"] != "0":
                            kc_qty = float(j["available"])
                            continue
                
                if kc_qty != 0 and usdt != 0:
                    print("Tengo ",kc_qty, " de ", sym, " en Kucoin")
                    
                    if (kc_qty*binance_price < usdt):
                        print("Puedo comprar en binance la cantidad equivalente porque tengo USDT")
                        
                        ### CHEQUEAR QUE ES VIABLE
                        valor_en_binance = kc_qty*binance_price - (0.1*kc_qty*binance_price/100)
                        valor_en_kucoin = kc_qty*kucoin_price - (0.1*kc_qty*binance_price/100)
                        
                        antes_bn = kc_qty*binance_price
                        antes_kc = kc_qty*kucoin_price
                        
                        #CONTAR LA COMISION
                        if ((valor_en_binance + valor_en_kucoin) > (antes_bn + antes_kc)):
                            
                            
                            #INSERTAR EN BASE DE DATOS
                            functions.insert_new_arbitraje(sym_bn, 0)  
                            
                            
                            print("Funcionaría")
                            print("DESPUES:", valor_en_binance + valor_en_kucoin)
                            print("ANTES:", antes_bn + antes_kc)
                            print("\n")
                            
                            #VENDER EN KUCOIN
                            '''
                            sell_order = kc.kc_make_sell_limit_order(kucoin_client, sym_kc, kucoin_price, kc_qty)
                            check_sell = None
                            while check_sell == None:
                                time.sleep(1)
                                check_sell = kc.kc_check_open_orders(kucoin_client, sym_kc)
                                
                            
                            #COMPRAR EN BINANCE
                            buy_order = bn.bn_make_buy_limit_order(binance_client, sym_bn, binance_price, kc_qty)
                            if buy_order is not None:                                        
                                time.sleep(1)

                                open_orders = binance_client.get_open_orders(symbol = sym_bn)
                                check_sell = kc.kc_check_open_orders(kucoin_client, sym_kc)

                                while check_sell != None and pd.Series(open_orders).empty == False:
                                    open_orders = binance_client.get_open_orders(symbol = sym_bn)
                                    check_sell = kc.kc_check_open_orders(kucoin_client, sym_kc)
                                  

                            '''
                            
                        else:
                            print("No es rentable con la cantidad de ", sym, " que tengo en KUCOIN")
                            
                    else:
                        print("Cantidad insuficiente de USDT en BINANCE para realizar arbitraje")
                
            elif (binance_price > kucoin_price):
                #COMPRAR EN KUCOIN Y VENDER EN BINANCE
                print("\n")
                print("Mayor en BINANCE que en KUCOIN")
                
                kc_usdt = 0
                kc_asset = kucoin_client.get_accounts()
                for j in kc_asset:
                    if (j["currency"] == "USDT"):
                        if j["available"] != 0.0:
                            kc_usdt = float(j["available"])
                            continue
                
                bn_qty = float(binance_client.get_asset_balance(asset=sym)["free"])

                if kc_usdt != 0 and bn_qty != 0:
                    print("Tengo ",bn_qty, " de ", sym, " en BINANCE")
                    
                    if (bn_qty*kucoin_price < kc_usdt):
                        print("Puedo comprar en kucoin la cantidad equivalente porque tengo USDT")
                        
                        ### CHEQUEAR QUE ES VIABLE
                        valor_en_kucoin = bn_qty*kucoin_price - (0.1*bn_qty*kucoin_price/100)
                        valor_en_binance = bn_qty*binance_price - (0.1*bn_qty*kucoin_price/100)
                        
                        antes_kc = bn_qty*kucoin_price
                        antes_bn = bn_qty*binance_price
                        
                        #CONTAR LA COMISION
                        if ((valor_en_binance + valor_en_kucoin) > (antes_bn + antes_kc)):
                            
                            
                            #INSERTAR EN BASE DE DATOS
                            functions.insert_new_arbitraje(sym_bn, 1)  
                            
                            
                            print("Funcionaría")
                            print("DESPUES:", valor_en_binance + valor_en_kucoin)
                            print("ANTES:", antes_bn + antes_kc)
                            print("\n")
                            
                            #COMPRAR EN KUCOIN
                            '''
                            buy_order = kc.kc_make_buy_limit_order(kucoin_client, sym_kc, kucoin_price, bn_qty)
                            check_buy = None
                            while check_buy == None:
                                time.sleep(1)
                                check_buy = kc.kc_check_open_orders(kucoin_client, sym_kc)
                                
                            
                            #VENDER EN BINANCE
                            sell_order = bn.bn_make_sell_limit_order(binance_client, sym_bn, binance_price, bn_qty)                                                            
                            if sell_order is not None:                                        
                                time.sleep(1)

                                open_orders = binance_client.get_open_orders(symbol = sym_bn)
                                check_buy = kc.kc_check_open_orders(kucoin_client, sym_kc)

                                while check_buy != None and pd.Series(open_orders).empty == False:
                                    open_orders = binance_client.get_open_orders(symbol = sym_bn)
                                    check_buy = kc.kc_check_open_orders(kucoin_client, sym_kc)
                            '''
                        else:
                            print("No es rentable con la cantidad de ", sym, " que tengo en BINANCE")    
                            
                    else:
                        print("Cantidad insuficiente de USDT en KUCOIN para realizar arbitraje")   
            
            custom_buy_time = time.time() - custom_buy_init
            

    else:
        print("El símbolo introducido no se encuentra en ambos exchanges")

    return True    
      
            
def select_arbitrage (mode, binance_client, kucoin_client):
    #functions.insert_mode(2, mode)
    sym = functions.get_arb_symbol()

    if mode == 1:
        return transfer_arb(binance_client, kucoin_client)
    
    if mode == 2:
        #print("\tINTRODUZCA SÍMBOLO PARA ARBITRAJE (Ej: btc)")
        #sym = input().upper()
        return multi_operation_arb(binance_client, kucoin_client, sym[0][1])

