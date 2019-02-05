# coding=utf-8
# Copyright 2018 The Tensor2Tensor Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the Evolved Transformer."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np

from tensor2tensor.data_generators import problem_hparams
from tensor2tensor.models import evolved_transformer
from tensor2tensor.models import transformer

import tensorflow as tf

BATCH_SIZE = 3
INPUT_LENGTH = 5
TARGET_LENGTH = 7
VOCAB_SIZE = 10


def get_model():
  hparams = transformer.transformer_tiny()
  hparams.layer_prepostprocess_dropout = 0.0

  p_hparams = problem_hparams.test_problem_hparams(VOCAB_SIZE, VOCAB_SIZE,
                                                   hparams)
  hparams.problem_hparams = p_hparams

  inputs = np.random.randint(VOCAB_SIZE, size=(BATCH_SIZE, INPUT_LENGTH, 1, 1))
  targets = np.random.randint(
      VOCAB_SIZE, size=(BATCH_SIZE, TARGET_LENGTH, 1, 1))
  features = {
      "targets": tf.constant(targets, dtype=tf.int32, name="targets"),
      "target_space_id": tf.constant(1, dtype=tf.int32),
      "inputs": tf.constant(inputs, dtype=tf.int32, name="inputs"),
  }

  return (evolved_transformer.EvolvedTransformer(
      hparams, tf.estimator.ModeKeys.TRAIN, p_hparams), features)


class EvolvedTransformerTest(tf.test.TestCase):

  def testEvolvedTransformer(self):
    model, features = get_model()
    logits, _ = model(features)
    with self.test_session() as session:
      session.run(tf.global_variables_initializer())
      res = session.run(logits)
    self.assertEqual(res.shape, (BATCH_SIZE, TARGET_LENGTH, 1, 1, VOCAB_SIZE))


if __name__ == "__main__":
  tf.test.main()
