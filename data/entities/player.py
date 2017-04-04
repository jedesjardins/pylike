{
	"Misc": {
		"name": "Player"
	},
	"Controlled": {
		"actions": {
			"up": "w",
			"down": "s",
			"left": "a",
			"right": "d"
		}
	},
	"Sprite": {
		"file": "$0",
		"frames": 12,
		"columns": 3,
		"frame_rect": {
			"x": 0,
			"y": 0,
			"w": 24,
			"h": 32
		},
		"edge_buffer": {
			"left": 3,
			"right": 3,
			"top": 3,
			"bottom": 3
		}
	},
	"Animation": {
		"frame_rect": {
			"x": 0,
			"y": 0,
			"w": 24,
			"h": 32
		},
		"actions": {	
			"up": {
				"name": "up",
				"frames": [3, 4, 3, 5],
				"length": 500
			},
			"down": {
				"name": "down",
				"frames": [0, 1, 0, 2],
				"length": 500
			},
			"left": {
				"name": "left",
				"frames": [6, 7, 6, 8],
				"length": 500
			},	
			"right": {
				"name": "right",
				"frames": [9, 10, 9, 11],
				"length": 500
			}
		}
	},
	"Hitbox": {
		"rect": {
			"x": 0,
			"y": 0,
			"w": 18,
			"h": 26
		}
	},
	"Hold": {
		"hand_locations": []
	},
	"Inventory": {
		"items": []
	}
}