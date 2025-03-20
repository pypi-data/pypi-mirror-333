from esu.base import BaseAPI, Field, FieldList


class DomainAlias(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        alias (str): Наименование домена

    .. warning:: Объект доступен только для чтения и не может быть создан,
                 изменен или удален.
    """
    class Meta:
        id = Field()
        alias = Field()


class Domain(BaseAPI):
    """
    Args:
        id (str): Идентификатор наименования домена
        name (str): Имя домена
        aliases (list): Список объектов класса :class:`esu.DomainAlias`.
                        Список наименований, которые относятся к домену

    .. warning:: Объект доступен только для чтения и не может быть создан,
                 изменен или удален.
    """
    class Meta:
        id = Field()
        aliases = FieldList(DomainAlias)
        name = Field()


class User(BaseAPI):
    """
    Args:
        id (str): Идентификатор пользователя
        domain (object): Объект класса :class:`esu.Domain`.
                         Объект который указывает на принадлежность
                         пользователя к определённому домену
        login (str): Логин пользователя
        username (str): Имя пользователя
        email (str): Почта
        phone (str): Телефон

    .. warning:: Объект доступен только для чтения и не может быть создан,
                 изменен или удален.
    """
    class Meta:
        id = Field()
        domain = Field(Domain)
        login = Field()
        username = Field(allow_none=True)
        email = Field(allow_none=True)
        phone = Field(allow_none=True)

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект пользователя по его ID или
        id='me' для получения объекта к которому привязан токен

        Args:
            id (str): Идентификатор клиента
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект клиента :class:`esu.User`
        """
        user = cls(token=token, id=id)
        user._get_object('v1/account', user.id)
        return user
