import torch
from transformers import BertTokenizer
from transformers import BertModel
from sentence_transformers import SentenceTransformer
from sentence_transformers import models
import numpy
import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import json
import cx_Oracle

#loading bert model for sentence embedding
word_embedding_model = models.Transformer("./bertmodels/output2")
# Apply mean pooling to get one fixed sized sentence vector
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                               pooling_mode_mean_tokens=True,
                               pooling_mode_cls_token=False,
                               pooling_mode_max_tokens=False)

model_sentence_embedding = SentenceTransformer(modules=[word_embedding_model, pooling_model])

#df = pd.read_excel('companylist.xlsx')
companys = [f for f in listdir("annual_reports/")]
for company in companys:
	sentences = []
	outputpath = 'jsons/'+ company + "/"
	if not os.path.exists(outputpath):
		os.makedirs(outputpath)
	companyPath = "annual_reports/" + company + "/"
	seasons = [f for f in listdir(companyPath)]
	for season in seasons:
		dic = {}
		rf = open(companyPath + season, 'r', encoding='utf-8')  
		lines = rf.readlines()
		string = ""
		MAXLEN = 300
		for line in lines:
			if len(string)+len(line) >= 200:
				while(len(string) > MAXLEN):
					sentences.append(string[:MAXLEN])
					string = string[MAXLEN:]
				sentences.append(string)
				string = line
			else:
				string = string + line
		sentences.append(string)
		all_sentence_embeddings = model_sentence_embedding.encode(sentences)  # Batch size 1
		vecs_sentence_embedding = all_sentence_embeddings
		vecs_sentence_embedding = numpy.array(vecs_sentence_embedding).tolist()
		#fp = open( outputpath + file + "/" + companyFile[:-4] + ".json", "w")
		#for vec in vecs_sentence_embedding:
		for i in range(len(vecs_sentence_embedding)):
			dic[sentences[i]] = vecs_sentence_embedding[i]
		with open(outputpath + season[:-4] + ".json", 'w') as fp:
			json.dump(dic, fp)
