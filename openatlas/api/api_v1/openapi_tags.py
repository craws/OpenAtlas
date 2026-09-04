from flask_openapi3 import Tag

lod_tag = Tag(name="LOD", description="Linked Open Data Endpoints")
system_tag = Tag(
    name="System",
    description="System information and configuration")
vocabulary_tag = Tag(name="Vocabulary", description="Types and Vocabularies")

# Files
# single images, iiif manifest, all public/licensed images
file_tag = Tag(name="Files", description="IIIF, display and licenses")

# Thanados, PFP, CSV, and other
export_tag = Tag(name="Export", description="Different export formats")

# All geographic entites, filter with bbox, search nearest entities, g
# pkg export, etc.
geographic_tag = Tag(name="Geographic", description="Geographic endpoints")

# presentation view, table, search
frontend_tag = Tag(name="Frontend", description="Frontend endpoints")

# Network analysis
# Network, ego network, SNA with special person connections
network_tag = Tag(name="Network", description="Network analysis endpoints")

metadata_tag = Tag(
    name="Metadata",
    description="Project metadata and case studies")
