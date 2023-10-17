#!/usr/bin/env python3
'''
11. Where can I learn Python?
'''


def schools_by_topic(mongo_collection, topic):
    '''Returns the list of school having a specific topic'''
    topics = {'topics': {'$in': [topic]}}
    return list(mongo_collection.find(topics))
