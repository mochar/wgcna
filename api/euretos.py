from collections import defaultdict
from pprint import pprint
import requests
import json
import os
import configparser
from cache import cache


class Euretos:
    """
    This class acts as a wrapper for the Euretos Swagger API, specifically for the
    search and connections-related calls.

    Class methods often expect or return a list of concepts. When requested as
    a parameter, a concept list should consist of dictionaries with at least
    one key 'id', the Euretos identifier of that concept. When returned by a
    method, the concept list contains at least the key 'name' in addition.
    """
    def __init__(self, config_file='config.ini', username=None, password=None,
                url=None, api_key=None, cache_enabled = False):

        self.cache_enabled = cache_enabled

        self.s = requests.Session()
        self.s.headers.update({'content-type': 'application/json; charset=UTF-8'})
        if all([username, password, url]):
            self.base_url = url + '{}'
            self.log_in(username, password)
            return
        config = configparser.ConfigParser()
        config.read(config_file)
        self.base_url = config['data']['url'] + '{}'
        if api_key is not None:
            self._set_key(api_key)
        else:
            username = config['data']['username']
            password = config['data']['password']
            self.log_in(username, password)

    def _flatten_concepts(self, concepts):
        """
        Flattens a dictionary 'source id => concepts' to a list of concepts.
        param concepts: A list of concepts. See class doc.

        Concepts that have the same sourceId as a previous are ignored.
        This has minimal side effects because concepts that share a
        sourceId have very similar concept profiles.
        """
        flattened_concepts = []
        for source_id, cs in concepts.items():
            for concept in cs:
                flattened_concept = {'name': concept['name'], 
                    'type': concept['type'], 'sourceId': source_id, 
                    'id': concept['id']}
                flattened_concepts.append(flattened_concept)
                break # Ignore concepts with the same sourceId
        return flattened_concepts

    def _set_key(self, key):
        """
        Stores the Swagger API key in the session headers for repeated use.
        param key: The Swagger API key.
        """
        print(key)
        self.s.headers.update({'x-token': key})
        
    def log_in(self, username, password):
        """
        Sends an authentication request to the API with the give credentials.
        param username: A username string.
        param password: A password string.
        """
        data = {'username': username, 'password': password}
        url = self.base_url.format('/login/authenticate')
        r = self.s.post(url, data=json.dumps(data))
        api_key = r.json()['token']
        self._set_key(api_key)

    def _iterate_chunks(self, values, chunk_size):
        """
        Breaks the list 'values' down into chunks of size 'chunk_size' and 
        returns these chunks. 
        param values: A list of arbitrary values.
        param chunk_size: An integer indicating the chunk size.
        """
        for pos in range(0, len(values), chunk_size):
            yield values[pos:pos + chunk_size]

    #@cache
    def search_for_concepts(self, terms, additional_fields=None, chunk_size=150):
        """
        Mimics the search bar of the Euretos mindmap, but allows for multiple terms
        to be searched at the same time. The list 'terms' can contain any number
        of arbitrary strings. Concepts are searched for in chunks to respect the
        query limits.
        param terms: A list of strings.
        param additional_fields: Optional, a list of additional fields. 
                                 (See Swagger docs)
        param chunk_size: Optional, size of the request chunks.
        """
        url = self.base_url.format('/external/concepts/search')
        concepts = []
        for chunk_terms in self._iterate_chunks(terms, chunk_size):
            query_string = ' OR '.join('term:\'{}\''.format(term) for term in chunk_terms)
            data = {
                'queryString': query_string,
                'searchType': 'TOKEN'
            }
            if additional_fields is not None:
                data['additionalFields'] = additional_fields
            for response in self._iterate_paginated_endpoint(url, data):
                concepts.extend(response)
        return concepts

    #@cache
    def ids_to_concepts(self, ids, prefix, type_=None, flatten=True):
        """
        A generalized function to search for Euretos concepts by some database
        identifier. This function utlizes the synonym list of a function to find
        concepts with a synonym in the format '<db_prefix><identifier>'.
        param ids: A list of identifiers from any Euretos-curated database.
        param prefix: The database name, as prefixed by Euretos.
        param type_: Optional, each concept dict returned has a key 'type_' with 
                     the supplied value.
        param flatten: Optional, flatten the concept dictionary. See method
                       '_flatten_concepts'.
        """
        concepts = self.search_for_concepts(ids, ['synonyms'])
        mapped_concepts = defaultdict(list)
        for concept in concepts:
            if 'id' in concept and 'name' in concept:
                concept['type'] = type_
                for synonym in concept['synonyms']:
                    if synonym['name'] not in ids:
                        continue
                    #if not synonym['name'].startswith(prefix):
                        #continue
                    if len(prefix) > 0:
                        _, id_ = synonym['name'].split(prefix)
                    else:
                        id_ = synonym['name']
                    del concept['synonyms']
                    mapped_concepts[id_].append(concept)
                    break
        return self._flatten_concepts(mapped_concepts) if flatten else mapped_concepts

    #@cache
    def chebis_to_concepts(self, chebis, flatten=True):
        """
        Return a list of Euretos concepts based on an input list of ChEBI identifiers.
        Identifiers should not be prefixed with 'CHEBI:'.
        param chebis: A list of ChEBI identifiers.
        param flatten: Optional, flatten the concept dictionary. See method
                       '_flatten_concepts'.
        """
        chebis = ['[chebi]{}'.format(chebi.lstrip('CHEBI:')).lower() for chebi in chebis]
        return self.ids_to_concepts(chebis, '[chebi]', 'metabolite', flatten)

    #@cache
    def entrez_to_concepts(self, entrez_ids, flatten=True):
        """
        Return a list of Euretos concepts based on an input list of Entrez identifiers.
        param entrez_ids: List of Entrez identifiers.
        param flatten: Optional, flatten the concept dictionary. See method
                       '_flatten_concepts'.
        """
        entrez_ids = ['[entrezgene]{}'.format(entrez).lower() for entrez in entrez_ids]
        return self.ids_to_concepts(entrez_ids, '[entrezgene]', 'gene', flatten)

    #@cache
    def ensg_to_concepts(self, ensembl_ids, flatten=True):
        """
        Return a list of Euretos concepts based on an input list of Ensembl identifiers.
        param ensembl_ids: List of Ensembl identifiers.
        param flatten: Optional, flatten the concept dictionary. See method
                       '_flatten_concepts'.
        """
        ensembl_ids = ['{}'.format(ensembl).lower() for ensembl in ensembl_ids]
        #this format assumes the ENSG prefix is included in the input ids.
        return self.ids_to_concepts(ensembl_ids, 'ensg', 'gene', flatten)

    #@cache
    def mesh_to_concepts(self, mesh_ids, flatten=True):
        """
        Return a list of Euretos concepts based on an input list of MeSH identifiers.
        param ensembl_ids: List of MeSH identifiers.
        param flatten: Optional, flatten the concept dictionary. See method
                       '_flatten_concepts'.
        """
        mesh_ids = ['{}'.format(mesh_id) for mesh_id in mesh_ids]
        return self.ids_to_concepts(mesh_ids, '', 'metabolite', flatten)

    def anyid_to_concepts(self, ids, flatten=True):
        """
        Return a list of Euretos concepts based on an input list of any identifiers.
        param ids: List of identifiers.
        param flatten: Optional, flatten the concept dictionary. See method
                       '_flatten_concepts'.
        """
        ids = ['{}'.format(id_).lower() for id_ in ids]
        return self.ids_to_concepts(ids, '', 'any', flatten)

    def symbols_to_concepts(self, symbols, organism, flatten=True):
        """
        Return a list of Euretos gene concepts of the specified organism based on an 
        input list of gene symbols. The parameter organism should be the scientific name
        of the organism, e.g. 'Homo sapiens'.
        param symbols: A list of gene symbols.
        param organism: An organism name, e.g. 'Homo sapiens'.
        param flatten: Optional, flatten the concept dictionary. See method
                       '_flatten_concepts'.
        """
        terms = ['{} ({})'.format(symbol, organism) for symbol in symbols]
        return self.ids_to_concepts(terms, '[entrezgene]', 'gene', flatten)

    def gene_name_to_concepts(self, gene_names):
        """
        Return a list of Euretos concepts based on an input list of gene names.
        These concepts are recognized by the 'gene' suffix.
        param gene_names: A list of gene names.
        """
        names = ['{} gene'.format(gene) for gene in gene_names]
        return self.search_for_concepts(names)
        
    def _find_triple_ids(self, concept_ids):
        """
        Returns the identifiers of the triples for which at least one of the concepts in 
        the input concept list is either the subject or object of.
        param concept_ids: A list of concepts identifiers.
        """
        url = self.base_url.format('/external/concept-to-concept/direct')
        triple_ids = set()
        data = {
            'additionalFields': ['tripleIds'],
            'leftInputs': concept_ids,
            'rightInputs': concept_ids,
            'relationshipWeightAlgorithm': 'PWS', 
            'sort': 'ASC' 
        }
        r = self.s.post(url, data=json.dumps(data), params={'size': 9999})
        for x in r.json()['content']:
            if x['concepts'][0]['id'] == x['concepts'][1]['id']:
                continue
            for relationship in x['relationships']:
                triple_ids.update(relationship['tripleIds'])
        return list(triple_ids)
        
    def find_triples(self, concepts):
        """
        Returns the triples for which at least one of the concepts in the input concept 
        list is either the subject or object of.
        param concepts: A list of concepts. See class doc.
        """
        triple_ids = self._find_triple_ids(concepts)
        url = self.base_url.format('/external/triples')
        data = {
            'additionalFields': ['publicationIds', 'predicateName'],
            'ids': triple_ids
        }
        r = self.s.post(url, data=json.dumps(data))
        triples = []
        for triple in r.json():
            triples.append({
                'id': triple['predicateId'],
                'name': triple['predicateName'],
                'tripleId': triple['id'],
                'source': triple['subjectId'],
                'target': triple['objectId'],
                'publicationCount': len(triple['publicationIds'])
            })
        return triples

    #@cache
    def find_direct_connections(self, concept_ids, algorithm='pws'):
        """
        Find concepts that are directly connected to at least one of the given
        concepts.
        param concept_ids: A list of Euretos concept identifiers.
        param algorithm: Optional, the algorithm used to calculate scores.
                         (See Swagger docs)
        """
        url = self.base_url.format('/external/direct-connections-with-scores')
        data = {
            'ids': concept_ids,
            'relationshipWeightAlgorithm': algorithm
        }
        ipe = self._iterate_paginated_endpoint # shorten
        return [concept for concepts in ipe(url, data) for concept in concepts]

    def _iterate_paginated_endpoint(self, url, data, pages=None, debug=False):
        """
        Iterates over the pages of a paginated endpoint.
        param url: The url to which to send a request.
        param data: A dictionary with the request body.
        param pages: Number of pages to iterate over. If None, all pages are iterated.
        param debug: Print info if True.
        """
        if debug:
            print('Iterating paginated endpoint:')
            print('\tPage: 1')
        params = {'size': 10000} # ~ max return size
        r = self.s.post(url, data=json.dumps(data), params=params).json()
        #print(r)
        if 'content' in r:
            yield r['content']
            pages = r['totalPages'] if pages is None else min(pages, r['totalPages'])
            for page in range(1, pages):
                if debug: print('\tPage: {}/{}'.format(page + 1, pages))
                params['page'] = page
                r = self.s.post(url, data=json.dumps(data), params=params).json()
                yield r['content']
        else:
            print(r)
            raise Exception('Response has no content')

    def find_go_concepts(self, semantic_type='38'):
        """
        Find all concepts of the Gene Ontology with the supplied semantic type.
        This semantic type identifier is necessary to retrieve GO terms of that
        specific hierarchy, e.g. Molecular function. Default value is 44, which
        is the Euretos identifier (T044) for Molecular function.
        param semantic_type: Euretos semantic type identifier.
        """
        url = self.base_url.format('/external/concepts/search')
        query_string = 'source:\'go\' AND semantictype:\'{}\''
        data = {
            'searchType': 'TOKEN',
            'queryString': query_string.format(semantic_type)
        }
        ipe = self._iterate_paginated_endpoint # shorten
        go_concepts = [concept for concepts in ipe(url, data) for concept in concepts]
        # Remove duplicate GO concepts
        return list({go['id']: go for go in go_concepts}.values())

    def search_disorders(self, disorder):
        """
        Find a concept of the category 'Disorder' based on string.
        param disorder: Name of disorder.
        """
        url = self.base_url.format('/external/concepts/search')
        query_string = 'term:\'{}\' AND semanticcategory:\'{}\''.format(disorder, 'Disorders')
        data = {'queryString': query_string, 'searchType': 'TOKEN'}
        r = self.s.post(url, data=json.dumps(data))
        return r.json()
        
    def find_connected(self, concept_ids, concept_id):
        """
        Filters the list 'concept_ids' down to concepts connected to
        'concept_id' with the predicate type 'is associated with'.
        param concept_ids: A list of concept identifiers.
        param concept_id: A concept identifier.
        """
        url = self.base_url.format('/external/concept-to-concept/direct')
        data = {
            'additionalFields': ['predicateNames'],
            'leftInputs': concept_ids,
            'rightInputs': [concept_id],
            'relationshipWeightAlgorithm': 'PWS', 
            'sort': 'ASC' 
        }
        r = self.s.post(url, data=json.dumps(data))
        connections = []
        for connection in r.json()['content']:
            if 'is associated with' in connection['relationships'][0]['predicateNames']:
                connections.append(connection['concepts'][0]['id'])
        return connections

    def find_direct_connections_count(self, concept_ids):
        """
        Finds the number of connections a concept has in Euretos for a
        list of concepts. This is done using a loop because the Euretos
        API does not return individual connections counts for a list of
        concepts. An error is thrown when the connection fails 5 times.
        """
        totalCounts = list()
        url = self.base_url.format('/external/direct-connections-count')
        for concept_id in concept_ids:
            data = {
                'additionalFields': ["totalCount"],
                'ids': [concept_id]
            }
            for tries in range(5):
                try:
                    r = self.s.post(url, data=json.dumps(data))
                    totalCounts.append(r.json()['totalCount'])
                    break
                except:
                    if tries == 4:
                        raise Exception("Connection error")
        return totalCounts


    def pathway_analysis(self, concept_ids, size=20):
        """
        NO PAGING IS USED!!
        """
        url = self.base_url.format('/external/gene-expression-analysis/pathway-analysis')
        data = {
            'conceptIds': concept_ids
        }
        params = {'size': size} # ~ max return size

        r = self.s.post(url, data=json.dumps(data), params=params).json()

        return r['content']


    def category_analysis(self, concept_ids, size=20, semantic_type='T044'):
        url = self.base_url.format('/external/gene-expression-analysis/category-analysis')
        data = {
            'conceptIds': concept_ids,
            'semanticType': semantic_type
        }
        params = {'size': size} # ~ max return size

        r = self.s.post(url, data=json.dumps(data), params=params).json()
        return r['content']
'''
{
  "conceptIds": [
    4223819, 2556487
  ],
  "semanticType": "43"
}
'''
