from ntuple_processor.utils import Selection


##### Drell-Yan #####

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


##### ZTauTau #####

def ZTT_process_selection(channel):
    if "mt" in channel:
        tt_cut = "gen_match_1==4 && gen_match_2==5"
    elif "et" in channel:
        tt_cut = "gen_match_1==3 && gen_match_2==5"
    elif "tt" in channel:
        tt_cut = "gen_match_1==5 && gen_match_2==5"
    elif "em" in channel:
        tt_cut = "gen_match_1==3 && gen_match_2==4"
    elif "mm" in channel:
        tt_cut = "gen_match_1==4 && gen_match_2==4"
    return Selection(name = "ZTT",
                     cuts = [(tt_cut, "ztt_cut")])


##### ZTauTau Embedded #####

def ZTT_embedded_process_selection(channel):
    if "mt" in channel:
        ztt_embedded_weights = [
            ("generatorWeight", "simulation_sf"),
            ("muonEffTrgWeight*muonEffIDWeight_1*muonEffIDWeight_2", "scale_factor"),
            ("idWeight_1*(trigger_24_27_Weight_1*(pt_1>25)+((0.81*(pt_1>=21 && pt_1<22) + 0.82*(pt_1>=22 && pt_1<23) + 0.83*(pt_1>=23))*(pt_1<25)))*isoWeight_1", "lepton_sf"),
            ("(pt_1>25)+(pt_1 >= 21 && pt_1<25)*((pt_2>=20 && pt_2<25)*0.12714+(pt_2>=25 && pt_2<30)*0.46930+0.71983*(pt_2>=30 && pt_2<35) + 0.75209*(pt_2>=35 && pt_2<40) + 0.78164*(pt_2>=40 && pt_2<45) + 0.83241*(pt_2>=45 && pt_2<50) + 0.86694*(pt_2>=50 && pt_2<60) + 0.89966*(pt_2>=60 && pt_2<80) + 0.88534*(pt_2>=80 && pt_2<100) + 0.90095*(pt_2>=100 && pt_2<150) + 0.84402*(pt_2>=150 && pt_2<200) + (pt_2>=200))","tau_leg_weight"),
            ("(gen_match_2==5)*0.97+(gen_match_2!=5)", "emb_tau_id"),
            ("gen_match_1==4 && gen_match_2==5","emb_veto"),
            ("embeddedDecayModeWeight", "decayMode_SF")
            ]
    elif "et" in channel:
        ztt_embedded_weights = [
            ("generatorWeight", "simulation_sf"),
            ("muonEffTrgWeight*muonEffIDWeight_1*muonEffIDWeight_2", "scale_factor"),
            ("(pt_1>28)+(pt_1<28)*(crossTriggerDataEfficiencyWeight_tight_MVAv2_2*(abs(eta_1)>=1.5)+((1.29079*(pt_2>=30 && pt_2<35) + 1.06504*(pt_2>=35 && pt_2<40) + 0.93972*(pt_2>=40 && pt_2<45) + 0.91923*(pt_2>=45 && pt_2<50) + 0.89598*(pt_2>=50 && pt_2<60) + 0.90597*(pt_2>=60 && pt_2<80) + 0.88761*(pt_2>=80 && pt_2<100) + 0.90210*(pt_2>=100 && pt_2<150) + 0.84939*(pt_2>=150 && pt_2<200) + (pt_2>=200))*(abs(eta_1)<1.5)))","tau_leg_weight"),
            ("(pt_1>28)+(pt_1<28)*(crossTriggerDataEfficiencyWeight_1*(abs(eta_1)>=1.5)+((0.39*(pt_1>=25 && pt_1<26) + 0.46*(pt_1>=26 && pt_1<27) + 0.48*(pt_1>=27 && pt_1<28))*(abs(eta_1)<1.5)))","lepton_leg_weight"),
            ("idWeight_1*((pt_1>28)*(trigger_27_32_35_Weight_1*(abs(eta_1) < 1.5) + singleTriggerDataEfficiencyWeightKIT_1*(abs(eta_1)>=1.5))+(pt_1<28))*isoWeight_1", "lepton_sf"),
            ("(gen_match_2==5)*0.97+(gen_match_2!=5)", "emb_tau_id"),
            ("gen_match_1==3 && gen_match_2==5","emb_veto"),
            ("embeddedDecayModeWeight", "decayMode_SF"))
            ]
    elif "tt" in channel:
        ztt_embedded_weights = [
            ("generatorWeight", "simulation_sf"),
            ("muonEffTrgWeight*muonEffIDWeight_1*muonEffIDWeight_2", "scale_factor"),
            ("(0.18321*(pt_1>=30 && pt_1<35) + 0.53906*(pt_1>=35 && pt_1<40) + 0.63658*(pt_1>=40 && pt_1<45) + 0.73152*(pt_1>=45 && pt_1<50) + 0.79002*(pt_1>=50 && pt_1<60) + 0.84666*(pt_1>=60 && pt_1<80) + 0.84919*(pt_1>=80 && pt_1<100) + 0.86819*(pt_1>=100 && pt_1<150) + 0.88206*(pt_1>=150 && pt_1<200) + (pt_1>=200))","tau1_leg_weight"),
            ("(0.18321*(pt_2>=30 && pt_2<35) + 0.53906*(pt_2>=35 && pt_2<40) + 0.63658*(pt_2>=40 && pt_2<45) + 0.73152*(pt_2>=45 && pt_2<50) + 0.79002*(pt_2>=50 && pt_2<60) + 0.84666*(pt_2>=60 && pt_2<80) + 0.84919*(pt_2>=80 && pt_2<100) + 0.86819*(pt_2>=100 && pt_2<150) + 0.88206*(pt_2>=150 && pt_2<200) + (pt_2>=200))","tau2_leg_weight"),
            ("((gen_match_1==5)*0.97+(gen_match_1!=5))*((gen_match_2==5)*0.97+(gen_match_2!=5))", "emb_tau_id"),
            ("gen_match_1==5 && gen_match_2==5","emb_veto"),
            ("embeddedDecayModeWeight", "decayMode_SF"))
            ]
    elif "em" in channel:
        ztt_embedded_weights = [
            ("1.043*generatorWeight", "simulation_sf"),
            ("(gen_match_1==3 && gen_match_2==4)", "emb_gen_match"),
            ("muonEffTrgWeight*muonEffIDWeight_1*muonEffIDWeight_2", "scale_factor"),
            ("0.99*trackWeight_1*trackWeight_2*idWeight_1*isoWeight_1*idWeight_2*looseIsoWeight_2", "idiso_lepton_sf"),
            ("(trigger_23_data_Weight_2*trigger_12_data_Weight_1*(trg_muonelectron_mu23ele12==1)+trigger_23_data_Weight_1*trigger_8_data_Weight_2*(trg_muonelectron_mu8ele23==1) - trigger_23_data_Weight_2*trigger_23_data_Weight_1*(trg_muonelectron_mu8ele23==1 && trg_muonelectron_mu23ele12==1))/(trigger_23_embed_Weight_2*trigger_12_embed_Weight_1*(trg_muonelectron_mu23ele12==1)+trigger_23_embed_Weight_1*trigger_8_embed_Weight_2*(trg_muonelectron_mu8ele23==1) - trigger_23_embed_Weight_2*trigger_23_embed_Weight_1*(trg_muonelectron_mu8ele23==1 && trg_muonelectron_mu23ele12==1))", "trigger_lepton_sf"))
            ]

    ztt_embedded_cuts = [("((gen_match_1>2 && gen_match_1<6) && (gen_match_2>2 && gen_match_2<6))", "dy_genuine_tau")]

    return Selection(name = "Embedded",
                     cuts = ztt_embedded_cuts,
                     weights = ztt_embedded_weights)


