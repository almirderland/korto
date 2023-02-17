from abc import abstractmethod, ABC
import random
from typing import Union
import json


def display(json):
    for i, v in json.items():
        for j in v:
            print('{:<20}'.format(j['id']),
                  '{:20}'.format(j['name']),
                  '{:20}'.format(j['driver']),
                  '{:20}'.format(j['state_name']))


def info(json):
    id = int(input())
    for i, v in json.items():
        for j in v:
            if j['id'] == id:
                print(f'{j["id"]:<20}{j["name"]:20}{j["driver"]:20}{j["state_name"]:20}')
                break
        else:
            print("Грузовик не найден")


def close_file(json_object):
    with open("auto.json", "w") as fh:
        json.dump(json_object, fh)


# path = input()
path = "auto.json"
try:
    with open(path, 'r') as openfile:
        json_object = json.load(openfile)
        print("Файл открыт")
except FileNotFoundError:
    print("Файла нет")


class Truck:
    def __init__(self, id: int):
        self.__state: State
        self.change_state(InBaseState)
        self.__id = id

    def change_state(self, state) -> None:
        self.__state = state
        self.__state.set_truck(self=self.__state, truck=self)

    @property
    def id(self) -> int:
        return self.__id

    def start_run(self) -> None:
        self.__state.start_run(self=self.__state)

    def change_driver(self):
        self.__state.change_driver(self)

    def start_repair(self):
        self.__state.start_repair(self)


class State(ABC):
    def __init__(self):
        self._truck: Union[Truck, None]

    def set_truck(self, truck: Truck) -> None:
        self._truck = truck

    @abstractmethod
    def change_driver(self) -> None:
        pass

    @abstractmethod
    def start_run(self) -> None:
        pass

    @abstractmethod
    def start_repair(self) -> None:
        pass


class InBaseState(State):
    def change_driver(self) -> None:
        print("Водитель поменян успешно")

    def start_run(self) -> None:
        if json_object['auto'][self._truck.id()] != None:
            json_object['auto'][self._truck.id()]['state_name'] = 'run'
            print("Состояние изменено")
            close_file(json_object)
            self._truck.change_state(InRunState)
        else:
            print("Грузовик не найден")

    def start_repair(self) -> None:
        if json_object['auto'][self.id()] != None:
            json_object['auto'][self.id()]['state_name'] = 'repair'
            print("Состояние изменено")
            close_file(json_object)
            self.change_state(InRepairState)
        else:
            print("Грузовик не найден")


class InRunState(State):
    def change_driver(self) -> None:
        print("Водитель нельзя менять в пути")

    def start_run(self) -> None:
        print("Грузовик и так в пути")

    def start_repair(self) -> None:
        if json_object['auto'][self.id()] != None:
            json_object['auto'][self.id()]['state_name'] = 'repair'
            print("Состояние изменено")
            close_file(json_object)
            self.change_state(InRepairState)
        else:
            print("Грузовик не найден")


class InRepairState(State):
    def change_driver(self) -> None:
        if json_object['auto'][self.id()] != None:
            json_object['auto'][self.id()]['driver'] = 'John'
            print("Состояние изменено")
            close_file(json_object)
        else:
            print("Грузовик не найден")

    def start_run(self) -> None:
        if json_object['auto'][self._truck.id()] != None:
            json_object['auto'][self._truck.id()]['state_name'] = random.choice(['run', 'base'])
            print("Состояние изменено")
            close_file(json_object)
            self._truck.change_state(states[json_object['auto'][self._truck.id()]['state_name']])
        else:
            print("Грузовик не найден")

    def start_repair(self) -> None:
        print('Грузовик уже в ремонте')


states = {'run': InRunState,
          'base': InBaseState,
          'repair': InRepairState}


def check_state(json_object, id):
    for i in range(len(json_object['auto'])):
        if i == id:
            return json_object['auto'][i]['state_name']


truck = Truck(0)
truck.change_state(states[check_state(json_object, 0)])

print("1.Отобразить текущее состояние грузовиков "
      "\n2.Показать данные грузовика по id "
      "\n3.Обновить состояние грузовика "
      "\n4.Завершить программу и выгрузить все данные")
s = int(input())
if s == 1:
    display(json_object)
elif s == 2:
    info(json_object)
elif s == 3:
    truck.start_repair()
elif s == 4:
    close_file(json_object)
