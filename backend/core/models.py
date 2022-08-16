from django.db import models


class Specialisation(models.Model):
    PY = "Python"
    PHP = "PHP"
    GO = "Go"
    BIT = "Bitrix"
    JA = "Java"
    TEST = "Тестирование"
    AN = "Аналитика"
    DE = "Design"
    NAMES = [
        (PY, "Python"),
        (PHP, "PHP"),
        (GO, "Go"),
        (BIT, "Bitrix"),
        (JA, "Java"),
        (TEST, "Тестирование"),
        (AN, "Аналитика"),
        (DE, "Design"),
    ]
    name = models.CharField("Название специализации", max_length=64, choices=NAMES)
    priority = models.IntegerField("Приоритет эксперта")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Специализация"
        verbose_name_plural = "Специализации"
        constraints = (
            models.UniqueConstraint(
                fields=("name", "priority"),
                name="unique_specialisation",
            ),
        )


class Slot(models.Model):
    MON = "пн"
    TUE = "вт"
    WED = "ср"
    THU = "чт"
    FRI = "пт"
    SAT = "сб"
    SUN = "вс"
    DAYS = [
        (MON, "пн"),
        (TUE, "вт"),
        (WED, "ср"),
        (THU, "чт"),
        (FRI, "пт"),
        (SAT, "сб"),
        (SUN, "вс"),
    ]
    day = models.CharField("День недели", max_length=16, choices=DAYS)
    hour = models.IntegerField("Час слота")

    def __str__(self):
        if self.hour <= 9:
            return f"{self.day} - 0{self.hour}:00"
        return f"{self.day} - {self.hour}:00"

    class Meta:
        verbose_name = "Слот"
        verbose_name_plural = "Слоты"
        constraints = (
            models.UniqueConstraint(
                fields=("day", "hour"),
                name="unique_slot",
            ),
        )


class User(models.Model):
    EXP = "EXPERT"
    HR = "HR"
    ADM = "ADMIN"
    POSITIONS = [
        (EXP, "Эксперт"),
        (HR, "HR-специалист"),
        (ADM, "Админ"),
    ]
    name = models.CharField("Фамилия и имя", max_length=64)
    tg_id = models.BigIntegerField("ID пользователя", unique=True)
    specialisation = models.OneToOneField(
        Specialisation,
        blank=True,
        null=True,
        related_name="users",
        on_delete=models.CASCADE,
    )
    slots = models.ManyToManyField(Slot, blank=True, related_name="users")
    position = models.CharField("Позиция", max_length=32, choices=POSITIONS)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Interview(models.Model):
    slot = models.ForeignKey(Slot, related_name="interviews", on_delete=models.CASCADE)
    date = models.DateField("Дата интервью")
    expert = models.ForeignKey(
        User,
        related_name="expert_interviews",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    hr = models.ForeignKey(
        User,
        related_name="hr_interviews",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    message = models.TextField("Сообщение рекрутера с дополнительной информацией")
    file = models.FileField(
        verbose_name="Файл резюме", upload_to="cvs/", blank=True, null=True
    )

    def __str__(self):
        return f"{self.slot} - {self.date}"

    class Meta:
        verbose_name = "Интервью"
        verbose_name_plural = "Интервью"


class Solution(models.Model):
    ACC = "Принять"
    OTH = "Предложить другое время"
    SKIP = "Пропустить"
    REF = "Отказаться"
    SKIP_SEC = "Пропустить второй раз"
    REF_CANDIDATE = "Отказаться от кандидата"
    TYPES = [
        (ACC, "Принять"),
        (OTH, "Предложить другое время"),
        (SKIP, "Пропустить"),
        (REF, "Отказаться"),
        (SKIP_SEC, "Пропустить второй раз"),
        (REF_CANDIDATE, "Отказаться от кандидата"),
    ]
    type = models.CharField("Тип решения", max_length=32, choices=TYPES)
    date = models.DateField("Дата решения")
    comment = models.CharField("Комментарий", max_length=128, blank=True)
    expert = models.ForeignKey(
        User,
        related_name="solutions",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        if self.comment:
            return f"{self.type} - {self.date} - {self.comment}"
        return f"{self.type} - {self.date}"

    class Meta:
        verbose_name = "Решение"
        verbose_name_plural = "Решения"
