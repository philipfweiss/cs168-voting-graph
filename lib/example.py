"""
CS168 Mini-Project by Philip Weiss.

See below for examples of how to use DatasetGenerator
"""
from DatasetGenerator import *

def year_from_session_id(session_id):
    return (session_id * 2) + 1788

def example():
    dg = DatasetGenerator()
    graphs = dg.generate_datasets()
    for (issue, session_id), (matrix, senator_ids) in graphs.items():
        print(f"issue: {issue}")
        print(f"session_id: {session_id}")
        print(f"matrix: {matrix.shape}")
        print(f"congress_ids: {len(senator_ids)}")
        print("-----")

    # Map from senator_id, session_id -> party 
    parties = dg.member_party_map
example()