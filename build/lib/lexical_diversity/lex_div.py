import re
from collections import Counter
import math
import pkg_resources

data_filename = pkg_resources.resource_filename('lexical_diversity', 'e_lemma_lower_clean.txt')

punctuation = "`` '' ' . , ? ! ) ( % / - _ -LRB- -RRB- SYM : ;".split(" ")
lemma_file = open(data_filename).read().split("\n")

lemma_dict = {}

for x in lemma_file:
	if x[0] == "#":
		continue
	else:
		lexes = x.split("\t")
		for word in lexes:
			lemma_dict[word] = lexes[0]
		

def tokenize(raw_text):
	for x in punctuation:
		raw_text = raw_text.replace(x,"")
	raw_text = re.sub('\s+',' ',raw_text)
	raw_text = raw_text.lower()
	text = raw_text.split(" ")
	
	return text

def flemmatize(raw_text):
	text = tokenize(raw_text)
	lem_text = []
	for word in text:
		if word in lemma_dict:
			lem_text.append(lemma_dict[word])
		else:
			lem_text.append(word)
	return(lem_text)
	

def safe_divide(numerator, denominator):
	if denominator == 0 or denominator == 0.0:
		index = 0
	else: index = numerator/denominator
	return index

def ttr(text):
	ntokens = len(text)
	ntypes = len(set(text))
	
	return safe_divide(ntypes,ntokens)

def root_ttr(text):
	ntokens = len(text)
	ntypes = len(set(text))
	
	return safe_divide(ntypes, math.sqrt(ntokens))

def log_ttr(text):
	ntokens = len(text)
	ntypes = len(set(text))
	
	return safe_divide(math.log10(ntypes), math.log10(ntokens))

def maas_ttr(text):
	ntokens = len(text)
	ntypes = len(set(text))
	
	return safe_divide((math.log10(ntokens)-math.log10(ntypes)), math.pow(math.log10(ntokens),2))


def mattr(text, window_length = 50):

	if len(text) < (window_length + 1):
		ma_ttr = safe_divide(len(set(text)),len(text))

	else:
		sum_ttr = 0
		denom = 0
		for x in range(len(text)):
			small_text = text[x:(x + window_length)]
			if len(small_text) < window_length:
				break
			denom += 1
			sum_ttr+= safe_divide(len(set(small_text)),float(window_length)) 
		ma_ttr = safe_divide(sum_ttr,denom)

	return ma_ttr

def msttr(text, window_length = 50):

	if len(text) < (window_length + 1):
		ms_ttr = safe_divide(len(set(text)),len(text))

	else:
		sum_ttr = 0
		denom = 0

		n_segments = int(safe_divide(len(text),window_length))
		seed = 0
		for x in range(n_segments):
			sub_text = text[seed:seed+window_length]
			#print sub_text
			sum_ttr += safe_divide(len(set(sub_text)), len(sub_text))
			denom+=1
			seed+=window_length

		ms_ttr = safe_divide(sum_ttr, denom)

	return ms_ttr

def hdd(text):
	#requires Counter import
	def choose(n, k): #calculate binomial
		"""
		A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
		"""
		if 0 <= k <= n:
			ntok = 1
			ktok = 1
			for t in range(1, min(k, n - k) + 1): #this was changed to "range" from "xrange" for py3
				ntok *= n
				ktok *= t
				n -= 1
			return ntok // ktok
		else:
			return 0

	def hyper(successes, sample_size, population_size, freq): #calculate hypergeometric distribution
		#probability a word will occur at least once in a sample of a particular size
		try:
			prob_1 = 1.0 - (float((choose(freq, successes) * choose((population_size - freq),(sample_size - successes)))) / float(choose(population_size, sample_size)))
			prob_1 = prob_1 * (1/sample_size)
		except ZeroDivisionError:
			prob_1 = 0
			
		return prob_1

	prob_sum = 0.0
	ntokens = len(text)
	types_list = list(set(text))
	frequency_dict = Counter(text)

	for items in types_list:
		prob = hyper(0,42,ntokens,frequency_dict[items]) #random sample is 42 items in length
		prob_sum += prob

	return prob_sum 


def mtld(input, min = 10): #original MTLD described in Jarvis & McCarthy 
	def mtlder(text):
		factor = 0
		factor_lengths = 0
		start = 0
		for x in range(len(text)):
			factor_text = text[start:x+1]
			if x+1 == len(text):
				factor += safe_divide((1 - ttr(factor_text)),(1 - .72))
				factor_lengths += len(factor_text)
			else:
				if ttr(factor_text) < .720 and len(factor_text) >= min:
					factor += 1
					factor_lengths += len(factor_text)
					start = x+1
				else:
					continue

		mtld = safe_divide(factor_lengths,factor)
		return mtld
	input_reversed = list(reversed(input))
	mtld_full = safe_divide((mtlder(input)+mtlder(input_reversed)),2)
	return mtld_full

def mtld_ma_bid(text, min = 10): #Average of moving average MTLD when ran forward and backward
	def mtld_ma(text, min = 10):
		factor = 0
		factor_lengths = 0
		for x in range(len(text)):
			sub_text = text[x:]
			breaker = 0
			for y in range(len(sub_text)):
				if breaker == 0:
					factor_text = sub_text[:y+1]	
					if ttr(factor_text) < .720 and len(factor_text) >= min:
						factor += 1
						factor_lengths += len(factor_text)
						breaker = 1
					else:
						continue
		mtld = safe_divide(factor_lengths,factor)
		return mtld

	forward = mtld_ma(text)
	backward = mtld_ma(list(reversed(text)))

	mtld_bi = safe_divide((forward + backward), 2) #average of forward and backward mtld

	return mtld_bi

def mtld_ma_wrap(text, min = 10): #Calculates moving average MTLD from left to right, but wraps to beginning of text instead of calculating partial factors
	factor = 0
	factor_lengths = 0
	start = 0
	double_text = text + text #allows wraparound
	for x in range(len(text)):
		breaker = 0
		sub_text = double_text[x:]
		for y in range(len(sub_text)):
			if breaker == 0:
				factor_text = sub_text[:y+1]
				if ttr(factor_text) < .720 and len(factor_text) >= min:
					factor += 1
					factor_lengths += len(factor_text)
					breaker = 1
				else:
					continue
	mtld = safe_divide(factor_lengths,factor)
	return mtld
