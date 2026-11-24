"""
Módulo de excepciones personalizadas del sistema Software FJ.

Todas las excepciones heredan de SoftwareFJError, así en el programa
principal se pueden capturar todas juntas con un solo "except".
"""


class SoftwareFJError(Exception):
    """Excepción base del sistema. De ella heredan todas las demás."""
    pass


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente son inválidos o faltan."""
    pass


class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos o parámetros de un servicio son inválidos."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta usar un servicio que no está disponible."""
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no se puede crear o procesar."""
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una operación que el estado actual no permite."""
    pass


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costos da valores que no tienen sentido."""
    pass
