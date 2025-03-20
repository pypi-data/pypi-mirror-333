from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId


class PublicKey(BaseAPI):
    """
    Args:
        id (str): Идентификатор публичного ключа
        name (str): Имя публичного ключа
        public_key (str): Публичный ключ
    """
    class Meta:
        id = Field()
        name = Field()
        public_key = Field()

    @classmethod
    def get_object(cls, id, user, token=None):
        """
        Получить объект публичного ключа по его ID

        Args:
            id (str): Идентификатор публичного ключа
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект публичного ключа :class:`esu.PublicKey`
        """
        key = cls(token=token, id=id)
        key._get_object('v1/account/{}/key'.format(user.id), key.id)
        return key

    def create(self, user):
        """
        Создать публичный ключ.

        Returns:
            object: Объект :class:`esu.Key`
        """
        if self.id is not None:
            raise ObjectAlreadyHasId

        self._commit(user=user)

    def _commit(self, user):
        key = {'name': self.name, 'public_key': self.public_key}
        self._commit_object('v1/account/{}/key'.format(user.id), **key)

    def destroy(self, user):
        """
        Удалить публичный ключ.
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/account/{}/key'.format(user.id), self.id)
        self.id = None
