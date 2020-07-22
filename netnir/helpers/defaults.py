default_config = {
    "directories": {
        "hostvars": "./host_vars",
        "groupvars": "./group_vars",
        "templates": "./templates",
        "output": "./output",
        "hier": "./conf/hier",
    },
    "domain": "example.net",
    "nornir": {"config": "./conf/nornir.yaml"},
    "plugins": {
        "setup": {
            "class": "netnir.core.tasks.setup.Setup",
            "description": "netnir setup commands",
        },
        "inventory": {
            "class": "netnir.core.tasks.inventory.Inventory",
            "description": "inventory search command",
        },
        "cp": {
            "class": "netnir.core.tasks.config_plan.ConfigPlan",
            "description": "config plan commands",
        },
        "mc": {
            "class": "netnir.core.tasks.multi_change.MultiChange",
            "description": "multi change/show via SSH",
        },
        "fetch": {
            "class": "netnir.core.tasks.fetch.Fetch",
            "description": "fetch commands",
        },
    },
}

nornir_defaults = {
    "core": {
        "num_workers": 20,
    },
    "inventory": {
        "plugin": "netnir.core.NornirInventory"
    },
}