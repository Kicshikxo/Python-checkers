>Дальнейшая информация предназначена для разработки или для лучшего понимания кода

## Описание констант в файле constants.py
- PLAYER_SIDE - Определяет сторону, за которую играет игрок
- X_SIZE и Y_SIZE - Определяют ширину и высоту поля в ячейках
- CELL_SIZE - Определяет размер одной ячейки поля (в пикселях)
- ANIMATION_SPEED - Определяет скорость анимации перемещения шашек (больше = быстрее)
- MAX_PREDICTION_DEPTH - Определяет то, сколько следующих ходов экспретная система будет обрабатывать
- BORDER_WIDTH - Определяет ширину рамки обвода ячейки при наведении или выделении (должно быть чётным числом)
- <details><summary>Цвета</summary>

  - FIELD_COLORS - Определяет два цвета для ячеек сетки игрового поля
  - HOVER_BORDER_COLOR - Определяет цвет обводки ячейки при наведении на неё
  - SELECT_BORDER_COLOR - Определяет цвет обводки ячейки при выделении стоящей на ней шашки
  - POSIBLE_MOVE_CIRCLE_COLOR - Определяет цвет кружков, которые появляются на месте возможных ходов выбранной шашки

</details>

## Описание перечислений (enums) в файле enums.py
- <details><summary>SideType - Тип стороны игры</summary>

  - WHITE - Сторона белых
  - BLACK - Сторона чёрных

</details>

- <details><summary>CheckerType - Тип шашки</summary>

  - NONE - Отсутствие типа (ячейка без шашки)
  - WHITE_REGULAR - Белая шашка
  - WHITE_QUEEN - Белая дамка
  - BLACK_REGULAR - Чёрная шашка
  - BLACK_QUEEN - Чёрная дамка 

</details>

## Описание полей и методов классов

- <details><summary>Field (field.py) - Класс поля</summary>

  - Поля
    - x_size - Ширина поля
    - y_size - Высота поля
    - size - Наибольшая из сторон поля
    - white_checkers_count и black_checkers_count - Количество белых и чёрных шашек на поле соответственно
    - white_score и black_score - Набранный счёт белых и чёрных соответственно (счёт = количество обычных шашек + количество дамок × 3)
  - Статические методы
    - copy - Создать копию поля из экземпляра
  - Методы
    - at - Получение шашки, стоящей по переданным координатам
    - type_at - Получение типа шашки, стоящей по переданным координатам
    - is_within - Определяет, находятся ли переданные координаты в пределах поля

</details>

- <details><summary>Checker (ckecker.py) - Класс шашки</summary>

  - Поля
    - type - Тип шашки
  - Методы
    - change_type - Изменить тип шашки

</details>

- <details><summary>Move (move.py) - Класс перемещения</summary>

  - Поля
    - from_x - Координата начальной точки перемещения по оси X
    - from_y - Координата начальной точки перемещения по оси Y
    - to_x - Координата конечной точки перемещения по оси X
    - to_y - Координата конечной перемещения по оси Y

</details>

- <details><summary>Point (point.py) - Класс точки на поле</summary>

  - Поля
    - x - Положение на поле по оси X
    - y - Положение на поле по оси Y

</details>
