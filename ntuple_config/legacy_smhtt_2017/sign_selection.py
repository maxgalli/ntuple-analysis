from ntuple_processor.utils import Selection

same_sign = Selection(name = "ss",
    cuts = [("q_1*q_2>0", "ss")])

opposite_sign = Selection(name = "os",
    cuts = [("q_1*q_2<0", "os")])
