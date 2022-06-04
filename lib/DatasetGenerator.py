import numpy as np
import pickle
import collections

class DatasetGenerator:
    def __init__(self):
        self.issues = [
            'Foreign and Defense Policy',
            'Abortion',
            'Pollution and Environmental Protection',
            'Social Welfare',
            'Medicaid',
            'Civil Liberties',
            'Israel',
            'all',
        ]
        self.issue_call_map = self.load_pickle('./pickle/issue_call_map.pkl')
        self.issue_map, self.call_uid_map = {}, {}
        self.congresses = range(65, 115)
        self.load_congress_to_call_uid_map()
        self.load_issue_map()
        self.member_party_map = self.load_pickle('./pickle/member_party_map.pkl')

    def generate_datasets(self):
        graphs = {}
        for issue in self.issues:
            if issue != 'all':
                for session_id in self.congresses:
                    matrix, senator_ids = self.generate_dataset(self.issue_map[issue][session_id])
                    if np.sum(matrix) > 2000:
                        graphs[(issue, session_id)] = matrix, senator_ids
            else:
                for session_id in self.congresses: 
                    matrix, senator_ids = self.generate_dataset(self.call_uid_map[session_id].values())
                    if np.sum(matrix) > 2000:
                        graphs[(issue, session_id)] = matrix, senator_ids

        return graphs

    def generate_dataset(self, rollcalls):
       
        all_senators = set()
        for rc in rollcalls:
            for key in rc.votes.keys():
                for senator in rc.votes[key]: 
                    all_senators.add(senator)
        sen_list = list(all_senators)
        all_senators = {v:k for k, v in enumerate(sen_list)}
        dim = len(all_senators)
        matrix = np.zeros((dim, dim))
        
        for rc in rollcalls:
            for key in rc.votes.keys():
                vec = np.zeros(dim)
                for senator in rc.votes[key]: 
                    vec[all_senators[senator]] = 1
                matrix += np.outer(vec, vec)
        return matrix, sen_list

    def generateAdjacencyMatrix(self, votes):
        nodes = set()
        for pair in votes.keys(): nodes |= set(pair)
        dim = len(nodes)
        matrix = np.matrix.shape((dim, dim))
        for k, v in votes.items():
            matrix[k[0], k[1]] = v
            matrix[k[1], k[0]] = v

        return matrix

    def load_pickle(self, file):
        with open(file, "rb") as input_file: return pickle.load(input_file)

    def load_issue_map(self):
        for issue in self.issues:
            roll_call_uids = self.issue_call_map[issue]
            self.issue_map[issue] = collections.defaultdict(list)
            for uid in roll_call_uids: ## (congress#,rollcall#)
                congressID = uid[0]
                if congressID not in self.call_uid_map: continue
                self.issue_map[issue][congressID].append(self.call_uid_map[congressID][uid])

    def load_congress_to_call_uid_map(self):
        for i in self.congresses:
            self.call_uid_map[i] = self.load_pickle("./pickle/call_uid_map/congress_%d.pkl" % i)
