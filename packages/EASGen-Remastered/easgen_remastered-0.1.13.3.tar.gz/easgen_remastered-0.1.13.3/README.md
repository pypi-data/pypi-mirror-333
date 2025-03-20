# 🌩️ **EASGen**: A Fast Python EAS Generation Library

![EASGen](https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/img/RefactoredEASGen.png)

EASGen is a powerful Python library for translating **EAS (Emergency Alert System)** ZCZC strings or other data into **SAME (Specific Area Messaging)** headers. It includes robust support for individual headers, attention tones, EOM generation, emulation modes, and WEA tone generation, ensuring a seamless experience for encoding emergency messages.

---

## 🛠️ **Features**
- ✅ **EAS Generation**: Converts raw ZCZC SAME strings into Individual headers, attention tones. Also allows generation of EOMs.
- ✅ **PyDub AudioSegment Output**: Provides easy integration through PyDub AudioSegments.
- ✅ **Audio File Input**: Allows for audio files to be input to allow for audio messages and other forms of audio injection.
- ✅ **Very Quick**: Generates headers quickly and efficiently, allowing for high performance usage.
- ✅ **Emulation Modes**: Mimic the sound of various EAS hardware/software systems.

---

## 🚀 **Installation**

### Linux (Debian-based)
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 -m pip install EASGen-Remastered
```

### Windows
1. [Install Python](https://www.python.org/downloads/).
2. Open CMD and run:
   ```bash
   python -m pip install EASGen-Remastered
   ```

---

## 📖 **Basic Usage**

### Generate a simple SAME Required Weekly Test:
```python
from EASGen import EASGen
from pydub.playback import play

header = "ZCZC-EAS-RWT-005007+0015-0010000-EAR/FOLF-" ## EAS Header to send
Alert = EASGen.genEAS(header=header, attentionTone=False, endOfMessage=True) ## Generate an EAS SAME message with no ATTN signal, and with EOMs.
play(Alert) ## Play the EAS Message
```

<details>
<summary>Output</summary>

<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0001.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
</details>

---

## 🔍 **Advanced Usage**

### To Insert Audio into an alert:
```python
from EASGen import EASGen
from pydub.playback import play
from pydub import AudioSegment

header = "ZCZC-CIV-DMO-033000+0100-0010000-EAR/FOLF-" ## EAS Header to send
audio = AudioSegment.from_wav("NewHampshireDMO.wav") ## Alert Audio import
Alert = EASGen.genEAS(header=header, attentionTone=True, audio=audio, endOfMessage=True) ## Generate an EAS SAME message with an ATTN signal, the imported WAV file as the audio, and with EOMs.
play(Alert) ## Play the EAS Message
## The New Hampshire State Police has activated the New Hampshire Emergency Alert System in order to conduct a practice demo. This concludes this test of the New Hampshire Emergency Alert System.
```

<details>
<summary>Output</summary>

<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0002.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
</details>

---

## Spamming New Hampshire Demos have never been easier!

### For a custom SampleRate:
```python
from EASGen import EASGen
from pydub.playback import play
from pydub import AudioSegment

header = "ZCZC-EAS-DMO-055079+0100-0010000-EAR/FOLF-" ## EAS Header to send
Alert = EASGen.genEAS(header=header, attentionTone=True, endOfMessage=True, sampleRate=48000) ## Generate an EAS SAME message with an ATTN signal, the imported WAV file as the audio, with EOMs, at a samplerate of 48KHz.
play(Alert) ## Play the EAS Message
```

<details>
<summary>Output</summary>

<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0003.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
</details>

---

### To export an alert instead of playing it back:
```python
from EASGen import EASGen
from pydub import AudioSegment

header = "ZCZC-EAS-RWT-055079+0100-0010000-EAR/FOLF-" ## EAS Header to send
Alert = EASGen.genEAS(header=header, attentionTone=True, endOfMessage=True, sampleRate=48000) ## Generate an EAS SAME message with an ATTN signal, the imported WAV file as the audio, and with EOMs.
EASGen.export_wav("Alert.wav", Alert)
```

<details>
<summary>Output</summary>

<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0004.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
</details>

---

### To resample an alert after generation (If sampleRate is making the audio weird):
```python
from EASGen import EASGen
from pydub.playback import play
from pydub import AudioSegment

header = "ZCZC-EAS-DMO-055079+0100-0010000-EAR/FOLF-" ## EAS Header to send
Alert = EASGen.genEAS(header=header, attentionTone=True, endOfMessage=True) ## Generate an EAS SAME message with an ATTN signal, the imported WAV file as the audio, and with EOMs.
Alert = Alert.set_frame_rate(8000) ## Resample the alert to 8KHz for no reason lol.
play(Alert) ## Play the EAS Message
```

<details>
<summary>Output</summary>

<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0005.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
</details>

---

### To simulate an ENDEC type:
```python
from EASGen import EASGen
from pydub.playback import play
from pydub import AudioSegment

