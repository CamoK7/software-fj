"""
Clase SistemaFJ.

Administra las listas internas de clientes, servicios y reservas
(no se usa base de datos, todo vive en memoria).
"""

import logging
from cliente import Cliente
from servicio import Servicio
from reserva import Reserva
from excepciones import ClienteInvalidoError, ServicioInvalidoError, OperacionNoPermitidaError


class SistemaFJ:
    """Sistema integral de gestión de clientes, servicios y reservas."""

    def __init__(self):
        self._clientes = []     # lista de objetos Cliente
        self._servicios = []    # lista de objetos Servicio
        self._reservas = []     # lista de objetos Reserva
        self._contador_reservas = 0  # para dar un número a cada reserva

    @property
    def clientes(self):
        return self._clientes

    @property
    def servicios(self):
        return self._servicios

    @property
    def reservas(self):
        return self._reservas

    def registrar_cliente(self, documento=None, nombre=None, correo=None, telefono=None):
        """Crea un cliente y lo agrega a la lista (no permite documentos repetidos)."""
        cliente = Cliente(documento, nombre, correo, telefono)  # puede lanzar ClienteInvalidoError
        for existente in self._clientes:
            if existente.id == cliente.id:
                raise OperacionNoPermitidaError(f"Ya existe un cliente con el documento {documento}")
        self._clientes.append(cliente)
        logging.info(f"Cliente registrado: {cliente.describir()}")
        return cliente

    def registrar_servicio(self, servicio):
        """Agrega un servicio ya creado a la lista (no permite ids repetidos)."""
        if not isinstance(servicio, Servicio):
            raise ServicioInvalidoError("Solo se pueden registrar objetos de tipo Servicio")
        for existente in self._servicios:
            if existente.id == servicio.id:
                raise OperacionNoPermitidaError(f"Ya existe un servicio con el id {servicio.id}")
        self._servicios.append(servicio)
        logging.info(f"Servicio registrado: {servicio.describir()}")
        return servicio

    def buscar_cliente(self, documento):
        """Busca un cliente por documento; si no existe lanza un error."""
        for cliente in self._clientes:
            if cliente.id == documento:
                return cliente
        raise ClienteInvalidoError(f"No existe un cliente con el documento {documento}")

    def buscar_servicio(self, id_servicio):
        """Busca un servicio por id; si no existe lanza un error."""
        for servicio in self._servicios:
            if servicio.id == id_servicio:
                return servicio
        raise ServicioInvalidoError(f"No existe un servicio con el id {id_servicio}")

    def crear_reserva(self, documento, id_servicio, horas):
        """Busca el cliente y el servicio, crea la reserva y la guarda en la lista."""
        cliente = self.buscar_cliente(documento)
        servicio = self.buscar_servicio(id_servicio)
        # El número de reserva solo aumenta si la reserva se crea bien
        reserva = Reserva(self._contador_reservas + 1, cliente, servicio, horas)
        self._contador_reservas += 1
        self._reservas.append(reserva)
        logging.info(f"Reserva creada: {reserva.describir()}")
        return reserva
