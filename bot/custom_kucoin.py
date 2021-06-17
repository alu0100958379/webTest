# -*- coding: utf-8 -*-
from kucoin.client import Client

import time
import pandas as pd
import re

import utils as ut

def kc_init(api_key, api_secret, api_passphrase):
    """
    Función para inicializar la conexión con el exchange de KUCOIN
    
    Parameters
    ----------
    api_key : string clave de api
    api_secret : string clave secreta

    Returns
    -------
        Devuelve un identificador de la conexión en caso de poder conectarse

    """   
    return Client(api_key, api_secret, api_passphrase)


def kc_get_market_info(client):
    time.sleep(0.01)
    """
    Funcion para obtener la informacion de todos los pares con USDT    
    
    Parameters
    ----------
    client : identificador de la conexion

    Returns
    -------
        Devuelve un objeto de tipo panda

    """  
        
    exchange_info = pd.Series(client.get_symbols())
    
    #expresiones regulares para pares con USDT que no interesan
    patron = re.compile('[A-Z]*-USDT')
    
    aux = []
    for i in exchange_info:
        if patron.match(i["symbol"]): 
            aux.append(i)
    
    return pd.Series(aux)


def kc_make_sell_limit_order(client, sym, actual_price, qty = 0):
    time.sleep(0.01)
    """
    Funcion para generar orden de venta limit en kucoin    
    
    Parameters
    ----------
    client : identificador de la conexion
    sym : simbolo
    actual_price : precio actual
    qty : cantidad 

    Returns
    -------
        Devuelve un objeto de tipo panda

    """
    print("\n")
    print("Generando orden de VENTA de cripto")
    if qty != 0:
        market_info = kc_get_market_info(client)
        for i in market_info:
            if i["symbol"] == sym:
                qty_filter = ut.filter_info_val(i["baseIncrement"])
                price_filter = ut.filter_info_val(i["priceIncrement"])
        
        qty = ut.truncate(float(qty), qty_filter)
        actual_price = ut.truncate(float(actual_price), price_filter)
     
        print(actual_price)
        try:
            order = client.create_limit_order(
                    sym,                #symbol
                    Client.SIDE_SELL,   #side
                    actual_price,       #price
                    qty)                #qty
            '''          
            order = client.create_limit_order(
                        'KCS-BTC',          #symbol
                        Client.SIDE_BUY,    #side
                        '0.01',             #price
                        '1000')             #qty
            '''
            
        except():
            print("No se ejecutó la venta")
         
    else: 
        print("La cantidad indicada es errónea")
       

def kc_check_open_orders(client, sym):
    orders = client.get_orders(symbol=sym, status='active')
