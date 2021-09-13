import sys
sys.path.append("./config.yaml")
from config import *

from neo4j import __version__ as neo4j_version
from neo4j import GraphDatabase
import pandas as pd
import re
from fuzzywuzzy import process

# Define a connection class to connect to the graph database.
class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response

# Create an instance of connection with the required parameters-the url,username and password
url = get_url()
username = get_username()
password = get_password()
conn = Neo4jConnection(uri=url, user=username, pwd=password)


def preprocess(input_list):
    # PREPROCESSING OF INPUT STATEMENTS
    # Remove leading & trailing spaces
    pre_input = [inp.strip() for inp in input_list]
    # Remove unwanted special characters
    pre_input1 = [re.sub(r"[^a-z&,%\ ]", " ", inp.lower()) for inp in pre_input]
    # Prefix removal
    serial_rem=[]
    for p in pre_input1:
        if re.match(r"^\w\s+", p):
            text1 = re.sub(r"^\w\s+", "", p)
            serial_rem.append(text1)
        elif re.match(r"^by ", p):
            text1 = re.sub(r"by ", "", p)
            serial_rem.append(text1)
        elif re.match(r"^to ", p):
            text1 = re.sub(r"to ", "", p)
            serial_rem.append(text1)
        else:
            serial_rem.append(p)
    # Conversion of '&' to 'and'
    serial_rem1 = []
    for s in serial_rem:
        if re.search(r"&", s):
            text1 = re.sub(r"&", "and", s)
            serial_rem1.append(text1)
        else:
            serial_rem1.append(s)
    # Remove leading & trailing spaces again
    serial_rem1 = [inp.strip() for inp in serial_rem1]
    # Remove extra space between words
    serial_rem1 = [re.sub(' +', ' ', inp) for inp in serial_rem1]
    # Remove empty statements for querying graph
    preprocessed_input = [inp.strip() for inp in serial_rem1 if inp.strip()]
    return serial_rem1, preprocessed_input


