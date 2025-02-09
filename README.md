# SystemMonitor

SystemMonitor - это десктопное приложение для Windows, разработанное на Python с использованием библиотеки Tkinter, которое предоставляет пользователю информацию о текущем состоянии его системы.  Приложение отображает ключевые метрики производительности, такие как загрузка процессора и видеокарты, использование памяти и диска, температуру процессора и видеокарты, а также скорость вращения кулеров.  Метрики отображаются в реальном времени и визуализируются с помощью графиков, предоставляя удобный способ мониторинга производительности системы.

## Возможности

*   **Мониторинг загрузки ЦП:** Отображает текущую загрузку центрального процессора в процентах.
*   **Мониторинг загрузки ГП:** Отображает текущую загрузку графического процессора в процентах.
*   **Мониторинг использования памяти:** Отображает текущее использование оперативной памяти в процентах.
*   **Мониторинг использования диска:** Отображает текущее использование дискового пространства в процентах.
*   **Мониторинг температуры ЦП и ГП:** Отображает текущую температуру центрального и графического процессоров в градусах Цельсия.
*   **Отображение скорости вращения кулеров:** Отображает текущую скорость вращения кулеров в оборотах в минуту (RPM).
*   **Графическое отображение метрик:**  Визуализирует метрики производительности в виде графиков, отображающих изменение значений во времени.
*   **Ведение лога:** Записывает собранные метрики в файл лога для последующего анализа.
*   **Установка пороговых значений:**  Позволяет пользователю устанавливать пороговые значения для каждой метрики, при превышении которых отображается предупреждение.
*   **Темный режим:**  Приложение имеет темную тему оформления для комфортного использования в условиях низкой освещенности.

## Установка

1.  **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/your-username/SystemMonitor.git
    ```

2.  **Перейдите в директорию проекта:**

    ```bash
    cd SystemMonitor
    ```

3.  **Создайте виртуальное окружение (рекомендуется):**

    ```bash
    python3 -m venv venv
    ```

4.  **Активируйте виртуальное окружение:**

    *   **В Linux/macOS:**

        ```bash
        source venv/bin/activate
        ```

    *   **В Windows:**

        ```bash
        venv\Scripts\activate
        ```

5.  **Установите зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

## Использование

1.  **Запустите приложение:**

    ```bash
    python main.py
    ```

2.  **Настройте пороговые значения (опционально):**

    Нажмите кнопку "Set Thresholds" и введите пороговые значения для каждой метрики.

3.  **Просматривайте метрики в реальном времени:**

    Приложение будет отображать метрики производительности и графики в реальном времени.

4.  **Ведение лога (опционально):**

    Нажмите кнопку "Log Metrics" для записи текущих метрик в файл `system_metrics.log`.

## Зависимости

*   Python 3.6+
*   psutil
*   GPUtil
*   matplotlib
*   tkinter
*   wmi (только для Windows)

## Лицензия

Этот проект лицензирован в соответствии с лицензией MIT - см. файл [LICENSE](LICENSE) для получения подробной информации.

## Контакты

Ваши контактные данные (имя, email, GitHub и т.д.).

## Благодарности

Выражаю благодарность следующим библиотекам и ресурсам, которые сделали возможным создание этого проекта:

*   **psutil:**  За предоставление кроссплатформенного доступа к информации о системе и процессах.
*   **GPUtil:**  За возможность получения информации о графических процессорах NVIDIA.
*   **matplotlib:**  За мощные инструменты для визуализации данных и создания графиков.
*   **Tkinter:**  За простой и удобный способ создания графического интерфейса пользователя.
*   **wmi:** За возможность получения информации о системе на Windows.
