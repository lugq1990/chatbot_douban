"""Load a trained t"""
import torch
import torch.nn as nn
import torch.optim as optim
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM, BertForPreTraining, BertAdam
import os, random
from read_data import readPairs
from tqdm import tqdm
import pickle


def transfer(pair, tokenizer):
	# tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
	# pairs = ['[CLS] do you like apple ? [SEP] ', 'i like apple so much .']
	input_token, label_token = pair[0], pair[1]
	input_text, label_text = tokenizer.tokenize(input_token), tokenizer.tokenize(label_token)

	for word in label_text:
		input_text.append('[MASK]')
	#print(input_text)

	for _ in range(128-len(input_text)):
		input_text.append('[MASK]')
	#print(input_text)

	indexed_tokens = tokenizer.convert_tokens_to_ids(input_text)
	#print(indexed_tokens)

	input_tensor = torch.tensor([indexed_tokens])
	#print(input_tensor)

	loss_ids = [-1] * len(tokenizer.tokenize(input_token))
	loss_ids += tokenizer.convert_tokens_to_ids(label_text)

	loss_ids.append(tokenizer.convert_tokens_to_ids(['[SEP]'])[0])
	for _ in range(128-len(loss_ids)):
		loss_ids.append(-1)
	loss_tensors = torch.tensor([loss_ids])
	# print(loss_tensors)
	return [input_tensor, loss_tensors]

def process(pairs, tokenizer, dump_file_name='processed_file.pkl', dump_file_path='sample_data'):
	"""
	process Processing a list of pairs that with pretrained tokenizer,
			but as pre-processing is a time-consuming task, so let's
			store already processed data from file instead.

	Args:
		pairs ([type]): [description]
		tokenizer ([type]): [description]

	Returns:
		[type]: [description]
	"""
	tensor_pairs = []
	if not os.path.exists(os.path.join(dump_file_path, dump_file_name)):
		for pair in pairs:
			input_text, label_text = tokenizer.tokenize(pair[0]), tokenizer.tokenize(pair[1])
			if len(input_text) + len(label_text) < 128:
				tensor_pair = transfer(pair, tokenizer)
				tensor_pairs.append(tensor_pair)
		print("Tokenize Trim {} Sentence Pair...".format(len(tensor_pairs)))

		print("Dump processed data into file.")
		with open(os.path.join(dump_file_path, dump_file_name), 'wb') as f:
			pickle.dump(tensor_pairs, f)
	else:
		# reload processed file from disk
		print("Load processed data from disk!")
		with open(os.path.join(dump_file_path, dump_file_name), 'rb') as f:
			tensor_pairs = pickle.load(f)
	return tensor_pairs

def train(tensor_pairs, model, batch_size, epochs=500, save_model_path='models'):
	if not os.path.exists(save_model_path):
		os.makedirs(save_model_path, exist_ok=True)

	optimizer = torch.optim.Adamax(model.parameters(), lr = 5e-3)
	for i in tqdm(range(epochs)):
		
		model.train()
		pair_batches = random.sample(tensor_pairs, batch_size)
		input_batch = [tensor[0] for tensor in pair_batches]
		label_batch = [tensor[1] for tensor in pair_batches]
		input_tensor = torch.cat(input_batch, 0)
		label_tensor = torch.cat(label_batch, 0)

		loss = model(input_tensor, masked_lm_labels=label_tensor)
		evalloss = loss.mean().item()
		optimizer.zero_grad()
		loss.backward()
		optimizer.step()

		if i % 10 == 0 or i == epochs - 1:
			print("Now is epoch: {}, Loss: {} ".format(i, evalloss))
			torch.save(model, os.path.join(save_model_path, '{}_backup.tar'.format(i)))
		

def infer_model(save_model_path='models'):
	print("Infer trained model...")

	latest_model_name = sorted([x for x in os.listdir(save_model_path)], key=lambda x: x.split("_")[0], reverse=False)[0]

	model = torch.load(os.path.join(save_model_path, latest_model_name))
	model.eval()

	tokenizer = BertTokenizer.from_pretrained(modelpath)

	with torch.no_grad():
		while(1):
			#try:
			question = input("> ")
			if question == 'q': break
			question = '[CLS] ' + question + ' [SEP] '
			tokenized_text = tokenizer.tokenize(question)
			# print(tokenized_text)
			for _ in range(128-len(tokenized_text)):
				tokenized_text.append("[MASK]")
			indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
			tokens_tensor = torch.tensor([indexed_tokens])
			predictions = model(tokens_tensor)
			start = len(tokenizer.tokenize(question))
			predicted_tokens = []
			while start < len(predictions[0]):
				predicted_index = torch.argmax(predictions[0,start]).item()
				predicted_token = tokenizer.convert_ids_to_tokens([predicted_index])
				if '[SEP]' in predicted_token or '.' in predicted_token:
					break
				predicted_tokens += predicted_token
				start+=1
			result = " ".join(predicted_tokens)
			print(result)



if __name__ == "__main__":
	# todo: How to create our own Q-A dataset and finetune it?
	pairs = readPairs()

	print("Load Bert Tokenizer and Model...")
	modelpath = "bert-base-uncased"
	tokenizer = BertTokenizer.from_pretrained(modelpath)
	model = BertForMaskedLM.from_pretrained(modelpath)

	print("Transfer to Tensor...")
	tensor_pairs = process(pairs, tokenizer)
	
	print("Start Training...")
	batch_size = 32
	train(tensor_pairs, model, batch_size, epochs=200)
		
	infer_model()