# -*- coding: utf-8 -*-
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.enums import *
from datetime import datetime

#import requests
import time

import pandas as pd
import talib
import re
#import math
import numpy

import utils as ut
#import strategies as st


def bn_init(api_key, api_secret):
    """
    Función para inicializar la conexión con el exchange de Binance
    
    Parameters
    ----------
    api_key : string clave de api
    api_secret : string clave secreta

    Returns
    -------
        Devuelve un identificador de la conexión en caso de poder conectarse

    """   
    return Client(api_key, api_secret, {"verify": True, "timeout": 20})
    #return Client(api_key, api_secret)


def bn_get_personal_crypto_balance(client):
    """
    Funcion para obtener el balance personal de todas las monedas de la cartera    
    
    Parameters
    ----------
    client : identificador de la conexion

    Returns
    -------
        Devuelve un objeto de tipo panda

    """  
    balance_info = (client.get_account())["balances"]
    aux = []
    for i in balance_info:
        if i["free"] > '0.000000000':
            aux.append(i)
            
    return pd.DataFrame(aux)


def bn_get_market_prices(client):
    time.sleep(0.01)
    """
    Funcion para obtener el precio actual de todas las monedas    
    
    Parameters
    ----------
    client : identificador de la conexion

    Returns
    -------
        Devuelve un objeto de tipo panda

    """  
    exchange_info = pd.Series(client.get_all_tickers())
    
    #expresiones regulares para pares con USDT que no interesan
    patron = re.compile('[A-Z]*USDT')
    patronDown = re.compile('[A-Z]*DOWNUSDT')
    patronUp = re.compile('[A-Z]*UPUSDT')
    patronAux = re.compile('USDT[A-Z]*')
    patronExc = re.compile('[A-Z]+USDT[A-Z]+')
    
    aux = []
    for i in exchange_info:
        if patron.match(i["symbol"]): 
            if not(patronAux.match(i["symbol"]) or patronDown.match(i["symbol"])
                   or patronUp.match(i["symbol"]) or patronExc.match(i["symbol"])):
                aux.append(i)
    
    return pd.Series(aux)


def bn_history_market_prices(client):
    """
    Funcion para mostrar el historico de precios de todas las monedas    
    
    Parameters
    ----------
    client : identificador de la conexion

    """  
    market_prices = bn_get_market_prices(client)
    for i in market_prices:
        #velas de 30 min representadas en 1 hora
        klines = client.get_historical_klines(i["symbol"], Client.KLINE_INTERVAL_15MINUTE, "1 hour ago UTC")       
        aux = pd.DataFrame(klines)
        if not len(aux) == 0:
            print("\n")
            print(i["symbol"])
            for i in klines:
                del i[5:]
            historic = pd.DataFrame(klines, columns=['date', 'open', 'high', 'low', 'close'])
            historic.set_index('date', inplace=True)
            print(historic)    

        
def bn_check_order_by_id(client, id, sym):
    """
    Funcion para obtener chequear si la orden está en el libro de ordenes    
    
    Parameters
    ----------
    client : identificador de la conexion
    id : identificador de la orden
    sym : simbolo que representa al par
    
    Returns
    -------
        Devuelve un objeto tipo bool que es true si la orden se encuentra en el libro de ordenes
        y false en caso contrario

    """  
    init = time.time()
    elapsed_time = 0
    check = False
    #open_orders = client.get_open_orders(symbol = sym)
    print(open_orders)
    while elapsed_time < 5 and check == False:
        open_orders = client.get_open_orders(symbol = sym)
        if pd.Series(open_orders).empty == False:
            check = True
        elapsed_time = time.time() - init
                                        
    '''
    all_orders = client.get_all_orders(symbol=sym)
    check = False
    init = time.time()
    elapsed_time = 0
    while check == False and elapsed_time < 5:
        for i in all_orders:
            elapsed_time = time.time() - init
            if (i['orderId'] == id):
                check = True
        all_orders = client.get_all_orders(symbol=sym)
    '''
    
    return check


