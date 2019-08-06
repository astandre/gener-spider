# OERS Scraping Tools
Aplicacion para recolectar OERS

# Guia de migracion
## Instalar python

Instalar la version de Python 3.5+

## Requerimientos
Instalar todos los requerimientos encontrados en el archivo requirements.txt

```
pip install requirements.txt
```

En caso de existir problemas con el libreria mysqlclient, intentar el comando para instalarla

```
pip install --only-binary :all: mysqlclient 
```

## Ejecucion
En el archivo generic_spider.py, dentro de la linea 26 se establece la key para conectar la spider al proyecto deseado
```
 data = init_spider("12345")
```
 

Dentro de la carpeta scraper ejectuar el siguiente comando para ejecutar

```
scrapy crawl generic
```

Podemos usar la generic_spider para ejecutar y guardar los datos en la bd. O el train_spider para probar los algoritmos.
