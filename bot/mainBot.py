from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.enums import *
from datetime import datetime

import time


import pandas as pd
import talib
import re
import math
import numpy
import threading
import keyboard
import socketio

import custom_binance as bn
import custom_kucoin as kc
import utils as ut
import strategies as st
import arbitraje as arb
import functions 

        ##########################
        ### PROGRAMA PRINCIPAL ###
        ##########################      


sio = socketio.Client()

def stop():
    sio.wait()

@sio.event
def llamadaRecibida(data):
    if len(data) > 0:
        functions.clean_all()
        arb.arbitraje_state = 1  
        st.trading_state = 1
        t1.join()
        t1.close()
        

# standard Python
#functions.clean_all()
sio.connect('http://localhost:8000')

option = functions.get_election()

while (arb.arbitraje_state == 0 and st.trading_state == 0):
    
    st.trading_state = 0
    arb.arbitraje_state = 0
    
    if option[0][1] == '1':
        
        t1 = threading.Thread(target = stop) 
        t1.start()
        
        #Claves de conexión con API de BINANCE
        #Correo: tester_ex_0@outlook.com
        api_key_tester_0 = 'ljGooMh23pyX6HoeTKVVM9ZqjBqx1kI5GFPS0ycuFOIohhv5l20NbKuP5mxFAIQT'
        api_secret_tester_0 = 'uOpgceZXaMUVW19bRPBMeSbe12oDEFWBiZlcZn09pR9Gq9X3TxB1TNJ3gVoVaQdT'
        
        #CONEXION CON API
        client = bn.bn_init(api_key_tester_0, api_secret_tester_0)
        
        balance = bn.bn_get_personal_crypto_balance(client)
        print(balance)
        
        st.select_strategy(option[0][2], client)
        
        time.sleep(1)
    
        
    if option[0][1] == '2':
        
        t1 = threading.Thread(target = stop) 
        t1.start()
    
        ###  BINANCE  ###
        #Claves de conexión con API de BINANCE
        #Correo: tester_ex_0@outlook.com
        binance_key_tester_0 = 'ljGooMh23pyX6HoeTKVVM9ZqjBqx1kI5GFPS0ycuFOIohhv5l20NbKuP5mxFAIQT'
        binance_secret_tester_0 = 'uOpgceZXaMUVW19bRPBMeSbe12oDEFWBiZlcZn09pR9Gq9X3TxB1TNJ3gVoVaQdT'
        
        ###  KUCOIN  ###
        #Claves de conexión con API de KUCOIN
        #Correo: tester_ex_0@outlook.com
        kucoin_key_tester_0 = "6092dd428304410006083336"
        kucoin_secret_tester_0 = "9c72097e-7607-41d0-83e4-cc882f68abdf"
        kucoin_passphrase_tester_0 = "tester_ex_0"
        
        #CONEXION CON API
        kucoin_client = kc.kc_init(kucoin_key_tester_0, kucoin_secret_tester_0, kucoin_passphrase_tester_0)
        binance_client = bn.bn_init(binance_key_tester_0, binance_secret_tester_0)
         
        ###  EMPIEZA EL ARBITRAJE  ###
        
        arb.select_arbitrage(option[0][2], binance_client, kucoin_client)
        t1.join()
