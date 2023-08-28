import datetime
from attr import validate
from src.core.business.crud_manager import CRUDManager
from src.core.database.board import Cuote
from src.core.database.auth import Associate
from datetime import date, datetime
from src.core.business.config_manager import ConfigManager
from src.core.business.service_manager import ServiceManager
from flask import abort
from sqlalchemy import func
from src.web.helpers.controller_helpers import validate_id


"""Capa de negocio de alto nivel, para la tabla de Cuotas de la BD, donde se requiere hacer CRUDs sobre sus tuplas."""
class CuoteManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase CuoteManager."""
        super().__init__(Cuote)
        self.sysconfig_m = ConfigManager()
        self.service_m = ServiceManager()

    def is_defaulter(self, associate_id):
        """Verifica si un asociado tiene cuotas impagas.

        Args:
            associate_id (int): Identificador del asociado.

        Returns:
            bool: True si tiene cuotas impagas, False en caso contrario.
        """
        today = date.today()

    def get_associate_cuotes(self, associate_id, page):
        """Obtiene las cuotas de un asociado. Sean pagadas o impagas."""
        return self.get_paginator(
            self.database.filter_by(associate_id=associate_id), page
        )

    def get_unpaid_coute(self, associate_id):
        today = date.today()
        return self.database.filter_by(
            associate_id=associate_id, paid_date=None
        ).filter(Cuote.expiration_date > today)

    def all_payments(self):
        query = self.database.query().filter(Cuote.paid_date != None).all()
        return [(e.paid_date, e.price + e.late_fee) for e in query]

    def income_by_month(self):
        lista = self.all_payments()
        dict = {}
        for tuple in lista:
            year = tuple[0].year
            month = tuple[0].month
            fecha = datetime(year, month, 1)
            precio = tuple[1]
            precio = precio + dict.get(fecha, 0)
            dict[fecha] = precio
        return dict

    def register_payment(self, cuote):
        """Registra el pago de una cuota.

        Args:
            cuote (Cuote): Cuota a pagar.
        """
        today = date.today()
        self.database.update(
            cuote.id, paid_date=today, late_fee=self.get_late_fee(cuote, today)
        )

    def generate_cuotes_new_month(self):
        """Genera las cuotas de los asociados para el mes actual."""
        expiration_date = date.today().replace(day=10)
        created_count = 0

        for service in self.service_m.filter_by():
            for associate in service.associates:
                if not associate.active:
                    continue

                if self.database.exists(
                    self.filter_by(
                        expiration_date=expiration_date,
                        associate=associate,
                        service=service,
                    )
                ):
                    continue

                self.database.create(
                    price=service.mensual_cost,
                    expiration_date=expiration_date,
                    associate=associate,
                    service=service,
                )

                created_count = created_count + 1

        return created_count

    def get_late_fee(self, cuote, today):
        """Calcula la multa por atraso de una cuota.

        Args:
            cuote (Cuote): Cuota a calcular.
            today (date): Fecha actual.

        Returns:
            float: precio de la cuota aumentado por la multa.
        """
        if today <= cuote.expiration_date:
            return 0.0

        return cuote.price * (self.sysconfig_m.get_field("late_fee_percentage") / 100.0)

    def validate_and_get(self, request_args, expected_paid_state):
        """Valida los argumentos de una solicitud y obtiene la cuota.

        Args:
            request_args (dict): Argumentos de la solicitud.
            expected_paid_state (bool): Estado de pago esperado.

        Returns:
            Cuote: Cuota obtenida.
        """
        cuote = validate_id(self, request_args)

        if bool(cuote.paid_date) != bool(expected_paid_state):
            abort(422)

        return cuote

    def finish_filter(self, associates, page):
        """Filtra las cuotas de los asociados.

        Args:
            associates (list): Lista de asociados.

        Returns:
            Paginator: Paginador con las cuotas filtradas.
        """
        return self.get_paginator(self.database.query(True).join(associates), page)

    def filter_surname_get_paginator(self, associate_m, surname, page):
        """Filtra las cuotas por apellido.

        Args:
            surname (str): Apellido a filtrar.

        Returns:
            Paginator: Paginador con las cuotas filtradas.
        """
        return self.finish_filter(
            associate_m.filter(False, Associate.last_name.ilike(f"%{surname}%")), page
        )

    def filter_id_get_paginator(self, associate_m, id, page):
        """Filtra las cuotas por identificador.

        Args:
            associate_m (AssociateManager): Manager de asociados.
            id (int): Identificador a filtrar.
            page (int): Página a mostrar.

        Returns:
            Paginator: Paginador con las cuotas filtradas.
        """
        return self.finish_filter(associate_m.filter_by(id=id), page)

    def cuote_detail_month(self, associate_id, date):
        """Obtiene el detalle de las cuotas de un asociado en un mes.

        Args:
            associate_id (int): Identificador del asociado.
            month (int): Mes a filtrar.
            year (int): Año a filtrar.

        Returns:
            list: Lista de cuotas filtradas.
        """

        return self.database.filter_by(
            associate_id=associate_id, expiration_date=date
        ).all()