##### ZL #####

def ZL_process_selection(channel):
    if "mt" in channel:
        emb_veto = "!(gen_match_1==4 && gen_match_2==5)"
        ff_veto = "!(gen_match_2 == 6)"
    elif "et" in channel:
        emb_veto = "!(gen_match_1==3 && gen_match_2==5)"
        ff_veto = "!(gen_match_2 == 6)"
    elif "tt" in channel:
        emb_veto = "!(gen_match_1==5 && gen_match_2==5)"
        ff_veto = "!(gen_match_1 == 6 || gen_match_2 == 6)"
    elif "em" in channel:
        emb_veto = "!(gen_match_1==3 && gen_match_2==4)"
        ff_veto = "(1.0)"
    elif "mm" in channel:
        emb_veto = "!(gen_match_1==4 && gen_match_2==4)"
        ff_veto = "(1.0)"
    return Selection(name = "ZL",
                     cuts = [("%s && %s"%(emb_veto,ff_veto), "dy_emb_and_ff_veto")])


##### TTT #####

def TTT_process_selection(channel):
    if "mt" in channel:
        tt_cut = "gen_match_1==4 && gen_match_2==5"
    elif "et" in channel:
        tt_cut = "gen_match_1==3 && gen_match_2==5"
    elif "tt" in channel:
        tt_cut = "gen_match_1==5 && gen_match_2==5"
    elif "em" in channel:
        tt_cut = "gen_match_1==3 && gen_match_2==4"
    elif "mm" in channel:
        tt_cut = "gen_match_1==4 && gen_match_2==4"
    return Selection(name = "TTT",
                     cuts = [(tt_cut, "ttt_cut")])
