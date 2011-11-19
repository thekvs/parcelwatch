## Общее описание.

Данная программа предназначена для отслеживания статусов почтовых отправлений на [сайте](http://russianpost.ru/)Почты России. При изменении статуса отправления программа выполняет посылку уведомлений о данном событии. Поддерживаются СМС-уведомления и email-уведомления. Для СМС уведомлений используется сервис [Comtube](http://www.comtube.ru/), поэтому вам нужно иметь там аккаунт и некоторое количество денег на нем (для оплаты СМС). На момент написания этого документа стоимость отправки 1-ой СМС на московский номер МТС составляла 40 копеек. При этом надо понимать, что длинное СМС-сообщение может быть отправлено по частям. Для email-уведомлений используется SMTP сервер с авторизацией, на данный момент протестирована работа только с почтовым сервисом компании Mail.Ru.

## Используемое программное обеспечение.

Программа написана на языке Python с использованием стандартных модулей. Работа программы тестировалась только в версии 2.7.

## Конфигурационный файл.

Конфигурационный файл состоит из нескольких секций, в каждой из которых содержится один или более параметров.
    
    [notifications]
    # email куда посылать уведомления
    email = ...
    # Мобильный в международном формате, т.е. например 79101234567
    mobile = ...
    
    [sms]
    # login на сервисе Comtube
    comtube_user = ...
    # пароль на сервисе Comtube
    comtube_password = ...
    
    [email]
    # сервер, через который отсылать email уведомления
    server = smtp.mail.ru
    # пользователь для авторизации на данном сервисе
    user = ...@mail.ru
    # пароль пользователя
    password = ...
    # email куда отсылать уведомления
    to = ...
    
    [status]
    # файл для сохранения результатов предыдущих проверок
    file = /home/kvs/work/devel/parcelwatch/parcelwatch.data
    
    [logging]
    # лог файл
    file = /tmp/parcelwatch.log
    

## Шелл.

Для управления номерами (т.н. tracking numbers) отслеживания используется shell-оподобный интерфейс, который запускается при использовании опции `--shell`:
    
    $ ./parcelwatch --config=/path/to/config/parcelwatch.cfg --shell
    

Пример сессии:
    
    parcelwatch> show 
      #0:    RJXXXXXXXXXGB
      #1:    RAYYYYYYYYYCN
    parcelwatch> tracking 1
      RAYYYYYYYYYCN# show 
        #0: 25.09.2011 20:23: Импорт (104001, МОСКВА PCI-1)
        #1: 26.09.2011 09:05: Передано таможне (104001, МОСКВА PCI-1)
        #2: 26.09.2011 09:12: Таможенное оформление завершено  (104001, МОСКВА PCI-1), Выпущено таможней
        #3: 26.09.2011 12:59: Обработка (104001, МОСКВА PCI-1), Покинуло место международного обмена
        #4: 25.10.2011 14:37: Обработка (185982, ПЕТРОЗАВОДСК PI-2), Сортировка
        #5: 01.11.2011 09:30: Обработка (190967, САНКТ-ПЕТЕРБУРГ МСЦ ЦСПО), Прибыло в сортировочный центр
        #6: 02.11.2011 05:53: Обработка (190966, САНКТ-ПЕТЕРБУРГ МСЦ ЦОПО), Покинуло сортировочный центр
        #7: 07.11.2011 20:50: Обработка (200983, САНКТ-ПЕТЕРБУРГ АСЦ ЦЕХ ПОСЫЛОК), Сортировка
        #8: 09.11.2011 00:00: Обработка (190916, САНКТ-ПЕТЕРБУРГ-ФРУНЗЕНСКИЙ УООП), Покинуло сортировочный центр
        #9: 10.11.2011 11:10: Обработка (193230, САНКТ-ПЕТЕРБУРГ 230), Прибыло в место вручения
        #10: 14.11.2011 00:00: Вручение , Вручение адресату
      RAYYYYYYYYYCN# delete 10
      RAYYYYYYYYYCN# show 
        #0: 25.09.2011 20:23: Импорт (104001, МОСКВА PCI-1)
        #1: 26.09.2011 09:05: Передано таможне (104001, МОСКВА PCI-1)
        #2: 26.09.2011 09:12: Таможенное оформление завершено  (104001, МОСКВА PCI-1), Выпущено таможней
        #3: 26.09.2011 12:59: Обработка (104001, МОСКВА PCI-1), Покинуло место международного обмена
        #4: 25.10.2011 14:37: Обработка (185982, ПЕТРОЗАВОДСК PI-2), Сортировка
        #5: 01.11.2011 09:30: Обработка (190967, САНКТ-ПЕТЕРБУРГ МСЦ ЦСПО), Прибыло в сортировочный центр
        #6: 02.11.2011 05:53: Обработка (190966, САНКТ-ПЕТЕРБУРГ МСЦ ЦОПО), Покинуло сортировочный центр
        #7: 07.11.2011 20:50: Обработка (200983, САНКТ-ПЕТЕРБУРГ АСЦ ЦЕХ ПОСЫЛОК), Сортировка
        #8: 09.11.2011 00:00: Обработка (190916, САНКТ-ПЕТЕРБУРГ-ФРУНЗЕНСКИЙ УООП), Покинуло сортировочный центр
        #9: 10.11.2011 11:10: Обработка (193230, САНКТ-ПЕТЕРБУРГ 230), Прибыло в место вручения
      RAYYYYYYYYYCN# 
    parcelwatch> show 
      #0:    RJXXXXXXXXXGB
      #1:    RAYYYYYYYYYCN
    parcelwatch> delete 0
    Ok
    parcelwatch> show 
      #0:    RAYYYYYYYYYCN
    parcelwatch> add RJXXXXXXXXXGB
    Ok
    parcelwatch> show 
      #0:    RJXXXXXXXXXGB
      #1:    RAYYYYYYYYYCN
    parcelwatch>
    

## Пример использования.

Я использую через cron, мой crontab выглядит следующим образом:
    
    11 10,12,14,16,18,20,22 * * *   /home/kvs/local/parcelwatch/parcelwatch.py --config=/home/kvs/local/parcelwatch/parcelwatch.cfg
    
