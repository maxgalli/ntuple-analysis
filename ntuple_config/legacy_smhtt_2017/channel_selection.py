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
                           ("trg_singlemuon==1", "trg_singlemuon")
                           ])
