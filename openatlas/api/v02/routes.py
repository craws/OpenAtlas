from flasgger import Swagger
from flask_restful import Api

from openatlas import app
from openatlas.api.v02.common.class_ import GetByClass
from openatlas.api.v02.common.code import GetByCode
from openatlas.api.v02.common.content import GetContent
from openatlas.api.v02.common.entity import GetEntity
from openatlas.api.v02.common.latest import GetLatest
from openatlas.api.v02.common.node_entities import GetNodeEntities
from openatlas.api.v02.common.node_entities_all import GetNodeEntitiesAll
from openatlas.api.v02.common.query import GetQuery
from openatlas.api.v02.common.subunit import GetSubunit
from openatlas.api.v02.common.subunit_hierarchy import GetSubunitHierarchy
from openatlas.api.v02.resources.error import errors

app.config['SWAGGER'] = {
    'openapi': '3.0.2',
    'uiversion': 3
}
template= {
  "openapi": "3.0.2",
  "info": {
    "title": "OpenAtlas API",
    "version": "0.2",
    "description": "A documentation of the OpenAtlas API",
    "license": {
      "name": "Apache 2.0",
      "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
    },
    "contact": {
      "name": "Bernhard Koschicek",
      "email": "bernhard.koschicek@oeaw.ac.at"
    }
  },
  "servers": [],
  "tags": [
    {
      "name": "Entities",
      "description": "Requesting entities through different means."
    },
    {
      "name": "Nodes",
      "description": "Requesting nodes and subunits"
    },
    {
      "name": "Content",
      "description": "Requesting content of the OpenAtlas instance."
    }
  ],
  "components": {
    "parameters": {
      "limitParam": {
        "name": "limit",
        "in": "query",
        "description": "Number of geojson representation to be returned",
        "schema": {
          "type": "number"
        }
      },
      "columnParam": {
        "name": "column",
        "in": "query",
        "description": "The result will sorted by the given column",
        "schema": {
          "type": "string",
          "enum": [
            "id",
            "class_code",
            "name",
            "description",
            "created",
            "modified",
            "system_type",
            "begin_from",
            "begin_to",
            "end_from",
            "end_to"
          ]
        }
      },
      "sortParam": {
        "name": "sort",
        "in": "query",
        "description": "Result will be sorted asc/desc (by default by the name column)",
        "schema": {
          "type": "string",
          "enum": [
            "asc",
            "desc"
          ]
        }
      },
      "filterParam": {
        "name": "filter",
        "in": "query",
        "description": "Specify request with custom SQL filter method",
        "schema": {
          "type": "string"
        }
      },
      "firstParam": {
        "name": "first",
        "in": "query",
        "description": "List of results start with given ID",
        "schema": {
          "type": "number"
        }
      },
      "lastParam": {
        "name": "last",
        "in": "query",
        "description": "List of results start with entity after given ID",
        "schema": {
          "type": "number"
        }
      },
      "countParam": {
        "name": "count",
        "in": "query",
        "description": "Returns a number which represents the total count of the result",
        "schema": {
          "type": "boolean"
        }
      },
      "downloadParam": {
        "name": "download",
        "in": "query",
        "description": "Triggers the file download of the given request",
        "schema": {
          "type": "boolean"
        }
      },
      "showParam": {
        "name": "show",
        "in": "query",
        "description": "Select which key should be shown e.g. when, types, relations, names, links, geometry, depictions, not",
        "schema": {
          "type": "string",
          "enum": [
            "when",
            "types",
            "relations",
            "names",
            "links",
            "geometry",
            "depictions",
            "not"
          ]
        }
      },
      "langParam": {
        "name": "language",
        "in": "query",
        "description": "Select output language",
        "schema": {
          "type": "string",
          "enum": [
            "en",
            "de"
          ]
        }
      }
    },
    "schemas": {
      "ContentModel": {
        "type": "object",
        "properties": {
          "contact": {
            "type": "string"
          },
          "intro": {
            "type": "string"
          },
          "legal-notice": {
            "type": "string"
          }
        }
      },
      "NodeModel": {
        "type": "object",
        "properties": {
          "id": {
            "type": "number"
          },
          "label": {
            "type": "string"
          },
          "url": {
            "type": "string"
          }
        }
      },
      "NodeOverviewModel": {
        "type": "object",
        "properties": {
          "nodes": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/NodeModel"
            }
          }
        }
      },
      "OutputModel": {
        "type": "object",
        "properties": {
          "GeoJson": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/GeoJsonModel"
            }
          },
          "pagination": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/PaginationModel"
            }
          }
        }
      },
      "PaginationModel": {
        "type": "object",
        "properties": {
          "entities": {
            "type": "number"
          },
          "entity_per_page": {
            "type": "number"
          },
          "total_pages": {
            "type": "number"
          },
          "index": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/PaginationIndexModel"
            }
          }
        }
      },
      "PaginationIndexModel": {
        "type": "object",
        "properties": {
          "page": {
            "type": "number"
          },
          "start_id": {
            "type": "number"
          }
        }
      },
      "LatestModel": {
        "type": "array",
        "items": {
          "$ref": "#/components/schemas/GeoJsonModel"
        }
      },
      "GeoJsonModel": {
        "type": "object",
        "required": [
          "type",
          "features"
        ],
        "properties": {
          "features": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/FeatureGeoJSON"
            }
          },
          "type": {
            "type": "string"
          },
          "@context": {
            "type": "string"
          }
        }
      },
      "FeatureGeoJSON": {
        "type": "object",
        "required": [
          "@id",
          "geometry",
          "type"
        ],
        "properties": {
          "@id": {
            "type": "string"
          },
          "crmClass:": {
            "type": "string"
          },
          "type": {
            "type": "string"
          },
          "depictions": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/DepictionModel"
            }
          },
          "description": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/DescriptionModel"
            }
          },
          "links": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/LinkModel"
            }
          },
          "names": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/NamesModel"
            }
          },
          "properties": {
            "type": "object",
            "properties": {
              "title": {
                "type": "string"
              }
            }
          },
          "relations": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/RelationModel"
            }
          },
          "types": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/TypeModel"
            }
          },
          "when": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/WhenModel"
            }
          }
        }
      },
      "DepictionModel": {
        "type": "object",
        "properties": {
          "@id": {
            "type": "string"
          },
          "license": {
            "type": "string"
          },
          "title": {
            "type": "string"
          },
          "url": {
            "type": "string"
          }
        }
      },
      "DescriptionModel": {
        "type": "object",
        "properties": {
          "value": {
            "type": "string"
          }
        }
      },
      "LinkModel": {
        "type": "object",
        "properties": {
          "identifier": {
            "type": "string"
          },
          "type": {
            "type": "string"
          }
        }
      },
      "NamesModel": {
        "type": "object",
        "properties": {
          "alias": {
            "type": "string"
          }
        }
      },
      "RelationModel": {
        "type": "object",
        "properties": {
          "label": {
            "type": "string"
          },
          "relationTo": {
            "type": "string"
          },
          "relationType": {
            "type": "string"
          }
        }
      },
      "TypeModel": {
        "type": "object",
        "properties": {
          "hierarchy": {
            "type": "string"
          },
          "identifier": {
            "type": "string"
          },
          "label": {
            "type": "string"
          }
        }
      },
      "TimeDetailModel": {
        "type": "object",
        "properties": {
          "earliest": {
            "type": "string"
          },
          "latest": {
            "type": "string"
          }
        }
      },
      "TimespansModel": {
        "type": "object",
        "properties": {
          "end": {
            "$ref": "#/components/schemas/TimeDetailModel"
          },
          "first": {
            "$ref": "#/components/schemas/TimeDetailModel"
          }
        }
      },
      "WhenModel": {
        "type": "object",
        "properties": {
          "timespans": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/TimespansModel"
            }
          }
        }
      }
    }
  }
}

