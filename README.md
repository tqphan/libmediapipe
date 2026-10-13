# libmediapipe

Builds of `libmediapipe`, the [MediaPipe](https://github.com/google-ai-edge/mediapipe) Tasks C API library, from MediaPipe's open-source tree, for [game-face](https://github.com/tqphan/game-face).

PyPI's `mediapipe` wheels from 0.10.35 on ship a `libmediapipe` built inside Google that contains the Clearcut usage logger, which uploads usage metrics to `play.googleapis.com`. The public MediaPipe source has no such code. MediaPipe's build only copies in a prebuilt library when `mediapipe/tasks/c/prebuilts/` exists, and the public repository has none, so a source build leaves the logger out. The workflow fails if a prebuilts folder appears.

## Releases

Each [release](https://github.com/tqphan/libmediapipe/releases) has one zip per platform, plus `SHA256SUMS` for the zips:

| Zip | Built with | Runs on | OpenCV 4.14.0 (core, imgproc) |
|---|---|---|---|
| `libmediapipe-<ref>-linux-x86_64.zip` | Clang 18 on Ubuntu 24.04 | glibc 2.39+ | built from source, linked in |
| `libmediapipe-<ref>-linux-arm64.zip` | Clang 18 on Ubuntu 24.04 | glibc 2.39+ | built from source, linked in |
| `libmediapipe-<ref>-windows-x86_64.zip` | clang-cl (LLVM) with VS 2022 | Windows 10+ | opencv.org `opencv_world` DLL, included |
| `libmediapipe-<ref>-windows-arm64.zip` | clang-cl (LLVM) with VS 2022 | Windows 11 on Arm | built from source, linked in |
| `libmediapipe-<ref>-macos-arm64.zip` | Apple Clang | macOS 12+ | built from source, linked in |

Each zip holds the library, anything it needs next to it, `LICENSE.mediapipe`, `LICENSE.opencv`, `SOURCE.txt` (the exact MediaPipe commit) and its own `SHA256SUMS`. Tags are `mediapipe-<MediaPipe ref>-<short commit of this repo>`, and a release is never overwritten.

Before publishing, every library passes these checks:

- `scripts/check_mediapipe_lib.py` finds no telemetry strings (`clearcut`, `play.googleapis.com`) and finds every C API function game-face loads.
- It imports no network code: no `socket`, `connect`, `getaddrinfo`, curl or SSL, and on Windows no `wininet`, `winhttp` or `ws2_32`.
- On Linux and macOS it links nothing beyond the OS and C++ runtime. On macOS it targets 12.0 and is ad hoc signed.
- On Windows it is built for the zip's architecture (x64 or ARM64), and on Windows arm64 it imports no OpenCV DLL.

## Building a release

Everything runs in GitHub Actions; nothing needs building locally.

1. Set `MEDIAPIPE_REF` in `.github/workflows/build.yml` to the MediaPipe tag, or pass `ref` on a manual run.
2. Push a commit whose message contains `[mediapipe release]`, or run the workflow by hand with `release` checked. Every platform is built, and the release is published only if all of them pass.
3. In game-face, update `MEDIAPIPE_VERSION`, `MEDIAPIPE_RELEASE` and the hashes in `cmake/FetchMediaPipe.cmake`. The steps are at the top of that file.

To build only some platforms while working on the workflow, put `[mediapipe: windows,macos]` in the commit message. The platform keys are `linux`, `linux-arm64`, `windows`, `windows-arm64` and `macos`.

## Licenses

MediaPipe and OpenCV are Apache-2.0; their licenses ship in every zip.
