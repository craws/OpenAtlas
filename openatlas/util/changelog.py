# Created by Alexander Watzinger and others. Please see README.md for licensing information


class Changelog:
    versions = {
        '4.0.0': ['TBA', {
            'feature': {
                '1049': 'Upgrade Python to 3.7',
                '1068': 'Place import with point coordinates'},
            'fix': {
                '1071': "Filter function in jsTree doesn't clear correctly",
                '1069': 'Overlay maps: interchanged easting and northing'
            }}],
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
            'feature': {'597': 'Option to display aliases in tables',
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
                '964': 'Forms: tables with pager ignoring selection after changing page'}}],
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
                '942': 'Server 500 Error after wrong date input at Actor/Person'}}],
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
                <p>This version includes many new features and changes. Some are listed below.</p>
                <p style="font-weight:bold">User Interface and Usability</p>
                &#8226 Performance improvements<br>
                &#8226 More possibilities to create and link entries in one go<br>
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
                '489': 'Layout - overwork, multiple possibilities to create and link entities',
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
                '420': 'First and last dates in list views (e.g. actor, place)'}}],
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
                '362': 'Document - Insert, update, delete, add texts, link with actors',
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
                '': 'Initial version based on the "Zend Base" project from '
                    '<a target="_blank" rel="noopener" href="https://craws.net">craws.net</a>'}}]}
