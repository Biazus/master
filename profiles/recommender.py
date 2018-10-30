import math
import sys

from .models import Process, Task, Organization
from resources.models import Resource


class Recommend(object):

    def create_organization_profile(self, process_instance):
        organization = process_instance.organization
        processes = Process.objects.filter(organization=organization)
        resource_count = 0
        point = [0,0,0,0,0]
        for process in processes:
            for task in process.task_set.all():
                if task.resource:
                    resource_count += 1
                    collaborative = 1 if task.resource.collaborative else 0
                    open_source = 1 if task.resource.open_source else 0
                    available_web = 1 if task.resource.available_web else 0
                    multiplatform = 1 if task.resource.multiplatform else 0
                    developed_inside = 1 if task.resource.developed_inside else 0
                    point[0] += collaborative
                    point[1] += open_source
                    point[2] += available_web
                    point[3] += multiplatform
                    point[4] += developed_inside
        point = [
            point[0]/resource_count,
            point[1]/resource_count,
            point[2]/resource_count,
            point[3]/resource_count,
            point[4]/resource_count,
        ]
        return point

    def get_most_similar_resource(self, org_profile, process_instance):
        for task in process_instance.task_set.all():
            if task.classified_type:
                candidate_resources = Resource.objects.filter(resource_type=task.classified_type)
                resource_to_recommend = None
                smaller_distance = sys.maxsize
                for resource in candidate_resources:
                    resource_profile = [0,0,0,0,0]
                    resource_profile[0] = 1 if resource.collaborative else 0
                    resource_profile[1] = 1 if resource.open_source else 0
                    resource_profile[2] = 1 if resource.available_web else 0
                    resource_profile[3] = 1 if resource.multiplatform else 0
                    resource_profile[4] = 1 if resource.developed_inside else 0
                    new_distance = self.calculate_euclidean_distance(org_profile, resource_profile)
                    if new_distance < smaller_distance:
                        smaller_distance = new_distance
                        resource_to_recommend = resource
                task.recommended_resource = resource_to_recommend
                task.save()


    def calculate_euclidean_distance(self, org_profile, resource_profile):
        final_value = 0
        for index, value in enumerate(org_profile):
            partial_value = resource_profile[index] - org_profile[index]
            final_value += math.pow(partial_value, 2)
        return math.sqrt(final_value)
