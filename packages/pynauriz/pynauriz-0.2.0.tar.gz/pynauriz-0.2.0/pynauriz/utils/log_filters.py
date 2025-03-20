import logging


class RequestPushUserFilter(logging.Filter):
    """
    Фильтр для логирования информации о пользователе, отправившем запрос.
    Этот фильтр добавляет информацию о пользователе в запись лога, если она доступна.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        if hasattr(record, 'request'):
            if hasattr(record.request, 'user'):
                record.user = f'{record.request.user}#{record.request.user.pk}'
            else:
                record.user = '?'
        else:
            record.user = '-'
        return True


class RequestUniqreqidFilter(logging.Filter):
    """
    Фильтр для добавления уникального идентификатора запроса в запись лога.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        if hasattr(record, 'request'):
            record._uniqreqid = getattr(record.request, '_uniqreqid', '?')
        else:
            record._uniqreqid = '-'

        return True
