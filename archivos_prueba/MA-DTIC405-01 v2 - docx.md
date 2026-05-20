**GUÍA DE ACTUALIZACIÓN DE VERSIÓN**

|  |  |
| --- | --- |
| **DATOS DE LA VERSIÓN** | |
| **Producto:** | Integración de los datos de Actio |
| **Versión:** | 1.0.0 |
| **Ruta de la solución:** | \\172.30.19.67\fcv oficina de medicina basada en valor - gestion datos\Documentación soluciones OGD\Python\IntegracionDatosActio\V.1.0.0 |
| **Ruta Git** | https://172.16.19.36/gestiondedatos/Python/IntegracionDatosActio/tree/V.1.0.0 |

# **VERSIONES RELACIONADAS**

![](data:image/png;base64...)No aplica

# **EJECUCIÓN DE SCRIPTS**

![](data:image/png;base64...)En la carpeta de Scripts, ejecutar los archivos:

* “Creacion CodigoActio.sql” en BDFCV.
* “Llenado CodigoActio.sql” en BDFCV.

# **CONFIGURACIÓN TABLAS BASICAS**

No aplica

# **CONFIGURACIÓN DE CONSTANTES**

No aplica

# **CONFIGURACIÓN DE MENÚ**

No aplica

# **CONFIGURACIÓN DE REPORTES**

No aplica

# **CONFIGURACIONES ADICIONALES**

**RUTINA PYTHON:**

Para este montaje se requiere que el implementador realice los siguientes pasos:

* Acepte el “merge request”
* Una vez ubicado en la ruta del proyecto, ejecutar el comando ./setup\_env.sh. Una vez finalizada la ejecución, se habrá creado exitosamente el ambiente virtual
* Cree y configure el archivo .env con las variables de base de datos y de conexión a telegram de producción.

|  |
| --- |
| **.env** |
| # ---------  # BASE DE DATOS  UID\_SQL = “A CONOCIMIENTO DEL IMPLEMENTADOR”  PASS\_SQL = “A CONOCIMIENTO DEL IMPLEMENTADOR”  # ---------  # ACTIO  UID\_ACTIO = “A CONOCIMIENTO DEL IMPLEMENTADOR” PASS\_ACTIO = “A CONOCIMIENTO DEL IMPLEMENTADOR”  # ---------  # URL BASE PARA API ACTIO  BASE\_URL = "https://fundacioncardiovascular-webapi.actiosoftware.com"  # ---------  # TELEGRAM  ID\_TELEGRAM = “A CONOCIMIENTO DEL IMPLEMENTADOR”  TOKEN\_TELEGRAM = “A CONOCIMIENTO DEL IMPLEMENTADOR” |

* *ORIGEN DE DATOS*
* **Servidor**: Edmond\datos
* **Base** **de datos**: BDFCV
* Finalmente, el CRON DEBE en el siguiente horario:
  + main.sh: Todos los días a las 9:00AM
* Una vez hechos los cambios, el implementador podrá validar la correcta configuración del proyecto mediante la ejecución del script, revisando los logs o los mensajes del proceso por Telegram.

# **CAMBIOS TÉCNICOS EN EL PROCESO**

No aplica

# **REQUERIMIENTOS TÉCNICOS PARA INSTALACIÓN**

No aplica