# Costos de Transporte, Precios Mayoristas y Brecha Inflacionaria Pasto–Colombia

Este repositorio contiene el código fuente, la metodología de procesamiento, los datos procesados y las evidencias de auditoría de la investigación sobre los costos de transporte de carga, los precios mayoristas de alimentos y la brecha inflacionaria entre Pasto y el agregado nacional de Colombia durante el periodo 2018–2024.

El estudio analiza las asociaciones dinámicas entre las variaciones de los fletes de transporte de carga con destino a Pasto, obtenidas a partir del Registro Nacional de Despachos de Carga (RNDC), el comportamiento de los precios mayoristas de productos agrícolas del mercado El Potrerillo, registrados por el Sistema de Información de Precios y Abastecimiento del Sector Agropecuario (SIPSA), y la inflación medida mediante el Índice de Precios al Consumidor (IPC) del DANE.

La investigación incorpora procedimientos de reconstrucción de indicadores, verificaciones de integridad mediante SHA-256, pruebas de sensibilidad econométrica y documentación de las limitaciones de las fuentes utilizadas.

## 1. Metodología de procesamiento y pipeline de datos

El procesamiento se organiza en un pipeline reproducible que integra distintas fuentes estadísticas oficiales y construye indicadores mensuales comparables.

### Fase 1. Configuración y normalización de fuentes

**Mercado de estudio:** El Potrerillo, Pasto, Nariño, Colombia.

Los procedimientos de limpieza incluyen:

- Normalización de nombres de variables y textos.
- Eliminación de diferencias de tildes y caracteres especiales cuando corresponde.
- Unificación de convenciones de escritura.
- Homologación semántica de columnas entre distintas versiones de los archivos del DANE.
- Verificación de las unidades de medida utilizadas.

Se incorporaron correcciones de escala para interpretar apropiadamente los puntos utilizados como separadores de miles en las fuentes originales.

Por ejemplo:

- En cantidades SIPSA-A, `1.250` puede representar 1.250 kilogramos.
- En precios SIPSA-P, `2.432` puede representar 2.432 pesos colombianos por kilogramo.

Estas conversiones se realizan de acuerdo con la estructura y la convención numérica identificada en cada fuente, evitando aplicar indiscriminadamente una interpretación única a todos los archivos.

### Fase 2. Descarga y recuperación reproducible de datos

El pipeline contempla mecanismos de adquisición de datos desde fuentes institucionales y respaldos públicos verificables.

Incluye:

- Recuperación de archivos originales disponibles en portales oficiales.
- Descarga alternativa desde respaldos públicos cuando la fuente institucional no está disponible.
- Comprobación de integridad mediante SHA-256.
- Verificación del tamaño de los archivos y de la correspondencia con los manifiestos disponibles.

Para SIPSA se emplean respaldos de archivos históricos y procedimientos de verificación criptográfica.

La disponibilidad de las fuentes originales depende de los servicios externos correspondientes. Los respaldos permiten reducir esa dependencia para los archivos efectivamente publicados.

### Fases 3 y 3B. Procesamiento del abastecimiento SIPSA-A

Se consolidó la información histórica de abastecimiento físico de alimentos para construir una serie mensual correspondiente al periodo enero de 2018 a diciembre de 2024.

El procedimiento comprende:

- Extracción de registros desde archivos históricos.
- Homologación de productos y unidades.
- Selección del mercado de estudio.
- Agregación mensual de cantidades físicas.
- Identificación de observaciones faltantes y restricciones de cobertura.

Se preservan las cantidades físicas observadas sin incorporar imputaciones artificiales.

La serie descriptiva comprende 84 meses.

### Fase 4. Procesamiento de precios mayoristas SIPSA-P

Se construyeron series de precios mayoristas mensuales correspondientes al mercado El Potrerillo.

El procedimiento incluye:

- Extracción de precios promedio.
- Normalización de productos y unidades.
- Homologación de denominaciones.
- Comparación de precios entre periodos consecutivos.
- Comprobaciones de consistencia temporal y de escala.

Se utiliza diciembre de 2017 como referencia para calcular los relativos correspondientes a enero de 2018.

### Fase 5. Homologación de precios y abastecimiento

Se realizó el emparejamiento de las cantidades físicas observadas en SIPSA-A con los precios correspondientes en SIPSA-P.

