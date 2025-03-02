# xmla v0.4.1
  
Магазин на xml, минимальный прототип проекта  
Python 3 и Bottle.py, чистый джаваскрипт  
  
* /catalog/ - страница каталога  
* /catalog/in/ - страница импорта с мэппингом полей  
  
структура проекта:  
+-xmla  
---codes/xmla - модули python  
---views - шаблоны bottle.py  
---static - статика bottle.py  
---js-src - исходники фронтенда  
+-extra  
---xml - файлы xml  
---imports - каталог для импорта  
---tests - тесты на selenium и pytest  
---scripts - скрипты  
---for tests - файлы импорта товаров с картинками (тестовые)  
  
Проект может работать с докер:  
--исправить index.py (порты)  
--sudo docker build -t xmla .    
--sudo docker run -p 8000:8000 -d xmla  
или  
docker compose up  
    