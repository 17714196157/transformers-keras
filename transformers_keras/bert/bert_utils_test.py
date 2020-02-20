import numpy as np
import tensorflow as tf

from transformers_keras.bert.bert_config import BertConfig
from transformers_keras.bert.bert_utils import build_bert_for_pretraining_model


class BertUtilsTest(tf.test.TestCase):

    def testBuildPretrainingModel(self):
        config = BertConfig(vocab_size=15, max_sequence_length=8)
        model = build_bert_for_pretraining_model(config, True)

        inputs = {
            'input_ids':  tf.constant([1, 2, 3, 4, 5, 6, 7, 8], shape=(1, 8), dtype=tf.int32),
            'input_mask': tf.constant([1, 1, 1, 1, 1, 1, 1, 0],  shape=(1, 8), dtype=tf.int32),
            'token_type_ids':  tf.constant([0, 0, 0, 0, 1, 1, 1, 1], shape=(1, 8),  dtype=tf.int32)
        }

        labels = {
            'relations': tf.constant([1], shape=(1,),  dtype=tf.int32),
            'predictions': np.random.randint(low=0, high=14, size=(1, 8,))
        }

        x_dataset = tf.data.Dataset.from_tensor_slices(inputs)
        y_dataset = tf.data.Dataset.from_tensor_slices(labels)
        dataset = tf.data.Dataset.zip((x_dataset, y_dataset))
        train_dataset = dataset.repeat(100).batch(2)
        print(next(iter(train_dataset)))
        model.fit(train_dataset)

        model.save('/tmp/keras_bert_example', include_optimizer=False, save_format='tf')

    def testLoadSavedModel(self):
        inputs = {
            'input_ids':  tf.constant([1, 2, 3, 4, 5, 6, 7, 8], shape=(1, 8), dtype=tf.int32),
            'input_mask': tf.constant([1, 1, 1, 1, 1, 1, 1, 0],  shape=(1, 8), dtype=tf.int32),
            'token_type_ids':  tf.constant([0, 0, 0, 0, 1, 1, 1, 1], shape=(1, 8),  dtype=tf.int32)
        }
        x_dataset = tf.data.Dataset.from_tensor_slices(inputs)
        loaded_model = tf.saved_model.load('/tmp/keras_bert_example')
        for _, x in enumerate(x_dataset.repeat(10).batch(2)):
            outputs = loaded_model(inputs=[x['input_ids'], x['token_type_ids'], x['input_mask']])
            predictions, relations, pooled, all_hidden_states, all_attention_scores = outputs
            print(relations)
            print(pooled)
            # print(all_attention_scores)
            print('=' * 80)


if __name__ == "__main__":
    tf.test.main()