"""
Programa principal de Software FJ.

Ejecuta 17 simulaciones (válidas e inválidas) para demostrar que el sistema
maneja los errores y sigue funcionando. Todo queda registrado en logs/software_fj.log
"""

import logging
from logger import configurar_logs
from excepciones import SoftwareFJError
from gestor import SistemaFJ
from servicios_especializados import ReservaSala, AlquilerEquipo, Asesoria

IVA = 0.19  # impuesto del 19 %


def ejecutar_simulacion(numero, titulo, funcion, sistema):
    """
    Ejecuta una simulación dentro de un try/except/else/finally.
    Si ocurre un error lo registra en el log y el programa sigue con la siguiente.
    """
    print(f"\n--- Simulación {numero}: {titulo} ---")
    logging.info(f"INICIO simulación {numero}: {titulo}")
    try:
        funcion(sistema)  # se ejecuta la simulación
    except SoftwareFJError as error:
        # Errores propios del sistema (los esperados)
        logging.error(f"Simulación {numero} - {type(error).__name__}: {error}")
        causa = error.__cause__
        while causa is not None:
            # Si el error venía encadenado, se registra cada causa hasta llegar a la original
            logging.error(f"Simulación {numero} - causa: {type(causa).__name__}: {causa}")
            causa = causa.__cause__
        print(f"  Error controlado -> {error}")
    except Exception as error:
        # Cualquier otro error inesperado: se registra y el programa NO se detiene
        logging.critical(f"Simulación {numero} - error inesperado {type(error).__name__}: {error}")
        print(f"  Error inesperado controlado -> {error}")
    else:
        # Solo se ejecuta si no hubo ningún error
        logging.info(f"Simulación {numero} terminó sin errores")
        print("  Resultado: OK")
    finally:
        # Se ejecuta siempre
        logging.info(f"FIN simulación {numero}")


# ---------------------------------------------------------------------------
# Simulaciones: cada una es una función que recibe el sistema
# ---------------------------------------------------------------------------

def sim_cliente_valido_1(sistema):
    cliente = sistema.registrar_cliente("1012345678", "Ana Martínez", "ana@correo.com", "3001234567")
    print(f"  {cliente.describir()}")


def sim_cliente_valido_2(sistema):
    cliente = sistema.registrar_cliente("52987654", "Luis Gómez", "luis@correo.com", "3109876543")
    print(f"  {cliente.describir()}")


def sim_cliente_correo_invalido(sistema):
    # El correo no tiene @
    sistema.registrar_cliente("80123456", "Pedro Ruiz", "pedrocorreo.com", "3201112233")


def sim_cliente_datos_faltantes(sistema):
    # Faltan el nombre y el teléfono
    sistema.registrar_cliente("90123456", None, "maria@correo.com")


def sim_cliente_duplicado(sistema):
    # El documento de Ana ya está registrado
    sistema.registrar_cliente("1012345678", "Ana Otra", "otra@correo.com", "3005556677")


def sim_servicios_validos(sistema):
    sala = ReservaSala("S01", "Sala Innovación", 50000, 12)
    equipo = AlquilerEquipo("S02", "Portátil Gamer", 20000, "portátil", 50000)
    asesoria = Asesoria("S03", "Asesoría en Python", 80000, "Dra. Rojas", "senior")
    for servicio in (sala, equipo, asesoria):
        sistema.registrar_servicio(servicio)
        print(f"  {servicio.describir()}")  # polimorfismo: cada uno se describe distinto


def sim_servicio_precio_invalido(sistema):
    # Precio negativo
    sistema.registrar_servicio(ReservaSala("S04", "Sala Pequeña", -30000, 6))


def sim_servicio_nivel_invalido(sistema):
    # El nivel 'experto' no existe
    sistema.registrar_servicio(Asesoria("S05", "Asesoría en Java", 70000, "Ing. Pérez", "experto"))


def sim_reserva_exitosa_sala(sistema):
    reserva = sistema.crear_reserva("1012345678", "S01", 3)
    reserva.confirmar()
    costo = reserva.procesar(IVA, 0.10)  # con impuesto y descuento
    print(f"  {reserva.describir()}")
    print(f"  Costo con IVA y 10% de descuento: ${costo:,.2f}")


def sim_reserva_horas_invalidas(sistema):
    # Una sala solo se reserva hasta 8 horas
    sistema.crear_reserva("1012345678", "S01", 20)


def sim_reserva_cliente_inexistente(sistema):
    sistema.crear_reserva("99999999", "S01", 2)


