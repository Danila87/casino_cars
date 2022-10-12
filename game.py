import time
from random import randrange
from operator import attrgetter
# ~*~^~*~^~*~^~*~^~*~^~*~^~*~^~*~ #
# leaders выводит только 1 из самых быстрых, даже если максимальуню из скоростей имеют несколько # fixme


class Vehicle(object):
    from_race: bool
    boost: int
    id_: int
    name: str
    speed: int
    distance: int

    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name
        self.speed = 0
        self.distance = 0
        cars_list.append(self)

    def add_speed(self, boost):
        self.speed += boost

    def start(self, duration: int = 10, from_race=False):
        print(f'{self.name} стартует!')
        if not from_race:
            for second in range(1, duration+1):
                self.add_speed(boost=randrange(5, 15))
                self.distance = second * self.speed
                print(f'{self.name} движется со скоростью {self.speed}, пройденное расстояние - {self.distance} метров')
                time.sleep(3)
            self.finish()

    def finish(self, from_race=False):
        if not from_race:
            print(f'{self.name} остановился, проехав {self.distance}')
        self.speed = 0
        self.distance = 0


class Race:
    duration: int
    orig_duration: int
    cars: list
    bank: int
    selected_car: int
    bet: int

    def __init__(self, cars, bank, duration):
        self.duration = duration
        self.orig_duration = duration
        self.cars = cars
        self.bank = bank
        self.selected_car = self.get_car_choice()
        self.bet = self.get_bet()
        self.start_race()

    def get_car_choice(self) -> int:
        """
        :return: номер выбранной машины
        """
        selected_car = 0

        while selected_car not in range(1, len(self.cars) + 1):
            print('Выберите машину:')
            for number, car in enumerate(cars_list):
                print(f"{number + 1}) {car.name}")
            selected_car = int(input('>> '))
        else:
            return selected_car

    def get_bet(self) -> int:
        """
        :return: размер ставки
        """
        bet = 0
        while bet not in range(1, self.bank+1):
            print(f'Ваш банк: {self.bank}\nВведите вашу ставку:')
            bet = int(input('>> '))
            print()
        else:
            return bet

    # Рекурсивная функция run_second вызывает сама себя, с изменённым аргументом (second) пока все секунды не пройдут
    def run_second(self, second=1):
        time.sleep(0.5)
        print("-" * 75, f'\n{second} секунда из {self.duration}')
        for car in self.cars:
            boost = randrange(5, 15)
            car.speed += boost
            car.distance = second * car.speed
            print(f'Скорость {car.name} - {car.speed} км/ч, пройденное расстояние - {car.distance}')
        leaders = [car.name for car in sorted(self.cars, key=attrgetter('distance'), reverse=True)][0]
        if len(set([car.distance for car in self.cars])) == 1:
            print('Удивительно, но все автомобили идут ноздря в ноздрю')
        else:
            print(f'{leaders} лидирует со скоростью '
                  f'{[car.__dict__["speed"] for car in self.cars if car.__dict__["name"] == leaders][0]} км/ч')
        # print(f'Second = {second}, duration = {self.duration}') #

        if second == self.duration:
            # print(f'********{second, self.duration}********') #
            # Если >1 участника имеют одинаковую скорость, равную максимальной из всех в текущую секунду:
            if len(set([car.__dict__['name'] for car in self.cars
                        if car.__dict__['speed'] == max([car.__dict__['speed'] for car in self.cars])])) > 1:
                self.duration += 1
                print('Добавочная секунда..')
                self.run_second(second=self.duration)
            else:
                self.finish_race(leaders)
        else:
            self.run_second(second+1)

    def start_race(self):
        for car in self.cars:
            car.start(from_race=True)
        print('■□' * 10)
        self.run_second()

    def finish_race(self, winner: str):
        print('■□'*10)
        print(f'{winner} финиширует первым!')
        winner_id = int([car.__dict__["id_"] for car in self.cars if car.__dict__["name"] == winner][0])
        for car in self.cars:
            # сбрасываем все изменяемые показатели автомобиля
            car.finish(from_race=True)
        if winner_id == self.selected_car:
            cost = self.bet * 2
            self.bank += cost
            print(f'Ваша машина выиграла! Ваш выигрыш составил {cost}$'
                  f'\nВаш банк в данный момент составляет {self.bank}$')
        else:
            self.bank -= self.bet
            print(f'Вы проиграли(\nВаш банк в данный момент составляет {self.bank}$')
        retry = input('Ещё? (Д/Н)\n>> ').lower()
        match retry:
            case 'д':
                Race(duration=self.orig_duration, cars=self.cars, bank=self.bank)
            case 'н':
                print('Скрипнув дверью, вы ненадолго покидаете казино..')


cars_list = []  # Каждый создавшийся машин заносит себя в этот список

car_one = Vehicle(1, 'УАЗ')
car_two = Vehicle(2, 'Camry')
car_three = Vehicle(3, 'Мэтр')
car_four = Vehicle(4, 'Каптюр')
"""
# Сразу несколько машин для теста:

for i in range(len(cars_list)+1, len(cars_list)+10):
    Vehicle(id_=i, name=f'Car{i}')
"""

# Создаём гонку:
race = Race(duration=15, cars=cars_list, bank=1000)
