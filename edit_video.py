#!/usr/bin/env python3
"""
FotiVidio - Professional Video Editor
Edits a green screen video with backgrounds, B-rolls, zoom effects,
split screen, background music, and audio effects.

Usage:
    python3 edit_video.py --input video_original.mp4

Requirements:
    pip install requests
    ffmpeg must be installed (brew install ffmpeg / apt install ffmpeg)
"""

import subprocess
import os
import sys
import argparse
import requests
from pathlib import Path

ASSETS_DIR = Path("assets")
OUTPUT_DIR = Path("output")
TEMP_DIR = Path("temp")

BACKGROUNDS = {
    "office_1": "https://pikaso.cdnpk.net/private/production/4617436947/render.jpg?token=exp=1782000000~hmac=e0cd4025f5591e70d82617a4648dfba7e0819003b814fe65fa0188a0f286f995",
    "office_2": "https://pikaso.cdnpk.net/private/production/4617436828/render.jpg?token=exp=1782000000~hmac=042f9c85ae9a93f003e11fb057f58c3d6c4d519cb0d6311c70e75056b3799dff",
    "office_3": "https://pikaso.cdnpk.net/private/production/4617438137/render.jpg?token=exp=1782000000~hmac=0dbe7a790843b7dd8e12896ff723927a799809e4d84b659231a35ccaffa940e8",
    "abstract_1": "https://pikaso.cdnpk.net/private/production/4617439380/render.jpg?token=exp=1782000000~hmac=8a011e47b273e68d7fc439bf244e2ea4e3010834774fe7055f5f91cf91aeff93",
    "abstract_2": "https://pikaso.cdnpk.net/private/production/4617439828/render.jpg?token=exp=1782000000~hmac=f8e968c1ff9f5d75e1af8eec9336af3b32db7f50ef6849c9a218325c9388d17a",
    "dashboard_1": "https://pikaso.cdnpk.net/private/production/4617440851/render.png?token=exp=1782000000~hmac=6be7c9dec41c67c30d2a4439858005a56d74df59eef570e9038061b4dda73d16",
    "dashboard_2": "https://pikaso.cdnpk.net/private/production/4617440954/render.png?token=exp=1782000000~hmac=5d77fc141225fd15053f88a065c7ec67117f536bc7699cadd9f307469b2b7542",
}

BROLLS = {
    "workspace": "https://pikaso.cdnpk.net/private/production/4617458509/1bec4235-12b8-4277-8316-20fff9c728fe-0.mp4?token=exp=1782000000~hmac=f267bef8f9b26cc56d8af399d0741cb043a90c8a2441bbe909bb985996921eaa",
    "marketing_graphs": "https://pikaso.cdnpk.net/private/production/4617463309/5a4cb727-bec1-4a48-9a9c-3fa94f12b929-0.mp4?token=exp=1782000000~hmac=b73b9a7dc593ea4380ef638363e24111b1775f80e1c69ad8d270e9e385b5a63e",
    "city_aerial": "https://pikaso.cdnpk.net/private/production/4617458612/f423b421-8cd3-425e-83d3-26f32551c99c-0.mp4?token=exp=1782000000~hmac=d6c99f765e5fd322f9cbad03287cdf6f4296246fb69f9db25efa3545d22e2a7b",
    "ai_chatbot": "https://pikaso.cdnpk.net/private/production/4617462180/0216c86d-303b-4db8-b703-45025dbf301e-0.mp4?token=exp=1782000000~hmac=c578e078c0cfeda260598ef03e016e3667b2953b3b1a358bdd2f70cb3135a098",
    "orlando_aerial": "https://pikaso.cdnpk.net/private/production/4617464057/0fe222a4-5c74-4dce-a76e-19936a9ff210-0.mp4?token=exp=1782000000~hmac=64b19cd48b21fa3ea2dc91f48c1783955253ff2fa17e0b0e461cee2c8a90577c",
    "ai_hand": "https://pikaso.cdnpk.net/private/production/4617467566/6020c72b-78e8-478e-83f3-8ceab49203ea-0.mp4?token=exp=1782000000~hmac=fa7cc3d9bbbe312d577c57d7f57a3b5ce31093c70465659f6122f56fd0b8f8c1",
    "students": "https://pikaso.cdnpk.net/private/production/4617464446/dc0d7dbe-022f-47f1-8a4f-3f65e98ec78e-0.mp4?token=exp=1782000000~hmac=ffafec6f013ca54b2c1dd3e9eb95c11e12fc29f797b5d0618fcd71983bc11a20",
}

