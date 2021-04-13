import tensorflow_text as tf_text
from model import *


reserved_tokens = ["[PAD]", "[START]", "[END]"]

START = tf.argmax(tf.constant(reserved_tokens) == "[START]")
END = tf.argmax(tf.constant(reserved_tokens) == "[END]")

MAX_LENGTH = 20
VOCAB_SIZE = 2**13


def add_start_end(ragged):
    count = ragged.bounding_shape()[0]
    starts = tf.fill([count, 1], START)
    ends = tf.fill([count, 1], END)

    return tf.concat([starts, ragged, ends], axis=1)


def load_model():
    D_MODEL = 128
    NB_LAYERS = 4
    FFN_UNITS = 512
    NB_PROJ = 8
    DROPOUT_RATE = 0.1

    transformer = Transformer(vocab_size_enc=VOCAB_SIZE,
                              vocab_size_dec=VOCAB_SIZE,
                              d_model=D_MODEL,
                              nb_layers=NB_LAYERS,
                              FFN_units=FFN_UNITS,
                              nb_proj=NB_PROJ,
                              dropout_rate=DROPOUT_RATE)

    transformer.load_weights('ckpt/model_weights/model')

    return transformer


def translate(sentence, transformer):
    tokenizer_en = tf_text.BertTokenizer('vocabs/vocab_en.txt')
    tokenizer_es = tf_text.BertTokenizer('vocabs/vocab_es.txt')

    sentence = tf.convert_to_tensor([sentence])
    encoder_input = tokenizer_en.tokenize(sentence)
    encoder_input = encoder_input.merge_dims(-2, -1)
    encoder_input = add_start_end(encoder_input).to_tensor()

    output = tf.convert_to_tensor([START])
    output = tf.expand_dims(output, 0)

    for i in range(MAX_LENGTH):
        predictions = transformer(encoder_input, output, False)
        predictions = predictions[:, -1:, :]
        predicted_id = tf.argmax(predictions, axis=-1)

        output = tf.concat([output, predicted_id], axis=-1)

        if predicted_id == END:
            break

    text = tokenizer_es.detokenize(output)[0].numpy()
    text = tf.strings.reduce_join(text, separator=' ', axis=-1)

    return text.numpy().decode('utf-8')[8:-6]
