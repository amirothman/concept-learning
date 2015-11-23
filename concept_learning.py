from collections import OrderedDict
import copy

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
  #print(count_of_question_marks(h1))
  #print(count_of_question_marks(h2))
  if count_of_T(h2) > count_of_T(h1):
    return False
  else:
    if count_of_question_marks(h1) > count_of_question_marks(h2):
      return True
    else:
      return False

def min_generalizations(h,x):
  """returns all minimal generalizations
  of hypothesis h that are fulfilled by example x."""
  """ can there be more than one??"""
  generalized = list(h)
  for i,element in enumerate(h):
    if element == "T":
      generalized[i] = x[i]
    else:
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
      possible_values = copy.deepcopy(domains[i])
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

def inconsistent_hypothesis(hypothesises,data):
  return list(filter(lambda h: not consistency(h,data),hypothesises))

def get_domains(features):
  return [ list(OrderedDict.fromkeys(feature)) for feature in features ]

def candidate_elimination(examples):
  # examples is a list of (n+1) tuples
  # Check if positive or negative example
  features = examples[:-1]
  domains = get_domains(features)

  #print(domains)
  labels = examples[-1]
  s = [s_0(len(features))]
  g = [g_0(len(features))]
  print("s",s)
  print("g",g)
  for idx, label in enumerate(labels):
    print("iteration",idx+1)
    x = get_data(features,idx)
    if label:
      print("true example",x)
      # remove inconsistent hypotheses
      g = consistent_hypothesis(g,x)
      new_hypothesises = []
      for h in s:
        # add minimal generalization
        new_hypothesis = min_generalizations(h,x)
        #print("new_hypothesis",new_hypothesis)
        # such that some member of G is more general than h
        # print("current_g",g)
        some_more_general = False
        for h_g in g:
          #print("h_g",h_g)
          #print("new_hypothesis",new_hypothesis)
          #print(more_general(h_g,new_hypothesis))
          if more_general(h_g,new_hypothesis):
            some_more_general = True
        if some_more_general:
          new_hypothesises.append(new_hypothesis)

      s = s + new_hypothesises
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
      s = inconsistent_hypothesis(s,x)
      new_hypothesises_list = []
      for h in g:
        # add minimal specialization
        #print("hypothesis",h)
        #print("domains",domains)
        #print("data",x)
        new_hypothesises = min_specializations(h,domains,x)
        # such some member of S is more specific than h
        for hypothesis in new_hypothesises:
          some_more_specific = False
          for h_s in s:
            if not more_general(h_s,hypothesis):
              some_more_specific = True
          if some_more_specific:
            new_hypothesises_list.append(hypothesis)
      g = g + new_hypothesises_list
      g = inconsistent_hypothesis(g,x)
    print("s",s)
    print("g",g)

  # cleaning G
  generalness_threshold = 0
  for h in g:
    if count_of_question_marks(h) > generalness_threshold:
        generalness_threshold = count_of_question_marks(h)
  g = list(filter(lambda h: count_of_question_marks(h) >= generalness_threshold,g))

  generalness_threshold = 0
  for h in g:
      if count_of_T(h) > generalness_threshold:
          generalness_threshold = count_of_T(h)
  g = list(filter(lambda h: count_of_T(h) < generalness_threshold,g))

  # cleaning S
  # there can be at most len(features) in a hypothesis
  generalness_threshold = len(features)
  for h in s:
    if count_of_question_marks(h) < generalness_threshold:
        generalness_threshold = count_of_question_marks(h)
  print("generalness_threshold",generalness_threshold)
  s = list(filter(lambda h: count_of_question_marks(h) <= generalness_threshold,s))
  
  generalness_threshold = len(features)
#  for h in s:
#    if count_of_question_marks
#  generalness_threshold = 0
#  for h in s:
#      if count_of_T(h) > generalness_threshold:
#          generalness_threshold = count_of_T(h)
#  g = list(filter(lambda h: count_of_T(h) < generalness_threshold,g))



  print("after pruning")
  print("s",s)
  print("g",g)
  return (s,g)