AUDIO = {
    "bg_music": "https://pikaso.cdnpk.net/private/production/4617440679/a20a351b-f6e7-4b57-821c-475c6519caba.mp3?token=exp=1782000000~hmac=598c17b6c8ca0f922bc11e32c30374475628e9828ed64fe979396d9e157b78a9",
    "transition_sfx": "https://pikaso.cdnpk.net/private/production/4617452184/a20a35f8-1bdb-4063-bea6-f2bbdd34e2f7.mp3?token=exp=1782000000~hmac=19ea6f8d8efc3f7868cd4514fe236a5b077b9a3ba9360f11f4508d6e48d758a5",
}

# Scene map from video analysis (timestamps in seconds)
SCENES = [
    {"num": 1,  "start": 0,  "end": 2,  "label": "Opening Hook",         "bg": "office_1",     "broll": None,              "zoom": "in",    "split": False},
    {"num": 2,  "start": 2,  "end": 6,  "label": "Opening Hook",         "bg": "office_1",     "broll": None,              "zoom": None,    "split": False},
    {"num": 3,  "start": 6,  "end": 13, "label": "Problem - AI passive", "bg": "abstract_1",   "broll": "ai_hand",         "zoom": None,    "split": True},
    {"num": 4,  "start": 13, "end": 22, "label": "Benefits",             "bg": "dashboard_1",  "broll": "marketing_graphs", "zoom": "out",   "split": False},
    {"num": 5,  "start": 22, "end": 35, "label": "Event Details",        "bg": "abstract_2",   "broll": "orlando_aerial",  "zoom": None,    "split": True},
    {"num": 6,  "start": 35, "end": 41, "label": "Event Perks",          "bg": "office_2",     "broll": None,              "zoom": "in",    "split": False},
    {"num": 7,  "start": 41, "end": 50, "label": "AI Tools",             "bg": "dashboard_2",  "broll": "ai_chatbot",      "zoom": None,    "split": True},
    {"num": 8,  "start": 50, "end": 60, "label": "Learn to Create",      "bg": "dashboard_1",  "broll": "workspace",       "zoom": "out",   "split": False},
    {"num": 9,  "start": 60, "end": 71, "label": "Study Benefits",       "bg": "office_3",     "broll": "students",        "zoom": None,    "split": True},
    {"num": 10, "start": 71, "end": 79, "label": "Multi-media Skills",   "bg": "abstract_1",   "broll": "marketing_graphs", "zoom": "in",    "split": False},
    {"num": 11, "start": 79, "end": 91, "label": "Closing - Value",      "bg": "office_1",     "broll": "city_aerial",     "zoom": "out",   "split": False},
]


def download_asset(name: str, url: str, ext: str) -> Path:
    path = ASSETS_DIR / f"{name}.{ext}"
    if path.exists():
        print(f"  [skip] {name} already downloaded")
        return path
    print(f"  [download] {name}...")
    r = requests.get(url, stream=True, timeout=120)
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    print(f"  [done] {name} ({path.stat().st_size // 1024} KB)")
    return path


def download_all_assets():
    print("\n=== Downloading Assets ===")
    for name, url in BACKGROUNDS.items():
        ext = "png" if ".png" in url else "jpg"
        download_asset(f"bg_{name}", url, ext)
    for name, url in BROLLS.items():
        download_asset(f"broll_{name}", url, "mp4")
    for name, url in AUDIO.items():
        download_asset(name, url, "mp3")
    print("All assets downloaded!\n")


