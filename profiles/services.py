import math
import unidecode
import copy
import xml.etree.ElementTree as ET
from nltk.stem import RSLPStemmer
from nltk.corpus import stopwords

from .models import Task

from django.db.models import Q
from django.core.paginator import Paginator
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
        """
            Save the tasks as part of the instance
        """
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

    def _get_probability_by_resource(self, training):
        """
        Args:
            training (list): Lista de treinamento

        Returns:
            dict: dicionario que ira conter a probabilidade a priori de uma palavra estar contida em um tipo
            de recurso
        """
        priori_prob_by_resource_types = {}
        for resource in ResourceType.objects.all():
            resource_task_count = resource.task_set.filter(id__in=[i.id for i in training]).count()
            priori_prob_by_resource_types[resource.name] = resource_task_count

        task_count = len(training)
        tasks_without_resource = len([task for task in training if task.application_type is None])
        for row in priori_prob_by_resource_types:
            priori_prob_by_resource_types[row] = priori_prob_by_resource_types[row] / task_count
        priori_prob_by_resource_types['undefined'] = tasks_without_resource/task_count
        return priori_prob_by_resource_types

    def _get_all_words_from_each_resource(self, training):
        """
        Returns:
            dict: dicionario contendo, para cada um dos tipos de recurso, as palavras contidas dentro das
            tarefas do tipo de recurso
        """
        all_words_from_a_resource = {'undefined': []}
        for task in training:
            cleaned_label = self._clean_label(task.label)
            application_name = task.application_type.name if task.application_type else 'undefined'
            all_words_from_a_resource.setdefault(application_name, [])
            all_words_from_a_resource[application_name] = all_words_from_a_resource[application_name] + cleaned_label
        return all_words_from_a_resource

    def _get_word_counter_by_resource_type(self, all_words_from_a_resource):
        """
        Returns:
            dict: dicionario com numero de vezes que uma dada palavra aparece para um recurso especifico
        """
        word_counter = {}
        for resource in all_words_from_a_resource:
            word_counter[resource] = {}
            for word in all_words_from_a_resource[resource]:
                word_counter[resource][word] = all_words_from_a_resource[resource].count(word)
        return word_counter

    def _calculate_likelihood(self, prob_condit, set_of_unique_words_all_docs, number_unique_words_all_docs,
            all_words_from_a_resource):
        """
            Calcula probabilidade condicional / likelihood de uma palavra para um tipo de recurso especifico
        """
        for resource in prob_condit:
            for word in set_of_unique_words_all_docs:
                p_word = prob_condit[resource][word]+1 if word in prob_condit[resource] else 1  # laplace smoothing
                number_of_all_words_in_category = len(all_words_from_a_resource[resource])
                prob_condit[resource][word] = p_word/(number_of_all_words_in_category+number_unique_words_all_docs)
        return prob_condit

    def classify(self, test, training):
        """
            Responsavel pelo treinamento e teste
        """

        priori_prob_by_resource_types = self._get_probability_by_resource(training)
        all_words_from_a_resource = self._get_all_words_from_each_resource(training)

        set_of_unique_words_all_docs = set()
        for i in all_words_from_a_resource:
            set_of_unique_words_all_docs.update(all_words_from_a_resource[i])

        word_counter = self._get_word_counter_by_resource_type(all_words_from_a_resource)

        prob_condit = copy.deepcopy(word_counter)
        number_unique_words_all_docs = len(set_of_unique_words_all_docs)

        prob_condit = self._calculate_likelihood(
                prob_condit,
                set_of_unique_words_all_docs,
                number_unique_words_all_docs,
                all_words_from_a_resource
        )
        self._classify_test_set(test, prob_condit, set_of_unique_words_all_docs, priori_prob_by_resource_types)

    def _classify_test_set(self, test, prob_condit, unique_words, priori):
        """
            Responsavel por, dado um conjunto de teste, classificar os elementos
        """
        probability = {}
        for task in test:
            probability[task.label] = {}
            for app_class in prob_condit:
                label = self._clean_label(task.label)
                probability[task.label][app_class] = priori[app_class]

                # testa se palavras existem no vocabulario. se nenhuma existe coloca 0 de prob
                existent_words = [i for i in label if i in unique_words]
                if len(existent_words) == 0:
                    probability[task.label][app_class] = 0

                else:
                    for word in label:
                        if word in prob_condit[app_class]:
                            probability[task.label][app_class] = probability[task.label][app_class] * prob_condit[app_class][word]
                # print('{} em {}: {}'.format(task.label, app_class, probability[task.label][app_class]))

        for label in probability:
            max_val = 0
            class_value = ''
            for app in probability[label]:
                # TODO aqui talvez necessario colocar um threshold para nao pegar qlqr label (?) . ver se isso
                # melhora de alguma forma / talvez nao
                if probability[label][app] > max_val:
                    max_val = probability[label][app]
                    class_value = app
            if class_value != '' and class_value != 'undefined':
                tasks_to_update = [task for task in test if task.label == label]
                # cleanup para checar se task é um servico ou manual: se for, nao classifica
                tasks_to_update = [task for task in tasks_to_update if task.task_type != 'service' and
                        task.task_type != 'manual']
                for task in tasks_to_update:
                    task.recommended_app = ResourceType.objects.get(name=class_value)
                    task.save()
            # print('{}: {}'.format(label, class_value))

    def _clean_label(self, label):
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

    def cross_validation(self, organization_pk):
        all_tasks = Task.objects.filter(process__organization__id=organization_pk).order_by('?')
        all_tasks.update(recommended_app=None)
        p = Paginator(all_tasks, math.ceil(len(all_tasks)/10))
        matches = 0
        mismatches = 0
        for i in range(10):
            page = p.page(i+1)
            test = page.object_list
            training = all_tasks.filter(~Q(id__in=[task.id for task in test]))
            self.classify(test, training)
            for t in test:
                print('%-60s%-25s%-25s' % (t.label, t.application_type, t.recommended_app))
                if t.recommended_app == t.application_type:
                    matches = matches + 1
                else:
                    mismatches = mismatches + 1
        accuracy = matches/(matches+mismatches)
        # print('Matches: {}'.format(matches))
        # print('Mismatches: {}'.format(mismatches))
        # print('Accuracy: {}'.format(accuracy))
        return accuracy
