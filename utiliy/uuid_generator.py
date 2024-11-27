from generics.id_generator import IDGenerator
from uuid import UUID, uuid4


class UUIDGenerator(IDGenerator[UUID]):
    @staticmethod
    def get_new_id() -> UUID:
        """
        Function to generate new UUID
        :return: UUID
        """
        return uuid4()
