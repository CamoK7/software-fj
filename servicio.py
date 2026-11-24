"""
Clase abstracta Servicio.

Es el molde de todos los servicios que ofrece Software FJ. Las clases hijas
(sala, equipo, asesoría) deben sobrescribir los métodos abstractos.
"""

from abc import abstractmethod
from entidad import Entidad
from excepciones import ServicioInvalidoError, CalculoInconsistenteError


class Servicio(Entidad):
    """Clase abstracta que representa un servicio de la empresa."""

    def __init__(self, id_servicio=None, nombre=None, precio_hora=None):
        # Validaciones de los datos básicos de cualquier servicio
        if id_servicio is None or not isinstance(id_servicio, str) or id_servicio.strip() == "":
            raise ServicioInvalidoError("El servicio necesita un identificador")
        if nombre is None or not isinstance(nombre, str) or nombre.strip() == "":
            raise ServicioInvalidoError("El servicio necesita un nombre")
        # bool es un tipo de número en Python, por eso se descarta aparte
        if isinstance(precio_hora, bool) or not isinstance(precio_hora, (int, float)):
            raise ServicioInvalidoError("El precio por hora debe ser un número")
        if precio_hora <= 0:
            raise ServicioInvalidoError("El precio por hora debe ser mayor que cero")

        super().__init__(id_servicio)      # guarda el id en la clase padre
        self._nombre = nombre.strip()      # atributos privados (encapsulación)
        self._precio_hora = precio_hora
        self._disponible = True            # todo servicio nuevo está disponible

    @property
    def nombre(self):
        """Nombre del servicio."""
        return self._nombre

    @property
    def precio_hora(self):
        """Precio por hora del servicio."""
        return self._precio_hora

    @property
    def disponible(self):
        """Indica si el servicio se puede reservar."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        """Cambia la disponibilidad (solo acepta True o False)."""
        if not isinstance(valor, bool):
            raise ServicioInvalidoError("La disponibilidad debe ser True o False")
        self._disponible = valor

    def _validar_horas(self, horas, maximo):
        """Revisa que las horas sean un entero entre 1 y el máximo permitido."""
        if isinstance(horas, bool) or not isinstance(horas, int):
            raise ServicioInvalidoError("La duración debe ser un número entero de horas")
        if horas < 1 or horas > maximo:
            raise ServicioInvalidoError(
                f"La duración de '{self._nombre}' debe estar entre 1 y {maximo} horas (se pidió {horas})"
            )

    # ---------- métodos abstractos: las hijas los sobrescriben ----------
    @abstractmethod
    def validar_parametros(self, horas):
        """Valida los parámetros propios de cada tipo de servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, horas):
        """Calcula el costo base de cada tipo de servicio (sin impuestos)."""
        pass

    # ---------- método "sobrecargado" ----------
    def calcular_costo_total(self, horas, impuesto=0.0, descuento=0.0):
        """
        Calcula el costo final. Python no tiene sobrecarga como Java, pero se
        logra con parámetros opcionales. Se puede llamar de varias formas:
            calcular_costo_total(3)                  -> solo costo base
            calcular_costo_total(3, 0.19)            -> con impuesto
            calcular_costo_total(3, 0.19, 0.10)      -> con impuesto y descuento
            calcular_costo_total(3, descuento=0.10)  -> solo con descuento
        impuesto y descuento se dan como fracción (0.19 = 19 %).
        """
        self.validar_parametros(horas)       # método sobrescrito en cada hija
        costo = self.calcular_costo(horas)   # polimorfismo: cada hija calcula distinto
        try:
            # Si llegan textos en lugar de números, esta comparación lanza TypeError
            if impuesto < 0 or impuesto > 1:
                raise CalculoInconsistenteError(f"El impuesto {impuesto} debe estar entre 0 y 1")
            if descuento < 0 or descuento > 1:
                raise CalculoInconsistenteError(f"El descuento {descuento} debe estar entre 0 y 1")
        except TypeError as error:
            # Encadenamiento: se conserva el error original con "from"
            raise CalculoInconsistenteError("El impuesto y el descuento deben ser números") from error
        costo = costo - costo * descuento    # primero se aplica el descuento
        costo = costo + costo * impuesto     # luego se suma el impuesto
        if costo <= 0:
            raise CalculoInconsistenteError(f"El costo final dio {costo}, un valor sin sentido")
        return round(costo, 2)