def run_ffmpeg(args: list, desc: str = ""):
    if desc:
        print(f"  [ffmpeg] {desc}...")
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "warning"] + args
    subprocess.run(cmd, check=True)


def step1_extract_audio(input_video: str):
    """Extract original narration audio."""
    print("\n=== Step 1: Extracting Audio ===")
    run_ffmpeg([
        "-i", input_video,
        "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2",
        str(TEMP_DIR / "narration.wav")
    ], "Extracting narration audio")


def step2_chromakey_segments(input_video: str):
    """Remove green screen and composite with backgrounds for each scene."""
    print("\n=== Step 2: Chromakey + Background Compositing ===")
    for scene in SCENES:
        bg_name = scene["bg"]
        ext = "png" if "dashboard" in bg_name else "jpg"
        bg_path = ASSETS_DIR / f"bg_{bg_name}.{ext}"
        seg_out = TEMP_DIR / f"scene_{scene['num']:02d}.mp4"
        duration = scene["end"] - scene["start"]

        zoom_filter = ""
        if scene["zoom"] == "in":
            zoom_filter = (
                f",scale=2*iw:2*ih,"
                f"zoompan=z='min(zoom+0.002,1.3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                f":d={duration * 30}:s=1920x1080:fps=30"
            )
        elif scene["zoom"] == "out":
            zoom_filter = (
                f",scale=2*iw:2*ih,"
                f"zoompan=z='if(eq(on,1),1.3,max(zoom-0.002,1.0))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                f":d={duration * 30}:s=1920x1080:fps=30"
            )

        chromakey_filter = (
            f"[0:v]chromakey=0x00FF00:0.25:0.1,format=yuva420p[fg];"
            f"[1:v]scale=1920:1080,setsar=1[bg_scaled];"
            f"[bg_scaled][fg]overlay=(W-w)/2:(H-h)/2{zoom_filter}[out]"
        )

        run_ffmpeg([
            "-ss", str(scene["start"]),
            "-t", str(duration),
            "-i", input_video,
            "-i", str(bg_path),
            "-filter_complex", chromakey_filter,
            "-map", "[out]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-r", "30", "-pix_fmt", "yuv420p",
            "-t", str(duration),
            str(seg_out)
        ], f"Scene {scene['num']}: {scene['label']} ({duration}s)")


def step3_broll_overlays():
    """Create B-roll split-screen and overlay versions."""
    print("\n=== Step 3: B-Roll Split Screen & Overlays ===")
    for scene in SCENES:
        if not scene["broll"]:
            continue

        seg_in = TEMP_DIR / f"scene_{scene['num']:02d}.mp4"
        broll_path = ASSETS_DIR / f"broll_{scene['broll']}.mp4"
        seg_out = TEMP_DIR / f"scene_{scene['num']:02d}_broll.mp4"
        duration = scene["end"] - scene["start"]

        if scene["split"]:
            # Split screen: presenter on left, B-roll on right
            filter_complex = (
                f"[0:v]scale=960:1080,setsar=1[left];"
                f"[1:v]scale=960:1080,setsar=1[right];"
                f"[left][right]hstack=inputs=2[out]"
            )
        else:
            # B-roll picture-in-picture (bottom-right corner)
            filter_complex = (
                f"[1:v]scale=480:270,setsar=1[pip];"
                f"[0:v][pip]overlay=W-w-30:H-h-30:enable='between(t,1,{min(duration, 4)})'[out]"
            )

        run_ffmpeg([
            "-i", str(seg_in),
            "-stream_loop", "-1",
            "-i", str(broll_path),
            "-filter_complex", filter_complex,
            "-map", "[out]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-r", "30", "-pix_fmt", "yuv420p",
            "-t", str(duration),
            str(seg_out)
        ], f"B-Roll scene {scene['num']}: {'split screen' if scene['split'] else 'PiP'}")

        os.replace(str(seg_out), str(seg_in))


