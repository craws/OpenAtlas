versions = {
    '7.2.0': ['TBA', {
        'feature': {
            '1445': 'Anthropological sex estimation',
            '1628': 'New maps',
            '1151': 'Map marker improvements',
            '1491': 'API: CSV export for network analysis',
            '1639': 'Refactor',
            '1406': 'Update OpenAtlas Website'},
        'fix': {
            '1588': 'Map problems adding geometries after deleting geometries',
            '1594': 'NPM warnings during install'}}],
    '7.1.1': ['2022-03-04', {
        'fix': {
            '1649': 'Minor label error in model image',
            '1650': 'Obsolete database version in install SQL'}}],
    '7.1.0': ['2022-02-15', {
        'feature': {
            '1506': 'Update CIDOC CRM to 7.1.1',
            '1285': 'Improved value types display',
            '1593': 'Adding multiple aliases at once instead one at a time',
            '1629': 'Improved mail function',
            '1624': 'Minor improvements and refactor',
            '1599': 'API: Search parameter include all subtypes',
            '1600': 'API: Search for values in value types',
            '1623': 'API: Show types for view name'},
        'fix': {
            '1626':
                "API: typed_entities doesn't show types in geojson format"}}],
    '7.0.4': ['2022-02-10', {
        'fix': {
            '1616': 'Error at inserting an administrative unit'}}],
    '7.0.3': ['2022-02-02', {
        'fix': {
            '1634': 'Value type with subtype error'}}],
    '7.0.2': ['2022-01-20', {
        'fix': {
            '1632': 'Multiple flag gets lost when updating a hierarchy'}}],
    '7.0.1': ['2022-01-05', {
        'fix': {
            '1627': 'Error when creating a source from file view'}}],
    '7.0.0': ['2022-01-01', {
        'feature': {
            '1566': 'Update OpenAtlas software to Debian/bullseye',
            '1297': 'Connecting events sequentially',
            '1577': 'Show actors at places from events',
            '1615': 'Additional step by step examples in manual',
            '1549': 'API: deprecation of node and subunit functions',
            '1579': 'API: Include Swagger documentation',
            '1598': 'API: Offset Pagination',
            '1603': 'API: Specialized GeoJSON format for subunits',
            '1622': 'API: search with dates',
            '1605': 'Refactor'},
        'fix': {
            '1614': 'Custom folders in uploads causing errors'}}],
    '6.6.4': ['2021-12-23', {
        'fix': {'1621': 'Error at CSV export'}}],
    '6.6.3': ['2021-12-08', {
        'fix': {'1616': 'Error at inserting an administrative unit'}}],
    '6.6.2': ['2021-11-23', {
        'fix': {'1609': 'Problem with types'}}],
    '6.6.1': ['2021-11-20', {
        'fix': {'1607': 'Error at profile for readonly users'}}],
    '6.6.0': ['2021-11-18', {
        'feature': {
            '1500': 'Production of artifacts',
            '1563': 'OpenAtlas model to database',
            '1597': 'Join artifacts and finds',
            '1584': 'Track needed and actual database version',
            '1589': 'Additional and improved system warnings',
            '1546': 'API: New search parameter',
            '1583': 'Refactor'}}],
    '6.5.2': ['2021-11-07', {
        'fix': {'#1596:': 'Sometimes unavailable add custom type button'}}],
    '6.5.1': ['2021-10-28', {
        'fix': {'#1592:': 'Error at import when using type ids'}}],
    '6.5.0': ['2021-09-19', {
        'feature': {
            '1462': 'Current owner of artifacts',
            '1562': 'Update manual overlay',
            '1184': 'API: add additional output format RDFS',
            '1551': 'API: Relation type adaptions, adding relationDescription',
            '1561': 'Refactor'},
        'fix': {
            '1557': 'Save buttons blocked by map',
            '1580': 'Hidden error messages for reference systems',
            '1570': 'API: Wrong type signature in OpenApi'}}],
    '6.4.1': ['2021-08-11', {
        'fix': {
            '1559': 'Installation problem because of missing upload folder'}}],
    '6.4.0': ['2021-08-10', {
        'feature': {
            '1280': 'Picture Preview',
            '1492': 'Image Processing',
            '1552': 'External reference systems for sources',
            '1538': 'Focus on table filter at overview pages',
            '1531': 'Map overlay improved',
            '1523': 'Performance issues while linking pictures',
            '1558': 'Manual entry profession',
            '1536': 'Refactor',
            '1426': 'API: Display image smaller size',
            '1495': 'API: Additional Geojson output for QGIS imports',
            '1529': 'API: Increase request performance',
            '1530': 'API: Geometries endpoint for frontend map',
            '1535': 'API: Get all entities linked to an entity',
            '1537': 'API: Type entities for actor types',
            '1545': 'API: Filter entities by types'},
        'fix': {
            '1414': 'Enlarged Description Field Covers up Entry Buttons',
            '1539': 'Pagination not shown for tables sometimes',
            '1554': 'Error at value type view'}}],
    '6.3.0': ['2021-06-13', {
        'feature': {
            '1513': 'Add reference page for multiple files',
            '1520': 'Better value type display',
            '1527': 'Improved tab system',
            '1502': 'Show count of finds when entering additional',
            '1509': 'Manual - examples for use cases',
            '1512': 'Refactor',
            '1478': 'API: latest with pagination',
            '1516': 'API: implement Google JSON style',
            '1526': 'API: Refactor'},
        'fix': {
            '1515': 'API: Paging count faulty'}}],
    '6.2.1': ['2021-05-12', {
        'fix': {
            '1514': 'End dates of entities are not displayed correctly'}}],
    '6.2.0': ['2021-05-08', {
        'feature': {
            '940': 'Multiple file upload',
            '1284': 'Show image when editing a place or artifact',
            '1428': 'Configuration of frontend site name',
            '1476': 'Show/hide button for multiple reference systems',
            '1494': 'Refactor',
            '1496': 'API: Endpoints for entities of type',
            '1490': 'API: Refactor'}}],
    '6.1.0': ['2021-04-05', {
        'feature': {
            '1215': 'Time spans for types',
            '1443': 'List view for untyped entities',
            '1457': 'Public notes',
            '963': 'API: Add type of places to export',
            '1402': 'API: CSV export in API',
            '1487': 'API: Endpoint for type hierarchies',
            '1489': 'API: Geometry for artifacts'}}],
    '6.0.1': ['2021-03-15', {
        'fix': {
            '1485': 'Cannot choose multiple for custom type'}}],
    '6.0.0': ['2021-03-13', {
        'feature': {
            '1091': 'Reference systems for types',
            '1109': 'Sustainable web map services',
            '1456': 'Artifacts',
            '1187': 'Add files for artifacts',
            '1465':
                'Merge legal body to group, information carrier to artifact',
            '1461': 'Also search in date comments',
            '1398': 'Compress SQL export files',
            '1274': 'API: Automatic documentation for code',
            '1390': 'API: Swagger file in OpenAtlas repository',
            '1479': 'API: get by view name and system class',
            '1484': 'API: Add new functions',
            '1447': 'Refactor'},
        'fix': {
            '1477': 'Unable to select an entity with single quote in name',
            '1452': 'API: "type" is empty if more entities are requested',
            '1471': 'API: Url to linked places deprecated'}}],
    '5.7.2': ['2021-01-27', {
        'fix': {
            '1455': 'Network graphic error'}}],
    '5.7.1': ['2021-01-26', {
        'fix': {
            '1454': 'Error in install instructions'}}],
    '5.7.0': ['2021-01-16', {
        'feature': {
            '1292': 'External reference systems',
            '1440': 'Search with unaccented characters',
            '1386': 'API: Flask restful framework'},
        'fix': {
            '1434': 'Errors with types if named like standard types',
            '1427': 'API: Paging is broken'}}],
    '5.6.0': ['2020-11-30', {
        'feature': {
            '930': 'Wikidata API',
            '1409': 'Redesign forms',
            '1393': 'Split profile display options',
            '1395': 'Content for frontends',
            '1347': 'All icons to Font Awesome icons',
            '1379': 'Feature votes',
            '1407': 'Extend session availability (prevent CSRF token timeout)',
            '1412': 'API: Include Wikidata',
            '1350': 'API: Pagination in an extra array',
            '1375': 'API: Download result of request path',
            '1401': 'API: file access',
            '1377': 'API: IP restrictions',
            '1348': 'Refactor'},
        'fix': {
            '1383': 'Map in tab views too big',
            '1408': 'Link checker broken'}}],
    '5.5.1': ['2020-10-09', {
        'fix': {'1380': "Empty date comment is saved as 'None'"}}],
    '5.5.0': ['2020-09-26', {
        'feature': {
            '929': 'Module options',
            '999': 'Navigation for archeological subunits',
            '1189': 'User interface improvements',
            '1222': 'Usability improvement at select tables',
            '1289': 'Citation example for edition and bibliography',
            '1206': 'API: Show entities of subtypes',
            '1331': 'API: Front end queries'}}],
    '5.4.0': ['2020-09-09', {
        'feature': {
            '1317': 'Additional manual content',
            '1321': 'Import with types',
            '1255': 'API: Content Negotiation',
            '1275': 'API: parameters',
            '1299': 'API: Setting for CORS allowance in UI',
            '1318': 'API: Selective requests'},
        'fix': {
            '1306':
                'Search results: small table, missing mouse over description',
            '1308': 'Missing connection for actors created from place',
            '1319': 'Data table error in view',
            '1326': 'User table in admin is not responsive',
            '1328': 'Table layout error at check link duplicates function'}}],
    '5.3.0': ['2020-07-15', {
        'feature': {
            '1272': 'Tabs redesign',
            '1279': 'Change "Add" button label to "Link"',
            '1229': 'Show descriptions in all tables',
            '1282': 'Additional submit buttons for sub units',
            '1283': 'More detailed type display',
            '1286': 'Notifications for date field',
            '1287': 'Map tiles max zoom',
            '1276': 'Show child nodes in tree search',
            '1258': 'Manual Text for Subunits',
            '1211': 'API: CORS handler',
            '1232': 'API: Error/Exception Handling'},
        'fix': {
            '547': 'Prevent double submit',
            '1235': 'Layout issues with forms on smaller screens',
            '1278': 'Broken table list views on smaller screens',
            '1267': 'Model link checker bug',
            '1288': 'Forward upon failed form validation',
            '1291': "Data tables mouse over doesn't work if filtered",
            '1234': "API: Relation inverse doesn't work proper"}}],
    '5.2.0': ['2020-05-11', {
        'feature': {
            '1065': 'User manual in application',
            '1167': 'Settings and profile'},
        'fix': {
            '1208': 'CSV export error with BC dates',
            '1218': 'Resizeable form elements vanish below map',
            '1223': 'Visibility of Full Entries'}}],
    '5.1.1': ['2020-04-12', {
        'fix': {
            '1190': 'Tabs not shown in file view',
            '1191': 'Show/Hide date is switched'}}],
    '5.1.0': ['2020-04-11', {
        'feature': {
            '991': 'Images/Files for Types',
            '1183': 'Mouse over effect for table rows'},
        'fix': {
            '1182': 'Type view: links and redirect',
            '1188': 'Missing map in add feature view'}}],
    '5.0.0': ['2020-03-24', {
        'feature': {
            '1048': 'Bootstrap layout',
            '1050': 'API',
            '1089': 'Human Remains',
            '1136': 'Map enhancements',
            '1138': 'Display usage of CIDOC CRM classes and properties',
            '1175': 'Additional date checks',
            '1066': 'Package Manager for JavaScript Libraries'},
        'fix': {
            '1134': 'Overlay maps: not enabled if Geonames disabled',
            '1139': 'Breadcrumbs show place twice',
            '1140': 'HTML Code is showing in description text Actions',
            '1152': "Menu item isn't marked as active in entity view"}}],
    '4.1.0': ['2020-01-30', {
        'feature': {
            '1070': 'Enhance network visualization',
            '952': 'Show subunits on map'}}],
    '4.0.0': ['2020-01-01', {
        'feature': {
            '905': 'Upgrade CIDOC CRM to 6.2.1.',
            '1049': 'Upgrade Python to 3.7',
            '1003': 'Import with dates',
            '1068': 'Place import with point coordinates',
            '1072': 'Show places of movement at the person view',
            '1079': 'Static type checking with Mypy',
            '1101': 'Disable showing default images for reference'},
        'fix': {
            '1069': 'Overlay maps: interchanged easting and northing',
            '1071': "Filter function in jsTree doesn't clear correctly",
            '1100': 'Save geometry not working'}}],
    '3.20.1': ['2019-10-13', {
        'fix': {
            '1069': 'Overlay maps: interchanged easting and northing'}}],
    '3.20.0': ['2019-10-06', {
        'feature': {
            '978': 'Image overlays for maps',
            '1038': 'Move events',
            '1060': 'New menu item "Object"',
            '1061': 'More options to link entries',
            '1058': 'SQL interface',
            '1043': 'DataTables',
            '1056': 'Additional codes for GeoNames search'}}],
    '3.19.0': ['2019-08-26', {
        'feature': {
            '928': 'GeoNames links for places',
            '1042': 'Personal notes for entities',
            '1040': 'New user group: Contributor',
            '1055': 'Add finds to overview count',
            '1044': 'Hide date form fields only if they are empty',
            '1041': 'Remove color themes',
            '1054': 'Remove Production and Destruction'}}],
    '3.18.1': ['2019-08-20', {
        'fix': {
            '1053': 'Bug at file upload with special characters'}}],
    '3.18.0': ['2019-07-07', {
        'feature': {
            '1036': 'Search for similar names',
            '1034': 'Advanced data integrity check functions',
            '1025': 'New OpenAtlas project site'}}],
    '3.17.1': ['2019-05-21', {
        'fix': {
            '1033': 'Map editing breaks upon save w/o edit'}}],
    '3.17.0': ['2019-05-13', {
        'feature': {
            '597': 'Option to display aliases in tables',
            '1026': 'Check function for duplicate links'},
        'fix': {
            '1015': "Multiple Place Add in Entity doesn't work correct",
            '1016': 'Lines cannot be deleted or edited',
            '1017': 'Lines, Areas and Shapes get sometimes deleted'}}],
    '3.16.0': ['2019-04-19', {
        'feature': {
            '994': 'Line drawing in map',
            '1011': 'Additional security features',
            '1012': 'Update GeoNames search for map'}}],
    '3.15.0': ['2019-04-04', {
        'feature': {
            '983': 'External References'},
        'fix': {
            '1010': 'Missing or misspelled map feature descriptions'}}],
    '3.14.1': ['2019-03-14', {
        'feature': {
            '997': 'Advanced date completion'},
        'fix': {
            '1000': 'Bookmarks not working',
            '987': 'Open Type in new Tab or Window'}}],
    '3.14.0': ['2019-03-12', {
        'feature': {
            '988': 'Search with date filter',
            '996': 'Better structured info tabs',
            '981': 'Documentation for dates in model'},
        'fix': {
            '995': 'Double Search Results'}}],
    '3.13.0': ['2019-02-28', {
        'feature': {
            '590': 'Search - advanced features',
            '975': 'Unit labels for value types',
            '985': 'Check for invalid dates at actor/event participation',
            '936': 'Refactor dates',
            '993': 'Refactor links'}}],
    '3.12.0': ['2018-12-31', {
        'feature': {
            '652': 'Maps update and rewrite',
            '891': 'Profile images',
            '959': 'Performance',
            '961': 'Check function for dates and circular dependencies',
            '962': 'Configurable character limit for live searches'},
        'fix': {
            '970': "Insert and Continue doesn't work with place in Chrome"}}],
    '3.11.1': ['2018-11-30', {
        'fix': {
            '964':
                'Forms: tables with pager ignoring selection after '
                'changing page'}}],
    '3.11.0': ['2018-11-24', {
        'feature': {
            '956': 'Clustering for maps',
            '949': 'Performance',
            '935': 'Remove forms from types'}}],
    '3.10.0': ['2018-11-09', {
        'feature': {
            '934': 'Import',
            '951': 'Export: additional options',
            '538': 'Move/delete types for multiple entities',
            '954': 'Documentation and links in application'},
        'fix': {
            '942':
                'Server 500 Error after wrong date input at  Actor/Person'}}],
    '3.9.0': ['2018-09-28', {
        'feature': {
            '867': 'Network visualization advanced'},
        'fix': {
            '939': 'Translation',
            '941': 'Text in brackets of subtypes disappears when edited'}}],
    '3.8.0': ['2018-08-26', {
        'feature': {
            '419': 'Export SQL',
            '915': 'Export CSV'},
        'fix': {
            '926': 'Language display bug'}}],
    '3.7.0': ['2018-07-22', {
        'feature': {
            '878': 'Enhanced admin functionality',
            '913': 'Change logo function'},
        'fix': {
            '914': 'Network view in Development Version'}}],
    '3.6.0': ['2018-06-09', {
        'feature': {
            '710': 'Value Types',
            '902': 'Insert and continue for types',
            '903': 'Check existing links function'}}],
    '3.5.0': ['2018-05-12', {
        'feature': {
            '896': 'Legal notice text option',
            '898': 'Option to send mail without login credentials',
            '901': 'Display available disk space'}}],
    '3.4.0': ['2018-04-17', {
        'feature': {
            '431': 'Sub-Units for Sites'}}],
    '3.3.0': ['2018-03-20', {
        'feature': {
            '422': 'File upload'}}],
    '3.2.0': ['2018-02-10', {
        'feature': {
            '732': 'Documentation and manual',
            '888': 'User and activity view',
            '879': 'Demo with MEDCON data'}}],
    '3.1.0': ['2018-01-18', {
        'feature': {
            '863': 'BC dates and date validation',
            '780': 'Color Schemes'}}],
    '3.0.0': ['2017-12-31', {
        'feature': {
            '877': """Python/Flask Port
            <p>
                This version includes many new features and changes.
                Some are listed below.
            </p>
            <p style="font-weight:bold">User Interface and Usability</p>
            &#8226 Performance improvements<br>
            &#8226 More possibilities to create and link entries in one go
            <br>
            &#8226 Merge of front and backend and cleaner user interface<br>
            &#8226 Advanced display and editing of source translations<br>
            &#8226 Acquisition: multiple recipients, donors and places<br>
            &#8226 Advanced type index view<br>
            &#8226 Restructured admin area<br>
            &#8226 Admin functions to check and deal with orphaned data<br>
            &#8226 Show more/less option for long descriptions
            <p style="font-weight:bold">Software and Code</p>
            &#8226 Switched main programming language to Python 3<br>
            &#8226 Switched web application framework to Flask<br>
            &#8226 Switched template engine to Jinja2<br>
            &#8226 Update of third party JavaScript libraries
            <p style="font-weight:bold">Security</p>
            &#8226 bcrypt hash algorithm for sensitive data<br>
            &#8226 CSRF protection for forms<br>
            &#8226 Adaptions for using HTTPS<br>
            &#8226 A show password option at forms"""}}],
    '2.4.0': ['2017-03-27', {
        'feature': {
            '539': 'Network graph visualisation',
            '819': 'Enable linebreaks for descriptions'}}],
    '2.3.0': ['2016-12-17', {
        'feature': {
            '764': 'Improved hierarchy overview',
            '702': 'Improved settings',
            '707': 'Improved performance',
            '494': 'Newsletter and registration mails',
            '319': 'SMTP settings in admin interface',
            '693': 'Event overview: show event dates if available',
            '569': 'Previous and next buttons',
            '768': 'Show info column in main lists'}}],
    '2.2.0': ['2016-09-11', {
        'feature': {
            '547': 'Map: multiple points and areas for Places',
            '719': 'Favicon support for current systems'}}],
    '2.1.0': ['2016-08-18', {
        'feature': {
            '643': 'Performance improvements',
            '700': 'Improved frontend',
            '703': 'Add multiple actors, events and places to source'},
        'fix': {
            '696': 'Add texts to source'}}],
    '2.0.0': ['2016-06-19', {
        'feature': {
            '428': 'Dynamic Types',
            '687': 'Remove required restriction from type fields'},
        'fix': {
            '688': 'Translation errors',
            '689': 'Show/Hide buttons'}}],
    '1.6.0': ['2016-05-04', {
        'feature': {
            '340': 'Multi user capability',
            '672': 'Add multiple sources for event/actor/place',
            '679': 'Improved credits',
            '683': 'Tooltips for form fields and profile'},
        'fix': {
            '674': 'Place error occurs during saving'}}],
    '1.5.0': ['2016-04-01', {
        'feature': {
            '564': 'Add multiple entries for relation, member and involvement',
            '586': 'Bookmarks',
            '671': 'Redmine links for changelog'}}],
    '1.4.0': ['2016-03-26', {
        'feature': {
            '528': 'jsTree views for hierarchies',
            '566': 'Enhanced profile and site settings',
            '580': 'Change menu and structure for easier access to types',
            '654': 'New map layers',
            '666': 'Added Credits'}}],
    '1.3.0': ['2016-02-28', {
        'feature': {
            '462': 'Actor - add member to group from actor view',
            '563': 'Actor - insert and continue for relations and members',
            '600': 'Update of JavaScript libraries (for jsTree)',
            '621': 'Revised and more compact schema'},
        'fix': {
            '601': 'Application is very slow on some views',
            '638': 'Names with an apostrophe in a table not selectable'}}],
    '1.2.0': ['2015-12-13', {
        'feature': {
            '499': 'Actor - place tab with map',
            '511': 'Search - advanced features'},
        'fix': {
            '547': 'Prevent double submit',
            '587': 'Support multiple email recipients'}}],
    '1.1.0': ['2015-11-09', {
        'feature': {
            '529': 'Reference - Information Carrier',
            '527': 'New user groups - manager and readonly',
            '540': 'Help and FAQ site',
            '555': 'Source - additional text type "Source Transliteration"',
            '556': 'Actor - function for member not required anymore',
            '560': 'Newsletter and show email option in profile'},
        'fix': {
            '551': 'Model - Updating type bug',
            '544': 'Map - Form data lost after map search',
            '533': 'Map - Markers outside of Map'}}],
    '1.0.0': ['2015-10-11', {
        'feature': {
            '487': 'Event - Acquisition of places',
            '508': 'Reference - Editions',
            '504': 'Option to add comments for entities in texts tab',
            '495': 'Layout - new OpenAtlas logo',
            '412': 'Layout - improved layout and color scheme',
            '525': 'Layout - overlays for tables in forms'}}],
    '0.11.0': ['2015-09-11', {
        'feature': {
            '433': 'Search functions'}}],
    '0.10.0': ['2015-09-01', {
        'feature': {
            '429': 'Actor - member of',
            '472': 'Actor - activity for event relations',
            '483': 'Actor - update for relations and involvements',
            '486': 'Place - administrative units and historical places',
            '389': 'Reference - bibliography',
            '489':
                'Layout - overwork, multiple possibilities to create and '
                'link entities',
            '421': 'CRM link checker'}}],
    '0.9.0': ['2015-07-12', {
        'feature': {
            '392': 'Event',
            '423': 'Map - advanced features',
            '474': 'Layout - new tab based layout for views'}}],
    '0.8.0': ['2015-06-18', {
        'feature': {
            '326': 'Map - search, show existing places',
            '425': 'More types'}}],
    '0.7.0': ['2015-05-29', {
        'feature': {
            '403': 'Physical things - places',
            '353': 'Maps - with Leaflet (GIS)',
            '420': 'First and last dates in list views'}}],
    '0.6.0': ['2015-05-13', {
        'feature': {
            '402': 'Begin, end, birth and death (precise and fuzzy))',
            '346': 'CRM - link checker',
            '412': 'Layout - New color scheme'},
        'fix': {
            '410': 'wrong domains for links'}}],
    '0.5.0': ['2015-04-08', {
        'feature': {
            '377': 'Hierarchical Data',
            '391': 'Time periods',
            '365': 'Actor to actor relations',
            '386': 'Filter for tables'}}],
    '0.4.0': ['2015-02-23', {
        'feature': {
            '362':
                'Document - Insert, update, delete, add texts, link with '
                'actors',
            '354': 'Alternative names',
            '360': 'New color theme'},
        'fix': {
            '357': 'wrong range link in list view properties'}}],
    '0.3.0': ['2015-02-10', {
        'feature': {
            '348': 'Actor - begin and end dates',
            '307': 'Log user CRM data manipulation'},
        'fix': {
            '344': 'tablesorter IE 11 bug'}}],
    '0.2.0': ['2015-01-18', {
        'feature': {
            '310': 'Actor - insert, update, delete, list, view',
            '337': 'CRM - new OpenAtlas shortcuts'}}],
    '0.1.0': ['2014-12-30', {
        'feature': {
            '318': 'Import definitions from CIDOC rdfs'}}],
    '0.0.1': ['2014-11-05', {
        'feature': {
            '':
                'Initial version based on the "Zend Base" project from '
                '<a  target="_blank" href="https://craws.net">craws.net</a>'}}]}
