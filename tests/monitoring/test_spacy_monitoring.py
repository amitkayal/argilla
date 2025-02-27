#  Copyright 2021-present, the Recognai S.L. team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import random

import argilla as ar
from tests.monitoring.helpers import mock_monitor


def test_spacy_ner_monitor(monkeypatch, mocked_client):
    dataset = "spacy-dataset"
    ar.delete(dataset)

    import spacy

    nlp = spacy.load("en_core_web_sm")
    nlp = ar.monitor(nlp, dataset=dataset, sample_rate=0.5)
    mock_monitor(nlp, monkeypatch)

    random.seed(42)

    for _ in range(0, 20):
        nlp("Paris is my favourite city")

    df = ar.load(dataset)
    df = df.to_pandas()
    assert len(df) == 11
    # assert 10 - std < len(df) < 10 + std
    assert df.text.unique().tolist() == ["Paris is my favourite city"]

    ar.delete(dataset)
    list(nlp.pipe(["This is a text"] * 20))

    df = ar.load(dataset)
    df = df.to_pandas()
    assert len(df) == 6
    assert df.text.unique().tolist() == ["This is a text"]

    ar.delete(dataset)
    list(nlp.pipe([("This is a text", {"meta": "data"})] * 20, as_tuples=True))

    df = ar.load(dataset)
    df = df.to_pandas()
    assert len(df) == 14
    for metadata in df.metadata.values.tolist():
        assert metadata == {"meta": "data"}
