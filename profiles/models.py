from django.db import models


class Organization(models.Model):
    name = models.CharField(verbose_name='Name', max_length=30,)

    def __unicode__(self):
        return self.name


class Process(models.Model):
    name = models.CharField(verbose_name='Name', max_length=30,)
    organization = models.ForeignKey(
        Organization,
        verbose_name='Organization',
        blank=True,
        null=True
    )
    upload_date = models.DateTimeField(
        verbose_name='Upload Date',
        auto_now_add=True
    )
    raw_file = models.FileField(upload_to='uploads/')
    # structure = models.JSONField(verbose_name='JSON Representation')

    def __unicode__(self):
        return self.name


class Task(models.Model):

    USER_TASK = 'user'
    SERVICE_TASK = 'service'
    RECEIVE_TASK = 'receive'
    SEND_TASK = 'send'
    BUSINESS_RULE_TASK = 'business_rule'
    SCRIPT_TASK = 'script'
    TASK = 'task'
    MANUAL_TASK = 'manual'

    TASK_TYPES = (
        (USER_TASK, 'User Task'),
        (SERVICE_TASK, 'Service Task'),
        (RECEIVE_TASK, 'Receive Task'),
        (SEND_TASK, 'Send Task'),
        (BUSINESS_RULE_TASK, 'Business Rule Task'),
        (SCRIPT_TASK, 'Script Task'),
        (TASK, 'Task'),
    )

    label = models.CharField(verbose_name='Label', max_length=256)
    task_type = models.CharField(verbose_name='Type', choices=TASK_TYPES, max_length=20,)
    process = models.ForeignKey(Process, verbose_name='Task', on_delete=models.CASCADE)
