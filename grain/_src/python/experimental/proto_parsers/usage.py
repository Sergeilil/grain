# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Usage example of fast_proto_parser."""
from collections.abc import Sequence

from absl import app
from grain._src.python.experimental.proto_parsers import fast_proto_parser
import memory_profiler
import numpy as np

from tensorflow.core.example import example_pb2


@memory_profiler.profile()
def test_parsing_int():
  e = example_pb2.Example()
  # 40 * 10^6 * 8 B = 320 MB
  e.features.feature["foo"].int64_list.value.extend([1, 2, 3, 4] * 10_000_000)
  e_serialized = e.SerializeToString()
  e_parsed: dict[str, np.ndarray] = fast_proto_parser.parse_tf_example(
      e_serialized
  )
  print(e_parsed)


@memory_profiler.profile()
def test_parsing_bytes():
  """Test parsing bytes."""
  e = example_pb2.Example()
  e.features.feature["foo"].bytes_list.value.extend(
      [b"foo", b"bar", b"baz"] * 10_000_000
  )
  # Adding one long string increases the memory footprint due to
  # padding. We may consider strings with variable size (numpy arrays with
  # dtype=object).
  e.features.feature["foo"].bytes_list.value.append(b"fooeiatnrstieanrtoirsent")
  e_serialized = e.SerializeToString()
  e_parsed: dict[str, np.ndarray] = fast_proto_parser.parse_tf_example(
      e_serialized
  )
  print(e_parsed)


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  test_parsing_int()


if __name__ == "__main__":
  app.run(main)
