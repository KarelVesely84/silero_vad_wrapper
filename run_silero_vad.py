#!/usr/bin/env python

import argparse
from pathlib import Path

from silero_vad import load_silero_vad, read_audio, get_speech_timestamps


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--audio-file",
        type=Path,
        required=True,
        help="Path to audio file for running VAD",
    )

    parser.add_argument(
        "--segments-file",
        type=Path,
        required=True,
        help="Path to store segmentation",
    )

    parser.add_argument(
        "--stop-merge-seconds",
        type=float,
        default=20.0,
        help="""
        Segment length after which it is no longer extended.
        Total duration of segment can be longer.
        """,
    )

    parser.add_argument(
        "--speech-pad-ms",
        type=int,
        default=500,
        help="""
        Speech padding in both directions in ms.
        This controls the number of segments.
        """,
    )

    return parser.parse_args()


class SileroVadWrapper:
    def __init__(self):
        self.model = load_silero_vad()

    def process_audio(
        self,
        audio_file: str,
        speech_pad_ms: int,
    ) -> list[dict]:
        # load
        # - is it okay without resampling ?
        audio_samples = read_audio(audio_file)

        # process
        speech_timestamps = get_speech_timestamps(
            audio=audio_samples,
            model=self.model,
            threshold=0.5,
            sampling_rate=16000,  # 8000, 16000 or N x 16000
            min_speech_duration_ms=500,
            max_speech_duration_s=40,
            min_silence_duration_ms=300,
            speech_pad_ms=speech_pad_ms,
            return_seconds=True,  # Return speech timestamps in seconds (default is samples)
            time_resolution=1,
            visualize_probs=False,
            progress_tracking_callback=None,
            neg_threshold=0.35,  # incl. histersis for transion back to non-speech state
            min_silence_at_max_speech=98,  # ms, Minimum silence duration at "max_speech_duration_s"
            use_max_poss_sil_at_max_speech=True,  # use the maximum possible silence at max_speech_duration_s
        )

        return speech_timestamps

    def merge_consecutive_segments(
        self,
        speech_timestamps: list[dict],
        stop_merge_seconds: float = 30.0,
    ) -> list[dict]:
        # post-process (merge speech segments)
        seg_out = None
        speech_timestamps_out = []

        for ii, cur_seg in enumerate(speech_timestamps):
            if seg_out is None:
                # start a new segment
                seg_out = cur_seg
            else:
                if seg_out['end'] == cur_seg['start']:
                    # extend the segment
                    seg_out['end'] = cur_seg['end']
                else:
                    # export segment, start a new one
                    speech_timestamps_out.append(seg_out)
                    seg_out = cur_seg

            # export segment (alredy too long ?)
            if seg_out['end'] - seg_out['start'] > stop_merge_seconds:
                speech_timestamps_out.append(seg_out)
                seg_out = None

        # last segment
        if seg_out:
            speech_timestamps_out.append(seg_out)

        return speech_timestamps_out


def main():
    args = get_args()

    silero_vad = SileroVadWrapper()

    filename = args.audio_file

    ret = silero_vad.process_audio(
        audio_file=filename,
        speech_pad_ms=args.speech_pad_ms,
    )

    ret2 = silero_vad.merge_consecutive_segments(
        speech_timestamps=ret,
        stop_merge_seconds=args.stop_merge_seconds,
    )

    # DEBUG
    #print(f"{filename} {ret} {ret2}")

    # export to audacity format:
    args.segments_file.parent.mkdir(parents=True, exist_ok=True)
    with open(args.segments_file, "w") as fd:
        for dct in ret2:
            print(f"{filename}\t{dct['start']}\t{dct['end']}\tSPEECH", file=fd)


if __name__ == "__main__":
    main()
