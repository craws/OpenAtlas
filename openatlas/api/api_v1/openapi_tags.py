from flask_openapi3 import Tag

lod_tag = Tag(
    name='LOD',
    description='Linked Open Data endpoints (e.g. Linked.Art).')

system_tag = Tag(
    name='System',
    description='System information, classes, and configuration.')

vocabulary_tag = Tag(
    name='Vocabulary',
    description='Controlled vocabularies, type hierarchies, and SKOS exports.')

file_tag = Tag(
    name='Files',
    description='File display, thumbnails, and public license overviews.')

iiif_tag = Tag(
    name='IIIF',
    description='IIIF Presentation and Image API endpoints.')

metadata_tag = Tag(
    name='Metadata',
    description='Project metadata, agents, and case studies.')

frontend_tag = Tag(
    name='Frontend',
    description='Frontend search and discovery endpoints.')