La homologación incorpora siete reglas conservadoras de equivalencia entre denominaciones de productos.

Estas reglas buscan evitar que diferencias de nomenclatura generen pérdidas innecesarias de información o emparejamientos conceptualmente incorrectos.

La cobertura física promedio anual documentada del emparejamiento fue de aproximadamente **79,64 %** de las toneladas de alimentos ingresadas al mercado de estudio.

### Fase 6. Construcción del indicador de precios mayoristas

Se construyó un indicador de variación mensual de precios mayoristas mediante una media geométrica de relativos de precios ponderados por las cantidades físicas contemporáneas.

La formulación es:

\[
PM_t=100\left[\exp\left(\sum_i w_{i,t}\ln\left(\frac{p_{i,t}}{p_{i,t-1}}\right)\right)-1\right]
\]

donde:

\[
w_{i,t}=\frac{q_{i,t}}{\sum_j q_{j,t}}
\]

Las variables corresponden a:

- \(p_{i,t}\): precio del producto \(i\) en el periodo \(t\).
- \(p_{i,t-1}\): precio del mismo producto en el periodo anterior.
- \(q_{i,t}\): cantidad física del producto \(i\) en el periodo \(t\).
- \(w_{i,t}\): participación física del producto en el conjunto de productos emparejados.

La construcción incluye especificaciones alternativas con ponderadores rezagados y ponderaciones uniformes para evaluar la sensibilidad de los resultados.

### Fase 7. Robustez de canasta y concentración

Se incorporaron procedimientos para examinar la concentración y estabilidad de las ponderaciones físicas.

Las comprobaciones comprenden:

- Índice de Herfindahl-Hirschman (HHI).
- Número efectivo de productos.
- Continuidad temporal de la canasta.
- Análisis *leave-one-out* sobre productos de mayor participación.
- Comparación de especificaciones de ponderación.

El procesamiento identificó 22 productos con continuidad completa en el horizonte de referencia documentado.

### Fase 8. Variable regional de transporte RNDC

La variable regional de fletes se construye mediante un índice encadenado de Törnqvist, utilizando registros de transporte de carga con destino a Pasto.

La serie dispone de:

- 60 niveles mensuales, entre enero de 2020 y diciembre de 2024.
- 59 variaciones porcentuales mensuales, entre febrero de 2020 y diciembre de 2024.

El código verifica la integridad de la serie procesada y permite contrastar su correspondencia con el índice publicado.

La metodología, las fuentes, las comprobaciones de reproducibilidad y el alcance de la conciliación con registros originales se documentan en la sección 3.

### Fase 9. Variable dependiente: brecha inflacionaria

La brecha inflacionaria mensual se define como la diferencia entre la inflación mensual de Pasto y la inflación mensual nacional:

\[
B_t=\pi_{Pasto,t}-\pi_{Colombia,t}
\]

La medida se expresa en puntos porcentuales.

La serie histórica del IPC total comprende 84 observaciones mensuales, correspondientes al periodo enero de 2018 a diciembre de 2024.

Como extensión metodológica, se incorporaron series de inflación de alimentos para distinguir las variaciones del IPC total de las variaciones de precios correspondientes específicamente al grupo de alimentos.

Esta diferenciación resulta importante porque SIPSA mide precios mayoristas de productos agroalimentarios, mientras que el IPC representa precios de consumo final.

### Fase 10. Indicador nacional de costos de transporte ICTC

Se incorporó el Índice de Costos del Transporte de Carga por Carretera (ICTC) del DANE como referencia nacional para análisis comparativos y ejercicios de sensibilidad.

El ICTC y el indicador RNDC regional no son medidas conceptualmente equivalentes.

El primero representa la evolución de costos de operación, mientras el segundo se construye a partir de registros de fletes regionales.

Por esta razón, no se realiza un empalme mecánico entre ambas series.

## 2. Advertencias metodológicas críticas

Los procedimientos empíricos y las conclusiones del estudio deben interpretarse considerando las siguientes restricciones.

### 2.1. Alcance no causal

Los modelos de rezagos distribuidos (DL), autorregresivos de rezagos distribuidos (ARDL) y sus ejercicios de sensibilidad permiten identificar asociaciones dinámicas condicionales.

**Sus resultados no constituyen evidencia causal de que las variaciones de los fletes provoquen cambios en la inflación de Pasto.**