def query_graph(branchname, preprocessed_list):
    # QUERY TO MAP FINANCIAL STATEMENTS TO GRAPH MODEL
    # Choose appropriate branch for querying
    if branchname == 'BS':
        branch = ':BalanceSheet'
    elif branchname == 'IS':
        branch = ':IncomeStmt'
    elif branchname == 'CF':
        branch = ':CashFlow'
    else:  # Choose entire graph
        branch = ''
    query_string = '''
    WITH {inp_list} as items
    MATCH (stmt)-[*]-> (header{branchname})
    WHERE any(item IN items where stmt.title = item and header:Level0)
    RETURN labels(stmt) as Labels,stmt.title as Statements,header.title as `Statement Type`
    ORDER BY id(stmt)
    UNION
    WITH {inp_list} as items
    MATCH (stmt)-[*]-> (header{branchname})
    WHERE any(item IN items where (
    ((item CONTAINS 'turnover') and (stmt:`Level1.1`)) or
    ((item CONTAINS 'cost' or item CONTAINS 'outlay' or item CONTAINS 'total cost' or item CONTAINS 'total outlay') and (stmt:`Level4.0a`)) or
    ((item CONTAINS 'due' or item CONTAINS 'outstanding') and (item CONTAINS 'micro' or item CONTAINS 'small' or item CONTAINS 'medium' or item CONTAINS 'msme' or item CONTAINS 'enterprise') and NOT(item CONTAINS 'other') and(stmt:`Level4b.1`)) or
    ((item CONTAINS 'enterprise' or item CONTAINS 'small' or item CONTAINS 'msme') and NOT (item CONTAINS 'outstanding') and NOT (item CONTAINS 'due') and(stmt:`Level4b.2`)) or
    ((item CONTAINS 'due' or item CONTAINS 'outstanding') and (item CONTAINS 'micro' or item CONTAINS 'small' or item CONTAINS 'medium' or item CONTAINS 'msme' or item CONTAINS 'enterprise' or item CONTAINS 'other') and(stmt:`Level4b.3`)) or
    ((item CONTAINS 'enterprise' or item CONTAINS 'small' or item CONTAINS 'msme') and NOT (item CONTAINS 'outstanding') and NOT (item CONTAINS 'due') and(stmt:`Level4b.4`)) or
    ((item CONTAINS 'due' or item CONTAINS 'outstanding') and (item CONTAINS 'micro' or item CONTAINS 'small' or item CONTAINS 'medium' or item CONTAINS 'msme' or item CONTAINS 'enterprise') and NOT(item CONTAINS 'other') and(stmt:`Level4b.5`)) or
    ((item CONTAINS 'enterprise' or item CONTAINS 'small' or item CONTAINS 'msme') and NOT (item CONTAINS 'outstanding') and NOT (item CONTAINS 'due') and(stmt:`Level4b.6`)) or
    ((item CONTAINS 'due' or item CONTAINS 'outstanding') and (item CONTAINS 'micro' or item CONTAINS 'small' or item CONTAINS 'medium' or item CONTAINS 'msme' or item CONTAINS 'enterprise' or item CONTAINS 'other') and(stmt:`Level4b.7`)) or
    ((item CONTAINS 'enterprise' or item CONTAINS 'small' or item CONTAINS 'msme') and NOT (item CONTAINS 'outstanding') and NOT (item CONTAINS 'due') and(stmt:`Level4b.8`)) or
    ((item CONTAINS 'advance') and (item CONTAINS 'from') and (stmt:`Level4c`)) or
    ((item CONTAINS 'raw material') and (item CONTAINS 'consum' or item CONTAINS 'used') and (stmt:`Level4.1`)) or
    ((item CONTAINS 'purchase') and (item CONTAINS 'stock in trade' or item CONTAINS 'finished goods' or item CONTAINS 'raw material' or item CONTAINS 'goods')  and(stmt:`Level4.2`)) or
    ((item CONTAINS 'change') and (item CONTAINS 'value' or item CONTAINS 'inventory' or item CONTAINS 'inventories')  and(stmt:`Level4.3`)) or
    ((item CONTAINS 'work in progress' or item CONTAINS 'stock in trade' or item CONTAINS 'finished goods') and (stmt:`Level4.3`)) or
    ((item CONTAINS 'increase') and (item CONTAINS 'decrease') and (item CONTAINS 'inventories' or item CONTAINS 'inventory') and (stmt:`Level4.4`)) or
    ((item CONTAINS 'purchase') and (item CONTAINS 'duty' or item CONTAINS 'tax') and (stmt:`Level4.11`)) or
    ((item CONTAINS 'cost of goods sold') and (stmt:`Level4.13`)) or
    ((item CONTAINS 'gross profit') and (stmt:`Level4.14`)) or
    ((item CONTAINS 'gross') and (item CONTAINS 'profit') and (stmt:`Level4.15`)) or
    ((item CONTAINS 'personnel') and (stmt:`Level4.16`)) or
    ((item CONTAINS 'direct') and (item CONTAINS 'expense') and NOT (item CONTAINS 'indirect') and (stmt:`Level4.20`)) or
    ((item CONTAINS 'cash in hand') and (stmt:Level5a)) or
    ((item CONTAINS 'capital') and NOT(item CONTAINS 'work') and (stmt:Level5b)) or
    ((item CONTAINS 'furniture' or item CONTAINS 'plant' or item CONTAINS 'machinery' or item CONTAINS 'equipment') and (stmt:Level5c)) or
    ((item CONTAINS 'fixed asset') and (stmt:Level5d)) or
    ((item CONTAINS 'working capital' or item CONTAINS 'cash credit' or item CONTAINS 'cc ') and (stmt:Level5e)) or
    ((item CONTAINS 'term loan' or item CONTAINS 'car loan' or item CONTAINS 'housing loan' or item CONTAINS 'loan against property' or item CONTAINS 'lap') and (stmt:Level5f)) or
    
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning') and (item CONTAINS 'before' or item CONTAINS 'pre') and (item CONTAINS 'depreciation') and (stmt:`Level5.1`)) or 
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning') and (item CONTAINS 'before' or item CONTAINS 'pre') and (item CONTAINS 'interest') and NOT (item CONTAINS 'minority') and (stmt:`Level5.1`)) or
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning') and (item CONTAINS 'before' or item CONTAINS 'pre') and (item CONTAINS 'finance') and (stmt:`Level5.1`)) or
    ((item CONTAINS 'result') and (item CONTAINS 'operation' or item CONTAINS 'operating') and (stmt:`Level5.4`)) or
    ((item CONTAINS 'result') and (item CONTAINS 'operation' or item CONTAINS 'operating') and (stmt:`Level5.5`)) or
    ((item CONTAINS 'depreciation') and (stmt:Level6a)) or
    ((item CONTAINS 'accountancy' or item CONTAINS 'accounting' or item CONTAINS 'audit') and (stmt:`Level8.0`)) or
    ((item CONTAINS 'impairment') and (stmt:`Level8.3`)) or
    ((item CONTAINS 'exceptional') and NOT(item CONTAINS 'profit') and NOT(item CONTAINS 'loss') and (stmt:`Level10.0`)) or
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning') and (item CONTAINS 'before' or item CONTAINS 'pre') and (item CONTAINS 'exceptional') and (stmt:Level9)) or
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning') and (item CONTAINS 'before' or item CONTAINS 'pre') and (item CONTAINS 'extraordinary' or item CONTAINS 'share' or item CONTAINS 'associate' or item CONTAINS 'appropriation') and (stmt:Level11)) or
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning') and (item CONTAINS 'after' or item CONTAINS 'post') and (item CONTAINS 'extraordinary') and (stmt:Level11a)) or
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning') and (item CONTAINS 'before' or item CONTAINS 'pre') and (item CONTAINS 'prior period') and (stmt:Level13)) or
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning' or item CONTAINS 'surplus' or item CONTAINS 'deficit') and
     (item CONTAINS 'before' or item CONTAINS 'pre') and (item CONTAINS 'ordinary') and NOT(item CONTAINS 'extra') and (stmt:Level15)) or
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning' or item CONTAINS 'surplus' or item CONTAINS 'deficit') and
     (item CONTAINS 'before' or item CONTAINS 'pre') and (item CONTAINS 'income' or item CONTAINS 'tax') and NOT(item CONTAINS 'extra') and NOT(item CONTAINS 'associate') and NOT(item CONTAINS 'exceptional') and (stmt:Level15)) or
    ((item CONTAINS 'balance' or item CONTAINS 'profit') and (item CONTAINS 'c d' or item CONTAINS 'carried' or item CONTAINS 'transfer' or item CONTAINS 'transferred' ) and (stmt:Level15)) or
    ((item CONTAINS 'net' or item CONTAINS 'book') and (item CONTAINS 'profit') and NOT(item CONTAINS 'year') and NOT(item CONTAINS 'group') and NOT(item CONTAINS 'consolidated') and
     NOT(item CONTAINS 'associate') and NOT(item CONTAINS 'joint') and NOT(item CONTAINS 'venture') and NOT(item CONTAINS 'after') and NOT(item CONTAINS 'post') and(stmt:Level15)) or
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'result') and (item CONTAINS 'pre tax' or item CONTAINS 'pre') and (stmt:`Level15`)) or
    ((item CONTAINS 'income') and (item CONTAINS 'tax') and (item CONTAINS 'expense') and (stmt:`Level16.4`)) or
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning' or item CONTAINS 'surplus' or item CONTAINS 'deficit') and
     (item CONTAINS 'after' or item CONTAINS 'post') and (item CONTAINS 'tax') and NOT(item CONTAINS 'before') and NOT(item CONTAINS 'pre') and (stmt:Level17)) or
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning' or item CONTAINS 'surplus' or item CONTAINS 'deficit') and
     (item CONTAINS 'for') and (item CONTAINS 'period') and NOT(item CONTAINS 'before') and NOT(item CONTAINS 'pre') and (stmt:Level17)) or
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning' or item CONTAINS 'surplus' or item CONTAINS 'deficit') and
     (item CONTAINS 'from') and NOT(item CONTAINS 'discontinuing') and NOT(item CONTAINS 'discontinued') and (item CONTAINS 'operations') and NOT(item CONTAINS 'before') and NOT(item CONTAINS 'pre') and (stmt:Level17)) or
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning' or item CONTAINS 'surplus' or item CONTAINS 'deficit') and
     (item CONTAINS ' continuing')and (item CONTAINS 'operations') and NOT(item CONTAINS 'before') and NOT(item CONTAINS 'pre') and (stmt:Level17)) or 
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning' or item CONTAINS 'surplus' or item CONTAINS 'deficit') and
     (item CONTAINS 'for ') and (item CONTAINS ' continuing') and NOT(item CONTAINS 'before') and NOT(item CONTAINS 'pre') and (stmt:Level17)) or
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning' or item CONTAINS 'surplus' or item CONTAINS 'deficit') and
     (item CONTAINS 'for ') and (item CONTAINS 'year') and NOT(item CONTAINS 'before') and NOT(item CONTAINS 'pre') and (stmt:Level17)) or
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning' or item CONTAINS 'surplus' or item CONTAINS 'deficit') and
     (item CONTAINS 'to') and (item CONTAINS 'capital') and NOT(item CONTAINS 'before') and NOT(item CONTAINS 'pre') and (stmt:Level17)) or
    ((item CONTAINS 'net profit') and (item CONTAINS 'group' or item CONTAINS 'consolidated') and NOT(item CONTAINS 'before') and NOT(item CONTAINS 'pre') and (stmt:Level17)) or
    ((item CONTAINS 'pat ') and (stmt:`Level17.1`)) or
    ((item CONTAINS 'net surplus') and (stmt:Level17b)) or
    ((item CONTAINS 'profit' or item CONTAINS 'loss' or item CONTAINS 'earning' or item CONTAINS 'surplus' or item CONTAINS 'deficit' or item CONTAINS 'result') and
     (item CONTAINS 'for ') and NOT(item CONTAINS 'pre tax') AND NOT(item CONTAINS 'pre') AND NOT(item CONTAINS 'before') and NOT(item CONTAINS 'other') and
     NOT(item CONTAINS 'comprehensive') and NOT(item CONTAINS 'impairment') and NOT(item CONTAINS 'extraordinary') and NOT(item CONTAINS 'share') and
     NOT(item CONTAINS 'sharing') and NOT(item CONTAINS 'investment') and NOT(item CONTAINS 'statement') and NOT(item CONTAINS 'march') and
     NOT(item CONTAINS 'discontinued') and NOT(item CONTAINS 'discontinuing') and (stmt:`Level17.3`)) or
    ((item CONTAINS 'other comprehensive income') and NOT (item CONTAINS 'equity') and NOT (item CONTAINS 'debt') and (stmt:`Level18.0`)) or
    ((item CONTAINS 'change' or item CONTAINS 'remeasurement') and (item CONTAINS 'defined benefit' or item CONTAINS 'obligation') and (stmt:`Level18.2`)) or
    ((item CONTAINS 'fair value' or item CONTAINS 'fvtoc') and (item CONTAINS 'equity' or item CONTAINS 'debt' or item CONTAINS 'financial instrument' or item CONTAINS 'financial asset') and (stmt:`Level18.3`)) or
    ((item CONTAINS 'income tax') and (item CONTAINS 'reclassified' or item CONTAINS 'effect') and (stmt:`Level18.4`)) or
    ((item CONTAINS 'fair value' or item CONTAINS 'fvtoc') and (item CONTAINS 'equity' or item CONTAINS 'debt' or item CONTAINS 'financial instrument' or item CONTAINS 'financial asset') and (stmt:`Level18.6`)) or
    ((item CONTAINS 'effective') and (item CONTAINS 'cash flow') and (stmt:`Level18.7`)) or
    ((item CONTAINS 'income tax') and (item CONTAINS 'reclassified' or item CONTAINS 'effect') and (stmt:`Level18.8`))
     )and header:Level0) 
    RETURN labels(stmt) as Labels,stmt.title as Statements,header.title as `Statement Type`
    ORDER BY id(stmt)
    '''.format(inp_list=preprocessed_list, branchname=branch)
    # Get the mapped statements
    data = pd.DataFrame([dict(_) for _ in conn.query(query_string)])
    return data

