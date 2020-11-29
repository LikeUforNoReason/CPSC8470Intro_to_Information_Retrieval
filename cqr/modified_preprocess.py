
import json
import copy

from utils import NUM_FOLD

with open('data/TREC_CAsT_2020_Data/2020_manual_evaluation_topics_v1.0.json', 'r') as fin:
    raw_data = json.load(fin)

topic_number_dict = {}
data = []
for group in raw_data:
    topic_number, turn = str(group['number']), group['turn']
    queries = []
    for query in turn:
        query_number, raw_utterance, manual_utterance, automatic_utterance, result_id = str(query['number']), query['raw_utterance'], query['manual_rewritten_utterance'], query['automatic_rewritten_utterance'], query['manual_canonical_result_id']
        queries.append(raw_utterance)
        if query_number == '1':
          continue
        record = {}
        annonated = []
        annonated.append(manual_utterance)
        annonated.append(automatic_utterance)
        record['topic_number'] = topic_number
        record['query_number'] = query_number
        #record['description'] = description
        #record['title'] = title
        record['input'] = copy.deepcopy(queries)
        record['target'] = copy.deepcopy(annonated)
        record['raw_result'] = result_id
        if not topic_number in topic_number_dict:
            topic_number_dict[topic_number] = len(topic_number_dict)
        data.append(record)

with open('data/eval_topics.jsonl', 'w') as fout:
    for item in data:
        json_str = json.dumps(item, ensure_ascii=False)
        fout.write(json_str + '\n')

# Split eval data into K-fold
topic_per_fold = len(topic_number_dict) // NUM_FOLD
for i in range(NUM_FOLD):
    with open('data/eval_topics.jsonl.%d' % i, 'w') as fout:
        for item in data:
            idx = topic_number_dict[item['topic_number']]
            if idx // topic_per_fold == i:
                json_str = json.dumps(item, ensure_ascii=False)
                fout.write(json_str + '\n')

