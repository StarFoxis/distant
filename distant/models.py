import datetime
from django.db import models

class assignment_dates(models.Model):
    date = models.DateField('Дата',  default=datetime.date.today)
    
    def __str__(self):
        return self.date.strftime('%d-%m-%Y')

    class Meta:
        ordering = ["date"]
        verbose_name = 'Дата'
        verbose_name_plural = 'Даты'


class homework(models.Model):
    num_task = models.PositiveSmallIntegerField('Номер задания')
    text_task = models.TextField('Текст задания')
    answer_task = models.TextField('Ответ')
    date = models.ForeignKey(assignment_dates, on_delete=models.SET_NULL, null=True, verbose_name='Дата задания')

    def __str__(self):
        return 'Задание '+str(self.num_task)

    class Meta:
        ordering = ["date", 'num_task']
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'