api = Api(app, catch_all_404s=False, errors=errors)  # Establish connection between API and APP
#swagger = Swagger(app, parse=False, template_file="static/swagger/Swagger.json")
swagger = Swagger(app, parse=False, template=template)

api.add_resource(GetEntity, '/api/0.2/entity/<int:id_>', endpoint='entity')
api.add_resource(GetByClass, '/api/0.2/class/<string:class_code>', endpoint="class")
api.add_resource(GetByCode, '/api/0.2/code/<string:item>', endpoint="code")
api.add_resource(GetContent, '/api/0.2/content/', endpoint="content")
api.add_resource(GetLatest, '/api/0.2/latest/<int:latest>', endpoint="latest")
api.add_resource(GetNodeEntities, '/api/0.2/node_entities/<int:id_>', endpoint="node_entities")
api.add_resource(GetNodeEntitiesAll, '/api/0.2/node_entities_all/<int:id_>',
                 endpoint="node_entities_all")
api.add_resource(GetSubunit, '/api/0.2/subunit/<int:id_>', endpoint="subunit")
api.add_resource(GetSubunitHierarchy, '/api/0.2/subunit_hierarchy/<int:id_>',
                 endpoint="subunit_hierarchy")
api.add_resource(GetQuery, '/api/0.2/query/', endpoint="query")
