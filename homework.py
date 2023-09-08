from dataclasses import dataclass
import typing


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: object
    duration: float
    distance: float
    speed: float
    calories: float
    msg = ('Тип тренировки: {}; '
           'Длительность: {} ч.; '
           'Дистанция: {} км; '
           'Ср. скорость: {} км/ч; '
           'Потрачено ккал: {}.')

    def get_message(self) -> str:
        return InfoMessage.msg.format(
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories)


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    M_IN_H: int = 60
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist = self.action * self.LEN_STEP / self.M_IN_KM
        return dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration

        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        def run(self):
            raise NotImplementedError(
                'Определите количество полтраченных калорий'
                f' в {self.__class__.__name__}.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        cals = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.M_IN_H)

        return cals


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.029
    KMH_MS: float = 0.278
    SM_MET: float = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        cals = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + (self.get_mean_speed() * self.KMH_MS) ** 2
                 / (self.height / self.SM_MET)
                 * self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.weight) * (self.duration * self.M_IN_H))

        return round(cals, 3)


class Swimming(Training):
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 2

    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = (self.length_pool * self.count_pool / self.M_IN_KM
                 / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        cals = ((self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
                * self.duration)

        return round(cals, 3)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings: dict[str, typing.Type()] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        tr = trainings[workout_type](*data)
    except KeyError:
        print('"{workout_type}" not found in dictionary, using default')

    return tr


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