def sim_reserva_servicio_no_disponible(sistema):
    equipo = sistema.buscar_servicio("S02")
    equipo.disponible = False  # se deja el equipo fuera de servicio
    reserva = sistema.crear_reserva("52987654", "S02", 5)
    reserva.confirmar()  # falla porque no está disponible


def sim_cancelar_y_confirmar(sistema):
    reserva = sistema.crear_reserva("52987654", "S01", 2)
    reserva.cancelar()
    print(f"  {reserva.describir()}")
    reserva.confirmar()  # una reserva cancelada no se puede confirmar


def sim_calculo_inconsistente(sistema):
    reserva = sistema.crear_reserva("1012345678", "S03", 2)
    reserva.confirmar()
    reserva.procesar(IVA, 1.5)  # un descuento de 150 % no tiene sentido


def sim_impuesto_como_texto(sistema):
    reserva = sistema.crear_reserva("52987654", "S03", 1)
    reserva.confirmar()
    reserva.procesar("diecinueve")  # el impuesto debe ser un número


def sim_reserva_exitosa_asesoria(sistema):
    reserva = sistema.crear_reserva("52987654", "S03", 2)
    reserva.confirmar()
    costo = reserva.procesar()  # sin impuesto ni descuento (parámetros opcionales)
    print(f"  {reserva.describir()}")
    print(f"  Costo base sin impuestos: ${costo:,.2f}")


def sim_reserva_exitosa_solo_impuesto(sistema):
    sistema.buscar_servicio("S02").disponible = True  # se vuelve a habilitar el equipo
    reserva = sistema.crear_reserva("1012345678", "S02", 4)
    reserva.confirmar()
    costo = reserva.procesar(IVA)  # solo con impuesto
    print(f"  {reserva.describir()}")
    print(f"  Costo con IVA: ${costo:,.2f}")


def main():
    """Función principal: prepara el log, corre las simulaciones y muestra el resumen."""
    configurar_logs()
    logging.info("===== INICIO DEL SISTEMA SOFTWARE FJ =====")
    sistema = SistemaFJ()

    # Lista de simulaciones: (título, función)
    simulaciones = [
        ("Registrar cliente válido (Ana)", sim_cliente_valido_1),
        ("Registrar cliente válido (Luis)", sim_cliente_valido_2),
        ("Cliente con correo inválido", sim_cliente_correo_invalido),
        ("Cliente con datos faltantes", sim_cliente_datos_faltantes),
        ("Cliente con documento duplicado", sim_cliente_duplicado),
        ("Crear tres servicios válidos", sim_servicios_validos),
        ("Servicio con precio negativo", sim_servicio_precio_invalido),
        ("Asesoría con nivel inválido", sim_servicio_nivel_invalido),
        ("Reserva de sala exitosa (IVA + descuento)", sim_reserva_exitosa_sala),
        ("Reserva con horas inválidas (encadenamiento)", sim_reserva_horas_invalidas),
        ("Reserva con cliente inexistente", sim_reserva_cliente_inexistente),
        ("Reserva de servicio no disponible", sim_reserva_servicio_no_disponible),
        ("Cancelar y luego confirmar una reserva", sim_cancelar_y_confirmar),
        ("Cálculo inconsistente (descuento de 150%)", sim_calculo_inconsistente),
        ("Impuesto escrito como texto", sim_impuesto_como_texto),
        ("Reserva de asesoría exitosa (sin impuestos)", sim_reserva_exitosa_asesoria),
        ("Reserva de equipo exitosa (solo IVA)", sim_reserva_exitosa_solo_impuesto),
    ]

    # Se ejecutan todas, una tras otra, aunque alguna falle
    for numero, (titulo, funcion) in enumerate(simulaciones, start=1):
        ejecutar_simulacion(numero, titulo, funcion, sistema)

    # Resumen final con los datos que quedaron en las listas internas
    print("\n========== RESUMEN FINAL ==========")
    print(f"Clientes registrados: {len(sistema.clientes)}")
    print(f"Servicios registrados: {len(sistema.servicios)}")
    print(f"Reservas creadas: {len(sistema.reservas)}")
    for reserva in sistema.reservas:
        print(f"  {reserva.describir()}")
    logging.info(
        f"RESUMEN: {len(sistema.clientes)} clientes, {len(sistema.servicios)} servicios, "
        f"{len(sistema.reservas)} reservas")
    logging.info("===== FIN DEL SISTEMA SOFTWARE FJ =====")


# Esto hace que main() solo se ejecute si se corre este archivo directamente
if __name__ == "__main__":
    main()
