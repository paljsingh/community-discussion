#!/bin/bash

kibana_export() {
  curl -X POST -H "kbn-xsrf: reporting" "http://localhost:5601/api/saved_objects/_export" -H 'Content-Type: application/json' -d '{"type": "index-pattern"}' --output data/kibana/index_patterns.ndjson
  curl -X POST -H "kbn-xsrf: reporting" "http://localhost:5601/api/saved_objects/_export" -H 'Content-Type: application/json' -d '{ "objects": [ { "type": "dashboard", "id": "d88728a0-05a2-11ec-91aa-9112380282eb" } ] }' --output data/kibana/dashboard-1.ndjson
  curl -X POST -H "kbn-xsrf: reporting" "http://localhost:5601/api/saved_objects/_export" -H 'Content-Type: application/json' -d '{ "objects": [ { "type": "dashboard", "id": "a1e105d0-05ae-11ec-9857-f17ef5ae9d52" } ] }' --output data/kibana/dashboard-2.ndjson
}

kibana_import() {
  curl -i -X POST -H "kbn-xsrf: reporting" "http://localhost:5601/api/saved_objects/_import" --form file=@data/kibana/index_patterns.ndjson
  curl -i -X POST -H "kbn-xsrf: reporting" "http://localhost:5601/api/saved_objects/_import" --form file=@data/kibana/dashboard-1.ndjson
  curl -i -X POST -H "kbn-xsrf: reporting" "http://localhost:5601/api/saved_objects/_import" --form file=@data/kibana/dashboard-2.ndjson
}

kibana_import
