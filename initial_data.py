

""" 
description of property parameters:

"way_grounded" : "left", "right", "not", "both" "inside"
"type": "VL", "single", "single_dielectric"
"PS": "left", "right", "not", "both",
"link_okgt" - generate automaticlu, without people
"""


okgt_info = {
    ("1","2"): [
        {
            "type": "VL",
            "name" : "one",
            "length": 10
        },
        {
            "type": "single_conductive",
            "name": "two", 
            "length": 5, 
            "groundwire":"ОКГТ-38", 
            "H_cable": 10,
            "X_cable": 0,
            "countercable": True,
            "H_countercable": 0.5,
            "X_countercable": 0.0,
            "D_countercable": 12,
            "point_grounded" : 3,
            "way_grounded": "both",
            "point_resistance": 30.0,
            "ground_resistance": 30.0,
        },
        {
            "type": "VL",
            "name" : "three",
            "length": 2 
        }
    ],
    ("2","3"):[
        {
            "type": "VL",
            "name" : "four",
            "length": 3 
        },
        {
            "type": "VL",
            "name" : "five",
            "length": 4 
        },
        {
            "type": "VL",
            "name" : "six",
            "length": 0.8 
        },
        {
            "type": "single_conductive",
            "name": "seven", 
            "length": 0.4, 
            "groundwire":"ОКГТ-38", 
            "H_cable": 10,
            "X_cable": 0,
            "countercable": False,
            "point_grounded" : 0,
            "way_grounded": "not",
        },
        {
            "type": "VL",
            "name" : "eight",
            "length": 0.8 
        },
        {
            "type": "VL",
            "name" : "nine",
            "length": 6.0 
        },
    ],
    ("2","4"): [
        {
            "type": "single_dielectric",
            "name" : "ten",
            "length": 0.6 
        },
        {
            "type": "VL",
            "name" : "eleven",
            "length": 4.0 
        },
        {
            "type": "single_dielectric",
            "name" : "twelve",
            "length": 0.6 
        },
    ],
}