header = "ZCZC-CIV-DMO-033000+0100-0010000-EAR/FOLF-" ## EAS Header to send
audio = AudioSegment.from_wav("NewHampshireDMO.wav") ## Alert Audio import
Alert = EASGen.genEAS(header=header, attentionTone=True, audio=audio, mode="DIGITAL", endOfMessage=True) ## Generate an EAS SAME message with an ATTN signal, the imported WAV file as the audio, with EOMs, and with a SAGE DIGITAL ENDEC style.
play(Alert) ## Play the EAS Message
## The New Hampshire State Police has activated the New Hampshire Emergency Alert System in order to conduct a practice demo. This concludes this test of the New Hampshire Emergency Alert System.
```

<details>
<summary>Output</summary>

<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0006.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
</details>

---

### Now you can make all the Mocks you want!

## Supported ENDECS:
> - [x] None
> - [x] TFT (Resample to 8KHZ using ".set_frame_rate(8000)" on the generated alert)
> - [x] EASyCAP (Basically the same as None)
> - [x] DASDEC (Crank up the Samplerate to 48000 for this one)
> - [x] SAGE EAS ENDEC (Mode = "SAGE")
> - [x] SAGE DIGITAL ENDEC (Mode = "DIGITAL")
> - [x] Trilithic EASyPLUS/CAST/IPTV (Mode = "TRILITHIC")
> - [x] NWS (Mode = "NWS", Resample to 11KHZ using ".set_frame_rate(11025)" on the generated alert)

## Unsupported ENDECS:
> - [ ] HollyAnne Units (Can't sample down to 5KHz... This is a good thing.)
> - [ ] Gorman-Reidlich Units (Don't listen to them enough to simulate. I think they're like TFT, but donno.)
> - [ ] Cadco Twister Units (No Data)
> - [ ] MTS Units (No Data)

---

### To hear all the ENDEC styles, do this:
```python
from EASGen import EASGen
from pydub.playback import play
from pydub import AudioSegment

print("Normal / EASyCAP")
play(EASGen.genEAS("ZCZC-EAS-DMO-055079+0100-0391810-EAR/FOLF-", True, True, AudioSegment.empty(), "", 24000, False))
print("DAS")
play(EASGen.genEAS("ZCZC-EAS-DMO-055079+0100-0391810-EAR/FOLF-", True, True, AudioSegment.empty(), "", 48000, True))
print("TFT")
play(EASGen.genEAS("ZCZC-EAS-DMO-055079+0100-0391810-EAR/FOLF-", True, True, AudioSegment.empty(), "", 24000, True).set_frame_rate(8000))
print("NWS")
play(EASGen.genEAS("ZCZC-EAS-DMO-055079+0100-0391810-EAR/FOLF-", True, True, AudioSegment.empty(), "NWS", 24000, True).set_frame_rate(11025))
print("SAGE")
play(EASGen.genEAS("ZCZC-EAS-DMO-055079+0100-0391810-EAR/FOLF-", True, True, AudioSegment.empty(), "SAGE", 24000, True))
print("DIGITAL")
play(EASGen.genEAS("ZCZC-EAS-DMO-055079+0100-0391810-EAR/FOLF-", True, True, AudioSegment.empty(), "DIGITAL", 24000, True))
print("EASyPLUS/CAST/IPTV")
play(EASGen.genEAS("ZCZC-EAS-DMO-055079+0100-0391810-EAR/FOLF-", True, True, AudioSegment.empty(), "TRILITHIC", 24000, True))
```

<details>
<summary>Output</summary>

<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0007.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0008.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0009.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0010.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0011.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0012.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0013.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
</details>

---

## To generate ATTN only alerts, such as NPAS or WEA:

### For NPAS:
```python
from EASGen import EASGen
from pydub.playback import play
from pydub import AudioSegment

Alert = EASGen.genATTN(mode="NPAS") ## Generate an NPAS (AlertReady) Tone
play(Alert) ## Play the NPAS Tones
```

<details>
<summary>Output</summary>

<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0014.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
</details>

---

### For WEA:
```python
from EASGen import EASGen
from pydub.playback import play
from pydub import AudioSegment

Alert = EASGen.genATTN(mode="WEA") ## Generate WEA Tones
play(Alert) ## Play the WEA Tones
```

<details>
<summary>Output</summary>

<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0015.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
</details>

---

### To use the Bandpass Filter functionality:
```python
from EASGen import EASGen
from pydub.playback import play
from pydub import AudioSegment

header = "ZCZC-CIV-DMO-033000+0100-0010000-EAR/FOLF-" ## EAS Header to send
Alert = EASGen.genEAS(header=header, attentionTone=True, mode="DIGITAL", endOfMessage=True, bandpass=True) # New BandPass feature, which improves the audio quality on some emulation modes.
play(Alert) ## Play the EAS Message
```

<details>
<summary>Output</summary>

<audio controls>
  <source src="https://github.com/Newton-Communications/EG/blob/new-gen-modes/doc/audio/docs0016.wav" type="audio/wav">
  Your browser does not support the audio tag.
</audio>
</details>

---

## ⚠️ **Reporting Issues**

- Bugs and other issues can be reported on [Discord](https://discord.com/users/637078631943897103) or in the GitHub Issues tab.
- Include **entire ZCZC SAME strings** and any Audio Files injected and details for accurate and quick fixes.

---

## 📜 **License**

**MIT License**

---

## 👤 **Contact**

- **Developer**: SecludedHusky Systems/Newton Communications
- **Discord**: [Contact Here](https://discord.com/users/637078631943897103)

---

### ❤️ **Thank You for Using My Version of EASGen!**  
Powered by [SecludedHusky Systems](https://services.secludedhusky.com). Get affordable internet radio services and VPS hosting today.