from collections import OrderedDict

def g_0(n):
  return ("?",) * n

def s_0(n):
  return ("T",) * n

def count_of_question_marks(h):
  counter = 0
  for element in h:
    if element == "?":
      counter += 1
  return counter

def count_of_T(h):
  counter = 0
  for element in h:
    if element == "T":
      counter += 1
  return counter

def more_general(h1,h2):
  """ h1 is more general if h1 has more "?" """
  """ fix this! what about cases with the T ??"""
  if count_of_question_marks(h1) > count_of_question_marks(h1):
    return True
  else:
    return False

def min_generalizations(h,x):
  """returns all minimal generalizations
  of hypothesis h that are fulfilled by example x."""
  """ can there be more than one??"""
  generalized = list(h)
  for i,element in enumerate(h):
    if element != x[i]:
      generalized[i] = "?"
  return tuple(generalized)

def min_specializations(h,domains,x):
  """Implement a function min_specializations(h, domains, x) 
  for a hypothesis h and an example x. The argument 
  domains is a list of lists, in which the i-th 
  sub-list contains the possible values of feature i. 
  The function should return all minimal specializations 
  of h with respect to domains which are not fulfilled by x."""
  specializations = []

  for i,element in enumerate(h):
    if element == "?":
      possible_values = domains[i]
      possible_values.remove(x[i])
      for val in possible_values:
        temp_h = list(h)
        temp_h[i] = val
        specializations.append(tuple(temp_h))
    else:
      temp_h = list(h)
      temp_h[i] = "T"
      specializations.append(tuple(temp_h))
  return specializations

def consistency(h,d):
  consistency = True
  for i, el in enumerate(h):
    if el != d[i] and el != "?":
        consistency = False
  return consistency

def get_data(features,idx):
  return tuple([feature[idx] for feature in features])

def consistent_hypothesis(hypothesises,data):
  return list(filter(lambda h: consistency(h,data),hypothesises))

def candidate_elimination(examples):
  # examples is a list of (n+1) tuples
  # Check if positive or negative example
  features = examples[:-1]
  domains = [ list(OrderedDict.fromkeys(feature)) for feature in features ]

  #print(domains)
  labels = examples[-1]
  s = [g_0(len(features))]
  g = [s_0(len(features))]

  for idx, label in enumerate(labels):
    print("iteration",idx+1)
    x = get_data(features,idx)
    if label:
      print("true example",x)
      # remove inconsistent hypotheses 
      g = consistent_hypothesis(g,x)
      s = consistent_hypothesis(s,x)
      for h in s:
        # add minimal generalization
        new_hypothesis = min_generalizations(h,x)
        # such that some member of G is more general than h
        some_more_general = False
        for h_g in g:
          if more_general(new_hypothesis,h_g):
            some_more_general = True
        if some_more_general:
          s.append(new_hypothesis)

      # and cosistent with x
      s = consistent_hypothesis(s,x) 

      # Remove from S any hypothesis that is less 
      # specific than another hypothesis in S
      # specificity is measured with the count of ?*-1
      # commented out because smells like bs
      #specificity_threshold = 0
      #for h in s:
     #  if -count_of_question_marks(h) < specificity_threshold:
     #    specificity_threshold = -count_of_question_marks(h)
     #
     #s = filter(lambda h: -count_of_question_marks(h) <= specificity_threshold,s)
    else:
      print("false example",x)
      s = consistent_hypothesis(s,x)
      g = consistent_hypothesis(g,x)
      for h in g:
        # add minimal specialization
        new_hypothesises = min_specializations(h,domains,x)
        # such some member of S is more specific than h
        for hypothesis in new_hypothesises:
          some_more_specific = False
          for h_s in s:
            if not more_general(hypothesis,h_s):
              some_more_specific = True
          if some_more_spec:
            g.append(hypothesis)

      g = consistent_hypothesis(g,x)

      #generalness_threshold = 0
      #for h in g:
      #  if count_of_question_mark(h) > generalness_threshold:
      #    generalness_threshold = count_of_question_mark(h)

      #g = filter(lambda h: count_of_question_marks(h) >= generalness_threshold,g)

    print("s",s)
    print("g",g)
  return (s,g)

#Sky,Temp,Humid,Wind,Water,Forecast,EnjoySport
#sunny,warm,normal,strong,warm,same,True
#sunny,warm,high,strong,warm,same,True
#rainy,cold,high,strong,warm,change,False
#sunny,warm,high,strong,cool,change,True

sky = ("sunny","sunny","rainy","sunny")
temp = ("warm","warm","cold","warm")
wind = ("strong","strong","strong","strong")
forecast = ("same","same","change","change")

enjoysport = (True,True,False,False)

examples = [sky,temp,wind,forecast,enjoysport]

candidate_elimination(examples)

