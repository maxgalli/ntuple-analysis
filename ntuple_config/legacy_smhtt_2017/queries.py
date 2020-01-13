##### Data #####

data_query = {
    "data": True,
    "campaign": "Run2017(B|C|D|E|F)",
    "scenario": "31Mar2018v1",
    "process": "SingleMuon"
}


##### DYJetsToLL #####

queryM10 = {
    "process": "DYJetsToLL_M10to50",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "madgraph\-pythia8",
    "extension": "ext1",
    "version": "v2"
}
queryM50_inclusive_2_3jet = {
    "process": "DY(|2|3)JetsToLL_M50",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "madgraph\-pythia8",
    "version": "(v1|v2)"
}
queryM50_1jet_v1 = {
    "process": "DY1JetsToLL_M50",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "madgraph\-pythia8",
    "extension": "^$",
    "version": "v1"
}
queryM50_1jet_ext1_v2 = {
    "process": "DY1JetsToLL_M50",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "madgraph\-pythia8",
    "extension": "ext1",
    "version": "v2"
}
queryM50_4jet = {
    "process": "DY4JetsToLL_M50",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "madgraph\-pythia8",
    "version": "v2"
}
queryEWKZ = {
    "process": "^EWKZ",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "madgraph\-pythia8",
}
queryM50NLO_inc = {
    "process": "DYJetsToLL_M50",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "amcatnlo\-pythia8",
}
DY_query_nlo = [
    queryM50NLO_inc, queryEWKZ
    ]
DY_query = [
    queryM50_inclusive_2_3jet,
    queryM50_1jet_v1,
    queryM50_1jet_ext1_v2,
    queryM50_4jet,
    queryM10,
    queryEWKZ
    ]


##### TT #####

tt_query = {
    "process": "TTTo.*",
    "scenario": "PU2017",
    "dbs" : ".*new_pmx.*",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
}


##### W #####

W_query = [{
    "process": "W.?JetsToLNu|WGToLNuG",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "madgraph-pythia8"
    }, {
    "process": "^EWKW",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "madgraph\-pythia8"
    }]


##### HTT #####

HTT_query = {
    "process": "(VBF|GluGlu|Z|W).*HToTauTau_M125",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "powheg\-pythia8"
}


##### VV #####

VV_query = [{
    "process": "(WW|ZZ|WZ)$",
    "data": False,
    "generator": "^pythia8",
    "campaign": "RunIIFall17MiniAODv2"
    }, {
    "process": "ST",
    "data": False,
    "scenario": "^PU2017$",
    "version": "v2",
    "generator": "powheg\-pythia8",
    "campaign": "RunIIFall17MiniAODv2"
    }, {
    "process": "ST",
    "data": False,
    "scenario": "^PU2017newpmx$",
    "generator": "powheg\-pythia8",
    "campaign": "RunIIFall17MiniAODv2"
    }]


##### ZTTEmbedded #####

def ZTT_embedded_query(channel):
    query = {
        "process": "Embedding2017(B|C|D|E|F)",
        "embedded": True
        }
    if "mt" in channel:
        query["campaign"] = "MuTauFinalState"
        query["scenario"] = ".*v2"
    elif "et" in channel:
        query["campaign"] = "ElTauFinalState"
        query["scenario"] = ".*v2"
    elif "tt" in channel:
        query["campaign"] = "TauTauFinalState"
        query["scenario"] = ".*(v2|v3)"
    elif "em" in channel:
        query["campaign"] = "ElMuFinalState"

    return query


##### HWW #####

HWW_query = {
    "process": "(VBF|GluGlu).*HToWWTo2L2Nu_M125",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "powheg\-pythia8"
}


##### ggHWW #####

ggHWW_query = {
    "process": "GluGlu.*HToWWTo2L2Nu_M125",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "powheg\-pythia8"
}


##### qqHWW #####

qqHWW_query = {
    "process": "VBF.*HToWWTo2L2Nu_M125",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "powheg\-pythia8"
}


##### VH #####

VH_query = {
    "process": "(^W(minus|plus)HToTauTau.*125.*|^ZHToTauTau.*125.*)",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "powheg\-pythia8"
}


##### WH #####

WH_query = {
    "process": "(^W(minus|plus)HToTauTau.*125.*)",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "powheg\-pythia8"
}


##### ZH #####

ZH_query = {
    "process": "(^ZHToTauTau.*125.*)",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "powheg\-pythia8"
}


##### ggH #####

ggH_query = {
    "process": "^GluGluHToTauTau.*125.*",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "powheg\-pythia8"
}


##### qqH #####

qqH_query = {
    "process": "(^VBFHToTauTau.*125.*|^W(minus|plus)HToTauTau.*125.*|^ZHToTauTau.*125.*)",
    "data": False,
    "campaign": "RunIIFall17MiniAODv2",
    "generator": "powheg\-pythia8"
}

