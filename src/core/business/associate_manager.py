from datetime import datetime
import re
from src.core.business.account_manager import AccountManager
from src.core.database.auth import Associate
from src.core.database.board import Service, Discipline
from src.core.database.board.associate_service import associate_service
from src.core.business.service_manager import DisciplineManager
from src.core.business.cuote_manager import CuoteManager
from src.api.auth.jwt import try_decode, encode
from src.api.responses import SimpleErrorResponse
from typing import Optional
from flask import request
import functools


"""Capa de negocio de alto nivel, para la tabla de Socios de la BD, donde se requiere hacer CRUDs sobre sus tuplas."""
class AssociateManager(AccountManager):
    def __init__(self):
        """Constructor de la clase AssociateManager."""
        super().__init__(Associate)
        self.discipline_m = DisciplineManager()
        self.cuote_m = CuoteManager()

    def get_asociate_for(self, email):
        return self.database.filter_by(email=email).first() or None

    def is_defaulter(self, associate_id):
        return self.cuote_m.is_defaulter(associate_id)

    def do_with_discipline(self, associate, discipline, check_defaulter, action):
        """Inscribir o desinscribir a un asociado de una disciplina.

        Args:
            associate (Associate): Instancia del asociado.
            discipline (Discipline): Instancia de la disciplina.
            check_defaulter (bool): Si es True, se verifica si el asociado es moroso.
            action (function): Función a ejecutar sobre la lista de disciplinas del asociado.

        Raises:
            ValueError: Si el asociado es moroso.
        """
        if check_defaulter and self.cuote_m.is_defaulter(associate.id):
            raise ValueError(
                f"El asociado {associate.first_name} {associate.last_name} no puede asociarse porque es moroso"
            )

        query = self.database.query_for(associate.id)
        self.database.for_each(
            query, lambda associate: action(associate.services, discipline)
        )

    def inscribe_to_discipline(self, associate, discipline):
        """Inscribir a un asociado a una disciplina.

        Args:
            associate (Associate): Instancia del asociado.
            discipline (Discipline): Instancia de la disciplina.
        """
        self.do_with_discipline(associate, discipline, True, lambda a, d: a.append(d))

    def unsubscribe_from_discipline(self, associate, discipline):
        """Desinscribir a un asociado de una disciplina.

        Args:
            associate (Associate): Instancia del asociado.
            discipline (Discipline): Instancia de la disciplina.
        """
        self.do_with_discipline(associate, discipline, False, lambda a, d: a.remove(d))

    def filter_like(self, lastname, state):
        query = self.database.query(True)
        if lastname is not None:
            query = query.filter(Associate.last_name.ilike(f"%{lastname}%"))
        if state is not None and state != "" and state.lower() in ["true", "false"]:
            query = query.filter(Associate.active == state)
        return query

    def filter_like_get_paginator(self, lastname, state, page):
        if re.match(r"\d+", page):
            return self.get_paginator(self.filter_like(lastname, state), int(page))
        else:
            return self.get_paginator(self.filter_like(lastname, state), 1)

    def filter_like_get_list(self, lastname, state):
        return self.get_list(self.filter_like(lastname, state))

    def filter_id_get_paginator(self, id, page):
        query = self.get_disciplines_of_associate(id)
        if re.match(r"\d+", page):
            return self.get_paginator(query, int(page))
        else:
            return self.get_paginator(query, 1)

    def get_disciplines_of_associate(self, id):
        return (
            self.discipline_m.filter_by()
            .join(Service.associates)
            .filter(Associate.id == id)
        )

    def get_paginator_except_inscribed(self, id, page):
        query = self.discipline_m.filter_by()
        my_disciplines = (
            self.discipline_m.filter_by()
            .join(Service.associates)
            .filter(Associate.id == id)
        )
        query = query.except_(my_disciplines)
        if re.match(r"\d+", page):
            return self.get_paginator(query, int(page))
        else:
            return self.get_paginator(query, 1)

    def new_associates_by_month(self):
        query = self.database.query(Associate.created_at).all()
        dict = {}

        for variable in query:
            year = variable.created_at.year
            month = variable.created_at.month
            full_date = datetime(year, month, 1)
            associate_amount = dict.get(full_date, 0)
            associate_amount = associate_amount + 1
            dict[full_date] = associate_amount

        return dict


"""Capa de negocio de alto nivel, para la tabla de Socios de la BD, donde se requiere hacer CRUDs sobre sus tuplas, y manejar autenticación y sesiones."""
class AssociateAuthManager(AssociateManager):
    def token_of(self, associate) -> str:
        return encode(id=associate.id)

    def current_token(self) -> Optional[str]:
        full_header = request.headers.get("Authorization", "")
        header_args = full_header.split(" ")

        if len(header_args) != 2:
            return None

        auth_type = header_args[0]
        auth_credentials = header_args[1]

        if auth_type != "Bearer":
            return None

        return auth_credentials

    def current_id(self) -> Optional[int]:
        token = self.current_token()

        if token is None:
            return None

        return try_decode(token).get("id")

    def current_associate(self) -> Optional[Associate]:
        associate_id = self.current_id()

        if associate_id is None:
            return None

        return self.database.get(associate_id)

    def is_current_logged_in(self) -> bool:
        associate_id = self.current_id()

        if associate_id is None:
            return False

        return self.database.exists(associate_id)

    def login_required(self, call_with_current_associate=False):
        """Verifica si el usuario está logueado.

        Args:
            call_with_current_associate (bool): Si es True, el primer argumento
                que se le pasará a la función decorada será el socio actual (el
                que llamó al endpoint).
        """

        def decorator(func):
            """Recibe una función y la retorna con la validación de login.
            Args:
                func (function): Función a validar.

            Returns:
                any: Resultado de la función.
            """

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                """Verifica si el usuario está logueado.

                Returns:
                    any: Resultado de la función.
                """
                if not self.is_current_logged_in():
                    return SimpleErrorResponse(
                        401, "El socio no tiene una sesión iniciada"
                    )

                if not call_with_current_associate:
                    return func(*args, **kwargs)

                return func(self.current_associate(), *args, **kwargs)

            return wrapper

        return decorator


auth_m = AssociateAuthManager()