vl_info = {
    "VL #1": {
        "branches" : {
            ("1","2") : {
                
                "PS": "both",
                "PS_name_1": "PS_1",
                "PS_name_2": "PS_2",
            },
        },
        "sectors": [
            {
                "type": "with_okgt",
                "link_okgt": "one",
                "lengthN": 3.3,
                "lengthK": 5.0,
                "link_branch": ("1","2"),
                "supportN" : 12,
                "supportK" : 26,
            },
            {
                "type": "with_okgt",
                "link_okgt": "one",
                "lengthN": 0.0,
                "lengthK": 3.3,
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 12,
            },
            {
                "type": "with_okgt",
                "link_okgt": "one",
                "lengthN": 5.0,
                "lengthK": 10.0,
                "link_branch": ("1","2"),
                "supportN" : 26,
                "supportK" : 51,
            },
            {
                "type": "without_okgt",
                "length": 2.0,
                "link_branch": ("1","2"),
                "supportN" : 51,
                "supportK" : 61,
            },
        ],
        "commonchains":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 51,
                "other_vl_name": "VL #5",
                "other_link_branch": ("1","2"),
                "other_supportN" : 1,
                "other_supportK" : 51,
            },
        ],
        "phases": [
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 51,
                "phase": "ABC"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 51,
                "supportK" : 61,
                "phase": "-BAC"
            },
        ],
        "conductors":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 61,
                "conductor": "AC 70/11"
            },
        ],
        "groundwires":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 51,
                "type": "one",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-38"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 51,
                "supportK" : 61,
                "type": "not",
                "is_okgt":None,
                "groundwire1": "AC 70/11"
            },
        ],
        "grounded": [
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 31,
                "type": "first",
                "resistance": 30.0
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 32,
                "supportK" : 61,
                "type": "first",
                "resistance": 15.0
            },
        ],
        "countercables":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 3,
                "H_countercable": 0.5,
                "X_countercable": 0.0,
                "D_countercable": 12,
                "ground_resistance": 30.0,
                "connect_to_ps": True,
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 6,
                "supportK" : 7,
                "H_countercable": 0.5,
                "X_countercable": 0.0,
                "D_countercable": 12,
                "ground_resistance": 30.0,
                "connect_to_ps": False,
            },
        ],
        "supports":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 51,
                "support": "ПБ(п)110-2/8"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 51,
                "supportK" : 61,
                "support": "ПБ-110-1,3,11,13"
            },
        ],
        "PSs":[
            {
                "PS_name": "PS_1",
                "length": 0.02,
            },
            {
                "PS_name": "PS_2",
                "length": 0.02,
            },
        ],
    },
    "VL #2": {
        "branches" : {
            ("1","2") : {
                "supportN" : 46,
                "supportK" : 1,
                "PS": "both",
                "PS_name_1": "PS_3",
                "PS_name_2": "PS_4",
            },
        },
        "sectors": [
            {
                "type": "without_okgt",
                "length": 1.0,
                "link_branch": ("1","2"),
                "supportN" : 46,
                "supportK" : 41,
            },
            {
                "type": "with_okgt",
                "link_okgt": "three",
                "lengthN": 0.0,
                "lengthK": 2.0,
                "link_branch": ("1","2"),
                "supportN" : 41,
                "supportK" : 31,
            },
            {
                "type": "with_okgt",
                "link_okgt": "four",
                "lengthN": 0.0,
                "lengthK": 3.0,
                "link_branch": ("1","2"),
                "supportN" : 31,
                "supportK" : 16,
            },
            {
                "type": "without_okgt",
                "length": 3.0,
                "link_branch": ("1","2"),
                "supportN" : 16,
                "supportK" : 1,
            },
        ],
        "commonchains":[],
        "phases": [
            {
                "link_branch": ("1","2"),
                "supportN" : 46,
                "supportK" : 1,
                "phase": "CAB"
            },
            
        ],
        "conductors":[
            {
                "link_branch": ("1","2"),
                "supportN" : 46,
                "supportK" : 30,
                "conductor": "AC 70/11"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 30,
                "supportK" : 1,
                "conductor": "AC 50/8"
            },
        ],
        "groundwires":[
            {
                "link_branch": ("1","2"),
                "supportN" : 46,
                "supportK" : 41,
                "type": "one",
                "is_okgt":None,
                "groundwire1": "AC 70/11"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 41,
                "supportK" : 16,
                "type": "one",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-38"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 16,
                "supportK" : 1,
                "type": "one",
                "is_okgt":None,
                "groundwire1": "AC 50/8"
            },
        ],
        "grounded": [
            {
                "link_branch": ("1","2"),
                "supportN" : 46,
                "supportK" : 1,
                "type": "first",
                "resistance": 30.0
            },
            
        ],
        "countercables":[
            
        ],
        "supports":[
            {
                "link_branch": ("1","2"),
                "supportN" : 46,
                "supportK" : 30,
                "support": "ПБ-110-1,3,11,13"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 30,
                "supportK" : 1,
                "support": "ПБ-23,21"
            },
        ],
        "PSs":[
            {
                "PS_name": "PS_3",
                "length": 0.01,
            },
            {
                "PS_name": "PS_4",
                "length": 0.03,
            },
        ],
    },
    "VL #3": {
        "branches" : {
            ("1","2") : {
                "supportN" : 31,
                "supportK" : 1,
                "PS": "both",
                "PS_name_1": "PS_5",
                "PS_name_2": "PS_6",
            },
        },
        "sectors": [
            {
                "type": "without_okgt",
                "length": 1.0,
                "link_branch": ("1","2"),
                "supportN" : 31,
                "supportK" : 26,
            },
            {
                "type": "with_okgt",
                "link_okgt": "eleven",
                "lengthN": 0.0,
                "lengthK": 4.0,
                "link_branch": ("1","2"),
                "supportN" : 26,
                "supportK" : 6,
            },
            {
                "type": "without_okgt",
                "length": 1.0,
                "link_branch": ("1","2"),
                "supportN" : 6,
                "supportK" : 1,
            },
        ],
        "commonchains":[],
        "phases": [
            {
                "link_branch": ("1","2"),
                "supportN" : 31,
                "supportK" : 26,
                "phase": "ABC"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 26,
                "supportK" : 6,
                "phase": "BCA"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 6,
                "supportK" : 1,
                "phase": "CAB"
            }
        ],
        "conductors":[
            {
                "link_branch": ("1","2"),
                "supportN" : 31,
                "supportK" : 20,
                "conductor": "AC 70/11"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 20,
                "supportK" : 1,
                "conductor": "AC 50/8"
            },
        ],
        "groundwires":[
            {
                "link_branch": ("1","2"),
                "supportN" : 31,
                "supportK" : 28,
                "type": "one",
                "is_okgt":None,
                "groundwire1": "AC 50/8"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 26,
                "supportK" : 6,
                "type": "one",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-55"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 4,
                "supportK" : 1,
                "type": "one",
                "is_okgt":None,
                "groundwire1": "AC 50/8"
            },
        ],
        "grounded": [
            {
                "link_branch": ("1","2"),
                "supportN" : 31,
                "supportK" : 28,
                "type": "first",
                "resistance": 30.0
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 26,
                "supportK" : 6,
                "type": "first",
                "resistance": 15.0
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 4,
                "supportK" : 1,
                "type": "first",
                "resistance": 30.0
            },
        ],
        "countercables":[
            
        ],
        "supports":[
            {
                "link_branch": ("1","2"),
                "supportN" : 31,
                "supportK" : 23,
                "support": "ПБ-110-1,3,11,13"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 23,
                "supportK" : 1,
                "support": "ПБ-110-1,3,11,13"
            },
        ],
        "PSs":[
            {
                "PS_name": "PS_5",
                "length": 0.01,
            },
            {
                "PS_name": "PS_6",
                "length": 0.01,
            },
        ],
    },
    "VL #4": {
        "branches" : {
            ("1","2") : {
                "supportN" : 1,
                "supportK" : 26,
                "PS": "left",
                "PS_name_1": "PS_7",
            },
            ("2","3") : {
                "supportN" : 26,
                "supportK" : 36,
                "PS": "not",
            },
            ("3","4") : {
                "supportN" : 36,
                "supportK" : 66,
                "PS": "right",
                "PS_name_2": "PS_8",
            },
            ("2","5") : {
                "supportN" : 26,
                "supportK" : 61,
                "PS": "right",
                "PS_name_2": "PS_9",
            },
            ("3","6") : {
                "supportN" : 46,
                "supportK" : 1,
                "PS": "right",
                "PS_name_2": "PS_10",
            },
        },
        "sectors": [
            {
                "type": "without_okgt",
                "length": 1.0,
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 6,
            },
            {
                "type": "with_okgt",
                "link_okgt": "five",
                "lengthN": 0.0,
                "lengthK": 4.0,
                "link_branch": ("1","2"),
                "supportN" : 6,
                "supportK" : 26,
            },
            {
                "type": "with_okgt",
                "link_okgt": "six",
                "lengthN": 0.0,
                "lengthK": 0.8,
                "link_branch": ("2","3"),
                "supportN" : 26,
                "supportK" : 30,
            },
            {
                "type": "without_okgt",
                "length": 0.4,
                "link_branch": ("2","3"),
                "supportN" : 30,
                "supportK" : 32,
            },
            {
                "type": "with_okgt",
                "link_okgt": "eight",
                "lengthN": 0.0,
                "lengthK": 0.8,
                "link_branch": ("2","3"),
                "supportN" : 32,
                "supportK" : 36,
            },
            {
                "type": "with_okgt",
                "link_okgt": "nine",
                "lengthN": 0.0,
                "lengthK": 6.0,
                "link_branch": ("3","4"),
                "supportN" : 36,
                "supportK" : 66,
            },
            {
                "type": "without_okgt",
                "length": 7.0,
                "link_branch": ("2","5"),
                "supportN" : 26,
                "supportK" : 61,
            },
            {
                "type": "without_okgt",
                "length": 9.0,
                "link_branch": ("3","6"),
                "supportN" : 46,
                "supportK" : 1,
            },
        ],
        "commonchains":[],
        "phases": [
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 26,
                "phase": "ABC"
            },
            {
                "link_branch": ("2","3"),
                "supportN" : 26,
                "supportK" : 36,
                "phase": "BAC"
            },
            {
                "link_branch": ("3","4"),
                "supportN" : 36,
                "supportK" : 66,
                "phase": "BAC"
            },
            {
                "link_branch": ("2","5"),
                "supportN" : 26,
                "supportK" : 61,
                "phase": "BAC"
            },
            {
                "link_branch": ("3","6"),
                "supportN" : 46,
                "supportK" : 1,
                "phase": "BAC"
            },
        ],
        "conductors":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 26,
                "conductor": "AC 70/11"
            },
            {
                "link_branch": ("2","3"),
                "supportN" : 26,
                "supportK" : 36,
                "conductor": "AC 70/11"
            },
            {
                "link_branch": ("3","4"),
                "supportN" : 36,
                "supportK" : 66,
                "conductor": "AC 70/11"
            },
            {
                "link_branch": ("2","5"),
                "supportN" : 26,
                "supportK" : 61,
                "conductor": "AC 70/11"
            },
            {
                "link_branch": ("3","6"),
                "supportN" : 46,
                "supportK" : 1,
                "conductor": "AC 70/11"
            },
        ],
        "groundwires":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 26,
                "type": "two",
                "is_okgt":"groundwire2",
                "groundwire1": "ОКГТ-38",
                "groundwire2": "AC 70/11",
            },
            {
                "link_branch": ("2","3"),
                "supportN" : 26,
                "supportK" : 30,
                "type": "two",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-38",
                "groundwire2": "AC 70/11",
            },
            {
                "link_branch": ("2","3"),
                "supportN" : 30,
                "supportK" : 32,
                "type": "two",
                "is_okgt":None,
                "groundwire1": None,
                "groundwire2": "AC 70/11",
            },
            {
                "link_branch": ("2","3"),
                "supportN" : 32,
                "supportK" : 36,
                "type": "two",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-38",
                "groundwire2": "AC 70/11",
            },
            {
                "link_branch": ("3","4"),
                "supportN" : 36,
                "supportK" : 66,
                "type": "two",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-38",
                "groundwire2": "AC 70/11",
            },
            {
                "link_branch": ("2","5"),
                "supportN" : 26,
                "supportK" : 61,
                "type": "one",
                "is_okgt":None,
                "groundwire1": "AC 70/11",
            },
            {
                "link_branch": ("3","6"),
                "supportN" : 46,
                "supportK" : 1,
                "type": "one",
                "is_okgt":None,
                "groundwire1": "AC 70/11",
            },
            
        ],
        "grounded": [
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 26,
                "type": "both",
                "resistance": 26.0
            },
            {
                "link_branch": ("2","3"),
                "supportN" : 26,
                "supportK" : 36,
                "type": "both",
                "resistance": 26.0
            },
            {
                "link_branch": ("3","4"),
                "supportN" : 36,
                "supportK" : 66,
                "type": "both",
                "resistance": 26.0
            },
            {
                "link_branch": ("2","5"),
                "supportN" : 26,
                "supportK" : 61,
                "type": "first",
                "resistance": 16.0
            },
            {
                "link_branch": ("3","6"),
                "supportN" : 46,
                "supportK" : 1,
                "type": "first",
                "resistance": 16.0
            },
        ],
        "countercables":[
            {
                "link_branch": ("2","3"),
                "supportN" : 35,
                "supportK" : 36,
                "H_countercable": 0.5,
                "X_countercable": 0.0,
                "D_countercable": 13,
                "ground_resistance": 30.0,
                "connect_to_ps": False,
            },
            {
                "link_branch": ("3","4"),
                "supportN" : 36,
                "supportK" : 37,
                "H_countercable": 0.5,
                "X_countercable": 0.0,
                "D_countercable": 14,
                "ground_resistance": 30.0,
                "connect_to_ps": False,
            },
        ],
        "supports":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 26,
                "support": "П-22-м"
            },
            {
                "link_branch": ("2","3"),
                "supportN" : 26,
                "supportK" : 36,
                "support": "П-22-м"
            },
            {
                "link_branch": ("3","4"),
                "supportN" : 36,
                "supportK" : 66,
                "support": "П-22-м"
            },
            {
                "link_branch": ("2","5"),
                "supportN" : 26,
                "supportK" : 61,
                "support": "ПБ-110-1,3,11,13"
                
            },
            {
                "link_branch": ("3","6"),
                "supportN" : 46,
                "supportK" : 1,
                "support": "ПБ-110-1,3,11,13"
                
            },
        ],
        "PSs":[
            {
                "PS_name": "PS_7",
                "length": 0.02,
            },
            {
                "PS_name": "PS_8",
                "length": 0.02,
            },
            {
                "PS_name": "PS_9",
                "length": 0.02,
            },
            {
                "PS_name": "PS_10",
                "length": 0.02,
            },
        ],
    },
    "VL #5": {
        "branches" : {
            ("1","2") : {
                "supportN" : 1,
                "supportK" : 71,
                "PS": "both",
                "PS_name_1": "PS_1",
                "PS_name_2": "PS_11",
            },
        },
        "sectors": [
            {
                "type": "with_okgt",
                "link_okgt": "one",
                "lengthN": 3.3,
                "lengthK": 5.0,
                "link_branch": ("1","2"),
                "supportN" : 12,
                "supportK" : 26,
            },
            {
                "type": "with_okgt",
                "link_okgt": "one",
                "lengthN": 0.0,
                "lengthK": 3.3,
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 12,
            },
            {
                "type": "with_okgt",
                "link_okgt": "one",
                "lengthN": 5.0,
                "lengthK": 10.0,
                "link_branch": ("1","2"),
                "supportN" : 26,
                "supportK" : 51,
            },
            {
                "type": "without_okgt",
                "length": 4.0,
                "link_branch": ("1","2"),
                "supportN" : 51,
                "supportK" : 71,
            },
        ],
        "commonchains":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 51,
                "other_vl_name": "VL #1",
                "other_link_branch": ("1","2"),
                "other_supportN" : 1,
                "other_supportK" : 51,
            },
        ],
        "phases": [
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 51,
                "phase": "ABC"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 51,
                "supportK" : 71,
                "phase": "-BAC"
            },
        ],
        "conductors":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 71,
                "conductor": "AC 70/11"
            },
        ],
        "groundwires":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 51,
                "type": "one",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-38"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 51,
                "supportK" : 71,
                "type": "one",
                "is_okgt":None,
                "groundwire1": "AC 70/11"
            },
        ],
        "grounded": [
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 31,
                "type": "first",
                "resistance": 30.0
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 32,
                "supportK" : 71,
                "type": "first",
                "resistance": 15.0
            },
        ],
        "countercables":[
            
        ],
        "supports":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 51,
                "support": "ПБ(л)110-2/8"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 51,
                "supportK" : 71,
                "support": "ПБ-110-1,3,11,13"
            },
        ],
        "PSs":[
            {
                "PS_name": "PS_1",
                "length": 0.02,
            },
            {
                "PS_name": "PS_11",
                "length": 0.02,
            },
        ],
    },
}


