GUÍA DE ACTUALIZACIÓN DE VERSIÓN

DATOS DE LA VERSIÓN

Integración de los datos de Actio

1.0.0

Producto:

Versión:

Ruta de la solución:

\\172.30.19.67\fcv oficina de medicina basada en valor - gestion
datos\Documentación soluciones
OGD\Python\IntegracionDatosActio\V.1.0.0

Ruta Git

https://172.16.19.36/gestiondedatos/Python/IntegracionDatosActio/tree/V.1
.0.0

No aplica

1.  VERSIONES RELACIONADAS

2.  EJECUCIÓN DE SCRIPTS

En la carpeta de Scripts, ejecutar los archivos:




“Creacion CodigoActio.sql” en BDFCV.
“Llenado CodigoActio.sql” en BDFCV.

3.  CONFIGURACIÓN TABLAS BASICAS

No aplica

No aplica

No aplica

No aplica

4.  CONFIGURACIÓN DE CONSTANTES

5.  CONFIGURACIÓN DE MENÚ

6.  CONFIGURACIÓN DE REPORTES

7.  CONFIGURACIONES ADICIONALES

RUTINA PYTHON:

Para este montaje se requiere que el implementador realice los siguientes pasos:

  Acepte el “merge request”
  Una vez ubicado en la ruta del proyecto, ejecutar el comando ./setup_env.sh. Una vez

finalizada la ejecución, se habrá creado exitosamente el ambiente virtual

  Cree y configure el archivo .env con las variables de base de datos y de conexión a

telegram de producción.

# ---------
# BASE DE DATOS
UID_SQL = “A CONOCIMIENTO DEL IMPLEMENTADOR”

PASS_SQL = “A CONOCIMIENTO DEL IMPLEMENTADOR”

.env

# ---------
# ACTIO
UID_ACTIO = “A CONOCIMIENTO DEL IMPLEMENTADOR”

PASS_ACTIO = “A CONOCIMIENTO DEL IMPLEMENTADOR”

# ---------
# URL BASE PARA API ACTIO
BASE_URL = "https://fundacioncardiovascular-webapi.actiosoftware.com"

# ---------
# TELEGRAM
ID_TELEGRAM = “A CONOCIMIENTO DEL IMPLEMENTADOR”

TOKEN_TELEGRAM = “A CONOCIMIENTO DEL IMPLEMENTADOR”

-  ORIGEN DE DATOS
o  Servidor: Edmond\datos
o  Base de datos: BDFCV

  Finalmente, el CRON DEBE en el siguiente horario:
o  main.sh: Todos los días a las 9:00AM

  Una vez hechos los cambios, el implementador podrá validar la correcta configuración del
proyecto mediante la ejecución del script, revisando los logs o los mensajes del proceso
por Telegram.

8.  CAMBIOS TÉCNICOS EN EL PROCESO

9.  REQUERIMIENTOS TÉCNICOS PARA INSTALACIÓN

No aplica

No aplica

