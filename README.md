# Software FJ – Sistema integral de gestión de clientes, servicios y reservas

Proyecto de la Fase 4 del curso **Programación (213023)** – UNAD.
Sistema orientado a objetos en Python, **sin base de datos**: todo se maneja con objetos y listas,
y se usa un archivo únicamente (logs).

## Ejecytar

Requiere Python 3.8 o superior (no necesita instalar librerías).

```bash
python main.py
```

Al ejecutarlo se corren 17 simulaciones y se genera el archivo `logs/software_fj.log`.

## Estructura del proyecto

| Archivo | Contenido |
|---|---|
| `main.py` | Programa principal con las 17 simulaciones |
| `excepciones.py` | Excepciones personalizadas (todas heredan de `SoftwareFJError`) |
| `logger.py` | Configuración del archivo de logs |
| `entidad.py` | Clase abstracta `Entidad` |
| `cliente.py` | Clase `Cliente` con encapsulación y validaciones |
| `servicio.py` | Clase abstracta `Servicio` y método sobrecargado `calcular_costo_total` |
| `servicios_especializados.py` | `ReservaSala`, `AlquilerEquipo` y `Asesoria` |
| `reserva.py` | Clase `Reserva` (confirmar, cancelar, procesar) |
| `gestor.py` | Clase `SistemaFJ` con las listas internas |
| `logs/software_fj.log` | Registro de eventos y errores de una ejecución |

## Conceptos aplicados

- **Abstracción:** clases abstractas `Entidad` y `Servicio` (módulo `abc`).
- **Herencia:** `Cliente`, `Servicio` y `Reserva` heredan de `Entidad`; los tres servicios heredan de `Servicio`.
- **Polimorfismo:** cada servicio sobrescribe `calcular_costo`, `describir` y `validar_parametros`.
- **Encapsulación:** atributos privados con propiedades (`@property`) que validan los datos.
- **Sobrecarga de métodos:** `calcular_costo_total(horas, impuesto=0.0, descuento=0.0)` se puede llamar con distintas combinaciones de parámetros (Python simula la sobrecarga con parámetros opcionales).
- **Manejo de excepciones:** excepciones personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from ...`.
- **Logs:** todos los eventos y errores quedan registrados con el módulo `logging`.

## Servicios

| Servicio | Duración permitida | Costo |
|---|---|---|
| Reserva de sala | 1 a 8 horas | precio por hora × horas |
| Alquiler de equipo | 1 a 24 horas | precio por hora × horas + depósito |
| Asesoría | 1 a 4 horas | precio por hora × horas (+20 % si el especialista es senior) |

## Simulaciones 

Clientes válidos e inválidos (correo mal escrito, datos faltantes, documento duplicado), servicios válidos e
inválidos (precio negativo, nivel inexistente), reservas exitosas y fallidas (horas fuera de rango, cliente
inexistente, servicio no disponible, reserva cancelada, descuento absurdo, impuesto escrito como texto).
El programa **nunca se detiene**: cada error se captura, se registra en el log y continúa con la siguiente simulación.
