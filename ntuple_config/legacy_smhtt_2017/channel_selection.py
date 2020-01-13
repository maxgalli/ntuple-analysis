from ntuple_processor.utils import Selection

mt_channel = Selection(name = "mt",
                       cuts = [
                                ("flagMETFilter == 1", "METFilter"),
                                ("extraelec_veto<0.5", "extraelec_veto"),
                                ("extramuon_veto<0.5", "extramuon_veto"),
                                ("dilepton_veto<0.5", "dilepton_veto"),
                                ("byTightDeepTau2017v2p1VSmu_2>0.5", "againstMuonDiscriminator"),
                                ("byVVLooseDeepTau2017v2p1VSe_2>0.5",
                                    "againstElectronDiscriminator"),
                                ("byTightDeepTau2017v2p1VSjet_2>0.5", "tau_iso"),
                                ("iso_1<0.15", "muon_iso"),
                                ("pt_2>30 && ((trg_singlemuon_27 == 1) || (trg_singlemuon_24 == 1) || (pt_1 < 25 && trg_crossmuon_mu20tau27 == 1))", "trg_selection")
                       ])

et_channel = Selection(name = "et",
    cuts = [
            ("flagMETFilter == 1", "METFilter"),
            ("extraelec_veto<0.5", "extraelec_veto"),
            ("extramuon_veto<0.5", "extramuon_veto"),
            ("dilepton_veto<0.5", "dilepton_veto"),
            ("againstMuonLoose3_2>0.5", "againstMuonDiscriminator"),
            ("againstElectronTightMVA6_2>0.5",
                "againstElectronDiscriminator"),
            ("byTightIsolationMVArun2017v2DBoldDMwLT2017_2>0.5", "tau_iso"),
            ("iso_1<0.15", "ele_iso"),
            ("pt_2>30 && pt_1 > 25 && (((trg_singleelectron_35 == 1) || (trg_singleelectron_32 == 1) || ((trg_singleelectron_27 == 1))) || (abs(eta_1)>1.5 && isEmbedded)) || (pt_1>25 && pt_1<28 && pt_2>35 && ((isEmbedded && (abs(eta_1)>1.5)) || (trg_crossele_ele24tau30 == 1)))", "trg_selection")
        ])

tt_channel = Selection(name = "tt",
    cuts = [
            ("flagMETFilter == 1", "METFilter"),
            ("extraelec_veto<0.5", "extraelec_veto"),
            ("extramuon_veto<0.5", "extramuon_veto"),
            ("dilepton_veto<0.5", "dilepton_veto"),
            ("againstMuonLoose3_1>0.5 && againstMuonLoose3_2>0.5",
                "againstMuonDiscriminator"),
            ("againstElectronVLooseMVA6_1>0.5 && againstElectronVLooseMVA6_2>0.5",
                "againstElectronDiscriminator"),
            ("byTightIsolationMVArun2017v2DBoldDMwLT2017_1>0.5",
                "tau_1_iso"),
            ("byTightIsolationMVArun2017v2DBoldDMwLT2017_2>0.5",
                "tau_2_iso"),
            ("(trg_doubletau_35_tightiso_tightid == 1) || (trg_doubletau_40_mediso_tightid == 1) || (trg_doubletau_40_tightiso == 1)", "trg_selection")
        ])

em_channel = Selection(name = "em",
    cuts = [
            ("flagMETFilter == 1", "METFilter"),
            ("extraelec_veto<0.5", "extraelec_veto"),
            ("extramuon_veto<0.5", "extramuon_veto"),
            ("dilepton_veto<0.5", "dilepton_veto"),
            ("iso_1<0.15", "ele_iso"),
            ("iso_2<0.2", "muon_iso"),
            ("pt_2>10 && ((trg_muonelectron_mu23ele12 == 1) || (trg_muonelectron_mu8ele23 == 1))",
                "trg_selection")
        ])

