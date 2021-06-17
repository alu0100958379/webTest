import time
import re

'''
def check_price(client, sym, actual_price):
    init = time.time()
    sell = 0
    
    while sell == 0:
        next_price = float((client.get_symbol_ticker(symbol = sym))["price"])
        print("comparando:", actual_price, "con ", next_price)
        elapsed_time = time.time() - init
        if next_price >= (actual_price + (actual_price*0.2/100)):
            sell = 1 
        elif next_price <= (actual_price - (actual_price*0.6/100)):
            break
        elif elapsed_time > 600 and sell == False:
            break
    
    return sell
'''

#TODO:
    #AJUSTARLOS MEJOR???????
    
def check_rsi(rsi_v):
    check = 0
    indice_c = -1   #Se asegura comenzar desde el principio
    
    if len(rsi_v) == 360:
        rsi = rsi_v[356:].tolist()
    else:
        rsi = rsi_v[355:].tolist()
        
    for elemento in rsi:
        indice_c = -1
        indice = rsi.index(elemento)  # Se asigna el numero de indice del elemento a comparar
        if indice == (len(rsi)-1):
            if elemento > 70.00000000 and elemento < 82.00000000:
                check = check + 1
                continue
        else:
            for comparacion in rsi: # Se toma el elemento a comparar
                indice_c += 1
                if indice_c == indice: 
                    continue # Se reinicia el bucle
                elif indice_c-indice >= 2 or indice_c-indice < 0:
                    continue # Se reinicia el bucle
                elif elemento < comparacion and comparacion < ((elemento*0.25)+elemento):
                    check = check + 1          
    
    if check == len(rsi):
        return True
        print(rsi)
    else:
        return False


def check_macd(diff_v):
    check = 0
    indice_c = -1   #Se asegura comenzar desde el principio
    
    if len(diff_v) == 360:
        diff = diff_v[356:].tolist()
    else:
        diff = diff_v[355:].tolist()
    
    for elemento in diff:
        indice_c = -1
        indice = diff.index(elemento)  # Se asigna el numero de indice del elemento a comparar
        if indice == (len(diff)-1):
            continue
        else:
            for comparacion in diff: # Se toma el elemento a comparar
                indice_c += 1
                if indice_c == indice: 
                    continue # Se reinicia el bucle
                elif indice_c-indice >= 2 or indice_c-indice < 0:
                    continue # Se reinicia el bucle
                elif comparacion >= elemento:
                    check = check + 1          
    
    if check == (len(diff)-1):
        return True
    else:
        return False

def check_boll(up_v, mid_v, low_v):
    check_up = check_mid = check_low = 0
    indice_c = -1   #Se asegura comenzar desde el principio
    
    if len(up_v) == 360:
        up = up_v[357:].tolist()
        mid = mid_v[357:].tolist()
        low = low_v[357:].tolist()
    else:
        up = up_v[356:].tolist()
        mid = up_v[356:].tolist()
        low = up_v[356:].tolist()
        
    for elemento in up:
        indice_c = -1
        indice = up.index(elemento)  # Se asigna el numero de indice del elemento a comparar
        if indice == (len(up)-1):
            continue
        else:
            for comparacion in up: # Se toma el elemento a comparar
                indice_c += 1
                if indice_c == indice: 
                    continue # Se reinicia el bucle
                elif indice_c-indice >= 2 or indice_c-indice < 0:
                    continue # Se reinicia el bucle
                elif comparacion > elemento:
                    check_up = check_up + 1          
    
    for elemento in mid:
        indice_c = -1
        indice = mid.index(elemento)  # Se asigna el numero de indice del elemento a comparar
        if indice == (len(mid)-1):
            continue
        else:
            for comparacion in mid: # Se toma el elemento a comparar
                indice_c += 1
                if indice_c == indice: 
                    continue # Se reinicia el bucle
                elif indice_c-indice >= 2 or indice_c-indice < 0:
                    continue # Se reinicia el bucle
                elif comparacion > elemento:
                    check_mid = check_mid + 1
    
    for elemento in low:
        indice_c = -1
        indice = low.index(elemento)  # Se asigna el numero de indice del elemento a comparar
        if indice == (len(low)-1):
            continue
        else:
            for comparacion in low: # Se toma el elemento a comparar
                indice_c += 1
                if indice_c == indice: 
                    continue # Se reinicia el bucle
                elif indice_c-indice >= 2 or indice_c-indice < 0:
                    continue # Se reinicia el bucle
                elif comparacion < elemento:
                    check_low = check_low + 1
                    
    if check_up == check_mid == check_low == (len(up)-1):
        return True
    else:
        return False

