import xml.etree.ElementTree as ET
from .models import Task
from resources.models import ResourceType


class ServicesProfiles(object):

    def parse_file(self, instance):
        task_strings = ['task', 'Task']
        tree = ET.parse(instance.raw_file)
        root = tree.getroot()
        for child in root:
            for subchild in child:
                if any(string in subchild.tag for string in task_strings):
                    print(subchild.attrib)
                    self._save_task(subchild.tag, subchild.attrib, instance)
        return instance.raw_file

    def _save_task(self, tag, attrib, instance):
        task_types_map = {
                'businessRuleTask': Task.BUSINESS_RULE_TASK,
                'userTask': Task.USER_TASK,
                'scriptTask': Task.SCRIPT_TASK,
                'serviceTask': Task.SERVICE_TASK,
                'sendTask': Task.SEND_TASK,
                'receiveTask': Task.RECEIVE_TASK,
                'task': Task.TASK,
                'manualTask': Task.MANUAL_TASK
                }

        task_type = task_types_map[tag.split('}', 1)[1]]
        label = attrib['name']
        Task.objects.create(label=label, task_type=task_type, process=instance)

    def recommend(self, instance):
        priori_resource_types = {
            'no_resource': 0
        }
        total_docs = 0
        for resource in ResourceType.objects.all():
            task_count = resource.task_set.all().count()
            total_docs = total_docs + task_count
            priori_resource_types[resource.name] = task_count

        for row in priori_resource_types:
            priori_resource_types[row] = priori_resource_types[row] / task_count

        # limpar dados? artigos, minusculas etc
        # calcular likelihood
