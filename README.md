# Fletes, precios mayoristas e inflación en Pasto

Repositorio de apoyo al proyecto de investigación sobre la relación entre los costos del transporte de carga, los precios mayoristas de alimentos y la brecha inflacionaria entre Pasto y Colombia.

El horizonte general de la investigación corresponde al periodo **2018–2024**. Sin embargo, el índice regional de fletes construido a partir de información del Registro Nacional de Despachos de Carga (RNDC) dispone de una serie mensual reproducible y homogénea para **2020–2024**.

## Objetivo del repositorio

Este repositorio almacena los archivos necesarios para reproducir, auditar y utilizar la segunda variable principal del proyecto:

**Índice regional de fletes de carga con destino a Pasto.**

El índice fue construido a partir de registros oficiales del **Registro Nacional de Despachos de Carga (RNDC) del Ministerio de Transporte de Colombia**.

La serie no corresponde a un índice oficial publicado por el Ministerio de Transporte. Es un **índice construido por los autores a partir de información oficial RNDC** para aproximar la dinámica mensual de los costos de transporte de carga asociados con Pasto.

## Cobertura temporal

La base consolidada contiene información mensual para:

**enero de 2020 – diciembre de 2024**

El índice se normaliza con:

**enero de 2020 = 100**

Las variaciones mensuales utilizadas posteriormente en los modelos econométricos están disponibles para:

**febrero de 2020 – diciembre de 2024**

Esto genera un total de:

**59 variaciones mensuales.**

La ausencia de observaciones equivalentes para 2018–2019 no se corrige mediante interpolaciones, imputaciones ni empalmes artificiales con otros indicadores.

## Construcción del índice

La unidad elemental utilizada para comparar los costos de transporte entre meses se define mediante la combinación:

`ORIGEN × CONFIGURACIÓN VEHICULAR × MERCANCÍA`

El destino se mantiene fijo en **Pasto**.

Para cada celda elemental y mes se calcula el valor medio pagado por viaje con información monetaria válida:

`p(i,t) = VALORESPAGADOS / VIAJES_CON_VALOR`

donde:

`VIAJES_CON_VALOR = VIAJESTOTALES - VIAJESVALORCERO`

El índice principal utiliza un **índice encadenado de Törnqvist**, calculado únicamente sobre celdas comparables entre los meses `t-1` y `t`.

Como ejercicios de robustez se incluyen:

- índice de Fisher sobre las mismas celdas comparables;
- índice Törnqvist calculado sin aplicar la regla jerárquica de elegibilidad monetaria;
- sensibilidad excluyendo observaciones con valor elemental de $2.000;
- agregación alternativa por origen y configuración vehicular.

## Tratamiento de observaciones monetarias

La construcción del índice sigue un criterio conservador.

No se realizan:

- imputaciones;
- winsorizaciones;
- sustituciones de valores;
- eliminación automática de observaciones altas;
- cortes monetarios arbitrarios.

Las observaciones monetarias excepcionalmente altas se conservan debido a que pueden corresponder a choques logísticos reales.

La depuración se concentra exclusivamente en valores monetarios anormalmente bajos cuando existe evidencia simultánea suficiente.

La regla utiliza:

- información histórica propia de la celda;
- comparación transversal dentro de la misma ruta;
- comparación con observaciones de la misma mercancía y configuración en otras rutas;
- umbral robusto basado en `z = 3.5`;
- únicamente información contemporánea o pasada.

No se utiliza información de meses futuros para decidir la elegibilidad de una observación.

## Resultado principal

La variable econométrica principal es:

`VAR_FLETE_TORNQVIST_PCT`

Esta variable representa la variación porcentual mensual del índice regional de fletes construido mediante Törnqvist.

También se conservan las siguientes variables de sensibilidad:

- `VAR_FLETE_FISHER_PCT`
- `VAR_FLETE_CRUDO_PCT`
- `VAR_FLETE_SIN_2000_PCT`

## Estructura del repositorio

```text
fletes-precios-inflacion-pasto/
│
├── data/
│   ├── RNDC_PASTO_MASTER_2020_2024.parquet
│   ├── RNDC_PASTO_PANEL_ELEMENTAL_2020_2024.parquet
│   ├── RNDC_PASTO_PANEL_JERARQUICO_2020_2024.parquet
│   ├── indice_flete_regional_pasto_2020_2024.parquet
│   ├── variable2_flete_regional_modelo_2020_2024.csv
│   ├── robustez_variable2.csv
│   ├── episodios_auditados_variable2.csv
│   └── metadata_variable2.json
│
├── notebooks/
│   └── construccion_indice_fletes_RNDC_Pasto.ipynb
│
└── README.md
```

## Descripción de los archivos

### `RNDC_PASTO_MASTER_2020_2024.parquet`

Base maestra consolidada con los registros RNDC utilizados para Pasto durante 2020–2024.

Contiene aproximadamente 78 mil registros y constituye el punto de partida de la construcción del índice.

### `RNDC_PASTO_PANEL_ELEMENTAL_2020_2024.parquet`

Panel mensual construido a partir de las combinaciones de origen, configuración vehicular y mercancía.

