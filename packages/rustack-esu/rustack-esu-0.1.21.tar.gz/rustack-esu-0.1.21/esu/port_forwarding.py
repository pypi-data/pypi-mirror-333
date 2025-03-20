from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId


class PortForwarding(BaseAPI):
    """
    Args:
        id (str): Идентификатор перенаправления портов
        floating (object): Объект класса :class:`esu.Port`. Порт на котором
                           будет создано перенаправление
        token (str): Токен для доступа к API. Если не передан, будет
            использована переменная окружения **ESU_API_TOKEN**

    .. note:: Управление перенаправлением портов создаваемом на порте возможно
              только в ресурсном пуле под управлением Openstack.
              Поле ``floating`` необходимо для создания.
    """
    class Meta:
        id = Field()
        name = Field()
        vdc = Field('esu.Vdc')
        floating = Field('esu.Port')

    @classmethod
    def get_object(cls, port_forwarding_id, token=None):
        """
        Получить объект перенаправления портов по его ID

        Args:
            id (str): Идентификатор перенаправления портов
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект маршрута на роутере
            :class:`esu.RouterRoute`
        """
        port_forwarding = cls(token=token, id=port_forwarding_id)
        port_forwarding._get_object('v1/port_forwarding', port_forwarding.id)
        return port_forwarding

    def create(self):
        """
        Создать объект

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует
        """
        if self.id is not None:
            raise ObjectAlreadyHasId

        self._commit()

    def _commit(self):
        self._commit_object('v1/port_forwarding', floating=self.floating.id)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/port_forwarding', self.id)
        self.id = None