def bn_check_open_orders(client, sym):
    """
    Funcion para chequear si la orden se ha ejecutado    
    
    Parameters
    ----------
    client : identificador de la conexion
    order : orden a chequear
    sym : simbolo que representa al par

    """   
    init = time.time()
    elapsed_time = 0
    
    while elapsed_time < 5 and len(client.get_open_orders(symbol = sym)) == 0:
        print("No ha llegado la orden")
        print(client.get_open_orders(symbol = sym))
        elapsed_time = time.time() - init
    
    if (elapsed_time >= 5):
        return False
    else: 
        return True        
            
def bn_check_order(client, order, sym):
    """
    Funcion para chequear si la orden se ha ejecutado    
    
    Parameters
    ----------
    client : identificador de la conexion
    order : orden a chequear
    sym : simbolo que representa al par

    """   
    print("\n")
    print("Chequeando la orden")
    aux = True
    while aux:
        print("La orden todavia no se ha publicado")
        trades = client.get_my_trades(symbol = sym)
        if trades[len(trades)-1]['orderId'] == order['orderId']:
            print("ORDEN PUBLICADA")
            aux = False

    
def bn_make_buy_limit_order(client, sym, actual_price, qty = 0):
    """
    Funcion para generar orden de compra tipo LIMIT    
    
    Parameters
    ----------
    client : identificador de la conexion
    sym : simbolo que representa al par
    actual_price : precio al que se realizará la orden

    Returns
    -------
        Devuelve la descripción de la orden generada

    """   
    print("\n")
    print("Generando orden de COMPRA de cripto")
    
    free_usdt_balance = 0.00000000
    balances = pd.Series(client.get_account()["balances"])
    for i in balances:
        if i["asset"] == 'USDT':
            free_usdt_balance = float(i["free"])
    
    lot_info = ut.filter_info(pd.Series(pd.Series(client.get_symbol_info(sym))["filters"]), 'LOT_SIZE')
    qty = float(ut.truncate(free_usdt_balance/actual_price, lot_info))
    
    if not qty * actual_price < 10.00000000:
        try:
            
            order = client.create_order(
                symbol = sym,
                side = 'BUY',
                type = 'LIMIT',
                timeInForce = 'GTC',
                quantity = qty,
                price = actual_price)
            
            #print(order)
            return order;

        except BinanceAPIException as ex:
            print(ex)
            
        except BinanceOrderException as ex:
            print(ex)
    else:
        print("La orden en el par", sym, "debe superar los 10 USDT")

        
def bn_make_sell_limit_order(client, sym, actual_price):
    """
    Funcion para generar orden de venta tipo LIMIT    
    
    Parameters
    ----------
    client : identificador de la conexion
    sym : simbolo que representa al par
    actual_price : precio al que se realizará la orden

    Returns
    -------
        Devuelve la descripción de la orden generada

    """   
    print("\n")
    print("Generando orden de VENTA de cripto")

    balances = pd.Series(client.get_account()["balances"])
    for i in balances:
        if float(i["free"]) > 0.00000000:
            #Condicion para q no mire el saldo de USDT
            if not i["asset"] == 'USDT':
                #Condicion porque me apetece tener ADA y no venderlo
                if not i["asset"] == 'ADA':
                    aux = i["asset"] + 'USDT'
                    if sym == aux:
                        
                        lot_info = ut.filter_info(pd.Series(pd.Series(client.get_symbol_info(sym))["filters"]), 'LOT_SIZE')
                        qty = float(ut.truncate(float(i["free"]),lot_info))                        
                        
                        lot_info = ut.filter_info(pd.Series(pd.Series(client.get_symbol_info(sym))["filters"]), 'PRICE_FILTER')
                        actual_price = ut.truncate(actual_price, lot_info)
                                                
                        if qty * float(actual_price) > 10.00000000:    
                            try:
                                
                                order = client.create_order(
                                    symbol = sym,
                                    side = 'SELL',
                                    type = 'LIMIT',
                                    timeInForce = 'GTC',
                                    quantity = qty,
                                    price = actual_price)
                                
                                #print(order)
                                return order
        
                            except BinanceAPIException as ex:
                                print(ex)
                                
                            except BinanceOrderException as ex:
                                print(ex)
                                
                                
