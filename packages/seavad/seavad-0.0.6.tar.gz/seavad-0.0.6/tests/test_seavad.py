#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import os
os.environ["VAD_MODEL_PATH"] = str(Path(__file__).parent.parent / "data/model/silero_vad.onnx")

import pytest

from seavad.main import SeaVAD


@pytest.fixture
def seavad():
    return {
        16000: SeaVAD(
            sample_rate=16000,sample_width=2, vad_on_needed=2, vad_off_needed=5
        ),
        8000: SeaVAD(
            sample_rate=16000,sample_width=2, vad_on_needed=2, vad_off_needed=5
        ),
    }


def test_get_vad_segments_16k(seavad):
    # Read test audio byte sequence
    audio_path = Path(__file__).parent.parent / "data/test_audio/16k_1ch_en_zh.wav"
    with open(audio_path, "rb") as f:
        audio = f.read()
    # Call get_vad_segments and check the result
    segments = seavad[16000].get_vad_segments(audio)
    expected_segments = [(1.376, 2.784), (4.512, 6.368)]
    assert segments == expected_segments


def test_model_states(seavad):
    """Ensure model states are not shared when reusing the onnx model"""
    data = [
        (Path(__file__).parent.parent / "data/test_audio/16k_dual_channel_ch01.wav", [(1.12, 2.656), (7.136, 8.8), (12.32, 14.304)]),
        (Path(__file__).parent.parent / "data/test_audio/16k_dual_channel_ch02.wav", [(3.2, 4.928), (9.472, 11.328)])
    ]
    for audio_path, expected_seg in data:
        # Read test audio byte sequence
        with open(audio_path, "rb") as f:
            audio = f.read()
        # Call get_vad_segments and check the result
        segments = seavad[16000].get_vad_segments(audio)
        assert segments == expected_seg, segments
