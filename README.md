# wspy
El propósito de este módulo es lograr transferencia de datos en formato 'json'
vía websockets de la manera más sencilla posible con python >=3.6,
este módulo usa el paquete [Websocket][websocket_link] en su versión 6.0
pueden ver el [código fuente][websocket_pypi_link] de dicho paquete en 
[pypi.org][pypi_link]


## Uso

```bash
python wspy/__init__.py -h localhost -p 8008
```

Recomiendo usar [supervisord][supervisord_link] para gestionar el proceso.


[supervisord_link]: <http://supervisord.org/>
[websocket_link]: <https://websockets.readthedocs.io/en/stable/>
[websocket_pypi_link]: <https://pypi.org/project/websockets/>
[pypi_link]: <https://pypi.org>