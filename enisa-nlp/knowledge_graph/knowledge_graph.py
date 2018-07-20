#!/usr/bin/env python3
"""This script processes the knowledge graph from the configuration file.
Here is an example on how to write a configuration file.

[threats]
category = Threats
subcategories =
  Web application attacks
  . Cross-Site Scripting, XSS
  . Local File Inclusion, LFI
  . Remote File Inclusion, RFI
  . SQL injection
  . Cross-Site Request Forgery, CSRF

The term in brackets defines a section in the configuration file and corresponds to one of the main legs
from the knowledge graph, linked to the cyber security blob.
The term that will be used for searching in elasticsearch is defined in the category variable.
In case there are multiple synonyms or abbreviations for this term, a comma-separated string can be used.
The subcategories variable defines the lower level of the knowledge graph.
Parents are writen with an indent and children are written with an indent followed by a dot.
"""

from configparser import ConfigParser
from pathlib import Path


class KnowledgeGraph:

    def __init__(self):
        self.cyber_security = dict()
        self.knowledge_graph = list()
        self.synonyms = list()

        self.read_config()


    def read_config(self):
        parser = ConfigParser()
        parser.read(str(Path(Path(__file__).parent / 'knowledge_graph.cfg')))
        #parser.read('knowledge_graph.cfg')

        for section_name in parser.sections():
            d = dict()
            for name, value in parser.items(section_name):
                d[name] = value
            self.cyber_security[section_name] = d


    def get_dictionary_per_category(self, subcategories_string):
        """Turn the string of subcategories into a dictionary with parents as keys and children as values.
        In case there are no children, an empty list will appear.
        """

        d = dict()
        for line in subcategories_string.split('\n'):
            # Skip empty lines
            if line.strip() == "":
                continue
            # A line beginning with a dot contains a child category.
            if line[0] == '.':
                d[parent].append(line[2:].lower())
            # A line without a dot contains a parent category.
            else:
                parent = line.lower()
                d[parent] = list()
        return d


    def get_synonyms_parent_to_children(self, subcategories_dict):
        """Turn the dictionary with parents as keys and children as values
        into a mapping of parent => parent, children.

        In case there are no children, parent => parent will be kept.
        Such line does not define any synonyms but it is important for the get_synonyms_category_to_subcategories
        to do the grandparent => grandparent, parents mapping correctly.

        Args:
            subcategories_dict: Dictionary with parents as keys and children as values.

        Returns:
            List of lines (strings) defining the synonyms for elasticsearch analyzers.
        """

        synonyms = list()
        for k, v in subcategories_dict.items():
            s = '"' + k + ' => ' + k
            if len(v):
                s += ', ' + ', '.join(v)
            s += '",'
            synonyms.append(s)

        return synonyms


    def get_synonyms_category_to_subcategories(self, category, subcategories_dict):
        """Turn the dictionary with parents as keys and children as values
        into a mapping of category => category, parents, children as well as
        parent => parent, children (for each parent).

        Args:
            category: Cyber security category (grandparent).
            subcategories_dict: Dictionary with parents as keys and children as values.

        Returns:
            List of lines (strings) defining the synonyms for elasticsearch analyzers.
        """

        synonyms = self.get_synonyms_parent_to_children(subcategories_dict)

        s = '"{} => {}, '.format(category, category)
        for k, v in subcategories_dict.items():
            s += k + ', '
            if len(v):
                s += ', '.join(v) + ', '
        s = s[:-2] + '",'

        synonyms.append(s)
        return synonyms


    def extract_knowledge_graph(self, printout=True):
        """This method extracts the hierarchy of terms from the full konwledge graph
        in the form of a list of lines (strings) defining the synonyms for elasitcsearch analyzers.
        This method uses the cyber_security dictionary as an input, make sure to run read_config() first.
        """

        self.knowledge_graph = list()
        for k, v in self.cyber_security.items():
            subcategories_dict = self.get_dictionary_per_category(v['subcategories'])
            synonyms = self.get_synonyms_category_to_subcategories(v['category'], subcategories_dict)
            self.knowledge_graph += synonyms
            if printout:
                for line in synonyms:
                    print(line)
                print()


    def extract_synonyms(self, printout=True):
        """This method extracts the synonyms from the full knowledge graph
        in the form of a list of lines (strings) defining the synonyms for elasitcsearch analyzers.
        These are the true synonyms, not the knowledge graph hierarchy as in the case of the get_knowledge_graph()
        method. This method extracts the synonyms from the cyber_security_dict items (category and subcategories)
        that are separated by a comma.
        This method uses the cyber_security dictionary as an input, make sure to run read_config() first.
        """

        self.synonyms = list()

        def extract_synonyms(s):
            if ',' in s:
                synonym = '"{} => {}",'.format(s, s)
                self.synonyms.append(synonym)
                if printout:
                    print(synonym)

        for k, v in self.cyber_security.items():
            # Extract synonyms in case there are comma-separated values in the category string (grandparent).
            extract_synonyms(v['category'])
            subcategories_dict = self.get_dictionary_per_category(v['subcategories'])
            for parent, children in subcategories_dict.items():
                # Extract synonyms in case there are comma-separated values in the sub-category parent.
                extract_synonyms(parent)
                for child in children:
                    # Extract synonyms in case there are comma-separated values in the sub-category children.
                    extract_synonyms(child)


    def get_terms_per_category(self, category):
        """Returns all terms per category from the knowledge graph as a list."""
        def get_terms(s):
            return [x.strip() for x in s.lower().split(',')]

        try:
            terms = get_terms(self.cyber_security[category]["category"])
            for line in self.cyber_security[category]["subcategories"].split('\n'):
                # Skip empty lines
                if line.strip() == "":
                    continue
                # A line beginning with a dot contains a child category.
                if line[0] == '.':
                    terms += get_terms(line[2:])
                # A line without a dot contains a parent category.
                else:
                    terms += get_terms(line)
        except KeyError:
            pass
        return terms


if __name__ == "__main__":
    kg = KnowledgeGraph()
    kg.extract_knowledge_graph()
    kg.extract_synonyms()
