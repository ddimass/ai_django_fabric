from django.http import HttpResponse, JsonResponse
from django.conf import settings
import numpy as np
from keras.utils import to_categorical
from sklearn import preprocessing
# Create your views here.
from datetime import datetime
from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from django.core.cache import cache
import json
from keras_ai import keras_model

def index():
    print('started')
    model = settings.MOD
    #Translate date to day of week
    data = getBars('EURUSD', 50, 60)
    data = data[-7:,]
    # Add categorical day of week
    bin_days = to_categorical(data[:,0], num_classes=8)
    data = np.delete(data, 0, 1)
    data = np.concatenate((bin_days, data), axis=1)
    data = data.reshape(1,7,13)
    y = model.predict(data)
    pred_data = json.dumps({'time': (datetime.now()).strftime('%Y-%m-%dT%H'), 'predicted': str(y[0][0])})
    ret = cache.set('EURUSD_'+(datetime.now()).strftime('%Y-%m-%dT%H'), pred_data, nx=False)
    return 'ok'


def use_fabric(request, symbol):
    if 'EURUSD_'+(datetime.now()).strftime('%Y-%m-%dT%H') in cache:
        pred_data = json.loads(cache.get('EURUSD_'+(datetime.now()).strftime('%Y-%m-%dT%H')))
        pred_data['cache'] = True
        return JsonResponse(pred_data, safe=True)
    else:
        mod1 = keras_model.create_model(keras_model.KerasFactory(), 'keras_ai/lstm_model.h5')
        data, succ = getBars(symbol, 50, 60)
        if succ:
            data1 = keras_model.KerasFactory().load_data(data, 7)
            mod1.add_data(data1)
            y = mod1.predict()
            pred_data = {}
            pred_data['time'] = (datetime.now()).strftime('%Y-%m-%dT%H')
            pred_data['symbol'] = symbol
            pred_data['predicted'] = str(y[0][0])
            pred_data['cache'] = False
            json_data = json.dumps(pred_data)
            cache.set(symbol+'_'+(datetime.now()).strftime('%Y-%m-%dT%H'), json_data, nx=False)
    return JsonResponse(pred_data, safe=True)


def create_model(factory, model_file_path, weights_file_path=''):
    """Для использования новой фабрики передайте имя новой фабрики"""
    model = factory.create_model()
    model.load(model_file_path, weights_file_path)
    return model

def getPredP():
    pairs = settings.PAIRS
    for pair in pairs:
        print(pair)

def getPrediction(request):
    if 'EURUSD_'+(datetime.now()).strftime('%Y-%m-%dT%H') in cache:
        pred_data = json.loads(cache.get('EURUSD_'+(datetime.now()).strftime('%Y-%m-%dT%H')))
        pred_data['cache'] = True
        return JsonResponse(pred_data, safe=True)
    else:
        if index():
            pred_data = json.loads(cache.get('EURUSD_'+(datetime.now()).strftime('%Y-%m-%dT%H')))
            pred_data['cache'] = False
            return JsonResponse(pred_data, safe=True)
        else:
            return JsonResponse({'Error': 'There is no predictions'}, safe=True)


def getBars(symbol, back_hours, timeframe):
    print(symbol)
    date = int((datetime.now()).timestamp())
    date_back = date - (60*60*back_hours)
    client = getSoapClient()
    items = {
        'Items': [
            {'ChartNeeded': {'symbol': symbol, 'period': timeframe, 'start': date_back, 'end': date, 'timesign': 0, 'mode': 0}},
        ]
    }
    manager = getSoapManager()
    resp = client.service.GetCharts(charts = items, manager = manager)
    try:
        charts = resp['GetChartsResult']['Items']['SymbolBarsInfo'][0]['charts']['Items']['BarInfo']
    except TypeError:
        return [], False
    data = soaptonumpy(charts, symbol)
    return data, True

def soaptonumpy(charts, symbol):
    data = np.zeros((len(charts),6), dtype=float)
    point = getSymbolPoint(symbol)
    for i, bar in enumerate(charts):
        data[i,0] = (datetime.fromtimestamp(bar['ctm'])).isoweekday()
        data[i,1] = bar['open'] * point
        data[i,2] = (bar['open'] + bar['high']) * point
        data[i,3] = (bar['open'] + bar['low']) * point
        data[i,4] = (bar['open'] + bar['close']) * point
        data[i,5] = bar['vol']
    return data


def getSymbolPoint(symbol):
    client = getSoapClient()
    manager = getSoapManager()
    return (client.service.GetSymbolInfo(symbol = symbol, manager = manager))['GetSymbolInfoResult']['point']


def getSoapClient():
    session = Session()
    session.auth = HTTPBasicAuth('959', 'N_:YFJagPuI%v')
    return Client('https://mtsoap1.ittrendex.com:9032/mtservice/mtservice.wsdl?wsdl', transport=Transport(session=session))


def getSoapManager():
    return {'Server': '78.140.179.183', 'Login': 959, 'Password': 'N_:YFJagPuI%v'}