def start_graph_process(input_dict):
    # Call the preprocessing function
    pre_list_with_empty_stmt, pre_list_without_empty_stmt = preprocess(input_dict['lineitem_list'])
    # Call the function for querying the graph
    data = query_graph(input_dict['branch_name'], pre_list_without_empty_stmt)
    if data.empty:
        print("NONE OF THE STATEMENTS ARE MAPPED TO GRAPH NODES")
    else:
        labels = data.iloc[:, 0].values.tolist()
        statement = data.iloc[:, 1].values.tolist()
        stmt_type = data.iloc[:, 2].values.tolist()
        # Reordering the labels
        pattern = r'Level[0-9]+[.]*[0-9]*'
        for label in labels:
            if re.search(pattern, label[1]):
                label[0], label[1] = label[1], label[0]

        avail_index=[]
        indexed = []
        input_data = pre_list_with_empty_stmt.copy()

        # Find the input list index for the mapped statements
        for i, stmt in enumerate(statement):
            for j, list_data in enumerate(input_data):
                if stmt == list_data and stmt not in avail_index:
                    indexed.append((stmt, j, labels[i],stmt_type[i]))
                    avail_index.append(stmt)
                    input_data[j] = ''

        # Find the mapped statements that are not indexed
        not_indexed = []
        not_indexed_label = []
        not_indexed_stmt_type = []
        for i, stmt in enumerate(statement):
            if stmt not in avail_index:
                not_indexed.append(stmt)
                not_indexed_label.append(labels[i])
                not_indexed_stmt_type.append(stmt_type[i])

        # Match the mapped non-indexed statements with input list based on keywords
        matched_stmt = []
        match_kw = []
        not_indexed_label1 = []
        not_indexed1 = []
        not_indexed_stmt_type1 = []

        for i, item in enumerate(not_indexed):
            if 'Level1.1' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['turnover'])]
            elif 'Level4.0a' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            ((all(word in sent for word in ['cost']) or all(word in sent for word in ['outlay'])) and
                             len(sent.split()) == 1) or
                            all(word in sent for word in ['total cost']) or
                            all(word in sent for word in ['total outlay'])]
            elif 'Level4b.1' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            (all(word in sent for word in ['due', 'micro']) or
                             all(word in sent for word in ['due', 'small']) or
                             all(word in sent for word in ['due', 'medium']) or
                             all(word in sent for word in ['due', 'msme']) or
                             all(word in sent for word in ['due', 'enterprise']) or
                             all(word in sent for word in ['outstanding', 'micro']) or
                             all(word in sent for word in ['outstanding', 'small']) or
                             all(word in sent for word in ['outstanding', 'medium']) or
                             all(word in sent for word in ['outstanding', 'msme']) or
                             all(word in sent for word in ['outstanding', 'enterprise'])) and
                            all(word1 not in sent for word1 in ['other'])]
            elif 'Level4b.2' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            (all(word in sent for word in ['enterprise']) or
                             all(word in sent for word in ['small']) or
                             all(word in sent for word in ['msme'])) and
                            (all(word1 not in sent for word1 in ['outstanding']) or
                             all(word2 not in sent for word2 in ['due']))]
            elif 'Level4b.3' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['due', 'micro']) or
                            all(word in sent for word in ['due', 'small']) or
                            all(word in sent for word in ['due', 'medium']) or
                            all(word in sent for word in ['due', 'msme']) or
                            all(word in sent for word in ['due', 'enterprise']) or
                            all(word in sent for word in ['due', 'other']) or
                            all(word in sent for word in ['outstanding', 'micro']) or
                            all(word in sent for word in ['outstanding', 'small']) or
                            all(word in sent for word in ['outstanding', 'medium']) or
                            all(word in sent for word in ['outstanding', 'msme']) or
                            all(word in sent for word in ['outstanding', 'enterprise']) or
                            all(word in sent for word in ['outstanding', 'other'])]
            elif 'Level4b.4' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            (all(word in sent for word in ['enterprise']) or
                             all(word in sent for word in ['small']) or
                             all(word in sent for word in ['msme'])) and
                            (all(word1 not in sent for word1 in ['outstanding']) or
                             all(word2 not in sent for word2 in ['due']))]
            elif 'Level4b.5' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            (all(word in sent for word in ['due', 'micro']) or
                             all(word in sent for word in ['due', 'small']) or
                             all(word in sent for word in ['due', 'medium']) or
                             all(word in sent for word in ['due', 'msme']) or
                             all(word in sent for word in ['due', 'enterprise']) or
                             all(word in sent for word in ['outstanding', 'micro']) or
                             all(word in sent for word in ['outstanding', 'small']) or
                             all(word in sent for word in ['outstanding', 'medium']) or
                             all(word in sent for word in ['outstanding', 'msme']) or
                             all(word in sent for word in ['outstanding', 'enterprise'])) and
                            all(word1 not in sent for word1 in ['other'])]
            elif 'Level4b.6' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            (all(word in sent for word in ['enterprise']) or
                             all(word in sent for word in ['small']) or
                             all(word in sent for word in ['msme'])) and
                            (all(word1 not in sent for word1 in ['outstanding']) or
                             all(word2 not in sent for word2 in ['due']))]
            elif 'Level4b.7' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['due', 'micro']) or
                            all(word in sent for word in ['due', 'small']) or
                            all(word in sent for word in ['due', 'medium']) or
                            all(word in sent for word in ['due', 'msme']) or
                            all(word in sent for word in ['due', 'enterprise']) or
                            all(word in sent for word in ['due', 'other']) or
                            all(word in sent for word in ['outstanding', 'micro']) or
                            all(word in sent for word in ['outstanding', 'small']) or
                            all(word in sent for word in ['outstanding', 'medium']) or
                            all(word in sent for word in ['outstanding', 'msme']) or
                            all(word in sent for word in ['outstanding', 'enterprise']) or
                            all(word in sent for word in ['outstanding', 'other'])]
            elif 'Level4b.8' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            (all(word in sent for word in ['enterprise']) or
                             all(word in sent for word in ['small']) or
                             all(word in sent for word in ['msme'])) and
                            (all(word1 not in sent for word1 in ['outstanding']) or
                             all(word2 not in sent for word2 in ['due']))]
            elif 'Level4c' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['advance', 'from'])
                            ]
            elif 'Level4.1' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['raw material', 'consum']) or
                            all(word in sent for word in ['raw material', 'used'])
                            ]
            elif 'Level4.2' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['purchase', 'stock in trade']) or
                            all(word in sent for word in ['purchase', 'finished goods']) or
                            all(word in sent for word in ['purchase', 'raw material']) or
                            all(word in sent for word in ['purchase', 'goods'])
                            ]
            elif 'Level4.3' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['change', 'value']) or
                            all(word in sent for word in ['change', 'inventory']) or
                            all(word in sent for word in ['change', 'inventories']) or
                            all(word in sent for word in ['work in progress']) or
                            all(word in sent for word in ['stock in trade']) or
                            all(word in sent for word in ['finished goods'])]
            elif 'Level4.4' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['increase', 'decrease', 'inventory']) or
                            all(word in sent for word in ['increase', 'decrease', 'inventories'])]
            elif 'Level4.11' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['purchase', 'duty']) or
                            all(word in sent for word in ['purchase', 'tax'])
                            ]
            elif 'Level4.13' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['cost of goods sold'])]
            elif 'Level4.14' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['gross profit'])]
            elif 'Level4.15' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['gross', 'profit'])]
            elif 'Level4.16' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['personnel'])]
            elif 'Level4.20' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['direct', 'expense']) and
                            (all(word1 not in sent for word1 in ['indirect']))]
            elif 'Level5a' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['cash in hand'])]
            elif 'Level5b' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            (all(word in sent for word in ['capital']) and
                             (all(word1 not in sent for word1 in ['work'])))]
            elif 'Level5c' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['furniture']) or
                            all(word in sent for word in ['plant']) or
                            all(word in sent for word in ['machinery']) or
                            all(word in sent for word in ['equipment'])]
            elif 'Level5d' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['fixed asset'])]
            elif 'Level5e' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['working capital']) or
                            all(word in sent for word in ['cash credit']) or
                            all(word in sent for word in ['cc '])]
            elif 'Level5f' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['term loan']) or
                            all(word in sent for word in ['car loan']) or
                            all(word in sent for word in ['housing loan']) or
                            all(word in sent for word in ['loan against property']) or
                            all(word in sent for word in ['lap'])]
            elif 'Level5.1' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['profit', 'before', 'depreciation']) or
                            (all(word in sent for word in ['profit', 'before', 'interest']) and
                             (all(word1 not in sent for word1 in ['minority']))) or
                            all(word in sent for word in ['profit', 'before', 'finance']) or
                            all(word in sent for word in ['profit', 'pre', 'depreciation']) or
                            (all(word in sent for word in ['profit', 'pre', 'interest']) and
                             (all(word1 not in sent for word1 in ['minority']))) or
                            all(word in sent for word in ['profit', 'pre', 'finance']) or

                            all(word in sent for word in ['loss', 'before', 'depreciation']) or
                            (all(word in sent for word in ['loss', 'before', 'interest']) and
                             (all(word1 not in sent for word1 in ['minority']))) or
                            all(word in sent for word in ['loss', 'before', 'finance']) or
                            all(word in sent for word in ['loss', 'pre', 'depreciation']) or
                            (all(word in sent for word in ['loss', 'pre', 'interest']) and
                             (all(word1 not in sent for word1 in ['minority']))) or
                            all(word in sent for word in ['loss', 'pre', 'finance']) or

                            all(word in sent for word in ['earning', 'before', 'depreciation']) or
                            (all(word in sent for word in ['earning', 'before', 'interest']) and
                             (all(word1 not in sent for word1 in ['minority']))) or
                            all(word in sent for word in ['earning', 'before', 'finance']) or
                            all(word in sent for word in ['earning', 'pre', 'depreciation']) or
                            (all(word in sent for word in ['earning', 'pre', 'interest']) and
                             (all(word1 not in sent for word1 in ['minority']))) or
                            all(word in sent for word in ['earning', 'pre', 'finance'])]
            elif 'Level5.4' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['result', 'operation']) or
                            all(word in sent for word in ['result', 'operating'])]
            elif 'Level5.5' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['result', 'operation']) or
                            all(word in sent for word in ['result', 'operating'])]
            elif 'Level6a' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['depreciation'])]
            elif 'Level8.0' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['accountancy']) or
                            all(word in sent for word in ['accounting']) or
                            all(word in sent for word in ['audit'])]
            elif 'Level8.3' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['impairment'])]
            elif 'Level10.0' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['exceptional']) and
                            all(word1 not in sent for word1 in ['profit']) and
                            all(word2 not in sent for word2 in ['loss'])]
            elif 'Level9' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['profit', 'before', 'exceptional']) or
                            all(word in sent for word in ['loss', 'before', 'exceptional']) or
                            all(word in sent for word in ['earning', 'before', 'exceptional']) or
                            all(word in sent for word in ['profit', 'pre', 'exceptional']) or
                            all(word in sent for word in ['loss', 'pre', 'exceptional']) or
                            all(word in sent for word in ['earning', 'pre', 'exceptional'])
                            ]
            elif 'Level11' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['profit', 'before', 'extraordinary']) or
                            all(word in sent for word in ['profit', 'before', 'share']) or
                            all(word in sent for word in ['profit', 'before', 'associate']) or
                            all(word in sent for word in ['profit', 'before', 'appropriation']) or
                            all(word in sent for word in ['profit', 'pre', 'extraordinary']) or
                            all(word in sent for word in ['profit', 'pre', 'share']) or
                            all(word in sent for word in ['profit', 'pre', 'associate']) or
                            all(word in sent for word in ['profit', 'pre', 'appropriation']) or
                            all(word in sent for word in ['loss', 'before', 'extraordinary']) or
                            all(word in sent for word in ['loss', 'before', 'share']) or
                            all(word in sent for word in ['loss', 'before', 'associate']) or
                            all(word in sent for word in ['loss', 'before', 'appropriation']) or
                            all(word in sent for word in ['loss', 'pre', 'extraordinary']) or
                            all(word in sent for word in ['loss', 'pre', 'share']) or
                            all(word in sent for word in ['loss', 'pre', 'associate']) or
                            all(word in sent for word in ['loss', 'pre', 'appropriation']) or
                            all(word in sent for word in ['earning', 'before', 'extraordinary']) or
                            all(word in sent for word in ['earning', 'before', 'share']) or
                            all(word in sent for word in ['earning', 'before', 'associate']) or
                            all(word in sent for word in ['earning', 'before', 'appropriation']) or
                            all(word in sent for word in ['earning', 'pre', 'extraordinary']) or
                            all(word in sent for word in ['earning', 'pre', 'share']) or
                            all(word in sent for word in ['earning', 'pre', 'associate']) or
                            all(word in sent for word in ['earning', 'pre', 'appropriation'])]

            elif 'Level11a' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['profit', 'after', 'extraordinary']) or
                            all(word in sent for word in ['loss', 'after', 'extraordinary']) or
                            all(word in sent for word in ['earning', 'after', 'extraordinary']) or
                            all(word in sent for word in ['profit', 'post', 'extraordinary']) or
                            all(word in sent for word in ['loss', 'post', 'extraordinary']) or
                            all(word in sent for word in ['earning', 'post', 'extraordinary'])]
            elif 'Level13' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['profit', 'before', 'prior period']) or
                            all(word in sent for word in ['loss', 'before', 'prior period']) or
                            all(word in sent for word in ['earning', 'before', 'prior period']) or
                            all(word in sent for word in ['profit', 'pre', 'prior period']) or
                            all(word in sent for word in ['loss', 'pre', 'prior period']) or
                            all(word in sent for word in ['earning', 'pre', 'prior period'])]
            elif 'Level15' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            ((all(word in sent for word in ['profit', 'before', 'ordinary'])) and
                             (all(word1 not in sent for word1 in ['extra']))) or
                            ((all(word in sent for word in ['loss', 'before', 'ordinary'])) and
                             (all(word1 not in sent for word1 in ['extra']))) or
                            ((all(word in sent for word in ['earning', 'before', 'ordinary'])) and
                             (all(word1 not in sent for word1 in ['extra']))) or
                            ((all(word in sent for word in ['surplus', 'before', 'ordinary'])) and
                             (all(word1 not in sent for word1 in ['extra']))) or
                            ((all(word in sent for word in ['deficit', 'before', 'ordinary'])) and
                             (all(word1 not in sent for word1 in ['extra']))) or
                            ((all(word in sent for word in ['profit', 'pre', 'ordinary'])) and
                             (all(word1 not in sent for word1 in ['extra']))) or
                            ((all(word in sent for word in ['loss', 'pre', 'ordinary'])) and
                             (all(word1 not in sent for word1 in ['extra']))) or
                            ((all(word in sent for word in ['earning', 'pre', 'ordinary'])) and
                             (all(word1 not in sent for word1 in ['extra']))) or
                            ((all(word in sent for word in ['surplus', 'pre', 'ordinary'])) and
                             (all(word1 not in sent for word1 in ['extra']))) or
                            ((all(word in sent for word in ['deficit', 'pre', 'ordinary'])) and
                             (all(word1 not in sent for word1 in ['extra']))) or

                            ((all(word in sent for word in ['profit', 'before', 'income']) or
                              all(word in sent for word in ['profit', 'before', 'tax'])) and
                             (all(word1 not in sent for word1 in ['extra'])) and
                             (all(word2 not in sent for word2 in ['associate'])) and
                             (all(word3 not in sent for word3 in ['exceptional']))) or
                            ((all(word in sent for word in ['loss', 'before', 'income']) or
                              all(word in sent for word in ['loss', 'before', 'tax'])) and
                             (all(word1 not in sent for word1 in ['extra'])) and
                             (all(word2 not in sent for word2 in ['associate'])) and
                             (all(word3 not in sent for word3 in ['exceptional']))) or
                            ((all(word in sent for word in ['earning', 'before', 'income']) or
                              all(word in sent for word in ['earning', 'before', 'tax'])) and
                             (all(word1 not in sent for word1 in ['extra'])) and
                             (all(word2 not in sent for word2 in ['associate'])) and
                             (all(word3 not in sent for word3 in ['exceptional']))) or
                            ((all(word in sent for word in ['surplus', 'before', 'income']) or
                              all(word in sent for word in ['surplus', 'before', 'tax'])) and
                             (all(word1 not in sent for word1 in ['extra'])) and
                             (all(word2 not in sent for word2 in ['associate'])) and
                             (all(word3 not in sent for word3 in ['exceptional']))) or
                            ((all(word in sent for word in ['deficit', 'before', 'income']) or
                              all(word in sent for word in ['deficit', 'before', 'tax'])) and
                             (all(word1 not in sent for word1 in ['extra'])) and
                             (all(word2 not in sent for word2 in ['associate'])) and
                             (all(word3 not in sent for word3 in ['exceptional']))) or
                            ((all(word in sent for word in ['profit', 'pre', 'income']) or
                              all(word in sent for word in ['profit', 'pre', 'tax'])) and
                             (all(word1 not in sent for word1 in ['extra'])) and
                             (all(word2 not in sent for word2 in ['associate'])) and
                             (all(word3 not in sent for word3 in ['exceptional']))) or
                            ((all(word in sent for word in ['loss', 'pre', 'income']) or
                              all(word in sent for word in ['loss', 'pre', 'tax'])) and
                             (all(word1 not in sent for word1 in ['extra'])) and
                             (all(word2 not in sent for word2 in ['associate'])) and
                             (all(word3 not in sent for word3 in ['exceptional']))) or
                            ((all(word in sent for word in ['earning', 'pre', 'income']) or
                              all(word in sent for word in ['earning', 'pre', 'tax'])) and
                             (all(word1 not in sent for word1 in ['extra'])) and
                             (all(word2 not in sent for word2 in ['associate'])) and
                             (all(word3 not in sent for word3 in ['exceptional']))) or
                            ((all(word in sent for word in ['surplus', 'pre', 'income']) or
                              all(word in sent for word in ['surplus', 'pre', 'tax'])) and
                             (all(word1 not in sent for word1 in ['extra'])) and
                             (all(word2 not in sent for word2 in ['associate'])) and
                             (all(word3 not in sent for word3 in ['exceptional']))) or
                            ((all(word in sent for word in ['deficit', 'pre', 'income']) or
                              all(word in sent for word in ['deficit', 'pre', 'tax'])) and
                             (all(word1 not in sent for word1 in ['extra'])) and
                             (all(word2 not in sent for word2 in ['associate'])) and
                             (all(word3 not in sent for word3 in ['exceptional']))) or

                            (all(word in sent for word in ['net', 'profit']) and
                             (all(word1 not in sent for word1 in ['year'])) and
                             (all(word2 not in sent for word2 in ['group'])) and
                             (all(word3 not in sent for word3 in ['consolidated'])) and
                             (all(word4 not in sent for word4 in ['associate'])) and
                             (all(word5 not in sent for word5 in ['joint'])) and
                             (all(word6 not in sent for word6 in ['venture'])) and
                             (all(word7 not in sent for word7 in ['after'])) and
                             (all(word8 not in sent for word8 in ['post']))) or
                            (all(word in sent for word in ['book', 'profit']) and
                             (all(word1 not in sent for word1 in ['year'])) and
                             (all(word2 not in sent for word2 in ['group'])) and
                             (all(word3 not in sent for word3 in ['consolidated'])) and
                             (all(word4 not in sent for word4 in ['associate'])) and
                             (all(word5 not in sent for word5 in ['joint'])) and
                             (all(word6 not in sent for word6 in ['venture'])) and
                             (all(word7 not in sent for word7 in ['after'])) and
                             (all(word8 not in sent for word8 in ['post']))) or

                            all(word in sent for word in ['profit', 'c d']) or
                            all(word in sent for word in ['profit', 'transfer']) or
                            all(word in sent for word in ['profit', 'transferred']) or
                            all(word in sent for word in ['profit', 'carried']) or
                            all(word in sent for word in ['balance', 'c d']) or
                            all(word in sent for word in ['balance', 'transfer']) or
                            all(word in sent for word in ['balance', 'transferred']) or
                            all(word in sent for word in ['balance', 'carried']) or

                            all(word in sent for word in ['profit', 'pre tax']) or
                            all(word in sent for word in ['profit', 'pre']) or
                            all(word in sent for word in ['loss', 'pre tax']) or
                            all(word in sent for word in ['loss', 'pre']) or
                            all(word in sent for word in ['result', 'pre tax']) or
                            all(word in sent for word in ['result', 'pre'])]

            elif 'Level16.4' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['income', 'tax', 'expense'])]

            elif 'Level17' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            (input_data.index(sent) not in [0, 1, 2, 3]) and
                            ((all(word in sent for word in ['profit', 'after', 'tax']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['loss', 'after', 'tax']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['earning', 'after', 'tax']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['surplus', 'after', 'tax']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['deficit', 'after', 'tax']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['profit', 'post', 'tax']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['loss', 'post', 'tax']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['earning', 'post', 'tax']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['surplus', 'post', 'tax']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['deficit', 'post', 'tax']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or

                             (all(word in sent for word in ['profit', 'for', 'period']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre'])) and
                              not re.match(r".*for\b.*\bprofit.*", sent)) or
                             (all(word in sent for word in ['loss', 'for', 'period']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre'])) and
                              not re.match(r".*for\b.*\bloss.*", sent)) or
                             (all(word in sent for word in ['earning', 'for', 'period']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre'])) and
                              not re.match(r".*for\b.*\bearning.*", sent)) or
                             (all(word in sent for word in ['surplus', 'for', 'period']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre'])) and
                              not re.match(r".*for\b.*\bsurplus.*", sent)) or
                             (all(word in sent for word in ['deficit', 'for', 'period']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre'])) and
                              not re.match(r".*for\b.*\bdeficit.*", sent)) or

                             (all(word in sent for word in ['profit', 'from', 'operations']) and
                              (all(word1 not in sent for word1 in ['discontinuing'])) and
                              (all(word2 not in sent for word2 in ['before'])) and
                              (all(word3 not in sent for word3 in ['discontinued'])) and
                              (all(word4 not in sent for word4 in ['pre']))) or
                             (all(word in sent for word in ['loss', 'from', 'operations']) and
                              (all(word1 not in sent for word1 in ['discontinuing'])) and
                              (all(word2 not in sent for word2 in ['before'])) and
                              (all(word3 not in sent for word3 in ['discontinued'])) and
                              (all(word4 not in sent for word4 in ['pre']))) or
                             (all(word in sent for word in ['earning', 'from', 'operations']) and
                              (all(word1 not in sent for word1 in ['discontinuing'])) and
                              (all(word2 not in sent for word2 in ['before'])) and
                              (all(word3 not in sent for word3 in ['discontinued'])) and
                              (all(word4 not in sent for word4 in ['pre']))) or
                             (all(word in sent for word in ['surplus', 'from', 'operations']) and
                              (all(word1 not in sent for word1 in ['discontinuing'])) and
                              (all(word2 not in sent for word2 in ['before'])) and
                              (all(word3 not in sent for word3 in ['discontinued'])) and
                              (all(word4 not in sent for word4 in ['pre']))) or
                             (all(word in sent for word in ['deficit', 'from', 'operations']) and
                              (all(word1 not in sent for word1 in ['discontinuing'])) and
                              (all(word2 not in sent for word2 in ['before'])) and
                              (all(word3 not in sent for word3 in ['discontinued'])) and
                              (all(word4 not in sent for word4 in ['pre']))) or

                             (all(word in sent for word in ['profit', ' continuing', 'operations']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['loss', ' continuing', 'operations']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['earning', ' continuing', 'operations']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['surplus', ' continuing', 'operations']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['deficit', ' continuing', 'operations']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or

                             (all(word in sent for word in ['profit', 'for ', ' continuing']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre'])) and
                              not re.match(r".*for\b.*\bprofit.*", sent)) or
                             (all(word in sent for word in ['loss', 'for ', ' continuing']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre'])) and
                              not re.match(r".*for\b.*\bloss.*", sent)) or
                             (all(word in sent for word in ['earning', 'for ', ' continuing']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre'])) and
                              not re.match(r".*for\b.*\bearning.*", sent)) or
                             (all(word in sent for word in ['surplus', 'for ', ' continuing']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre'])) and
                              not re.match(r".*for\b.*\bsurplus.*", sent)) or
                             (all(word in sent for word in ['deficit', 'for ', ' continuing']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre'])) and
                              not re.match(r".*for\b.*\bdeficit.*", sent)) or

                             (all(word in sent for word in ['profit', 'for ', 'year']) and
                              (all(word1 not in sent for word1 in ['statement'])) and
                              (all(word2 not in sent for word2 in ['march'])) and
                              (all(word3 not in sent for word3 in ['before'])) and
                              (all(word4 not in sent for word4 in ['pre'])) and
                              not re.match(r".*for\b.*\bprofit.*", sent)) or
                             (all(word in sent for word in ['loss', 'for ', 'year']) and
                              (all(word1 not in sent for word1 in ['statement'])) and
                              (all(word2 not in sent for word2 in ['march'])) and
                              (all(word3 not in sent for word3 in ['before'])) and
                              (all(word4 not in sent for word4 in ['pre'])) and
                              not re.match(r".*for\b.*\bloss.*", sent)) or
                             (all(word in sent for word in ['earning', 'for ', 'year']) and
                              (all(word1 not in sent for word1 in ['statement'])) and
                              (all(word2 not in sent for word2 in ['march'])) and
                              (all(word3 not in sent for word3 in ['before'])) and
                              (all(word4 not in sent for word4 in ['pre'])) and
                              not re.match(r".*for\b.*\bearning.*", sent)) or
                             (all(word in sent for word in ['surplus', 'for ', 'year']) and
                              (all(word1 not in sent for word1 in ['statement'])) and
                              (all(word2 not in sent for word2 in ['march'])) and
                              (all(word3 not in sent for word3 in ['before'])) and
                              (all(word4 not in sent for word4 in ['pre'])) and
                              not re.match(r".*for\b.*\bsurplus.*", sent)) or
                             (all(word in sent for word in ['deficit', 'for ', 'year']) and
                              (all(word1 not in sent for word1 in ['statement'])) and
                              (all(word2 not in sent for word2 in ['march'])) and
                              (all(word3 not in sent for word3 in ['before'])) and
                              (all(word4 not in sent for word4 in ['pre'])) and
                              not re.match(r".*for\b.*\bdeficit.*", sent)) or

                             (all(word in sent for word in ['profit', 'to', 'capital']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['loss', 'to', 'capital']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['earning', 'to', 'capital']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['surplus', 'to', 'capital']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['deficit', 'to', 'capital']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or

                             (all(word in sent for word in ['net profit', 'group']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))) or
                             (all(word in sent for word in ['net profit', 'consolidated']) and
                              (all(word1 not in sent for word1 in ['before'])) and
                              (all(word2 not in sent for word2 in ['pre']))))
                            ]
            elif 'Level17.1' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['pat '])]
            elif 'Level17b' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['net surplus'])]

            elif 'Level17.3' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            (input_data.index(sent) not in [0, 1, 2, 3]) and
                            ((all(word in sent for word in ['profit', 'for']) and
                              all(word1 not in sent for word1 in ['pre tax']) and
                              all(word2 not in sent for word2 in ['tax']) and
                              all(word3 not in sent for word3 in ['before']) and
                              all(word4 not in sent for word4 in ['other']) and
                              all(word5 not in sent for word5 in ['comprehensive']) and
                              all(word6 not in sent for word6 in ['impairment']) and
                              all(word7 not in sent for word7 in ['extraordinary']) and
                              all(word8 not in sent for word8 in ['share']) and
                              all(word9 not in sent for word9 in ['sharing']) and
                              all(word10 not in sent for word10 in ['investment']) and
                              all(word11 not in sent for word11 in ['statement']) and
                              all(word12 not in sent for word12 in ['march']) and
                              all(word13 not in sent for word13 in ['discontinued']) and
                              all(word14 not in sent for word14 in ['discontinuing']) and
                              not re.match(r".*for\b.*\bprofit.*", sent)) or
                             (all(word in sent for word in ['loss', 'for']) and
                              all(word1 not in sent for word1 in ['pre tax']) and
                              all(word2 not in sent for word2 in ['tax']) and
                              all(word3 not in sent for word3 in ['before']) and
                              all(word4 not in sent for word4 in ['other']) and
                              all(word5 not in sent for word5 in ['comprehensive']) and
                              all(word6 not in sent for word6 in ['impairment']) and
                              all(word7 not in sent for word7 in ['extraordinary']) and
                              all(word8 not in sent for word8 in ['share']) and
                              all(word9 not in sent for word9 in ['sharing']) and
                              all(word10 not in sent for word10 in ['investment']) and
                              all(word11 not in sent for word11 in ['statement']) and
                              all(word12 not in sent for word12 in ['march']) and
                              all(word13 not in sent for word13 in ['discontinued']) and
                              all(word14 not in sent for word14 in ['discontinuing']) and
                              not re.match(r".*for\b.*\bloss.*", sent)) or
                             (all(word in sent for word in ['earning', 'for']) and
                              all(word1 not in sent for word1 in ['pre tax']) and
                              all(word2 not in sent for word2 in ['tax']) and
                              all(word3 not in sent for word3 in ['before']) and
                              all(word4 not in sent for word4 in ['other']) and
                              all(word5 not in sent for word5 in ['comprehensive']) and
                              all(word6 not in sent for word6 in ['impairment']) and
                              all(word7 not in sent for word7 in ['extraordinary']) and
                              all(word8 not in sent for word8 in ['share']) and
                              all(word9 not in sent for word9 in ['sharing']) and
                              all(word10 not in sent for word10 in ['investment']) and
                              all(word11 not in sent for word11 in ['statement']) and
                              all(word12 not in sent for word12 in ['march']) and
                              all(word13 not in sent for word13 in ['discontinued']) and
                              all(word14 not in sent for word14 in ['discontinuing']) and
                              not re.match(r".*for\b.*\bearning.*", sent)) or
                             (all(word in sent for word in ['surplus', 'for']) and
                              all(word1 not in sent for word1 in ['pre tax']) and
                              all(word2 not in sent for word2 in ['tax']) and
                              all(word3 not in sent for word3 in ['before']) and
                              all(word4 not in sent for word4 in ['other']) and
                              all(word5 not in sent for word5 in ['comprehensive']) and
                              all(word6 not in sent for word6 in ['impairment']) and
                              all(word7 not in sent for word7 in ['extraordinary']) and
                              all(word8 not in sent for word8 in ['share']) and
                              all(word9 not in sent for word9 in ['sharing']) and
                              all(word10 not in sent for word10 in ['investment']) and
                              all(word11 not in sent for word11 in ['statement']) and
                              all(word12 not in sent for word12 in ['march']) and
                              all(word13 not in sent for word13 in ['discontinued']) and
                              all(word14 not in sent for word14 in ['discontinuing']) and
                              not re.match(r".*for\b.*\bsurplus.*", sent)) or
                             (all(word in sent for word in ['deficit', 'for']) and
                              all(word1 not in sent for word1 in ['pre tax']) and
                              all(word2 not in sent for word2 in ['tax']) and
                              all(word3 not in sent for word3 in ['before']) and
                              all(word4 not in sent for word4 in ['other']) and
                              all(word5 not in sent for word5 in ['comprehensive']) and
                              all(word6 not in sent for word6 in ['impairment']) and
                              all(word7 not in sent for word7 in ['extraordinary']) and
                              all(word8 not in sent for word8 in ['share']) and
                              all(word9 not in sent for word9 in ['sharing']) and
                              all(word10 not in sent for word10 in ['investment']) and
                              all(word11 not in sent for word11 in ['statement']) and
                              all(word12 not in sent for word12 in ['march']) and
                              all(word13 not in sent for word13 in ['discontinued']) and
                              all(word14 not in sent for word14 in ['discontinuing']) and
                              not re.match(r".*for\b.*\bdeficit.*", sent)) or
                             (all(word in sent for word in ['result', 'for']) and
                              all(word1 not in sent for word1 in ['pre tax']) and
                              all(word2 not in sent for word2 in ['tax']) and
                              all(word3 not in sent for word3 in ['before']) and
                              all(word4 not in sent for word4 in ['other']) and
                              all(word5 not in sent for word5 in ['comprehensive']) and
                              all(word6 not in sent for word6 in ['impairment']) and
                              all(word7 not in sent for word7 in ['extraordinary']) and
                              all(word8 not in sent for word8 in ['share']) and
                              all(word9 not in sent for word9 in ['sharing']) and
                              all(word10 not in sent for word10 in ['investment']) and
                              all(word11 not in sent for word11 in ['statement']) and
                              all(word12 not in sent for word12 in ['march']) and
                              all(word13 not in sent for word13 in ['discontinued']) and
                              all(word14 not in sent for word14 in ['discontinuing']) and
                              not re.match(r".*for\b.*\bresult.*", sent)))]

            elif 'Level18.0' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['other comprehensive income']) and
                            (all(word1 not in sent for word1 in ['equity'])) and
                            (all(word2 not in sent for word2 in ['debt']))]
            elif 'Level18.2' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['change', 'defined benefit']) or
                            all(word in sent for word in ['change', 'obligation']) or
                            all(word in sent for word in ['remeasurement', 'defined benefit']) or
                            all(word in sent for word in ['remeasurement', 'obligation'])]
            elif 'Level18.3' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['fair value', 'equity']) or
                            all(word in sent for word in ['fair value', 'debt']) or
                            all(word in sent for word in ['fair value', 'financial instrument']) or
                            all(word in sent for word in ['fair value', 'financial asset']) or
                            all(word in sent for word in ['fvtoc', 'equity']) or
                            all(word in sent for word in ['fvtoc', 'debt']) or
                            all(word in sent for word in ['fvtoc', 'financial instrument']) or
                            all(word in sent for word in ['fvtoc', 'financial asset'])]
            elif 'Level18.4' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['income tax', 'reclassified']) or
                            all(word in sent for word in ['income tax', 'effect'])]
            elif 'Level18.6' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['fair value', 'equity']) or
                            all(word in sent for word in ['fair value', 'debt']) or
                            all(word in sent for word in ['fair value', 'financial instrument']) or
                            all(word in sent for word in ['fair value', 'financial asset']) or
                            all(word in sent for word in ['fvtoc', 'equity']) or
                            all(word in sent for word in ['fvtoc', 'debt']) or
                            all(word in sent for word in ['fvtoc', 'financial instrument']) or
                            all(word in sent for word in ['fvtoc', 'financial asset'])]
            elif 'Level18.7' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['effective', 'cash flow'])]
            elif 'Level18.8' in (not_indexed_label[i]):
                match_kw = [sent for sent in input_data if
                            all(word in sent for word in ['income tax', 'reclassified']) or
                            all(word in sent for word in ['income tax', 'effect'])]

            if match_kw:  # Check if the match list is not empty
                matched_stmt.append(match_kw[0])
                not_indexed_label1.append(not_indexed_label[i])
                not_indexed1.append(not_indexed[i])
                not_indexed_stmt_type1.append(not_indexed_stmt_type[i])
                remove_indexed = input_data.index(match_kw[0])
                input_data[remove_indexed] = ''

        # Append the input list index for keyword matched statements
        for i, match in enumerate(matched_stmt):
            for j, inp in enumerate(pre_list_with_empty_stmt):
                if match == inp:
                    # indexed.append((match, j, not_indexed_label1[i]))
                    indexed.append((not_indexed1[i], j, not_indexed_label1[i], not_indexed_stmt_type1[i]))
                    break

        # For mapping duplicate line items
        result = []
        index = []
        for i, item in enumerate(indexed):
            for j, inp in enumerate(pre_list_with_empty_stmt):
                if item[0] == inp and j not in index:
                    result.append((item[0], j, item[2], item[3]))
                    index.append(j)
                elif pre_list_with_empty_stmt[item[1]] == inp and j not in index:
                    result.append((item[0], j, item[2], item[3]))
                    index.append(j)

        if input_dict['branch_name'] == '':
            return result
        else:
            result_without_stmt_type=[]
            for i, item in enumerate(result):
                result_without_stmt_type.append((item[0], item[1], item[2]))
            return result_without_stmt_type