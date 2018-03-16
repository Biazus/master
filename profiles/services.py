import unidecode
import copy
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

        # calculate priori probability
        priori_prob_by_resource_types = {}
        for resource in ResourceType.objects.all():
            resource_task_count = resource.task_set.filter(process__organization=instance.organization).count()
            priori_prob_by_resource_types[resource.name] = resource_task_count

        task_count = Task.objects.filter(process__organization=instance.organization).count()
        tasks_without_resource = Task.objects.filter(process__organization=instance.organization, application_type=None).count()
        for row in priori_prob_by_resource_types:
            priori_prob_by_resource_types[row] = priori_prob_by_resource_types[row] / task_count
        priori_prob_by_resource_types['no_resources'] = tasks_without_resource/task_count


        all_words_from_a_resource = {'undefined': []}
        for process in instance.organization.process_set.all().exclude(id=instance.id):
            for task in process.task_set.all():
                cleaned_label = self.clean_label(task.label)
                application_name = task.application_type.name if task.application_type else 'undefined'
                all_words_from_a_resource.setdefault(application_name, [])
                all_words_from_a_resource[application_name] = all_words_from_a_resource[application_name] + cleaned_label

        set_of_unique_words_all_docs = set()
        for i in all_words_from_a_resource:
            # cria set a partir das palavras de cada resource type
            set_of_unique_words_all_docs.update(all_words_from_a_resource[i])

        # adiciona as palavras do processo passado como instancia para o set
        for task in instance.task_set.all():
            set_of_unique_words_all_docs.update(self.clean_label(task.label))

        # calcular likelihood
        word_counter = {}
        for resource in all_words_from_a_resource:
            word_counter[resource] = {}
            for word in all_words_from_a_resource[resource]:
                word_counter[resource][word] = all_words_from_a_resource[resource].count(word)

        prob_condit = copy.deepcopy(word_counter)
        for resource in prob_condit:
            for word in set_of_unique_words_all_docs:
                p_word = prob_condit[resource][word]+1 if word in prob_condit[resource] else 1
                number_of_all_words_in_category = len(all_words_from_a_resource[resource])
                number_unique_words_all_docs = len(set_of_unique_words_all_docs)
                prob_condit[resource][word] = p_word/(number_of_all_words_in_category+number_unique_words_all_docs)


        print(prob_condit)

        # CALCULATE PROB

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
