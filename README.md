# Points of Sale RDF Mapping

This project focuses on transforming a JSON dataset describing points of sale (e.g. ticket machines, stations, contact points) into RDF using RML mappings. The goal is to create a structured RDF graph that can be queried using SPARQL and linked to controlled vocabularies.

## Project Structure

**pointsOfSale.json**

* Original input dataset in JSON format.

**json_transformator.py**

* Python script used to transform the original JSON into a structure more suitable for RDF mapping.

**pointsOfSale_transformed.json**

* Output of the transformation script. This file is used as the main input for the RML mappings.

**graph.ttl**

* The final graph: Output of the RML mapping process.

**codelist.ttl**

* RML mapping for codelists (point types, services, payment methods), modeled using SKOS.

**consts-cs.json**

* Source JSON file containing codelists used for mapping controlled vocabularies.

**pointsOfSale.ttl**

* RML mapping for codelists for points of sale.

**map.py**

* Python code for visualising points of sale on the map. 

**requirements.txt**

* List of Python dependencies required to run the transformation and mapping scripts.
