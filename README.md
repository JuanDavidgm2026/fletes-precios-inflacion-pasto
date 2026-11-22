# Costos de Transporte, Precios Mayoristas y Brecha Inflacionaria Pasto–Colombia

Este repositorio contiene el código fuente, la metodología de procesamiento y la auditoría econométrica de la investigación sobre la brecha inflacionaria mensual entre el municipio de Pasto (Mercado Mayorista El Potrerillo) y el agregado nacional de Colombia para el periodo **2018–2024**.

El estudio analiza la interrelación dinámica entre las variaciones de los fletes de transporte de carga con destino a Pasto (obtenidos de registros oficiales de la base RNDC), el comportamiento de los precios mayoristas de alimentos agrícolas (SIPSA) y la brecha inflacionaria medida a partir del Índice de Precios al Consumidor (IPC).

---

## 1. Metodología de Procesamiento y Pipeline de Datos

El procesamiento de datos se estructura en un pipeline unificado y reproducible que consta de las siguientes fases:

### Fase 1: Configuración y Normalización de Fuentes
* **Mercado de Estudio:** Pasto, El Potrerillo.
* **Limpieza de Datos:** Normalización de texto (eliminación de tildes, caracteres especiales y unificación a minúsculas) y resolución semántica de columnas entre diferentes versiones estructurales del DANE.
* **Correcciones Críticas de Escala:** Corrección sistemática de la notación colombiana de puntos de miles para evitar la subestimación de unidades:
  * En cantidades (SIPSA-A): `1.250` se interpreta correctamente como `1250` kg.
  * En precios (SIPSA-P): `2.432` se interpreta correctamente como `2432` COP/kg.

### Fase 2: Descarga de Datos de Alta Reproducción
* **Descarga Dinámica:** El script realiza scraping directo en los portales oficiales de microdatos del DANE.
* **Mecanismo de Respaldo (Fallback):** En caso de indisponibilidad del servidor institucional, se activa una descarga desde un release clonado en GitHub (`JuanDavidgm2026/SIPSA-PASTO`).
* **Auditoría Criptográfica:** Validación estricta del tamaño en bytes y del hash criptográfico **SHA-256** de los 23 archivos `.zip` descargados contra un manifiesto predefinido.

### Fases 3 y 3B: Procesamiento del Abastecimiento (SIPSA-A)
* Extracción y unificación de 15 semestres/cuatrimestres históricos para consolidar la serie temporal mensual de abastecimiento (84 meses continuos de 2018-01 a 2024-12).
* Exclusión estricta de variables imputadas, conservando exclusivamente la serie física observada.

### Fase 4: Procesamiento de Precios Mayoristas (SIPSA-P)
* Extracción de precios promedios mensuales para el mercado El Potrerillo.
* Inclusión de **diciembre de 2017** como línea base de comparación temporal para el cálculo de los relativos de precio en enero de 2018.
* Auditoría matemática de la consistencia interanual para evitar saltos artificiales por quiebre de escala.

### Fase 5: Homologación y Cruce Físico-Financiero (Precio-Volumen)
* Aplicación manual y conservadora de **7 reglas de equivalencia** de productos para evitar sesgos por denominaciones inconsistentes en el mercado (ej. *cebolla junca* $\leftrightarrow$ *cebolla junca pastusa*).
* Cálculo de la **cobertura física del índice**, logrando emparejar un promedio histórico anual de **79.64%** de las toneladas físicas de alimentos ingresadas a Pasto con un precio de mercado válido.

### Fase 6: Construcción de Indicadores de Variación Mensual
* **Indicador Principal ($PM\_ponderado\_t$):** Cálculo de variaciones mensuales acumuladas mediante una **media geométrica ponderada por volumen físico contemporáneo** ($Q_t$):
  $$PM_t = 100 \times \left( \exp\left[ \sum w_{i,t} \ln\left(\frac{p_{i,t}}{p_{i,t-1}}\right) \right] - 1 \right)$$
  Donde $w_{i,t} = \frac{q_{i,t}}{\sum q_{j,t}}$.
* **Análisis de Sensibilidad:** Construcción de variaciones con ponderadores rezagados ($Q_{t-1}$) y especificaciones no ponderadas (pesos iguales en canasta).

### Fase 7: Análisis de Robustez de Canasta y Concentración
* Medición de la concentración de ponderación en el mercado físico de Pasto mediante el **Índice Herfindahl-Hirschman (HHI)** y el número efectivo de productos.
* Simulaciones de canasta restringida (*Leave-One-Out*) excluyendo secuencialmente los 10 productos más importantes por peso físico.
* Cálculo de la continuidad temporal de la canasta (22 productos 100% continuos durante todo el horizonte temporal).

### Fase 8: Variable de Transporte (RNDC Regional)
* Carga y auditoría de la serie mensual congelada del flete regional hacia Pasto construida con el **Índice encadenado de Törnqvist** (59 variaciones mensuales, febrero 2020 - diciembre 2024).
* Integridad física de la base validada con SHA-256.

