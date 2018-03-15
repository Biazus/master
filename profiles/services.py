import unidecode
import xml.etree.ElementTree as ET
from nltk.stem import RSLPStemmer
from nltk.corpus import stopwords
from .models import Task
from resources.models import ResourceType


class ServicesProfiles(object):

    stopwords = set(stopwords.words('portuguese'))
    porter = RSLPStemmer()

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

        all_labels = {'undefined': []}  # dicionario com as labels de cada task por resource type
        for process in instance.organization.process_set.all():
            for task in process.task_set.all():
                cleaned_label = self.clean_label(task.label)
                application_name = task.application_type.name if task.application_type else 'undefined'
                all_labels.setdefault(application_name, [])
                all_labels[application_name] = all_labels[application_name] + cleaned_label

        set_labels = {}
        for i in all_labels:
            # cria set a partir das palavras de cada resource type
            set_labels.setdefault(i, set())
            set_labels[i] = set(all_labels[i])

        print(all_labels)
        print(set_labels)
        # transformar lista em set
        # calcular likelihood

    def clean_label(self, label):
        '''
            Returns a list of the words that compose the provided label
        '''
        list_of_words = []
        for word in label.split():
            stemmed_word = self.porter.stem(word.lower())
            new_word = unidecode.unidecode(stemmed_word).replace('-', '')
            # TODO alterar labels com numeros (ex. 1o, 2o)
            if new_word not in self.stopwords:
                list_of_words.append(new_word)
        return list_of_words
