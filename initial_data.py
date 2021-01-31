

""" 
description of property parameters:

"way_grounded" : "left", "right", "not", "both"
"type": "VL", "single", "single_dielectric"
"PS": "left", "right", "not", "both"
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
            "countercable": True,
            "H_countercable": 0.5,
            "X_countercable": 0.0,
            "D_countercable": 12,
            "point_grounded" : 3,
            "way_grounded": "not",
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
                "supportN" : 1,
                "supportK" : 61,
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
                "phase": "BAC"
            },
        ],
        "conductors":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 61,
                "conductor": "AC-70/11"
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
                "type": "one",
                "is_okgt":None,
                "groundwire1": "AC-70/11"
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
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 6,
                "supportK" : 7,
                "H_countercable": 0.5,
                "X_countercable": 0.0,
                "D_countercable": 12,
                "ground_resistance": 30.0,
            },
        ],
        "supports":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 61,
                "support": "ПБ-110/1"
            },
        ],
        "PSs":[
            {
                "PS_name": "PS_1",
                "resistance": 0.5,
                "length": 0.02,
            },
            {
                "PS_name": "PS_2",
                "resistance": 0.4,
                "length": 0.02,
            },
        ],
    },
    "VL #2": {
        "branches" : {
            ("1","2") : {
                "nodeN": "1",
                "nodeK": "2",
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
                "conductor": "AC-70/11"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 30,
                "supportK" : 1,
                "conductor": "AC-50/7"
            },
        ],
        "groundwires":[
            {
                "link_branch": ("1","2"),
                "supportN" : 46,
                "supportK" : 41,
                "type": "one",
                "is_okgt":None,
                "groundwire1": "AC-70/11"
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
                "groundwire1": "AC-50/7"
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
                "support": "ПБ-110/1"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 30,
                "supportK" : 1,
                "support": "ПБ-110/3"
            },
        ],
        "PSs":[
            {
                "PS_name": "PS_3",
                "resistance": 0.5,
                "length": 0.01,
            },
            {
                "PS_name": "PS_4",
                "resistance": 0.6,
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
                "conductor": "AC-70/11"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 20,
                "supportK" : 1,
                "conductor": "AC-50/7"
            },
        ],
        "groundwires":[
            {
                "link_branch": ("1","2"),
                "supportN" : 31,
                "supportK" : 28,
                "type": "one",
                "is_okgt":None,
                "groundwire1": "AC-50/7"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 26,
                "supportK" : 6,
                "type": "one",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-50"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 4,
                "supportK" : 1,
                "type": "one",
                "is_okgt":None,
                "groundwire1": "AC-50/7"
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
                "support": "ПБ-110/1"
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 23,
                "supportK" : 1,
                "support": "ПБ-110/3"
            },
        ],
        "PSs":[
            {
                "PS_name": "PS_5",
                "resistance": 0.6,
                "length": 0.01,
            },
            {
                "PS_name": "PS_6",
                "resistance": 0.7,
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
                "PS": "no",
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
                "conductor": "AC-70/11"
            },
            {
                "link_branch": ("2","3"),
                "supportN" : 26,
                "supportK" : 36,
                "conductor": "AC-70/11"
            },
            {
                "link_branch": ("3","4"),
                "supportN" : 36,
                "supportK" : 66,
                "conductor": "AC-70/11"
            },
            {
                "link_branch": ("2","5"),
                "supportN" : 26,
                "supportK" : 61,
                "conductor": "AC-70/11"
            },
            {
                "link_branch": ("3","6"),
                "supportN" : 46,
                "supportK" : 1,
                "conductor": "AC-70/11"
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
                "groundwire2": "AC-70/11",
            },
            {
                "link_branch": ("2","3"),
                "supportN" : 26,
                "supportK" : 30,
                "type": "two",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-38",
                "groundwire2": "AC-70/11",
            },
            {
                "link_branch": ("2","3"),
                "supportN" : 30,
                "supportK" : 32,
                "type": "two",
                "is_okgt":None,
                "groundwire1": None,
                "groundwire2": "AC-70/11",
            },
            {
                "link_branch": ("2","3"),
                "supportN" : 32,
                "supportK" : 36,
                "type": "two",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-38",
                "groundwire2": "AC-70/11",
            },
            {
                "link_branch": ("3","4"),
                "supportN" : 36,
                "supportK" : 66,
                "type": "two",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-38",
                "groundwire2": "AC-70/11",
            },
            {
                "link_branch": ("2","5"),
                "supportN" : 26,
                "supportK" : 61,
                "type": "one",
                "is_okgt":None,
                "groundwire1": "AC-70/11",
            },
            {
                "link_branch": ("3","6"),
                "supportN" : 46,
                "supportK" : 1,
                "type": "one",
                "is_okgt":None,
                "groundwire1": "AC-70/11",
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
            },
            {
                "link_branch": ("3","4"),
                "supportN" : 36,
                "supportK" : 37,
                "H_countercable": 0.5,
                "X_countercable": 0.0,
                "D_countercable": 14,
                "ground_resistance": 30.0,
            },
        ],
        "supports":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 26,
                "support": "ПБ-110/5"
            },
            {
                "link_branch": ("2","3"),
                "supportN" : 26,
                "supportK" : 36,
                "support": "ПБ-110/5"
            },
            {
                "link_branch": ("3","4"),
                "supportN" : 36,
                "supportK" : 66,
                "support": "ПБ-110/5"
            },
            {
                "link_branch": ("2","5"),
                "supportN" : 26,
                "supportK" : 61,
                "support": "ПБ-110/1"
                
            },
            {
                "link_branch": ("3","6"),
                "supportN" : 46,
                "supportK" : 1,
                "support": "ПБ-110/1"
                
            },
        ],
        "PSs":[
            {
                "PS_name": "PS_7",
                "resistance": 0.7,
                "length": 0.02,
            },
            {
                "PS_name": "PS_8",
                "resistance": 0.6,
                "length": 0.02,
            },
            {
                "PS_name": "PS_9",
                "resistance": 0.5,
                "length": 0.02,
            },
            {
                "PS_name": "PS_10",
                "resistance": 0.4,
                "length": 0.02,
            },
        ],
    },
}