def bn_make_sell_oco_order(client, sym, actual_price, limit_per, stop_per):
    """
    Funcion para generar orden de venta tipo OCO    
    
    Parameters
    ----------
    client : identificador de la conexion
    sym : simbolo que representa al par
    actual_price : precio actual 

    Returns
    -------
        Devuelve la descripción de la orden generada

    """  
    print("\n")
    print("Generando orden de VENTA de cripto")

    balances = pd.Series(client.get_account()["balances"])
    for i in balances:
        if float(i["free"]) > 0.00000000:
            #Condicion para q no mire el saldo de USDT
            if not i["asset"] == 'USDT':
                #Condicion porque me apetece tener ADA y no venderlo
                if not i["asset"] == 'ADA':
                    aux = i["asset"] + 'USDT'
                    if sym == aux:
                        
                        lot_info = ut.filter_info(pd.Series(pd.Series(client.get_symbol_info(sym))["filters"]), 'LOT_SIZE')
                        qty = float(ut.truncate(float(i["free"]),lot_info))                        
                        
                        lot_info = ut.filter_info(pd.Series(pd.Series(client.get_symbol_info(sym))["filters"]), 'PRICE_FILTER')
                        stop = ut.truncate(actual_price - actual_price*stop_per/100, lot_info)
                        actual_price = ut.truncate(actual_price + actual_price*limit_per/100, lot_info)
                        print("Stop ",stop)
                        print("Price ",actual_price)
                                                
                        if qty * float(actual_price) > 10.00000000:    
                            try:
                                
                                order= client.order_oco_sell(
                                    symbol= sym,                                            
                                    quantity= qty,                                            
                                    price= actual_price,                                            
                                    stopPrice= stop,                                            
                                    stopLimitPrice= stop,                                            
                                    stopLimitTimeInForce= 'GTC')                
                                
                                #print(order)
                                return order
        
                            except BinanceAPIException as ex:
                                print(ex)
                                
                            except BinanceOrderException as ex:
                                print(ex)
                                 

def bn_cancel_open_orders(client, sym):
    """
    Funcion para cancelar ordenes abiertas en un par   
    
    Parameters
    ----------
    client : identificador de la conexion
    sym : simbolo que representa al par

    """   
    print("\n")
    #print("Cancelando las ordenes en el par: ", sym)
    open_orders = client.get_open_orders(symbol = sym)
    while len(open_orders) != 0:
        for i in open_orders:
            try:
                cancel = client.cancel_order(
                    symbol = sym,
                    orderId = i['orderId'])
            
            except BinanceAPIException as ex:
                print(ex)

        open_orders = client.get_open_orders(symbol = sym)

        #######################
        ###### WITHDRAWAL #####
        #######################
        
def bn_get_withdrawal_fees (client):
    time.sleep(0.01)
    """
    Funcion para obtener los precios de cierre de un par    
    
    Parameters
    ----------
    client : identificador de la conexion
    sym : simbolo que representa al par
    interval : intervalo de tiempo de velas

    Returns
    -------
        Devuelve una lista con los valores

    """
    r = client.get_asset_details()
    #r =requests.get('https://xkcd.com/1906/')
    return r        



        #############################
        ###### TEST INDICATORS ######
        #############################
        
def bn_get_close_prices(client, sym, interval):
    time.sleep(0.01)
    """
    Funcion para obtener los precios de cierre de un par    
    
    Parameters
    ----------
    client : identificador de la conexion
    sym : simbolo que representa al par
    interval : intervalo de tiempo de velas

    Returns
    -------
        Devuelve una lista con los valores

    """
    klines = client.get_historical_klines(sym, Client.KLINE_INTERVAL_1MINUTE, "6 hour ago UTC")       
    aux = pd.DataFrame(klines)
    close = []
    if not len(aux) == 0:
        for i in klines:
            del i[5:]
            close.append(float(i[4]))
    
    return close

def bn_get_low_prices(client, sym, interval):
    time.sleep(0.01)
    """
    Funcion para obtener los precios bajos de las velas de una grafico   
    
    Parameters
    ----------
    client : identificador de la conexion
    sym : simbolo que representa al par
    interval : intervalo de tiempo de velas

    Returns
    -------
        Devuelve una lista con los valores

    """
    time.sleep(0.01)
    klines = client.get_historical_klines(sym, Client.KLINE_INTERVAL_1MINUTE, "15 minutes ago UTC")       
    aux = pd.DataFrame(klines)
    low = []
    if not len(aux) == 0:
        for i in klines:
            del i[5:]
            low.append(float(i[3]))
            
    return low
    