### Fase 9: Variable Dependiente (Brecha Inflacionaria)
* Extracción directa de las series mensuales del IPC de Pasto y el IPC nacional del DANE.
* Definición de la brecha mensual: $B_t = \pi_{Pasto, t} - \pi_{Colombia, t}$ (84 meses continuos, 2018-01 a 2024-12).

### Fase 10: Benchmark de Transporte (ICTC Nacional)
* Descarga y estructuración del Índice de Costos del Transporte de Carga (ICTC) nacional para análisis comparativo y de sensibilidad econométrica.

---

## 2. Advertencias Metodológicas Críticas

El equipo investigador y el lector deben considerar de forma explícita las siguientes limitaciones y precisiones estadísticas:

1. **Inexistencia de Relación Causal:** Ningún modelo de rezagos distribuidos (DL) o autorregresivo (ARDL) presentado en esta investigación constituye evidencia causal de efectos de transporte sobre la brecha inflacionaria. Las relaciones encontradas representan únicamente **asociaciones dinámicas condicionales**.
2. **Sin Imputaciones ni Modificaciones:** El estudio prohíbe de manera absoluta la imputación, interpolación o alteración de datos ausentes. Los periodos de fletes no disponibles (2018-01 a 2020-01) se excluyen de la estimación, preservando la muestra originalmente reportada.
3. **Muestras Diferentes según el Análisis:** El repositorio maneja tres muestras diferenciadas:
   * **Muestra Histórica (84 meses):** Para análisis descriptivo general.
   * **Muestra Común Completa (59 meses):** Intersección física de las variables.
   * **Muestra de Estimación ARDL (56 meses):** Rango común ajustado por el consumo de rezagos temporales ($t-3$) para mantener muestras comparables entre especificaciones.
4. **ICTC vs RNDC:** El ICTC es un indicador nacional de costos teóricos de operación. No es conceptualmente equivalente ni debe empalmarse con el indicador regional RNDC, el cual mide variaciones de fletes reales observados en transacciones con destino Pasto.
5. **Semáforo y Alertas Ilustrativas:** El semáforo de presiones de fletes/precios implementado es una **construcción matemática retrospectiva** con fines académicos. No constituye un predictor operativo de bloqueos viales, cierres físicos ni situaciones de fuerza mayor en tiempo real.
6. **Diferencia entre Boletines y Tasas Mensuales:** El colapso del abastecimiento quincenal reportado para mayo de 2021 corresponde a datos de boletines publicados por el DANE para quincenas específicas. Estas cifras no deben interpretarse como si fueran variaciones mensuales promedio ni mezclarse aritméticamente con el panel econométrico.


---

## 3. Reproducibilidad y auditoría de la variable RNDC

### 3.1. Construcción del indicador

La variable regional de fletes hacia Pasto fue construida
a partir de registros del Registro Nacional de Despachos
de Carga (RNDC) del Ministerio de Transporte de Colombia.

El periodo estudiado comprende enero de 2020 a diciembre
de 2024, con 60 niveles mensuales del índice encadenado
de Törnqvist y 59 variaciones porcentuales mensuales.

La unidad de análisis del panel elemental corresponde
a combinaciones de origen, configuración vehicular,
mercancía y periodo.

**Repositorio público de datos y código:**

https://github.com/JuanDavidgm2026/fletes-precios-inflacion-pasto

**Notebook original de construcción:**

https://github.com/JuanDavidgm2026/fletes-precios-inflacion-pasto/blob/main/notebooks/construccion_indice_fletes_RNDC_Pasto.ipynb

### 3.2. Auditoría independiente de reproducibilidad

Se desarrolló una auditoría técnica para examinar
la cadena de procesamiento del indicador regional.

Las comprobaciones incluyen:

- Integridad de archivos mediante SHA-256.
- Cobertura temporal entre 2020 y 2024.
- Verificación de registros con destino Pasto.
- Reconstrucción del panel elemental desde el maestro.
- Comprobación de reglas de depuración N1/N2.
- Reejecución del bloque estadístico original.
- Reconstrucción matemática del índice Törnqvist.
- Comparación de los niveles del índice con la
  serie utilizada en las estimaciones econométricas.

**Notebook de auditoría RNDC depurado:**

https://colab.research.google.com/drive/1zDI2n_Fg7ZAQZcsfIWlTUVsdKStBiwbN

El notebook anterior constituye el anexo técnico
de auditoría y puede ejecutarse independientemente
del notebook econométrico principal.

### 3.3. Principales resultados de la auditoría

Las comprobaciones efectuadas permitieron verificar:

- 78.819 registros en la base maestra procesada.
- 76.218 celdas en el panel elemental.
- 76.218 celdas en el panel jerárquico.
- Reproducción de las reglas de depuración N1/N2
  mediante el bloque estadístico original.
- 60 niveles mensuales del índice de Törnqvist.
- 59 variaciones porcentuales mensuales.
- Concordancia numérica del índice publicado
  con la serie econométrica utilizada.

Estas comprobaciones corresponden a la
reproducibilidad desde los artefactos procesados
disponibles en el repositorio de investigación.

