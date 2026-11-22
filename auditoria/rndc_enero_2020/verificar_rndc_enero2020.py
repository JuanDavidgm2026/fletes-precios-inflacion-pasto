"""Reconstruye el subconjunto Pasto desde el Excel RNDC mensual de enero de 2020."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from decimal import Decimal, InvalidOperation
import pandas as pd

BASE = Path(__file__).resolve().parent
EXCEL = BASE / 'EstadisticasRNDC_202001.xlsx'
SHA_ORIGEN = 'ec1a0ea3c4697a622424472bc681bb3043318961e483170ca16c09ac18b47218'
CSV_REFERENCIA = '668e80fcf56033a11155bc9f82726bc4df7ffd9cc4e9e1736a60c1d59aeacbea'
CAMPOS_N = ['CODMUNICIPIOORIGEN','CODMUNICIPIODESTINO','COD_CONFIG_VEHICULO','CODMERCANCIA','VIAJESTOTALES','VIAJESVALORCERO','KILOGRAMOS','VALORESPAGADOS','KILOMETROS']
NUMERICOS = {'MES','CODMUNICIPIOORIGEN','CODMUNICIPIODESTINO','VIAJESTOTALES','KILOGRAMOS','GALONES','VIAJESLIQUIDOS','VIAJESVALORCERO','KILOMETROS','VALORESPAGADOS'}

def hashfile(p):
    return sha256(p.read_bytes()).hexdigest()

def canon(v, col):
    s = str(v).strip()
    if col in NUMERICOS and s:
        try:
            x = Decimal(s)
            if x.is_finite():
                return format(x.normalize(),'f')
        except InvalidOperation:
            pass
    return s

def as_counter(df, cols):
    return Counter(tuple(canon(v, c) for c, v in zip(cols, row)) for row in df[cols].itertuples(index=False, name=None))

if not EXCEL.is_file():
    raise FileNotFoundError(f'Falta {EXCEL}. Descarga el Excel original del portal RNDC.')
if hashfile(EXCEL) != SHA_ORIGEN:
    raise RuntimeError('ERROR: SHA-256 del Excel diferente del archivo auditado.')
df = pd.read_excel(EXCEL, sheet_name='Exportar Hoja de Trabajo', dtype=str, keep_default_na=False)
df.columns = df.columns.str.strip().str.upper()
if len(df) != 134426 or len(df.columns) != 23:
    raise RuntimeError(f'Cobertura diferente: {df.shape}')
if {canon(x, 'MES') for x in df['MES']} != {'202001'}:
    raise RuntimeError('MES diferente de 202001.')
pasto = df.loc[df['MUNICIPIODESTINO'].str.contains(r'\bPASTO\b', case=False, regex=True, na=False)].copy()
if len(pasto) != 1156:
    raise RuntimeError(f'Se esperaban 1156 registros; hay {len(pasto)}.')
print(f'PASS fuente: {len(df)} registros nacionales, {len(pasto)} de Pasto, {len(df.columns)} columnas')
print('Distribución destino:')
print(pasto.groupby(['MUNICIPIODESTINO','CODMUNICIPIODESTINO']).size().to_string())

# Archivo de auditoría externo opcional; se verifica por contenido y multiplicidad.
csv = BASE / 'RNDC_202001_destino_pasto_original.csv'
if csv.exists():
    if hashfile(csv) != CSV_REFERENCIA:
        raise RuntimeError('CSV de auditoría con SHA diferente.')
    ref = pd.read_csv(csv, dtype=str, keep_default_na=False, encoding='utf-8-sig')
    ref.columns = ref.columns.str.strip().str.upper()
    for cols in [list(df.columns), CAMPOS_N]:
        a, b = as_counter(pasto, cols), as_counter(ref, cols)
        if a != b:
            raise RuntimeError(f'Diferencias en conciliación de {len(cols)} columnas: {sum((a-b).values())}/{sum((b-a).values())}')
    print('PASS conciliación completa: 23 y 9 columnas sin diferencias')
else:
    print('El CSV de referencia no está presente: reconstrucción verificada; comparación externa no ejecutada.')
