# -*- coding: utf-8 -*-

import chapter2.recommendations as reco
from chapter2.data.filmrating import prefs

if __name__ == "__main__":
    print reco.get_recommendations(prefs, 'Lisa Rose', reco.sim_pearson)
