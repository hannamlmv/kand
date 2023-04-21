"""
panelclass.py

Contains a class for panel objects and a sub-class for isolate objects.

Date: 20/4-23
"""


class Panel:

    class Isolate:
        def __init__(self, name, antibiotics, sir_mic):
            self.name = name
            self.mic = {antibiotics[i]:(sir_mic[i][0], sir_mic[i][1]) for i in range(len(antibiotics))}

    def __init__(self, ava_iso, chosen_iso = [], a = [1,1,1,1]):
        self.ava_iso = ava_iso
        self.chosen_iso = chosen_iso
        self.spr = self.spr_score()
        self.cov = self.cov_score()
        self.red = self.red_score()
        self.hyppar = a #a list with hyperparameters to be used when constructing panel

    def spr_score(self):
        pass
        #calculate spread score based on self.chosen_iso
        #return score

    def cov_score(self):
        pass
        #calculate coverage score based on self.chosen_iso
        #return score

    def red_score(self):
        pass
        #calculate redundance score based on self.chosen_iso
        #return score

    def add_isolate(self):

        #Find isolate which gives minimum cost
        iso_cost = {}
        for isolate in self.ava_iso:
            iso_cost[isolate] = try_isolate(isolate)
            remove_isolate(isolate)

        def try_isolate(isolate):
            #Add isolates and calculate temporary scores
            self.chosen_iso.append(isolate)
            temp_scores = [-self.spr_score(), -self.cov_score(), self.red_score(), len(self.chosen_iso)]
            #Calculate the overall cost
            cost = sum([i*j for (i,j) in zip(self.hyppar,temp_scores)])
            return cost

        def remove_isolate(isolate):
            self.chosen_iso.remove(isolate)
        
        #Add isolate
        best_iso = min(iso_cost, key=iso_cost.get) #gives the key with the maximum value
        self.chosen_iso.append(best_iso)
        self.ava_iso.remove(best_iso)

        #Update all scores
        self.spr = self.spr_score()
        self.cov = self.cov_score()
        self.red = self.red_score()