La significancia estadística individual de un coeficiente tampoco garantiza la significancia conjunta de sus rezagos ni la estabilidad del resultado frente a especificaciones alternativas.

### 2.2. Tratamiento de datos faltantes

No se realizan imputaciones ni interpolaciones para completar artificialmente observaciones inexistentes.

Los periodos para los cuales no existe información RNDC compatible con la variable de investigación se excluyen de las estimaciones correspondientes.

### 2.3. Diferencias de cobertura temporal

Se distinguen tres muestras principales:

| Muestra | Cobertura | Uso |
|---|---|---|
| Histórica | 84 meses, 2018-01 a 2024-12 | Descripción general |
| Común | 59 meses, 2020-02 a 2024-12 | Análisis conjunto con RNDC |
| Econométrica comparable | 56 meses, 2020-05 a 2024-12 | Comparación entre especificaciones con hasta tres rezagos |

La utilización de una muestra común permite reducir las diferencias de resultados atribuibles exclusivamente a cambios en el periodo observado.

### 2.4. Diferencias conceptuales entre RNDC e ICTC

El indicador regional RNDC representa variaciones construidas a partir de fletes observados hacia Pasto.

El ICTC corresponde a un indicador nacional de costos del transporte de carga.

No deben interpretarse como medidas idénticas ni reemplazarse entre sí sin considerar sus diferencias de construcción, cobertura y significado económico.

### 2.5. IPC total, inflación de alimentos y precios mayoristas

La brecha calculada con el IPC total comprende diversos grupos de bienes y servicios.

Por su parte, SIPSA representa precios mayoristas de productos agroalimentarios.

En consecuencia, una variación de precios SIPSA no puede interpretarse automáticamente como una variación equivalente del IPC total o del IPC de alimentos.

Las estimaciones que incorporan inflación de alimentos buscan mejorar la correspondencia conceptual entre las variables, sin establecer por ello una relación causal.

### 2.6. Semáforo y alertas exploratorias

El semáforo de presiones de fletes y precios constituye una herramienta descriptiva y retrospectiva de carácter académico.

**No ha sido validado como un sistema predictivo de bloqueos viales, cierres de carreteras o interrupciones logísticas en tiempo real.**

Su interpretación debe limitarse a los indicadores y criterios explícitamente documentados.

### 2.7. Periodicidad de las estadísticas

Los datos quincenales de abastecimiento y las variaciones mensuales del panel econométrico corresponden a unidades temporales diferentes.

No deben mezclarse aritméticamente sin una agregación metodológicamente justificada.

## 3. Reproducibilidad y auditoría de la variable RNDC

### 3.1. Construcción del indicador

La variable regional de fletes hacia Pasto fue construida a partir de información del Registro Nacional de Despachos de Carga (RNDC) del Ministerio de Transporte de Colombia.

El periodo estudiado comprende enero de 2020 a diciembre de 2024, con 60 niveles mensuales del índice encadenado de Törnqvist y 59 variaciones porcentuales mensuales.

La unidad de análisis del panel elemental corresponde a combinaciones de origen, configuración vehicular, mercancía y periodo.

**Repositorio público del proyecto:**

