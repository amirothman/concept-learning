import concept_learning as cl

#Sky,Temp,Humid,Wind,Water,Forecast,EnjoySport
#sunny,warm,normal,strong,warm,same,True
#sunny,warm,high,strong,warm,same,True
#rainy,cold,high,strong,warm,change,False
#sunny,warm,high,strong,cool,change,True
def test_consistency(version_space,labels,features):
    print(cl.count_of_T(h_1))
    for boundaries in version_space:
        for h in boundaries:
            # print(h)
            for idx,label in enumerate(labels):
                cnstncy = cl.consistency(h,cl.get_data(features,idx))
                # print(label)
                print(cnstncy==label)
                # print(cnstncy)
                # print(label)
                print(h)
                print(cl.get_data(features,idx))

sky = ("sunny","sunny","rainy","sunny")
temp = ("warm","warm","cold","warm")
humid = ("normal","high","high","high")
wind = ("strong","strong","strong","strong")
forecast = ("same","same","change","change")
enjoysport = (True,True,False,False)

examples = [sky,temp,humid,wind,forecast,enjoysport]

features = examples[:-1]
labels = examples[-1]
domains = cl.get_domains(features)
data = cl.get_data(features,3)
#print("min_specializations")
#print("domains: ",domains)
#print("data: ",data)
#cl.min_specializations()
#cl.candidate_elimination(examples)
#Implement a function min_specializations(h, domains, x) for a hypothesis h and an
#example x. The argument domains is a list of lists, in which the i-th sub-list contains the possible
#values of feature i. The function should return all minimal specializations of h with respect to
#domains which are not fulfilled by x. Example output:
#cl.min_specializations()
dummy_h = ("?","warm","strong","change")
specializations = cl.min_specializations(dummy_h,domains,data)
#print("hypthesis: ", dummy_h)
#print("specializations: ",specializations)

#print("candidate_elimination")
version_space = cl.candidate_elimination(examples)
h_1 = ("T","T","d","T")
x = ("a","b","c","d")
#print(cl.min_generalizations(h_1,x))

h_g = ('?', '?', '?', '?')
new_hypothesis = ('sunny', 'warm', 'strong', 'same')

# test_consistency(version_space,labels,features)

print(version_space)
