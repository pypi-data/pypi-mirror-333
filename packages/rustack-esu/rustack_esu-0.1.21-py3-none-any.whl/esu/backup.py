from esu.base import BaseAPI, Field, FieldList, ObjectAlreadyHasId, \
    ObjectHasNoId


class RestorePoint(BaseAPI):
    """
   Args:
       id (str): Идентификатор точки восстановления
       backup_type (str): Тип точки восстановления
       backup_size (int): Размер точки восстановления (bytes)
       vm (object): Сервер для которого создана точка :class:`esu.Vm`
   """
    class Meta:
        id = Field()
        backup_type = Field()
        backup_size = Field()
        vm = Field('esu.Vm')


class VmInBackup(BaseAPI):
    """
   Args:
       id (str): Идентификатор сервера в задаче резервного копирования
       name (str): Имя сервера в задаче резервного копирования
    """
    class Meta:
        id = Field()
        name = Field()


class Backup(BaseAPI):
    """
   Args:
       id (str): Идентификатор задачи резервного копирования
       name (str): Имя задачи резервного копирования
       size (int): Суммарный размер точек восстановления задачи
                   резервного копирования (bytes)
       vdc (object): Объект ВЦОДа :class:`esu.Vdc`
       retain_cycles (int): Глубина хранения задачи резервного копирования
       time (str): Время выполнения задачи по расписанию в UTC
       schedule_type (str): Тип расписания (every_day, days_week, days_month,
                            last_day_month)
       schedule_days (list): Дни выполнения задачи по расписанию [1,2,3]
       vms (list): Список серверов для которых создана задача

   .. note:: Поля ``name``, ``vms``, ``retain_cycles``, ``schedule_days``,
             ``time`` могут быть изменены для существующего объекта.
   """
    class Meta:
        id = Field()
        name = Field()
        vdc = Field('esu.Vdc')
        vms = FieldList(VmInBackup)
        retain_cycles = Field()
        schedule_type = Field()
        schedule_days = Field()
        time = Field()
        size = Field()

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект задачи резервного копирования по ее ID

        Args:
            id (str): Идентификатор задачи резервного копирования
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект диска :class:`esu.Disk`
        """
        job = cls(token=token, id=id)
        job._get_object('v1/backup', job.id)
        return job

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

    def save(self):
        """
        Сохранить изменения

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._commit()

    def _commit(self):
        vms = [i.id for i in self.vms]

        job = {
            'name': self.name,
            'vdc': self.vdc.id,
            'schedule_type': self.schedule_type,
            'schedule_days': self.schedule_days,
            'time': self.time,
            'retain_cycles': self.retain_cycles,
            'vms': vms
        }
        self._commit_object('v1/backup', **job)

    def start_immediately(self):
        """
        Запустить выполнение задачи - создание точек восстановления
        """
        self._call('POST', 'v1/backup/{}/start_immediately'.format(self.id))

    def get_restore_points(self):
        """
        Получить список точек восстановления в задаче резервного копирования.

        Returns:
            list: Список объектов :class:`esu.RestorePoint`
        """
        if self.id is None:
            raise ObjectHasNoId

        return self._get_list(
            'v1/backup/{}/restore_points?'
            'sort=-ctime'.format(self.id), RestorePoint)

    def restore(self, restore_point, power_on=True, quick_restore=False):
        """
        Восстановить сервер из точки восстановления

        Args:
            vm (object): :class:`esu.Vm`, сервер, который необходимо
                восстановить
            restore_point (object): :class:`esu.RestorePoint`, точка
                восстановления из которой необходимо восстановить сервер
            power_on (bool) True если после восстановления сервер должен
                быть включен
            quick_restore (bool) True если требуется быстрое восстановление
                (не рекомендуется)

         .. warning:: в сегменте KVM восстановление происходит в новый сервер,
                в сегменте VMware восстановление происходит в текущий сервер
        """
        restore = {
            "power_on": power_on,
            "quick_restore": quick_restore,
            "vm": restore_point.vm.id,
            "restore_point": restore_point.id
        }
        self._call('POST', 'v1/backup/{}/restore'.format(self.id), **restore)

    def get_backup_log(self):
        """
        Получить лог создания точек восстановления из задачи

        Returns:
            dict: Отчёт создания точек восстановления
        """

        log = self._call(
            'GET', 'v1/backup/log?backup={}'
            '&sort=-ctime'.format(self.id))
        return log

    def get_restore_log(self, vm):
        """
        Получить лог восстановления сервера из задачи

        Returns:
            dict: Отчёт восстановления сервера
        """

        log = self._call('GET', 'v1/backup/log?vm={}'
                         '&sort=-ctime'.format(vm.id))
        return log

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/backup', self.id)
        self.id = None