def check_ema(ema25, ema50, ema100):
    
    if len(ema25) == 360:
        ema25 = ema25[340:].tolist()
        ema50 = ema50[340:].tolist()
        ema100 = ema100[340:].tolist()
    
    else:
        ema25 = ema25[339:].tolist()
        ema50 = ema50[339:].tolist()
        ema100 = ema100[339:].tolist()
    
    check = 0
    if len(ema25) == len(ema50) and len(ema25) == len(ema100):
        for i in range(0,len(ema25)):
            if (i == len(ema25)-1):
                continue
            else:
                for j in range(0, len(ema25)):
                    if j == i:
                        continue
                    elif j-i >= 2 or j-i < 0:
                        continue
                    #else:
                    #    print("Comparando posicion ", i , " con posicion " , j)
                    elif ema25[j] > ema25[i] and ema50[j] > ema50[i] and ema100[j] > ema100[i]:
                        check = check + 1
                
    if check == (len(ema25)-1):
        return True
    else:
        return False
    

def check_close_ema(ema25, close):
    if len(ema25) == 360:
        ema25 = ema25[340:].tolist()
        close = close[340:]
        
    else:
        ema25 = ema25[339:].tolist()
        close = close[339:]
        
    check = True
    if len(ema25) == len(close):
        for i in range(0,len(ema25)):
            if ema25[i] > close[i]:
                check = False
                
    return check


def check_close_engulfing(ema200, close):
    if len(ema200) == 360:
        ema200 = ema200[350:].tolist()
        close = close[350:]
        
    else:
        ema200 = ema200[349:].tolist()
        close = close[349:]
        
    check = True
    if len(ema200) == len(close):
        for i in range(0,len(ema200)):
            if ema200[i] > close[i]:
                check = False
                
    return check
    
def filter_info_val(filt):
    """
    Función para obtener numero de decimales de un filtro
    
    Parameters
    ----------      
    filt : string contiene el filtro a aplicar

    Returns
    -------
        Devuelve el numero de decimales del filtro
        
    """
    patron1 = re.compile('0.1[0]*')
    patron2 = re.compile('0.01[0]*')
    patron3 = re.compile('0.001[0]*')
    patron4 = re.compile('0.0001[0]*')
    patron5 = re.compile('0.00001[0]*')
    patron6 = re.compile('0.000001[0]*')
    patron7 = re.compile('0.0000001[0]*')
    patron8 = re.compile('0.00000001[0]*')
    
    val = 0
    
    if patron1.match(filt): 
        val = 1
    elif patron2.match(filt): 
        val = 2
    elif patron3.match(filt): 
        val = 3
    elif patron4.match(filt): 
        val = 4
    elif patron5.match(filt): 
        val = 5
    elif patron6.match(filt): 
        val = 6
    elif patron7.match(filt): 
        val = 7
    elif patron8.match(filt): 
        val = 8
    
    print(val)
    return val


def filter_info(info, filt):
    """
    Función para obtener numero de decimales de un filtro
    
    Parameters
    ----------
    info : string contiene informacion acerca del par       
    filt : string contiene el filtro a aplicar

    Returns
    -------
        Devuelve el numero de decimales del filtro
        
    """  
    val = 0
    if filt == 'LOT_SIZE':
        for i in info:
            if i["filterType"] == 'LOT_SIZE':
                #print(i["stepSize"])
                if i["stepSize"] == '0.10000000':
                    val = 1
                elif i["stepSize"] == '0.01000000':
                    val = 2
                elif i["stepSize"] == '0.00100000':
                    val = 3
                elif i["stepSize"] == '0.00010000':
                    val = 4
                elif i["stepSize"] == '0.00001000':
                    val = 5
                elif i["stepSize"] == '0.00000100':
                    val = 6
                elif i["stepSize"] == '0.00000010':
                    val = 7
                elif i["stepSize"] == '0.00000001':
                    val = 8
    
    elif filt == 'PRICE_FILTER':
        for i in info:
            if i["filterType"] == 'PRICE_FILTER':
                #print(i["stepSize"])
                if i["tickSize"] == '0.10000000':
                    val = 1
                elif i["tickSize"] == '0.01000000':
                    val = 2
                elif i["tickSize"] == '0.00100000':
                    val = 3
                elif i["tickSize"] == '0.00010000':
                    val = 4
                elif i["tickSize"] == '0.00001000':
                    val = 5
                elif i["tickSize"] == '0.00000100':
                    val = 6
                elif i["tickSize"] == '0.00000010':
                    val = 7
                elif i["tickSize"] == '0.00000001':
                    val = 8
    return val

def truncate(f, n):
    """
    Función para truncar decimales de una variable tipo float
    
    Parameters
    ----------
    f : float numero a truncar        
    n : int numero de decimales a los que se quiere truncar

    Returns
    -------
        Devuelve un string con el valor truncado
        
    """
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])
