okgt_info = {
    ("1","2"): [
        {
            "type": "VL",
            "name" : "one",
            "length": 74.15,
        },
    ]
}

vl_info = {
    "VL #1": {
        "branches" : {
            ("1","2") : {
                "supportN" : 1,
                "supportK" : 225,
                "PS": "both",
                "PS_name_1": "PS_1",
                "PS_name_2": "PS_2",
            },
        },
        "sectors": [
            {
                "type": "with_okgt",
                "link_okgt": "one",
                "lengthN": 0,
                "lengthK": 74.15,
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 225,
            },
        ],
        "commonchains":[
            
        ],
        "phases": [
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 225,
                "phase": "ABC"
            },
            
        ],
        "conductors":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 225,
                "conductor": "AC 2x300/39"
            },
        ],
        "groundwires":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 4,
                "type": "two",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-150",
                "groundwire2": "ТК-70",
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 4,
                "supportK" : 8,
                "type": "two",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-150",
                "groundwire2": "ТК-70",
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 8,
                "supportK" : 35,
                "type": "one",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-150",
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 35,
                "supportK" : 56,
                "type": "one",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-55",
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 56,
                "supportK" : 225,
                "type": "one",
                "is_okgt":"groundwire1",
                "groundwire1": "ОКГТ-55",
            },
        ],
        "grounded": [
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 8,
                "type": "both",
                "resistance": 30.0
            },
            {
                "link_branch": ("1","2"),
                "supportN" : 9,
                "supportK" : 225,
                "type": "first",
                "resistance": 30.0
            },
            
        ],
        "countercables":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 20,
                "H_countercable": 0.5,
                "X_countercable": 0.0,
                "D_countercable": 16,
                "ground_resistance": 30.0,
                "connect_to_ps": True,
            },
        ],
        "supports":[
            {
                "link_branch": ("1","2"),
                "supportN" : 1,
                "supportK" : 225,
                "support": "ПБ330-7н"
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
}

ps_info = {
    "PS_1": {"resistance": 0.22,},
    "PS_2": {"resistance": 0.32,},
}

rpa_info = {
    ("VL #1", "PS_1"):{
        "Tswitch": 0.0,
        "Tautomation":0.0,
        "arc_times":0,
        "rpa_I_setting":[1],
        "rpa_time_setting":[0.3],
        "arc_setting":[],
        "arc_pause":[],
        "I_sc":[46.7,26.6,18.44,14.03,11.26,9.35,7.9,6.8,5.97,5.252,4.632,4.086,3.589,3.415],
        "L_sc":[0,6,12,18,24,30,36,42,48,54,60,66,72,74.2],
    },
    ("VL #1", "PS_2"):{
        "Tswitch": 0.0,
        "Tautomation":0.0,
        "arc_times":0,
        "rpa_I_setting":[1],
        "rpa_time_setting":[0.3],
        "arc_setting":[],
        "arc_pause":[],
        "I_sc":[1.285,2.321,2.852,3.239,3.578,3.905,4.242,4.603,5,5.447,5.961,6.563,7.284,7.585],
        "L_sc":[0,6,12,18,24,30,36,42,48,54,60,66,72,74.2],
    },
}