### 3.4. Contraste con registros oficiales y reconstrucción de enero de 2020

Se desarrolló una verificación independiente de la información correspondiente a enero de 2020, utilizando el archivo mensual `EstadisticasRNDC_202001 (1).xlsx`, obtenido mediante la consulta pública del Registro Nacional de Despachos de Carga (RNDC) del Ministerio de Transporte de Colombia.

El archivo mensual contiene 134.426 registros nacionales y 23 columnas. A partir de la selección de operaciones con destino al municipio de Pasto, incluyendo sus localidades identificadas en la fuente, se recuperaron 1.156 registros.

La auditoría permitió comprobar:

- **Reconstrucción desde el archivo mensual:** coincidencia de los 1.156 registros del Excel filtrado con el extracto previamente auditado, contrastando las 23 columnas y conservando la multiplicidad de las observaciones.
- **Conciliación con el maestro procesado:** coincidencia en nueve campos comunes, sin discrepancias entre los multiconjuntos de registros.
- **Integridad documental:** comprobación del archivo Excel mediante SHA-256.
- **Reproducibilidad automática:** descarga del Excel, el manifiesto y el script desde GitHub, seguida de la reconstrucción de los registros de Pasto sin carga manual de archivos.

La evidencia está disponible en [Auditoría RNDC — enero de 2020](auditoria/rndc_enero_2020/).

El archivo mensual original tiene la siguiente huella SHA-256:

`ec1a0ea3c4697a622424472bc681bb3043318961e483170ca16c09ac18b47218`

**Alcance y limitaciones:** la verificación directa desde el archivo mensual oficial corresponde exclusivamente a enero de 2020. Los 59 meses restantes no han sido conciliados individualmente desde sus archivos primarios. La reconstrucción general del índice Törnqvist para 2020–2024 se comprueba mediante los archivos procesados publicados en el repositorio.

La coincidencia computacional no constituye evidencia de causalidad ni garantiza la robustez econométrica de las asociaciones estimadas.

### 3.5. Integración con el notebook principal

La fase 8 del notebook econométrico principal
descarga la serie RNDC congelada y verifica
su integridad mediante SHA-256.

La fase 8B descarga el índice Törnqvist
publicado, verifica su integridad y reproduce
las 59 variaciones mensuales para comprobar
su concordancia con la serie econométrica.

La auditoría independiente amplía esas pruebas
hacia el panel elemental y la depuración
jerárquica del indicador.

No se realizan imputaciones ni modificaciones
de los datos empleados en las estimaciones.

### 3.6. Instrucciones de reproducibilidad

**Notebook econométrico principal:**

https://colab.research.google.com/drive/1mKtipF99zHAk_ys3SQE7UQrjTuhYTuF_

**Notebook de auditoría RNDC:**

https://colab.research.google.com/drive/1zDI2n_Fg7ZAQZcsfIWlTUVsdKStBiwbN

**Procedimiento recomendado:**

1. Abrir el notebook principal en Google Colab.
2. Seleccionar "Entorno de ejecución" y "Ejecutar todas".
3. Verificar las fases 8 y 8B.
4. Abrir y ejecutar el notebook independiente RNDC.
5. Revisar los dictámenes de las comprobaciones.
6. Consultar las tablas, figuras y diagnósticos
   econométricos generados por el notebook principal.

La correcta ejecución del código demuestra
consistencia computacional dentro del alcance
de las comprobaciones realizadas.

No constituye evidencia de causalidad ni
garantiza significancia o estabilidad
estadística de las asociaciones estimadas.

**Prueba automatizada desde GitHub — enero de 2020**

La carpeta [auditoria/rndc_enero_2020](auditoria/rndc_enero_2020/) contiene el archivo mensual de referencia, su manifiesto de integridad, el código de verificación y la documentación correspondiente.

La reproducción automática fue comprobada en un entorno independiente de Google Colab:

[Notebook de prueba automática RNDC](https://colab.research.google.com/drive/1m3msgeROiLGZIZsHsoMNXn69yOKmtCoR?usp=sharing)

La prueba RNDC 12 descarga los insumos publicados, verifica el SHA-256 del Excel y reconstruye los 1.156 registros con destino a Pasto. El dictamen obtenido fue `PASS_REPRODUCCION_AUTOMATICA_RNDC`.

Esta prueba no sustituye las conciliaciones RNDC 06D y RNDC 11, ni implica una validación directa de los archivos oficiales de los otros 59 meses.
---

## 4. Alcance y limitaciones

La investigación utiliza datos oficiales
y artefactos procesados publicados para
facilitar la reproducción de sus resultados.

La reproducibilidad del índice RNDC desde
las bases procesadas fue comprobada mediante
auditorías independientes.

La verificación directa con registros oficiales
originales abarcó únicamente enero de 2020
y nueve campos comunes.

Los demás periodos no se consideran
conciliados directamente con la fuente primaria.

Los resultados econométricos deben interpretarse
como asociaciones dinámicas condicionales,
sin atribuciones causales.


