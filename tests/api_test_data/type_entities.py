test_type_entities = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': 'http://local.host/entity/104',
        'type': 'Feature',
        'crmClass': 'crm:E18 Physical Thing',
        'systemClass': 'place',
        'properties': {'title': 'Shire'},
        'description': [
            {'value': 'The Shire was the homeland of the hobbits.'}],
        'when': {
            'timespans': [
                {'start': {'earliest': '2018-01-31', 'latest': '2018-03-01'},
                 'end': {'earliest': '2019-01-31', 'latest': '2019-03-01'}}]},
        'types': [
            {'identifier': 'http://local.host/api/0.2/entity/65',
             'label': 'Place', 'description': None, 'hierarchy': '',
             'value': None, 'unit': None},
            {'identifier': 'http://local.host/api/0.2/entity/102',
             'label': 'Height', 'description': None,
             'hierarchy': 'Dimensions', 'value': 23.0,
             'unit': 'centimeter'}],
        'relations': [
            {'label': 'Height',
             'relationTo': 'http://local.host/api/0.2/entity/102',
             'relationType': 'crm:P2 has type',
             'relationSystemClass': 'type',
             'relationDescription': '23.0',
             'type': None,
             'when': {
                 'timespans': [{
                     'start': {
                         'earliest': 'None',
                         'latest': 'None'},
                     'end': {
                         'earliest': 'None',
                         'latest': 'None'}}]}},
            {'label': 'Home of Baggins',
             'relationTo': 'http://local.host/api/0.2/entity/108',
             'relationType': 'crm:P46 is composed of',
             'relationSystemClass': 'feature',
             'relationDescription': None,
             'type': None,
             'when': {
                 'timespans': [
                     {
                         'start': {
                             'earliest': 'None',
                             'latest': 'None'},
                         'end': {
                             'earliest': 'None',
                             'latest': 'None'}}]}},
            {'label': 'Location of Shire',
             'relationTo': 'http://local.host/api/0.2/entity/105',
             'relationType': 'crm:P53 has former or current location',
             'relationSystemClass': 'object_location',
             'relationDescription': None,
             'type': None,
             'when': {
                 'timespans': [
                     {
                         'start': {
                             'earliest': 'None',
                             'latest': 'None'},
                         'end': {
                             'earliest': 'None',
                             'latest': 'None'}}]}},
            {'label': 'Place',
             'relationTo': 'http://local.host/api/0.2/entity/65',
             'relationType': 'crm:P2 has type',
             'relationSystemClass': 'type',
             'relationDescription': None,
             'type': None,
             'when': {
                 'timespans': [{
                     'start': {
                         'earliest': 'None',
                         'latest': 'None'},
                     'end': {
                         'earliest': 'None',
                         'latest': 'None'}}]}},
            {'label': 'Sûza',
             'relationTo': 'http://local.host/api/0.2/entity/106',
             'relationType': 'crm:P1 is identified by',
             'relationSystemClass': 'appellation',
             'relationDescription': None,
             'type': None,
             'when': {
                 'timespans': [{
                     'start': {
                         'earliest': 'None',
                         'latest': 'None'},
                     'end': {
                         'earliest': 'None',
                         'latest': 'None'}}]}},
            {'label': 'GeoNames',
             'relationTo': 'http://local.host/api/0.2/entity/1',
             'relationType': 'crm:P67i is referred to by',
             'relationSystemClass': 'reference_system',
             'relationDescription': '2761369',
             'type': 'closeMatch',
             'when': {
                 'timespans': [{
                     'start': {
                         'earliest': 'None',
                         'latest': 'None'},
                     'end': {
                         'earliest': 'None',
                         'latest': 'None'}}]}},
            {
                'label': 'https://lotr.fandom.com/',
                'relationTo': 'http://local.host/api/0.2/entity/107',
                'relationType': 'crm:P67i is referred to by',
                'relationSystemClass': 'external_reference',
                'relationDescription': 'Fandom Wiki of lord of the rings',
                'type': None,
                'when': {
                    'timespans': [
                        {
                            'start': {
                                'earliest': 'None',
                                'latest': 'None'},
                            'end': {
                                'earliest': 'None',
                                'latest': 'None'}}]}},
            {
                'label': 'Picture with a License',
                'relationTo': 'http://local.host/api/0.2/entity/112',
                'relationType': 'crm:P67i is referred to by',
                'relationSystemClass': 'file',
                'relationDescription': None,
                'type': None,
                'when': {
                    'timespans': [
                        {
                            'start': {
                                'earliest': 'None',
                                'latest': 'None'},
                            'end': {
                                'earliest': 'None',
                                'latest': 'None'}}]}}],
        'names': [{'alias': 'Sûza'}],
        'links': [{'type': 'closeMatch',
                   'identifier': 'https://www.geonames.org/2761369',
                   'referenceSystem': 'GeoNames'}],
        'geometry': {'type': 'Point',
                     'coordinates': [9, 17],
                     'title': '',
                     'description': ''},
        'depictions': [{
            '@id': 'http://local.host/api/0.2/entity/112',
            'title': 'Picture with a License', 'license': 'Open license',
            'url': 'N/A'}]}]}],
    'pagination': {
        'entities': 1,
        'entitiesPerPage': 20,
        'index': [{'page': 1, 'startId': 104}],
        'totalPages': 1}}
