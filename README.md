# Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ

**Curso:** Programación (213023A_2204) — UNAD
**Actividad:** Fase 4 — Componente práctico, prácticas simuladas
**Autor:** Alvaro Steven Carreño Nasayo

## Descripción
Aplicación orientada a objetos en Python que gestiona clientes, servicios (reserva de salas, alquiler de equipos y asesorías) y reservas para la empresa Software FJ. **No usa bases de datos**: toda la información vive en objetos y listas en memoria, y solo se usa un archivo para el registro de eventos y errores (`logs/sistema.log`).

## Cómo ejecutar
Requiere Python 3.10 o superior (no usa librerías externas).

```bash
python main.py
```

## Estructura
| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas (`SoftwareFJError` y derivadas) |
| `entidad.py` | Clase abstracta `Entidad` (base de todo el sistema) |
| `cliente.py` | Clase `Cliente` con atributos privados y validaciones |
| `servicios.py` | Clase abstracta `Servicio` + `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| `reserva.py` | Clase `Reserva` (confirmar, cancelar, procesar) |
| `sistema.py` | Gestor con listas internas y captura de errores |
| `logger.py` | Configuración del archivo de logs |
| `main.py` | Simulación de 24 operaciones válidas e inválidas |

## Conceptos aplicados
- **Abstracción:** `Entidad` y `Servicio` son clases abstractas (`ABC`, `@abstractmethod`).
- **Herencia:** `Cliente`, `Servicio` y `Reserva` heredan de `Entidad`; los tres servicios heredan de `Servicio`.
- **Polimorfismo:** cada servicio sobrescribe `costo_base()`, `validar_parametros()` y `describir()`.
- **Encapsulación:** atributos privados (`__nombre`, `__documento`…) con `@property` y setters validados.
- **Sobrecarga de métodos:** `calcular_costo(duracion[, impuesto[, descuento]])` y `cotizar()` con `@singledispatchmethod` (acepta número o diccionario).
- **Manejo de excepciones:**
  - `try/except` → `sistema.ejecutar_operacion()`
  - `try/except/else` → `Reserva.confirmar()`, `sistema.registrar_cliente()`
  - `try/except/finally` → `Reserva.procesar()`, `sistema.crear_reserva()`
  - Encadenamiento `raise ... from ...` → `Reserva.confirmar()` y `Reserva.procesar()`
- **Logs:** todos los eventos y errores quedan en `logs/sistema.log`.
