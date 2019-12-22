from ntuple_processor.utils import Selection

DY_process_base_weights = [
    ("puweight", "puweight"),
    ("idWeight_1*idWeight_2","idweight"),
    ("isoWeight_1*isoWeight_2","isoweight"),
    ("trackWeight_1*trackWeight_2","trackweight"),
    ("eleTauFakeRateWeight*muTauFakeRateWeight", "leptonTauFakeRateWeight"),
    ("zPtReweightWeight", "zPtReweightWeight"),
    ("prefiringweight", "prefireWeight")
    ]
DY_process_weights = DY_process_base_weights
DY_process_weights_nlo = DY_process_base_weights
DY_process_weights.append((
        "((genbosonmass >= 50.0)*6.3654e-05*((npartons == 0 || npartons >= 5)*1.0 + (npartons == 1)*0.1743 \
                + (npartons == 2)*0.3556 \
                + (npartons == 3)*0.2273 \
                + (npartons == 4)*0.2104) \
                + (genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight)",
         "z_stitching_weight"
         ))
DY_process_weights_nlo.append((
        "((genbosonmass >= 50.0)*2.9688e-05 \
                + (genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight)",
        "z_stitching_weight"
        ))

DY_process_selection = Selection(name = "DrellYan",
                                 weights = DY_process_weights)
DY_nlo_process_selection = Selection(name = "DrellYan_nlo",
                                      weights = DY_process_weights_nlo)
