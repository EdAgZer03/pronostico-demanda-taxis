# Datos de demanda de taxis

Utilicé el archivo `taxi.csv`, proporcionado en el proyecto de series temporales del bootcamp de Data Science de TripleTen para el caso Sweet Lift Taxi. Contiene pedidos registrados cada 10 minutos entre marzo y agosto de 2018.

| Campo | Descripción |
|---|---|
| `datetime` | Fecha y hora del intervalo, utilizada como índice |
| `num_orders` | Pedidos registrados en el intervalo |

Sumé los seis intervalos de cada hora para formar la variable objetivo horaria. El archivo original no se distribuye en este repositorio.

## Configuración

Si cuentas con los datos del ejercicio, puedes guardarlos fuera del repositorio y definir su ruta:

```powershell
$env:TAXI_DATA_PATH = 'C:\ruta\a\taxi.csv'
```

En macOS o Linux:

```bash
export TAXI_DATA_PATH='/ruta/a/taxi.csv'
```

También puedes colocar el archivo en `data/raw/taxi.csv`, que Git ignora. Si no cuentas con los datos, el notebook ejecutado permite consultar los gráficos, decisiones y resultados agregados.
