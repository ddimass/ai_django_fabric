import numpy as np
from keras.utils import to_categorical
from datetime import datetime
from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from django.core.cache import cache
import json
from keras.models import load_model
from abc import ABC, abstractmethod


class ModelInterface(ABC):
    """

    Интерфейс класса модели предсказания
    - Модель должна содержать обязательный методы load и predict

    """
    @abstractmethod
    def load(self, model_file_path, weights_file_path=''):
        pass

    @abstractmethod
    def predict(self):
        pass


class DataInterface(ABC):
    """

    Интерфейс класса модели предсказания
    - Модель должна содержать обязательный метод predict

    """
    @abstractmethod
    def prepare_data(self, last_hours_count):
        pass


class PredictFactory:
    """

    Базовый класс для абстрактной фабрики модели предсказания
    """
    @classmethod
    def create_model(Class):
        return Class.Model()

    @classmethod
    def load_data(Class, data, last_hours_count):
        return Class.Data(data, last_hours_count)


class KerasFactory(PredictFactory):
    """

    Фабрика предсказания через Keras.
    - Использует рекурентные ноды LSTM.
    - Предсказывает по последним 50 минутам на час вперёд.
    - Вовращает число - вероятность того что цена вырастит.
    - Больше 0.5 - вырастит, меньше 0.5 - упадёт.
    Для создание новой фабрики, необходимо создать класс по аналогии с KerasFactory,
    родителем данного класс должен быть PredictFactory.
    Для использования новой фабрики необходимо вызывать функцию create_model с новым названием фабрики.
    """
    class Model(ModelInterface):
        def __init__(self):
            self.model = None
            self.data = None

        def load(self, model_file_path, weights_file_path=''):
            self.model = load_model(model_file_path)
            if weights_file_path != '':
                self.model.load_weights(weights_file_path)

        def add_data(self, data: DataInterface):
            self.data = data.prepare_data()

        def predict(self) -> float:
            return self.model.predict(self.data)

    class Data(DataInterface):
        """
        Класс данных занимется подготовкой данных
        - Инициализируется двумерным массивом данных [0-49,0-12]
        """
        def __init__(self, data, last_hours_count):
            self.data = data
            self.last_hours_count = last_hours_count

        def prepare_data(self):
            """
            Метод возвращает данные подготовленные
            для выпольнения метода 'predict' класса 'Model' фабрики
            """
            data = self.data[-self.last_hours_count:, ]
            bin_days = to_categorical(data[:,0], num_classes=8)
            data = np.delete(data, 0, 1)
            data = np.concatenate((bin_days, data), axis=1)
            data = data.reshape(1, self.last_hours_count,13)
            return data


def create_model(factory, model_file_path, weights_file_path=''):
    """Для использования новой фабрики передайте имя новой фабрики"""
    model = factory.create_model()
    model.load(model_file_path, weights_file_path)
    return model

def create_AI():
    model = load_model('keras_ai/lstm_model.h5')
    model.load_weights('keras_ai/best-weights.hdf5')

    return model


def index():
    print('started')
    model = create_AI()
    #Translate date to day of week
    data = getBars('EURUSD', 50, 60)
    data = data[-50:,]
    # Add categorical day of week
    bin_days = to_categorical(data[:,0], num_classes=8)
    data = np.delete(data, 0, 1)
    data = np.concatenate((bin_days, data), axis=1)
    data = data[:50,].reshape(1,50,13)
    y = model.predict(data)
    pred_data = json.dumps({'time': (datetime.now()).strftime('%Y-%m-%dT%H'), 'predicted': str(y[0][0])})
    ret = cache.set('EURUSD_'+(datetime.now()).strftime('%Y-%m-%dT%H'), pred_data, nx=False)
    return 'ok'

def getBars(symbol, back_hours, timeframe):
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
    charts = resp['GetChartsResult']['Items']['SymbolBarsInfo'][0]['charts']['Items']['BarInfo']

    data = soaptonumpy(charts)

    return data

def soaptonumpy(charts):
    data = np.zeros((len(charts),6), dtype=float)
    point = getSymbolPoint('EURUSD')
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
