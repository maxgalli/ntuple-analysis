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
    "version": "v1"
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
DY_query = [
    queryM50NLO_inc, queryEWKZ
    ]
DY_query_ntlo = [
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