def step4_concatenate_scenes():
    """Concatenate all scene segments into one video."""
    print("\n=== Step 4: Concatenating Scenes ===")
    concat_file = TEMP_DIR / "concat.txt"
    with open(concat_file, "w") as f:
        for scene in SCENES:
            seg = TEMP_DIR / f"scene_{scene['num']:02d}.mp4"
            f.write(f"file '{seg.absolute()}'\n")

    run_ffmpeg([
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-r", "30", "-pix_fmt", "yuv420p",
        str(TEMP_DIR / "video_no_audio.mp4")
    ], "Joining all scenes")


def step5_mix_audio():
    """Mix narration + background music + transition SFX."""
    print("\n=== Step 5: Mixing Audio ===")

    # Transition timestamps (between scenes)
    transition_times = [s["start"] for s in SCENES if s["start"] > 0]
    sfx_filters = ""
    sfx_inputs = ""
    sfx_idx = 3
    for i, t in enumerate(transition_times):
        sfx_inputs += f"-i {ASSETS_DIR / 'transition_sfx.mp3'} "
        sfx_filters += f"[{sfx_idx}:a]adelay={int(t * 1000)}|{int(t * 1000)},volume=0.4[sfx{i}];"
        sfx_idx += 1

    mix_labels = "[narr][music_low]"
    for i in range(len(transition_times)):
        mix_labels += f"[sfx{i}]"

    n_inputs = 2 + len(transition_times)
    filter_audio = (
        f"[0:a]volume=1.0[narr];"
        f"[1:a]volume=0.12,afade=t=in:st=0:d=2,afade=t=out:st=87:d=4[music_low];"
        f"{sfx_filters}"
        f"{mix_labels}amix=inputs={n_inputs}:duration=first:dropout_transition=3[final_audio]"
    )

    cmd_parts = [
        "-i", str(TEMP_DIR / "narration.wav"),
        "-i", str(ASSETS_DIR / "bg_music.mp3"),
    ]
    for _ in transition_times:
        cmd_parts += ["-i", str(ASSETS_DIR / "transition_sfx.mp3")]

    cmd_parts += [
        "-filter_complex", filter_audio,
        "-map", "[final_audio]",
        "-c:a", "aac", "-b:a", "192k",
        str(TEMP_DIR / "mixed_audio.m4a")
    ]

    run_ffmpeg(cmd_parts, "Mixing narration + music + SFX")


def step6_final_compose():
    """Combine final video with mixed audio."""
    print("\n=== Step 6: Final Composition ===")
    output = OUTPUT_DIR / "video_editado_final.mp4"

    run_ffmpeg([
        "-i", str(TEMP_DIR / "video_no_audio.mp4"),
        "-i", str(TEMP_DIR / "mixed_audio.m4a"),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(output)
    ], "Creating final video")

    size_mb = output.stat().st_size / (1024 * 1024)
    print(f"\n{'='*50}")
    print(f"  VIDEO PRONTO!")
    print(f"  Arquivo: {output}")
    print(f"  Tamanho: {size_mb:.1f} MB")
    print(f"{'='*50}\n")


def main():
    parser = argparse.ArgumentParser(description="FotiVidio - Professional Video Editor")
    parser.add_argument("--input", "-i", required=True, help="Path to original green screen video")
    parser.add_argument("--skip-download", action="store_true", help="Skip asset download (if already downloaded)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input video not found: {args.input}")
        sys.exit(1)

    for d in [ASSETS_DIR, OUTPUT_DIR, TEMP_DIR]:
        d.mkdir(exist_ok=True)

    print("=" * 50)
    print("  FotiVidio - Professional Video Editor")
    print("=" * 50)
    print(f"  Input: {args.input}")
    print(f"  Effects: Chromakey, Zoom, Split Screen, B-Rolls")
    print(f"  Audio: Background Music + Transition SFX")
    print("=" * 50)

    if not args.skip_download:
        download_all_assets()

    step1_extract_audio(args.input)
    step2_chromakey_segments(args.input)
    step3_broll_overlays()
    step4_concatenate_scenes()
    step5_mix_audio()
    step6_final_compose()


if __name__ == "__main__":
    main()
