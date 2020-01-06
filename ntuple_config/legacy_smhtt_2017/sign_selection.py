from ntuple_processor.utils import Selection

same_sign = Selection(name = "same sign",
    cuts = [("q_1*q_2>0", "ss")])

opposite_sign = Selection(name = "opposite sign",
    cuts = [("q_1*q_2<0", "os")])
