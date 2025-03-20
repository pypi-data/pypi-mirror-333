# NeonAI Audio Files TTS Plugin
[Mycroft](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mycroft-core/plugins) compatible
TTS Plugin for playing back static audio files. Plugin will look for a file whose name matches the requested
TTS string and play it back.

## Configuration:
```yaml
tts:
    module: neon-tts-plugin-audiofiles
    neon-tts-plugin-audiofiles:
      audio_file_path: ~/tts_audio_files
```

## Usage
The path to audio files should be specified in configuration as [noted above](#configuration). 
If using this with the default [Neon Docker Implementation](https://github.com/NeonGeckoCom/NeonCore/tree/dev/docker),
audio files will be read from `xdg/data/neon/AudioFileTTS` by default. 

Audio filenames should generally match the text used to generate them, 
with any special characters (i.e. `/`) replaced with `_`. If
unsure about capitalization, files may be lowercased, though a properly cased
file will take priority over a lowercased one.
For example, the tts request `What time is it?` would resolve
the file `what time is it_.wav`

Some default audio files are provided with this plugin, but it is expected that
any potential TTS requests have supporting `wav` audio files at `audio_file_path`.
Audio files may be organized in any directory structure within that directory.

### Examples
| text             | filename             |
|------------------|----------------------|
| What time is it? | What time is it_.wav |
| It is 11:30 AM   | it is 11_30 am.wav   |

