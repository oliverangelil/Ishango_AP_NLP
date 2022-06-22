from neo4j import GraphDatabase
from collections import Counter
import itertools


class Neo4jConnect:
    def __init__(self, uri, user, password):
        """
            uri: [neo4j, neo4j+s, bolt+s, bolt] neo4j does not support https
            user: username
            password: password
        """
        self.db_uri = uri
        self.db_user = user
        self.db_pass = password

        self.driver = None

        try:
            self.driver = GraphDatabase.driver(
                self.db_uri, auth=(self.db_user, self.db_pass))
        except Exception as err:
            print("Failed to connect to Database: ", err)

    @staticmethod
    def unpackResults(items2unpack: list) -> list:
        """
            Helper fucntion:
                unpack a list of lists into list
        """
        return list(itertools.chain(*items2unpack))

    def getEntities(self) -> dict:
        """
            Returns a dictionary:
                key: database entity (node)
                value: number of occurence
        """
        query = "MATCH (n) RETURN labels(n)"
        if self.driver is not None:
            with self.driver.session() as session:
                result = session.run(query)
                node_results = [dict(ii)['labels(n)'][0] for ii in result]
        else:
            print("No connected to Neo4j")
        return dict(Counter(node_results))

    def getRelations(self):
        """
            return a dictionary:
                key: database relationship type
                value: number of occurence
        """
        query = "MATCH p=()-[r]-() RETURN TYPE(r)"
        if self.driver is not None:
            with self.driver.session() as session:
                result = session.run(query)
                relations = [dict(i)['TYPE(r)'] for i in result]
        else:
            pass
        return dict(Counter(relations))

    def getProperties(self) -> dict:
        """
            return a dictionary:
                key: database properties key
                value: number of occurence
        """
        query = "MATCH (n) RETURN KEYS(n)"
        if self.driver is not None:
            with self.driver.session() as session:
                result = session.run(query)
                props_results = [dict(i)['KEYS(n)'] for i in result]
                props_keys = self.unpackResults(props_results)
        else:
            pass
        return dict(Counter(props_keys))

    def getArticles(self) -> dict:
        """
            Returns a dictionary:
                key: articleId
                value: dictionary(datePublished: mainArticle)
        """
        if self.driver is not None:
            query = """
                    MATCH (n:Article)
                    RETURN n.articleId,
                    n.description, n.author, n.headline,
                    n.articleBody, n.datePublished,
                    n.probability
                    """
            with self.driver.session() as session:
                ent_props = session.run(query)
                ent_props = [dict(i) for i in ent_props]
                articles = {
                    i['n.articleId']:
                    {'date': i['n.datePublished'],
                     'author': i['n.author'],
                     'headline': i['n.headline'],
                     'propability': i['n.probability'],
                     'desciption': i['n.description'],
                     'mainArticle': i['n.articleBody']}
                    for i in ent_props}
        self.driver.close()
        return articles