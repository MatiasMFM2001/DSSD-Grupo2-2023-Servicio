from src.core.database.board import Producer
from src.core.business.crud_manager import CRUDManager


class ProducerManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase MaterialManager."""
        super().__init__(Producer)