ps_info = {
    "PS_1": {"resistance": 0.5,},
    "PS_2": {"resistance": 0.4,},
    "PS_3": {"resistance": 0.5,},
    "PS_4": {"resistance": 0.6,},
    "PS_5": {"resistance": 0.6,},
    "PS_6": {"resistance": 0.7,},
    "PS_7": {"resistance": 0.7,},
    "PS_8": {"resistance": 0.6,},
    "PS_9": {"resistance": 0.5,},
    "PS_10": {"resistance": 0.4,},
    "PS_11": {"resistance": 0.4,},
}


rpa_info = {
    ("VL #1", "PS_1"):{
        "Tswitch": 0.13,
        "Tautomation":0.02,
        "arc_times":1,
        "rpa_I_setting":[22,9.68,3.74,2.2],
        "rpa_time_setting":[0,0.7,1.7,2.7],
        "arc_setting":[[0,0.2,0.5,0.9]],
        "arc_pause":[0.5],
        "I_sc":[34,25,20,16,15,12,10,9,8,7,6,5.5,5],
        "L_sc":[0,1,2,3,4,5,6,7,8,9,10,11,12],
    },
    ("VL #1", "PS_2"):{
        "Tswitch": 0.13,
        "Tautomation":0.02,
        "arc_times":2,
        "rpa_I_setting":[5.0, 2.2, 0.85, 0.5],
        "rpa_time_setting":[0,0.66,1.78,2.58],
        "arc_setting":[[0,0.2,0.5,0.9],[0,0.25,0.47,0.85]],
        "arc_pause":[0.4,0.3],
        "I_sc":[2,2.1,2.4,2.6,2.75,3,3.3,3.6,3.9,4.25,4.65,5.1,5.7],
        "L_sc":[4,5,6,7,8,9,10,11,12,13,14,15,16],
    },
    ("VL #3", "PS_5"):{
        "Tswitch": 0.13,
        "Tautomation":0.02,
        "arc_times":1,
        "rpa_I_setting":[12.8,10.4,8.8,7.5],
        "rpa_time_setting":[0,0.7,1.7,2.7],
        "arc_setting":[[0,0.2,0.5,0.9]],
        "arc_pause":[0.2],
        "I_sc":[14.5,12.8,11.5,10.4,9.5,8.8,8.0,7.6],
        "L_sc":[0,1,2,3,4,5,6,7],
    },
    ("VL #3", "PS_6"):{
        "Tswitch": 0.13,
        "Tautomation":0.02,
        "arc_times":1,
        "rpa_I_setting":[2.2, 2.15, 2.1, 1.8],
        "rpa_time_setting":[0.1,0.8,1.8,2.8],
        "arc_setting":[[0,0.2,0.5,0.9]],
        "arc_pause":[0.25],
        "I_sc":[2.3, 2.2, 2.15, 2.12, 2.1, 2.05, 2.0, 1.98],
        "L_sc":[13,12,11,10,9,8,7,6],
    },
    ("VL #2", "PS_3"):{
        "Tswitch": 0.13,
        "Tautomation":0.02,
        "arc_times":1,
        "rpa_I_setting":[2.6, 2.2, 1.75, 1.2],
        "rpa_time_setting":[0.5,0.65,1.75,2.7],
        "arc_setting":[[0,0.2,0.5,0.9]],
        "arc_pause":[0.15],
        "I_sc":[3.0,2.8,2.6,2.4,2.2,2.0,1.75,1.6,1.45,1.25],
        "L_sc":[0,1,2,3,4,5,6,7,8,9],
    },
    ("VL #2", "PS_4"):{
        "Tswitch": 0.11,
        "Tautomation":0.02,
        "arc_times":1,
        "rpa_I_setting":[3.9, 3.25, 2.75, 1.9],
        "rpa_time_setting":[0.5,0.65,1.75,2.7],
        "arc_setting":[[0,0.2,0.5,0.9]],
        "arc_pause":[0.18],
        "I_sc":[2.0,2.1,2.4,2.55,2.75,3.0,3.25,3.6,3.9,4.25],
        "L_sc":[0,1,2,3,4,5,6,7,8,9],
    },
    ("VL #4", "PS_7"):{
        "Tswitch": 0.11,
        "Tautomation":0.02,
        "arc_times":1,
        "rpa_I_setting":[21.6, 13.65, 8.84, 4.4],
        "rpa_time_setting":[0,0.65,1.75,2.7],
        "arc_setting":[[0,0.2,0.5,0.9],[0,0.25,0.55,0.95]],
        "arc_pause":[0.18,0.9],
        "I_sc":[34.1,26.5,21.6,18.15,15.6,13.65,12.1,10.82,9.75,8.84,8.04,7.34,6.70,6.12,5.57,5.05,4.54],
        "L_sc":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    },
    ("VL #4", "PS_8"):{
        "Tswitch": 0.13,
        "Tautomation":0.02,
        "arc_times":1,
        "rpa_I_setting":[11.764, 8.22, 5.546, 2.8],
        "rpa_time_setting":[0.1,0.7,1.75,2.8],
        "arc_setting":[[0.1,0.2,0.5,0.9]],
        "arc_pause":[0.24],
        "I_sc":[2.955, 3.605,4.145,4.63,5.091,5.546,6.012,6.5,7.022,7.591,8.22,8.926,9.732,10.666,11.764,13.08],
        "L_sc":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    },
    ("VL #4", "PS_9"):{
        "Tswitch": 0.13,
        "Tautomation":0.02,
        "arc_times":1,
        "rpa_I_setting":[3.321, 2.971, 2.546, 2.1],
        "rpa_time_setting":[0.3,0.7,1.75,2.8],
        "arc_setting":[[0.1,0.2,0.5,0.9]],
        "arc_pause":[0.22],
        "I_sc":[3.523,3.321,3.138,2.971,2.818,2.677,2.546,2.425,2.312,2.205],
        "L_sc":[0,2,4,6,8,10,12,14,16,18],
    },
    ("VL #4", "PS_10"):{
        "Tswitch": 0.13,
        "Tautomation":0.02,
        "arc_times":1,
        "rpa_I_setting":[1.716, 1.556,1.33,1.0],
        "rpa_time_setting":[0.05,0.65,1.55,2.55],
        "arc_setting":[[0.1,0.2,0.5,0.9]],
        "arc_pause":[0.21],
        "I_sc":[1.107,1.182,1.256,1.33,1.404,1.48,1.556,1.635,1.716,1.8],
        "L_sc":[0,2,4,6,8,10,12,14,16,18],
    },
    ("VL #5", "PS_1"):{
        "Tswitch": 0.13,
        "Tautomation":0.02,
        "arc_times":1,
        "rpa_I_setting":[2.268, 2.143, 1.99,1.6],
        "rpa_time_setting":[0.05,0.55,1.6,2.6],
        "arc_setting":[[0,0.3,0.6,1.0]],
        "arc_pause":[0.21],
        "I_sc":[2.312,2.268,2.225,2.183,2.143,2.103,2.064,2.027,1.99,1.954,1.919,1.884,1.85,1.817,1.785],
        "L_sc":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    },

    ("VL #5", "PS_11"):{
        "Tswitch": 0.13,
        "Tautomation":0.03,
        "arc_times":3,
        "rpa_I_setting":[1.5, 2.206, 1.991, 1.846],
        "rpa_time_setting":[2.6,0.05,0.7,1.6],
        "arc_setting":[[0,0.3,0.6,1.0],[0,0.4,0.7,1.1],[0,0.5,0.8,1.2]],
        "arc_pause":[0.12,0.15,0.2],
        "I_sc":[1.668,1.711,1.755,1.8,1.846,1.893,1.942,1.991,2.043,2.096,2.15,2.206,2.264,2.324,2.387],
        "L_sc":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    },
}