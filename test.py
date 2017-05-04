#!/usr/bin/python3

from engine import BehaviorTree

test_json = """
{
	"name": "root",
	"class": "Node",
	"children": [
		{
			"name": "child1",
			"class": "Node",
			"children":[]
		}
	]
}
"""

bt = BehaviorTree(test_json)