### `RNDC_PASTO_PANEL_JERARQUICO_2020_2024.parquet`

Panel resultante después de aplicar la regla jerárquica de elegibilidad monetaria.

### `indice_flete_regional_pasto_2020_2024.parquet`

Serie mensual del índice regional de fletes.

Incluye el índice Törnqvist principal y las principales alternativas utilizadas para robustez.

### `variable2_flete_regional_modelo_2020_2024.csv`

Archivo compacto destinado al análisis econométrico.

Contiene las **59 variaciones mensuales entre febrero de 2020 y diciembre de 2024** y será utilizado posteriormente en el notebook maestro de la investigación.

### `robustez_variable2.csv`

Resultados de las principales especificaciones alternativas utilizadas para evaluar la estabilidad del índice.

### `episodios_auditados_variable2.csv`

Registro de meses con movimientos o coberturas particulares que fueron revisados individualmente.

Estos episodios se conservaron cuando existía evidencia de que podían corresponder a cambios reales y no a errores evidentes de los datos.

### `metadata_variable2.json`

Metadatos metodológicos de la Variable 2, incluyendo periodo, método de construcción, restricciones de tratamiento de datos y hashes de verificación.

### `construccion_indice_fletes_RNDC_Pasto.ipynb`

Notebook de construcción y auditoría de la Variable 2.

Contiene el proceso utilizado para descargar, transformar, validar, consolidar y construir el índice regional.

La reconstrucción completa desde los archivos mensuales RNDC puede requerir un tiempo considerable. Para el análisis econométrico posterior se recomienda utilizar directamente los archivos finales incluidos en `data/`, cuya integridad puede comprobarse mediante SHA-256.

## Verificación de integridad

Los principales archivos congelados pueden verificarse mediante los siguientes hashes SHA-256.

### Serie econométrica

```text
variable2_flete_regional_modelo_2020_2024.csv

aaec180a88d32bbccbfb13b94be4784c9e9b4c6f23d9a93b7475b1acd1bd3891
```

### Índice regional

```text
indice_flete_regional_pasto_2020_2024.parquet

4336398949cbc5c74a95b7bf982f241a5b4e5564e44b6d67313536c0a4fa0e19
```

### Base maestra RNDC

```text
RNDC_PASTO_MASTER_2020_2024.parquet

b6db3d2caef389ade80117f36c2db58dd3d4fe25a27425c796eb8dd1dadb6096
```

### Panel con regla jerárquica

```text
RNDC_PASTO_PANEL_JERARQUICO_2020_2024.parquet

c285c6e3c1f9de3eb10b38ef2ab5fe9236617d04a4d404a9a7362e19ec09d9b0
```

## Reproducibilidad

La construcción busca preservar la trazabilidad entre los datos oficiales y la serie econométrica final.

Para reproducir completamente la Variable 2:

1. Abrir `notebooks/construccion_indice_fletes_RNDC_Pasto.ipynb`.
2. Ejecutar las celdas en orden en un entorno limpio de Google Colab.
3. Permitir la descarga de los archivos oficiales RNDC requeridos.
4. Ejecutar las validaciones de estructura y cobertura.
5. Construir el panel elemental.
6. Aplicar la regla jerárquica de elegibilidad monetaria.
7. Construir los índices Törnqvist y Fisher.
8. Ejecutar las pruebas de robustez y auditorías.
9. Comparar los hashes obtenidos con los registrados en este repositorio.

Para replicar únicamente el análisis econométrico posterior no es necesario reconstruir toda la base RNDC. Puede utilizarse directamente:

`data/variable2_flete_regional_modelo_2020_2024.csv`

verificando previamente su hash SHA-256.

## Limitaciones

El horizonte general del proyecto es 2018–2024, pero la fuente pública actualmente reproducible permite construir de manera homogénea el índice regional RNDC utilizado en el modelo principal únicamente para 2020–2024.

Por esta razón:

- no se imputan observaciones para 2018–2019;
- no se interpolan meses faltantes;
- no se empalma artificialmente el índice RNDC con el ICTC;
- la especificación econométrica principal que incorpora el índice regional utiliza la muestra temporal común disponible.

Esta decisión prioriza la comparabilidad y la integridad de la información frente a la ampliación artificial del número de observaciones.

## Proyecto de investigación

El índice forma parte del proyecto:

**Costos del transporte de carga, precios mayoristas de alimentos y brecha inflacionaria Pasto–Colombia: evidencia mensual, 2018–2024.**

El análisis posterior integrará:

1. precios mayoristas de alimentos provenientes de SIPSA;
2. índice regional de fletes construido con RNDC;
3. brecha inflacionaria mensual entre Pasto y Colombia.

Las estimaciones se interpretarán como **asociaciones estadísticas y dinámicas**, no como efectos causales identificados.

## Licencia y fuentes

Los datos originales pertenecen a sus respectivas entidades públicas.

Este repositorio conserva productos derivados utilizados exclusivamente con fines académicos y de reproducibilidad de la investigación.

Fuente principal de la Variable 2:

**Registro Nacional de Despachos de Carga (RNDC) — Ministerio de Transporte de Colombia.**
