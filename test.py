#!/usr/bin/python3

from engine.behaviortree import BehaviorTree, Blackboard

test_json = """
{
	"name": "root",
	"class": "AlwaysTrueD",
	"children": [
		{
			"name": "chooseaction",
			"class": "Sequence",
			"children":[
				{
					"name": "movetoplayer",
					"class": "Sequence",
					"children":[
						{
							"name": "movetoplayer",
							"class": "Sequence",
							"children":[

							]
						}
					]
				},
				{
					"name": "movetodoor",
					"class": "Node",
					"children":[]
				},
				{
					"name": "idle",
					"class": "Node",
					"children":[]
				}
			]
		}
	]
}
"""

bt = BehaviorTree(test_json)
#bt.traverse(bt.root)
print(bt.update(None, None))

blck = Blackboard()

blck.store('root', True)
