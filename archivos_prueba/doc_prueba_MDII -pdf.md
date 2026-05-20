Predicción del Precio de Viviendas Mediante Análisis de
Características Inmobiliarias
Este tema trata sobre cómo estimar el precio de una casa a partir de sus características. La
idea básica es que no se mira el valor de una vivienda como un número aislado, sino como
el resultado de varias variables que influyen en su costo. Entre esas variables están la
ubicación, el área construida, el número de habitaciones, baños, garaje, antigüedad, estrato,
distancia al centro y algunos atributos adicionales como piscina o seguridad privada.
En un caso típico de regresión, lo que se busca es encontrar una relación entre esas
características y el precio final. Por ejemplo, normalmente una casa más grande, mejor
ubicada y con más comodidades tendrá un precio mayor que otra más pequeña, más
antigua o ubicada en una zona menos valorizada. La tabla de datos sirve precisamente para
eso: reunir ejemplos con entradas conocidas para que luego un modelo pueda aprender
patrones y predecir precios de casas nuevas.
La forma de abordar el problema empieza por definir qué variable se quiere predecir, que en
este caso es el precio. Después se identifican las variables explicativas, que son las
características de la casa. Luego se organiza un conjunto de datos con varias viviendas,
procurando que haya diversidad en zonas, tamaños y condiciones. Con eso ya se puede
analizar si existe una tendencia clara, por ejemplo si el precio sube cuando aumenta el área,
o si baja cuando la casa tiene más años de antigüedad.
Después de tener los datos, normalmente se limpia la información y se convierte a un
formato usable. Algunas variables son numéricas, como el área o la cantidad de baños,
mientras que otras son categóricas, como la ciudad o el barrio. Estas últimas deben
transformarse para que puedan ser usadas en un modelo matemático. A partir de ahí se
puede aplicar regresión lineal u otro modelo similar para estimar el precio.
Este tipo de ejercicio es útil porque muestra cómo se puede pasar de datos simples a una
predicción. También sirve para entender que el precio de una casa no depende de una sola
cosa, sino de la combinación de varias características. La ubicación suele tener mucho
peso, pero no es lo único: el tamaño, el estado de conservación y las comodidades también
cambian bastante el valor.
En resumen, el tema se aborda como un problema de predicción supervisada, donde se
usan datos de casas conocidas para aprender una relación entre sus atributos y su precio.
Es un ejemplo clásico porque es fácil de entender, tiene variables claras y permite aplicar
técnicas de análisis de datos y regresión de una manera bastante práctica.

TABLA Precio de Viviendas

| ID               | Ciudad  | Barrio/Zona     | Área (m²)  | Habitaciones  |     |
| ---------------- | ------- | --------------- | ---------- | ------------- | --- |
| 1 Bogotá         |         | Chapinero       | 85         |               | 3   |
| 2 Medellín       |         | El Poblado      | 120        |               | 3   |
| 3 Cali           |         | Ciudad Jardín   | 95         |               | 4   |
| 4 Bucaramanga    |         | Cabecera        | 70         |               | 2   |
| 5 Barranquilla   |         | Riomar          | 140        |               | 4   |
| 6 Bogotá         |         | Suba            | 60         |               | 2   |
| 7 Medellín       |         | Laureles        | 110        |               | 3   |
| 8 Cali           |         | Valle del Lili  | 78         |               | 3   |
| 9 Bucaramanga    |         | Cañaveral       | 130        |               | 4   |
| 10 Cartagena     |         | Bocagrande      | 160        |               | 4   |
| 11 Bogotá        |         | Usaquén         | 90         |               | 3   |
| 12 Medellín      |         | Envigado        | 150        |               | 5   |
| 13 Cali          |         | San Fernando    | 65         |               | 2   |
| 14 Barranquilla  |         | Villa Carolina  | 88         |               | 3   |
| 15 Bucaramanga   |         | Provenza        | 55         |               | 2   |
| 16 Cartagena     |         | Manga           | 125        |               | 3   |
| 17 Bogotá        |         | Kennedy         | 50         |               | 2   |
| 18 Medellín      |         | Sabaneta        | 100        |               | 3   |
| 19 Cali          |         | Normandía       | 180        |               | 5   |
| 20 Bucaramanga   |         | Sotomayor       | 92         |               | 3   |
| 21 Bogotá        |         | Teusaquillo     | 115        |               | 4   |
| 22 Medellín      |         | Belén           | 72         |               | 3   |
Alameda del
| 23 Barranquilla  |     | Río     | 98   |     | 3   |
| ---------------- | --- | ------- | ---- | --- | --- |
| 24 Cartagena     |     | Crespo  | 135  |     | 4   |
Lagos del
| 25 Bucaramanga  |     | Cacique  | 155  |     | 4   |
| --------------- | --- | -------- | ---- | --- | --- |