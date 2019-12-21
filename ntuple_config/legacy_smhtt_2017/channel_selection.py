from ntuple_processor.utils import Selection

mt_channel = Selection(name = "mt",
                       cuts = [
                           ("extraelec_veto<0.5", "extraelec_veto"),
                           ("extramuon_veto<0.5", "extramuon_veto"),
                           ("dilepton_veto<0.5", "dilepton_veto"),
                           ("againstMuonTight3_2>0.5", "againstMuonDiscriminator"),
                           ("againstElectronVLooseMVA6_2>0.5",
                               "againstElectronDiscriminator"),
                           ("byTightIsolationMVArun2v1DBoldDMwLT_2>0.5", "tau_iso"),
                           ("iso_1<0.15", "muon_iso"),
                           ("q_1*q_2<0", "os"),
                           #("trg_singlemuon==1", "trg_singlemuon")
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
            ("q_1*q_2<0", "os"),
            ("pt_2>30 && pt_1 > 25 && (((trg_singleelectron_35 == 1) || (trg_singleelectron_32 == 1) || ((trg_singleelectron_27 == 1))) || (abs(eta_1)>1.5 && isEmbedded)) || (pt_1>25 && pt_1<28 && pt_2>35 && ((isEmbedded && (abs(eta_1)>1.5)) || (trg_crossele_ele24tau30 == 1)))", "trg_selection")
        ])