def bn_get_rsi(client, sym):
    """
    Funcion para obtener el indicador RSI de un par    
    
    Parameters
    ----------
    client : identificador de la conexion
    sym : simbolo que representa al par

    Returns
    -------
        Devuelve un array de tipo numpy.array con los valores

    """  
    klines = client.get_historical_klines(sym, Client.KLINE_INTERVAL_1MINUTE, "6 hour ago UTC")       
    aux = pd.DataFrame(klines)
    values = []
    if not len(aux) == 0:
        for i in klines:
            del i[5:]
            values.append(float(i[4]))
    
    rsi = talib.RSI(numpy.array(values), timeperiod = 6)
    
    return rsi

        
def bn_get_macd(client, sym): 
    """
    Funcion para obtener el indicador MACD de un par    
    
    Parameters
    ----------
    client : identificador de la conexion
    sym : simbolo que representa al par

    Returns
    -------
        Devuelve un array de tipo numpy.array con los valores

    """
    klines = client.get_historical_klines(sym, Client.KLINE_INTERVAL_1MINUTE, "6 hour ago UTC")       
    aux = pd.DataFrame(klines)
    values = []
    if not len(aux) == 0:
        for i in klines:
            del i[5:]
            values.append(float(i[4]))
    
    macd, signal, diff = talib.MACD(numpy.array(values))

    return macd, signal, diff


def bn_get_boll(client, sym):
    """
    Funcion para obtener el indicador BOLL de un par    
    
    Parameters
    ----------
    client : identificador de la conexion
    sym : simbolo que representa al par

    Returns
    -------
        Devuelve un array de tipo numpy.array con los valores

    """
    klines = client.get_historical_klines(sym, Client.KLINE_INTERVAL_1MINUTE, "6 hour ago UTC")       
    aux = pd.DataFrame(klines)
    values = []
    if not len(aux) == 0:
        for i in klines:
            del i[5:]
            values.append(float(i[4]))
    
    up, mid, low = talib.BBANDS(numpy.array(values), timeperiod=21, nbdevup=2, nbdevdn=2, matype=0)
    
    return up, mid, low


def bn_get_ema(client, sym, timeperiod):
    time.sleep(0.01)
    """
    Funcion para obtener el indicador EMA de un par    
    
    Parameters
    ----------
    client : identificador de la conexion
    sym : simbolo que representa al par
    timeperiod : periodo de las velas

    Returns
    -------
        Devuelve un array de tipo numpy.array con los valores

    """
    klines = client.get_historical_klines(sym, Client.KLINE_INTERVAL_1MINUTE, "6 hour ago UTC")       
    aux = pd.DataFrame(klines)
    values = []
    if not len(aux) == 0:
        for i in klines:
            del i[5:]
            values.append(float(i[4]))
    
    ema = talib.EMA(numpy.array(values), timeperiod=timeperiod)
    
    return ema

def bn_get_engulfing_pattern (client, sym):
    time.sleep(0.01)
    """
    Funcion para obtener Patrón envolvente en grafico de velas   
    
    Parameters
    ----------
    client : identificador de la conexion
    sym : simbolo que representa al par

    Returns
    -------
        Devuelve un array de tipo numpy.array con los valores

    """
    time.sleep(0.01)
    klines = client.get_historical_klines(sym, Client.KLINE_INTERVAL_1MINUTE, "15 minutes ago UTC")       
    aux = pd.DataFrame(klines)
    open = []
    high = []
    close = []
    low = []
    if not len(aux) == 0:
        for i in klines:
            del i[5:]
            open.append(float(i[1]))
            high.append(float(i[2]))
            low.append(float(i[3]))
            close.append(float(i[4]))
            
    integer = talib.CDLENGULFING(numpy.array(open), numpy.array(high), numpy.array(low), numpy.array(close))
    
    return integer