[Costos de transporte, precios mayoristas e inflación en Pasto](https://github.com/JuanDavidgm2026/fletes-precios-inflacion-pasto)

**Notebook de construcción del indicador:**

[Construcción del índice de fletes RNDC Pasto](notebooks/construccion_indice_fletes_RNDC_Pasto.ipynb)

### 3.2. Auditoría independiente de reproducibilidad

Se desarrolló una auditoría técnica independiente para examinar la cadena de procesamiento del indicador.

Las comprobaciones comprenden:

- Integridad de archivos mediante SHA-256.
- Cobertura temporal entre 2020 y 2024.
- Verificación de los registros procesados con destino a Pasto.
- Reconstrucción del panel elemental desde el maestro.
- Comprobación de las reglas de depuración N1/N2.
- Reejecución del bloque estadístico de agregación.
- Reconstrucción matemática del índice Törnqvist.
- Comparación del índice reconstruido con las series utilizadas en las estimaciones econométricas.

**Notebook independiente de auditoría:**

[Auditoría RNDC limpia y reproducible — Google Colab](https://colab.research.google.com/drive/1zDI2n_Fg7ZAQZcsfIWlTUVsdKStBiwbN)

Este cuaderno constituye un anexo técnico y puede utilizarse independientemente del notebook econométrico principal.

### 3.3. Principales resultados de la auditoría

Las comprobaciones realizadas permitieron verificar:

| Componente | Resultado |
|---|---:|
| Registros del maestro procesado | 78.819 |
| Celdas del panel elemental | 76.218 |
| Celdas del panel jerárquico | 76.218 |
| Niveles mensuales del índice Törnqvist | 60 |
| Variaciones mensuales del indicador | 59 |

Se verificaron adicionalmente las reglas de depuración N1/N2, la reconstrucción del índice y la concordancia numérica de las series publicadas con las utilizadas en la investigación.

Estas pruebas acreditan consistencia computacional **desde los archivos procesados disponibles en el repositorio**.

No equivalen, por sí solas, a una reconstrucción de todos los registros originales del Ministerio de Transporte.

### 3.4. Contraste con registros oficiales y reconstrucción de enero de 2020

Se desarrolló una verificación independiente correspondiente a enero de 2020 mediante el archivo mensual `EstadisticasRNDC_202001 (1).xlsx`, descargado desde el sistema de consultas públicas RNDC del Ministerio de Transporte.

**Fuente institucional:** [Registro Nacional de Despachos de Carga — Ministerio de Transporte](https://rndc.mintransporte.gov.co/menuprincipal)

El archivo mensual contiene 134.426 registros nacionales y 23 columnas.

Mediante la selección de registros correspondientes al municipio de Pasto, incluyendo las localidades identificadas como pertenecientes a dicho destino en el archivo de origen, se obtuvieron 1.156 registros.

La auditoría comprendió las siguientes comprobaciones:

**A. Reconstrucción desde el archivo mensual**

Se contrastaron los 1.156 registros del Excel filtrado con el extracto CSV utilizado previamente en la auditoría.

La comparación incluyó las 23 columnas y conservó la multiplicidad de las observaciones repetidas.

**Resultado:** coincidencia completa de los registros contrastados.

**B. Conciliación con el maestro procesado**

Se comparó el extracto de enero de 2020 con los registros correspondientes del maestro RNDC procesado.

Se utilizaron nueve campos comunes:

1. `CODMUNICIPIOORIGEN`
2. `CODMUNICIPIODESTINO`
3. `COD_CONFIG_VEHICULO`
4. `CODMERCANCIA`
5. `VIAJESTOTALES`
6. `VIAJESVALORCERO`
7. `KILOGRAMOS`
8. `VALORESPAGADOS`
9. `KILOMETROS`

La comparación mediante multiconjuntos no identificó discrepancias en los campos contrastados.

**Resultado:** `PASS_9_COLUMNAS_COMUNES`.

**C. Integridad del archivo original**

Se verificó la huella criptográfica SHA-256 del archivo mensual:

`ec1a0ea3c4697a622424472bc681bb3043318961e483170ca16c09ac18b47218`

La integridad del Excel publicado en GitHub fue comprobada mediante una descarga independiente.

**D. Reproducibilidad automática desde GitHub**

Se implementó una prueba que descarga automáticamente el Excel, el manifiesto y el script de verificación desde el repositorio público.

La prueba permite:

- Recuperar los archivos sin carga manual.
- Comprobar la integridad SHA-256.
- Leer el archivo mensual.
- Aplicar el procedimiento de identificación territorial.
- Reconstruir los 1.156 registros de Pasto.
- Generar un dictamen de ejecución.

El resultado obtenido fue:

`PASS_REPRODUCCION_AUTOMATICA_RNDC`

**Archivos de respaldo y código:**

[Auditoría RNDC — enero de 2020](auditoria/rndc_enero_2020/)

Esta carpeta contiene:

- `EstadisticasRNDC_202001 (1).xlsx`
- `verificar_rndc_enero2020.py`
- `manifest.json`
- `README.md`

**Alcance y limitaciones**

La reconstrucción directa desde el archivo mensual original corresponde exclusivamente a enero de 2020.

Los restantes 59 meses no han sido conciliados individualmente desde los archivos mensuales primarios.

La reconstrucción completa del índice Törnqvist para 2020–2024 se verifica desde los archivos procesados publicados.

La identidad computacional entre archivos tampoco implica evidencia causal ni garantiza la estabilidad de los resultados econométricos.

### 3.5. Integración con el notebook principal

La fase 8 del notebook econométrico principal descarga la serie regional de fletes y comprueba su integridad mediante SHA-256.

La fase 8B incorpora verificaciones adicionales del índice Törnqvist publicado y su correspondencia con las variaciones mensuales utilizadas en la investigación.

La auditoría independiente amplía las comprobaciones hacia el panel elemental, la depuración jerárquica y la reconstrucción matemática del indicador.

La validación del archivo original de enero de 2020 complementa estas pruebas, pero no sustituye la reconstrucción desde archivos primarios para los demás meses.

No se realizan imputaciones para completar los datos empleados en las estimaciones.

### 3.6. Instrucciones de reproducibilidad

**Notebook econométrico principal:**

[Notebook principal de investigación — Google Colab](https://colab.research.google.com/drive/1mKtipF99zHAk_ys3SQE7UQrjTuhYTuF_)

**Notebook independiente de auditoría RNDC:**

[Auditoría RNDC — Google Colab](https://colab.research.google.com/drive/1zDI2n_Fg7ZAQZcsfIWlTUVsdKStBiwbN)

**Notebook de prueba automática:**

[Reproducibilidad RNDC desde GitHub — Google Colab](https://colab.research.google.com/drive/1m3msgeROiLGZIZsHsoMNXn69yOKmtCoR?usp=sharing)

**Procedimiento recomendado**

1. Abrir el notebook principal en Google Colab.
2. Seleccionar «Entorno de ejecución» y «Ejecutar todas».
3. Comprobar los resultados de las fases 8 y 8B.
4. Abrir el notebook independiente de auditoría RNDC.
5. Revisar la reconstrucción del indicador y los dictámenes correspondientes.
6. Abrir el notebook de prueba automática RNDC.
7. Ejecutar la fase RNDC 12 para recuperar los insumos directamente desde GitHub.
8. Verificar la reconstrucción de los registros de enero de 2020 y el dictamen final.

La prueba RNDC 12 fue ejecutada satisfactoriamente en un entorno independiente, sin necesidad de cargar archivos manualmente.

**Resultado:** `PASS_REPRODUCCION_AUTOMATICA_RNDC`.

Esta prueba no sustituye las conciliaciones RNDC 06D y RNDC 11, que verifican otras etapas de la cadena de procesamiento.

La reproducción automática depende de la disponibilidad pública del repositorio y de los archivos necesarios.

El archivo Excel fue identificado como una descarga mensual del sistema de consultas públicas RNDC y se conserva con su huella SHA-256. Las condiciones de redistribución del archivo deben verificarse conforme a las disposiciones aplicables de la fuente institucional.

La correcta ejecución del código demuestra consistencia computacional dentro del alcance de las pruebas realizadas. No constituye evidencia causal ni demuestra por sí sola significancia o estabilidad estadística.

## 4. Alcance y limitaciones

La investigación utiliza información de fuentes estadísticas oficiales y archivos procesados documentados para facilitar la reproducción de sus resultados.

La reconstrucción del indicador RNDC desde las bases procesadas fue comprobada mediante auditorías independientes.

La verificación directa desde el archivo mensual original abarcó exclusivamente enero de 2020.

Se comprobó la correspondencia de **1.156 registros en 23 columnas** entre el Excel mensual filtrado y el extracto CSV auditado.

Posteriormente, se verificó la coincidencia de esos registros con el maestro procesado en **nueve campos comunes**.

Los restantes 59 meses no han sido conciliados individualmente contra sus archivos primarios.

En consecuencia, debe distinguirse entre:

- Reproducibilidad del índice desde los archivos procesados.
- Reproducción de la extracción y conciliación oficial correspondiente a enero de 2020.
- Validación completa desde fuentes primarias para todos los meses, que permanece pendiente.

Asimismo, la brecha del IPC total y las variaciones de precios mayoristas SIPSA representan conceptos económicos distintos.

Las especificaciones econométricas y sus pruebas de robustez deben interpretarse en función de esa diferencia conceptual, de la disponibilidad temporal de las variables y de la sensibilidad de los resultados.

**Las asociaciones estimadas no deben interpretarse como relaciones causales.**

El semáforo de presiones de transporte y precios constituye un instrumento exploratorio académico y no una herramienta validada para anticipar bloqueos viales.
