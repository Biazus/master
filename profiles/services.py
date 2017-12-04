import xml.etree.ElementTree as ET
from .models import Task


class ServicesProfiles(object):

    def parse_file(self, raw_file):
        # import pdb;
        # pdb.set_trace()
        tree = ET.parse(raw_file)
        root = tree.getroot()
        for child in root:
            for subchild in child:
                if "task" in subchild.tag:
                    self._save_task(subchild.tag, subchild.attrib)
        return raw_file

    def _save_task(self, tag, attrib):
        label = 'Teste'
        task_type = Task.USER_TASK
        Task.objects.create(label=label, task_type=task_type)
