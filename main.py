# -*- coding: utf-8 -*-

from data.filmrating import prefs
import lib.recommendations as reco

if __name__ == "__main__":
    print reco.get_recommendations(prefs, 'Lisa Rose', reco.sim_pearson)
