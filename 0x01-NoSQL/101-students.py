#!/usr/bin/env python3
'''
14. Top students
'''


def top_students(mongo_collection):
    '''Returns all students sorted by average score'''
    avgFilter = [
        {
            '$project': {
                '_id': 1,
                'name': 1,
                'averageScore': {
                    '$avg': '$topics.score'
                }
            }
        },
        {
            '$sort': {'averageScore': -1}
        }
    ]
    return list(mongo_collection.aggregate(avgFilter))