test_type_entities_all_special = {'results': [{
    '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
    'type': 'FeatureCollection',
    'features': [{
        '@id': 'http://local.host/entity/84',
        'type': 'Feature',
        'crmClass': 'crm:E53 Place',
        'systemClass': 'administrative_unit',
        'properties': {
            'title': 'Austria'},
        'description': None,
        'when': {
            'timespans': [
                {
                    'start': {
                        'earliest': 'None',
                        'latest': 'None'},
                    'end': {
                        'earliest': 'None',
                        'latest': 'None'}}]},
        'types': None,
        'relations': [
            {
                'label': 'Administrative unit',
                'relationTo': 'http://local.host/api/0.2/entity/83',
                'relationType': 'crm:P89 falls within',
                'relationSystemClass': 'administrative_unit',
                'relationDescription': None,
                'type': None,
                'when': {
                    'timespans': [
                        {
                            'start': {
                                'earliest': 'None',
                                'latest': 'None'},
                            'end': {
                                'earliest': 'None',
                                'latest': 'None'}}]}},
            {
                'label': 'Niederösterreich',
                'relationTo': 'http://local.host/api/0.2/entity/86',
                'relationType': 'crm:P89i contains',
                'relationSystemClass': 'administrative_unit',
                'relationDescription': None,
                'type': None,
                'when': {
                    'timespans': [
                        {
                            'start': {
                                'earliest': 'None',
                                'latest': 'None'},
                            'end': {
                                'earliest': 'None',
                                'latest': 'None'}}]}},
            {
                'label': 'Wien',
                'relationTo': 'http://local.host/api/0.2/entity/85',
                'relationType': 'crm:P89i contains',
                'relationSystemClass': 'administrative_unit',
                'relationDescription': None,
                'type': None,
                'when': {
                    'timespans': [
                        {
                            'start': {
                                'earliest': 'None',
                                'latest': 'None'},
                            'end': {
                                'earliest': 'None',
                                'latest': 'None'}}]}}],
        'names': None,
        'links': None,
        'geometry': None,
        'depictions': None}]},
    {
        '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
        'type': 'FeatureCollection',
        'features': [{
            '@id': 'http://local.host/entity/89',
            'type': 'Feature',
            'crmClass': 'crm:E53 Place',
            'systemClass': 'administrative_unit',
            'properties': {
                'title': 'Czech Republic'},
            'description': None,
            'when': {
                'timespans': [
                    {
                        'start': {
                            'earliest': 'None',
                            'latest': 'None'},
                        'end': {
                            'earliest': 'None',
                            'latest': 'None'}}]},
            'types': None,
            'relations': [
                {
                    'label': 'Administrative unit',
                    'relationTo': 'http://local.host/api/0.2/entity/83',
                    'relationType': 'crm:P89 falls within',
                    'relationSystemClass': 'administrative_unit',
                    'relationDescription': None,
                    'type': None,
                    'when': {
                        'timespans': [
                            {
                                'start': {
                                    'earliest': 'None',
                                    'latest': 'None'},
                                'end': {
                                    'earliest': 'None',
                                    'latest': 'None'}}]}}],
            'names': None,
            'links': None,
            'geometry': None,
            'depictions': None}]},
    {
        '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
        'type': 'FeatureCollection',
        'features': [{
            '@id': 'http://local.host/entity/87',
            'type': 'Feature',
            'crmClass': 'crm:E53 Place',
            'systemClass': 'administrative_unit',
            'properties': {
                'title': 'Germany'},
            'description': None,
            'when': {
                'timespans': [
                    {
                        'start': {
                            'earliest': 'None',
                            'latest': 'None'},
                        'end': {
                            'earliest': 'None',
                            'latest': 'None'}}]},
            'types': None,
            'relations': [
                {
                    'label': 'Administrative unit',
                    'relationTo': 'http://local.host/api/0.2/entity/83',
                    'relationType': 'crm:P89 falls within',
                    'relationSystemClass': 'administrative_unit',
                    'relationDescription': None,
                    'type': None,
                    'when': {
                        'timespans': [
                            {
                                'start': {
                                    'earliest': 'None',
                                    'latest': 'None'},
                                'end': {
                                    'earliest': 'None',
                                    'latest': 'None'}}]}}],
            'names': None,
            'links': None,
            'geometry': None,
            'depictions': None}]},
    {
        '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
        'type': 'FeatureCollection',
        'features': [{
            '@id': 'http://local.host/entity/88',
            'type': 'Feature',
            'crmClass': 'crm:E53 Place',
            'systemClass': 'administrative_unit',
            'properties': {
                'title': 'Italy'},
            'description': None,
            'when': {
                'timespans': [
                    {
                        'start': {
                            'earliest': 'None',
                            'latest': 'None'},
                        'end': {
                            'earliest': 'None',
                            'latest': 'None'}}]},
            'types': None,
            'relations': [
                {
                    'label': 'Administrative unit',
                    'relationTo': 'http://local.host/api/0.2/entity/83',
                    'relationType': 'crm:P89 falls within',
                    'relationSystemClass': 'administrative_unit',
                    'relationDescription': None,
                    'type': None,
                    'when': {
                        'timespans': [
                            {
                                'start': {
                                    'earliest': 'None',
                                    'latest': 'None'},
                                'end': {
                                    'earliest': 'None',
                                    'latest': 'None'}}]}}],
            'names': None,
            'links': None,
            'geometry': None,
            'depictions': None}]},
    {
        '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
        'type': 'FeatureCollection',
        'features': [{
            '@id': 'http://local.host/entity/90',
            'type': 'Feature',
            'crmClass': 'crm:E53 Place',
            'systemClass': 'administrative_unit',
            'properties': {
                'title': 'Slovakia'},
            'description': None,
            'when': {
                'timespans': [
                    {
                        'start': {
                            'earliest': 'None',
                            'latest': 'None'},
                        'end': {
                            'earliest': 'None',
                            'latest': 'None'}}]},
            'types': None,
            'relations': [
                {
                    'label': 'Administrative unit',
                    'relationTo': 'http://local.host/api/0.2/entity/83',
                    'relationType': 'crm:P89 falls within',
                    'relationSystemClass': 'administrative_unit',
                    'relationDescription': None,
                    'type': None,
                    'when': {
                        'timespans': [
                            {
                                'start': {
                                    'earliest': 'None',
                                    'latest': 'None'},
                                'end': {
                                    'earliest': 'None',
                                    'latest': 'None'}}]}}],
            'names': None,
            'links': None,
            'geometry': None,
            'depictions': None}]},
    {
        '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
        'type': 'FeatureCollection',
        'features': [{
            '@id': 'http://local.host/entity/91',
            'type': 'Feature',
            'crmClass': 'crm:E53 Place',
            'systemClass': 'administrative_unit',
            'properties': {
                'title': 'Slovenia'},
            'description': None,
            'when': {
                'timespans': [
                    {
                        'start': {
                            'earliest': 'None',
                            'latest': 'None'},
                        'end': {
                            'earliest': 'None',
                            'latest': 'None'}}]},
            'types': None,
            'relations': [
                {
                    'label': 'Administrative unit',
                    'relationTo': 'http://local.host/api/0.2/entity/83',
                    'relationType': 'crm:P89 falls within',
                    'relationSystemClass': 'administrative_unit',
                    'relationDescription': None,
                    'type': None,
                    'when': {
                        'timespans': [
                            {
                                'start': {
                                    'earliest': 'None',
                                    'latest': 'None'},
                                'end': {
                                    'earliest': 'None',
                                    'latest': 'None'}}]}}],
            'names': None,
            'links': None,
            'geometry': None,
            'depictions': None}]},
    {
        '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
        'type': 'FeatureCollection',
        'features': [{
            '@id': 'http://local.host/entity/86',
            'type': 'Feature',
            'crmClass': 'crm:E53 Place',
            'systemClass': 'administrative_unit',
            'properties': {
                'title': 'Niederösterreich'},
            'description': None,
            'when': {
                'timespans': [
                    {
                        'start': {
                            'earliest': 'None',
                            'latest': 'None'},
                        'end': {
                            'earliest': 'None',
                            'latest': 'None'}}]},
            'types': None,
            'relations': [
                {
                    'label': 'Austria',
                    'relationTo': 'http://local.host/api/0.2/entity/84',
                    'relationType': 'crm:P89 falls within',
                    'relationSystemClass': 'administrative_unit',
                    'relationDescription': None,
                    'type': None,
                    'when': {
                        'timespans': [
                            {
                                'start': {
                                    'earliest': 'None',
                                    'latest': 'None'},
                                'end': {
                                    'earliest': 'None',
                                    'latest': 'None'}}]}}],
            'names': None,
            'links': None,
            'geometry': None,
            'depictions': None}]},
    {
        '@context': 'https://raw.githubusercontent.com/LinkedPasts/linked-places/master/linkedplaces-context-v1.1.jsonld',
        'type': 'FeatureCollection',
        'features': [{
            '@id': 'http://local.host/entity/85',
            'type': 'Feature',
            'crmClass': 'crm:E53 Place',
            'systemClass': 'administrative_unit',
            'properties': {
                'title': 'Wien'},
            'description': None,
            'when': {
                'timespans': [
                    {
                        'start': {
                            'earliest': 'None',
                            'latest': 'None'},
                        'end': {
                            'earliest': 'None',
                            'latest': 'None'}}]},
            'types': None,
            'relations': [
                {
                    'label': 'Austria',
                    'relationTo': 'http://local.host/api/0.2/entity/84',
                    'relationType': 'crm:P89 falls within',
                    'relationSystemClass': 'administrative_unit',
                    'relationDescription': None,
                    'type': None,
                    'when': {
                        'timespans': [
                            {
                                'start': {
                                    'earliest': 'None',
                                    'latest': 'None'},
                                'end': {
                                    'earliest': 'None',
                                    'latest': 'None'}}]}}],
            'names': None,
            'links': None,
            'geometry': None,
            'depictions': None}]}],
    'pagination': {'entities': 8,
                   'entitiesPerPage': 20,
                   'index': [{'page': 1,
                              'startId': 84}],
                   'totalPages': 1}}
