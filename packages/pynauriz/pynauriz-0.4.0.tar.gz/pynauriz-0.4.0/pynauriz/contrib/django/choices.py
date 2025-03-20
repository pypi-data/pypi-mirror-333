class MaxLengthMixin:
    """
    Миксин для вычисления максимальной длины значений в перечислениях (Choices).

    Используется для задания `max_length` в моделях Django.
    """

    @classmethod
    def get_max_length(cls) -> int:
        """
        Возвращает максимальную длину значений, определенных в Choices.

        :return: Максимальная длина значений.
        """
        return max(len(choice.value) for choice in cls)
