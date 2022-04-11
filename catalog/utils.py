from django.core.files import File

from .models import CATEGORY_CHOICES, Project


def validate_get_request_categories(categories):
    # validate categories from request
    valid_choices = [i for k in CATEGORY_CHOICES for i in k]
    for cat in categories:
        if cat not in valid_choices:
            return False
    return categories


def validate_get_request_counts(counts):
    # validate number of selected categories from request
    try:
        counts = [int(i) for i in counts]
    except ValueError:
        return False
    return counts


def generate_file(project):
    with open(f"catalog/files/{project.slug}.txt", "w") as f:
        f.write(generator(project.slug))
        project = Project.objects.get(slug=project.slug)
        project.file.save(f'{project.slug}.txt', File(f))
    # SaveFileProject(f"catalog/files/{slug}.txt", slug)


# #TODO why class
# class SaveFileProject:
#     def __init__(self, filepath, slug):
#         self.filepath = filepath
#         self.project = Project.objects.get(slug=slug)
#         with open(self.filepath) as f:
#             self.project.file.save(f'{slug}.txt', File(f))


def generator(project):
    obj = GeneratorFile(project)
    obj.prepare_data()
    wire = obj.generate_cable_part()
    components = obj.generate_components_part()
    connects = obj.generate_connection_part()
    return wire + components + connects


class GeneratorFile:
    def __init__(self, project):
        self.project = project.prefetch_related('models')
        self.selected_model_list = []
        self.scheme_object_list = []
        self.cable_object_list = []

    def prepare_data(self):
        for selected_model in self.project[0].models.all():
            self.selected_model_list.append(selected_model)
            for scheme in selected_model.schemes.all():
                self.scheme_object_list.append(scheme)
                self.cable_object_list.append(scheme.cable)

    def generate_cable_part(self):
        result = ' ! Wire and cable spools\n\n'
        for cable in self.cable_object_list:
            result += f'NEW WIRE_SPOOL {cable.code}\n' \
                      f'PARAMETER MIN_BEND_RADIUS {cable.min_bend_radius}\n' \
                      f'PARAMETER THICKNESS {cable.thickness}\nPARAMETER UNITS MM\n' \
                      f'PARAMETER COLOR {cable.color}\n\n'
        return result

    def generate_components_part(self):
        result = '! Components and connectors\n\n'
        for selected_model in self.selected_model_list:
            result += f'NEW CONNECTOR {selected_model.symbol}\n' \
                      f'PARAMETER MODEL_NAME {selected_model.model.name}\n' \
                      f'PARAMETER NUM_OF_PINS {selected_model.model.ports.count()}\n'
            for k, port in enumerate(selected_model.model.ports.all()):
                result += f'PIN {port.name}\n' \
                          f'PARAMETER ENTRY_PORT {port.name}\n' \
                          f'PARAMETER GROUPING ROUND\nPARAMETER INTERNAL_LEN 50\n'
            result += '\n'
        return result

    def generate_connection_part(self):
        result = '! Rails\n\n! Wires and cables\n\n'
        for i, item in enumerate(self.scheme_object_list):
            result += f'NEW WIRE {item.cable_symbol} {self.cable_object_list[i].code}\n' \
                      f'ATTACH {item.model.symbol} {item.port} {item.connect} E\n\n'
        return result
