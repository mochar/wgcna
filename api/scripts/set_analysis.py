from euretos import Euretos
import json
import random
from multiprocessing import Pool
import time
import csv
import os
import pandas as pd

class Set_analysis:
    def __init__(self, annotation_source, min_connected=3, annotation_count=20):
        source_dict = {'Pathway': 'Pathway',
                        'Molecular Function': 'T044',
                        'Cell Function': 'T043',
                        'Organ or Tissue Function': 'T042',
                        'Biologic Function': 'T038'
    #phenotype
                        }

        try:
            self.annotation_source = source_dict[annotation_source]
        except:
            raise Exception('Annotation source not valid')


        self.euretos = Euretos('config.ini')
        self.pool_size = 1
        self.min_connected = int(min_connected)
        self.annotation_count = int(annotation_count)

    def load_modules_json(self, path, id_type):
        '''
        This function loads a dictionary with ids.
        All the ids in the dictionary are converted to euretos ids.
        The modules are then stored in a dictionary where the key is
        the module name and the value is the list of ids for that
        module.
        '''
        if type(path) == str:
            modules = json.load(open(path, 'r'))
        elif type(path) == dict:
            modules = path
        else:
            raise Exception('Path as no valid type')

        keys = []
        modules_list = []
        for key, module in modules.items():
            keys.append(key)
            modules_list.append(module)

        function_dict = {'Entrez': self.euretos.entrez_to_concepts,
                        'ENSG': self.euretos.ensg_to_concepts,
                        'ChEBI': self.euretos.chebis_to_concepts,
                        'Euretos synonym': self.euretos.anyid_to_concepts}

        try:
            concept_function = function_dict[id_type]
        except:
            raise Exception('Invalid id type:', id_type)

        with Pool(self.pool_size) as p:
            concepts_list = p.map(concept_function, modules_list)

        for item in zip(keys, concepts_list):
            key, concepts = item
            euretos_ids = [int(concept['id']) for concept in concepts]
            modules[key] = euretos_ids

        return modules

    def load_modules_webtool(self, project_folder, id_type):
        '''
        This function loads modules from a modules.csv file.
        All the ids in the dictionary are converted to euretos ids.
        The modules are then stored in a dictionary where the key is
        the module name and the value is the list of ids for that
        module.
        '''

        # get list of euretos ids
        genetree_path = os.path.join(project_folder, 'genetree.csv')
        modules_path = os.path.join(project_folder, 'modules.csv')

        genetree = json.load(open(genetree_path, 'r'))
        source_ids = genetree['ordered']

        #concept_list = self.euretos.anyid_to_concepts(source_ids)
        #euretos_ids = [int(concept['id']) for concept in concept_list]

        # get list of modules with same ordering as ids
        df = pd.read_csv(modules_path)

        use_premade_modules = True # Uses modules.csv for all data.
        if use_premade_modules:
            module_names = list(df.module)
            source_ids = list(df.name) # For using modules.csv as input
        else:
            module_names = list(df.modules)

        # convert into dictionary
        if len(module_names) != len(source_ids):
            raise Exception('Number of module assignments is not equal to number of ids.')

        modules = {}
        for pair in zip(module_names, source_ids):
            module_name, source_id = pair
            try:
                modules[module_name].append(source_id)
            except KeyError:
                modules[module_name] = [source_id]

        modules = self.load_modules_json(modules, id_type)

        return modules

    def permutate_module(self, modules, module_length):
        '''
        This function makes a permutated module witht the same size of
        the real module based on the ids of all modules.
        '''
        all_members = []
        for key, module in modules.items():
            all_members += module

        random.shuffle(all_members)

        new_module = []
        for i in range(module_length):
            new_module.append(all_members.pop())

        return new_module

    def get_annotation(self, module_members, details=False):
        '''
        This functions obtains a list of annotations for a list of
        Euretos ids.
        '''
        annotations = []

        #TODO better error handling
        delay = 1
        while delay < 32:
            try:
                if self.annotation_source == 'Pathway':
                    pathways = self.euretos.pathway_analysis(module_members,
                                size=200)
                else:
                    pathways = self.euretos.category_analysis(module_members,
                                size=200, semantic_type=self.annotation_source)
                break
            except:
                #print('pathway analysis on module failed:')
                #print(module_members)
                time.sleep(delay)
                delay *= 2
        else:
            raise Exception('Connection error')


        for pathway in pathways:
            if len(annotations) < self.annotation_count: # Add pathways until there are 20
                if pathway['connectedGenesCount'] >= self.min_connected:
                    if details:
                        annotations.append([pathway['candidateName'],
                                pathway['connectedGenesCount'], 
                                '{:.2E}'.format(pathway['pValue'])])
                    else:
                        annotations.append(pathway['candidateName'])

        return annotations

    def annotation_overlap(self, annotationA, annotationB):
        '''
        This function returns the overlap between two lists of annotations.
        '''
        return len(set(annotationA) & set(annotationB))

    def annotate(self, project_folder, id_type):
        '''
        This function annotatates the modules in the input file.
        '''
        modules = self.load_modules_webtool(project_folder, id_type)

        modules_annotations = {}

        for key, module in modules.items():
            annotations = self.get_annotation(module, details=True)
            modules_annotations[key] = annotations

        annotations_file = os.path.join(project_folder, 'annotations.json')

        json.dump(modules_annotations, open(annotations_file, 'w'))

        return modules_annotations

        annotation_file = os.path.join(project_folder, 'annotations.csv')
        with open(annotation_file, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['module', 'annotation', 'connected genes', 'pValue'])
            for key, module in modulesA.items():
                annotations = self.get_annotation(module, details=True)
                for annotation in annotations:
                    csvwriter.writerow([key] + annotation)

    def make_real_matrix(self, project_folderA, project_folderB, id_typeA, id_typeB):
        '''
        This function calculates the overlap of annotations between two
        files with annotations.
        '''
        modulesA = self.load_modules_webtool(project_folderA, id_typeA)
        modulesB = self.load_modules_webtool(project_folderB, id_typeB)

        annotationsA = {}

        for key, module in modulesA.items():
            annotationsA[key] = self.get_annotation(module)

        annotationsB = {}

        for key, module in modulesB.items():
            annotationsB[key] = self.get_annotation(module)

        overlap_list = []

        for keyA, annotationA in annotationsA.items():
            for keyB, annotationB in annotationsB.items():
                overlap_list.append([keyA, keyB,
                            self.annotation_overlap(annotationA, annotationB),
                            annotationA, annotationB,
                            list(set(annotationA) & set(annotationB))])

        return overlap_list

        # TODO re-enable for MinP?
        with open('./real', 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['omic1', 'omic2', 'overlap'])
            for keyA, annotationA in annotationsA.items():
                for keyB, annotationB in annotationsB.items():
                    csvwriter.writerow([keyA, keyB,
                            self.annotation_overlap(annotationA, annotationB)])

    def make_permutation_row(self, modulesA, modulesB, module_lengthA, module_lengthB):
        '''
        This functions calculates all permutations for two modules.
        '''
        permutated_modulesA = []
        permutated_modulesB = []

        for i in range(100):
            permutated_modulesA.append(self.permutate_module(modulesA, module_lengthA))

        for i in range(100):
            permutated_modulesB.append(self.permutate_module(modulesB, module_lengthB))

        with Pool(self.pool_size) as p:
            permutated_annotationsA = p.map(self.get_annotation, permutated_modulesA)
            permutated_annotationsB = p.map(self.get_annotation, permutated_modulesB)

        overlap_scores = []

        for annotationA in permutated_annotationsA:
            for annotationB in permutated_annotationsB:
                overlap_scores.append(self.annotation_overlap(annotationA, annotationB))

        return overlap_scores

    def make_permutation_matrix(self, project_folderA, project_folderB):
        '''
        This function calculates the permutation matrix.
        '''
        modulesA = self.load_modules_webtool(project_folderA)
        modulesB = self.load_modules_webtool(project_folderB)

        with open('/tmp/wgcna_out/permutations', 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            for keyA, moduleA in modulesA.items():
                for keyB, moduleB in modulesB.items():
                    print(keyA, keyB)
                    overlap_scores = self.make_permutation_row(modulesA,
                                    modulesB, len(moduleA), len(moduleB))
                    csvwriter.writerow(overlap_scores)


if __name__ == "__main__":
    pass
    #set_analysis = Set_analysis('Pathway')
    #set_analysis.annotate()
    #set_analysis.make_real_matrix()
    #set_analysis.make_permutation_matrix()
