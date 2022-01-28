import operator
from itertools import groupby


from openatlas.models.entity import Entity


def export_csv_for_network_analysis(entities: list[Entity]):

    entities = sorted(entities,key=operator.attrgetter('cidoc_class'), reverse=False)
    groups = []
    uniquekeys = []
    for type, entities in groupby(entities, key=lambda entity: entity.cidoc_class):
        groups.append(list(entities))  # Store group iterator as a list
        uniquekeys.append(type)
    print(uniquekeys)
    print('===============================')
    print(groups)


