# Copyright (C) 2017 Beijing Didi Infinity Technology and Development Co.,Ltd.
# All rights reserved.
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
# ==============================================================================

import tensorflow as tf

from delta.layers.ops import py_x_ops
from delta.utils.hparam import HParams
from delta.data.frontend.base_frontend import BaseFrontend


class Spectrum(BaseFrontend):

  def __init__(self, config: dict):
    super().__init__(config)

  @classmethod
  def params(cls, config=None):
    """
    Set params.
    :param config: contains ten optional parameters.
          --sample_rate			: Sample frequency of waveform data. (int, default = 16000)
          --window_length		: Window length in seconds. (float, default = 0.025)
          --frame_length			: Hop length in seconds. (float, default = 0.010)
          --snip_edges			: If 1, the last frame (shorter than window_length) will be cutoff. If 2, 1 // 2 frame_length data will be padded to data. (int, default = 1)
          ---raw_energy			: If 1, compute frame energy before preemphasis and windowing. If 2,  compute frame energy after preemphasis and windowing. (int, default = 1)
          --preEph_coeff			: Coefficient for use in frame-signal preemphasis. (float, default = 0.97)
          --window_type			: Type of window ("hamm"|"hann"|"povey"|"rect"|"blac"|"tria"). (string, default = "povey")
          --remove_dc_offset		: Subtract mean from waveform on each frame (bool, default = true)
          --is_fbank				: If true, compute power spetrum without frame energy. If false, using the frame energy instead of the square of the constant component of the signal. (bool, default = false)
          --output_type			: If 1, return power spectrum. If 2, return log-power spectrum. (int, default = 2)
    :return: An object of class HParams, which is a set of hyperparameters as name-value pairs.
    """

    window_length = 0.025
    frame_length = 0.010
    output_type = 2
    sample_rate = 16000
    snip_edges = 2
    raw_energy = 1
    preEph_coeff = 0.97
    window_type = 'povey'
    remove_dc_offset = True
    is_fbank = False

    hparams = HParams(cls=cls)
    hparams.add_hparam('window_length', window_length)
    hparams.add_hparam('frame_length', frame_length)
    hparams.add_hparam('output_type', output_type)
    hparams.add_hparam('sample_rate', sample_rate)
    hparams.add_hparam('snip_edges', snip_edges)
    hparams.add_hparam('raw_energy', raw_energy)
    hparams.add_hparam('preEph_coeff', preEph_coeff)
    hparams.add_hparam('window_type', window_type)
    hparams.add_hparam('remove_dc_offset', remove_dc_offset)
    hparams.add_hparam('is_fbank', is_fbank)

    if config is not None:
      hparams.override_from_dict(config)

    return hparams

  def call(self, audio_data, sample_rate=None):
    """
    Caculate power spectrum or log power spectrum of audio data.
    :param audio_data: the audio signal from which to compute spectrum. Should be an (1, N) tensor.
    :param sample_rate: [option]the samplerate of the signal we working with, default is 16kHz.
    :return: A float tensor of size (num_frames, num_frequencies) containing power spectrum (output_type=1)
        or log power spectrum (output_type=2) of every frame in speech.
    """

    p = self.config
    with tf.name_scope('spectrum'):

      if sample_rate == None:
        sample_rate = tf.constant(p.sample_rate, dtype=tf.int32)

      assert_op = tf.compat.v1.assert_equal(
          tf.constant(p.sample_rate), tf.cast(sample_rate, dtype=tf.int32))
      with tf.control_dependencies([assert_op]):

        sample_rate = tf.cast(sample_rate, dtype=float)
        spectrum = py_x_ops.spectrum(
            audio_data,
            sample_rate,
            window_length=p.window_length,
            frame_length=p.frame_length,
            output_type=p.output_type,
            snip_edges=p.snip_edges,
            raw_energy=p.raw_energy,
            preEph_coeff=p.preEph_coeff,
            window_type=p.window_type,
            remove_dc_offset=p.remove_dc_offset,
            is_fbank=p.is_fbank)

        return spectrum
