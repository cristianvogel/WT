# WAVETABLE PROCESSING WORKFLOW
## For BitWig WT Format
##  Documentation 
_27th November 2024_

Yes, this can all be scripted into SOX or Python, but I find the manual steps are a good way to check the quality of the slices on the way through. 

Critical quality points to check are:

### 1. Zero crossing at the start and end of the slice ideal. 
### 2. Consider normalisation carefully. 
In general, do not allow signals louder than -3dB.
### 3. Decide where the interpolation should be done. 
It can be done in realtime inside BitWig with a minimum of two single cycles. Or it can be done to an arbitrary key frame count during the source processing and export as outlined below. Factors are whether the source material contains complex details that an interpolation would smooth over.
### 4. Check file ordering
Slices can be ordered explicitly by adding numerical sequence at the start of each filename which is interpreted by the `sortByNameANdResampleTo2048.py` script. This opens possibilities to temporal rearrangment and editing of segments hardcoded in the WT file or a hardcoded sort by brightness, loudness etc. 

### 5. Find a way to play and listen before the final export.
Crucial to check the practicality the table concept before final bake.

## 1. Source Requirements

`WAV mono 44.1 kHz 16-bit`

For simple single cycle interpolated WTs, one really neat way where you can listen as you go and a few more more keyframes if needed, is to load WAV frames into the [Sonic Academy Node](https://www.sonicacademy.com/products/node) plug in and export the WT with suggested fixed size of 2048 samples. This wavetable output should then be sliced into individual cycles. I found [ReNoise](https://www.renoise.com) and the [Simple Slicer](https://www.renoise.com/tools/simpleslicer) tool best for this. Jump straight to [Scripted Processing](#3.-Scripted-Processing) when you have the slices ready.

## 2. Pre-Processing
First step is to slice into zero crossing segments. Best tool to do this I find is again, `ReNoise`. Use the [Zero Crossing Slicer](https://www.renoise.com/tools/zerocrossings) tool from the sampler context menu, under `Slices`.

Suggested settings are:
```
Exact Crossings: 1
Min.size: 512
```

Adjust as needed. Main goal is to keep the slices as small as possible whilst containing mostly about one cycle of the waveform.

At this point, its a good idea to run a [Reaper](https://www.reaper.fm) batch script on the exported slices, no normalisation, but add the extra `bext` chunk that seems to get dropped on export from ReNoise. Also double conforms the mono, 16bit 44.1kHz format.

Ideally, the desired sort order should be set by the first two digits of the filename. This is because the slices will be sorted by filename in the next step.   eg. `01-MySlice.wav`, `02-MySlice.wav`, `03-MySlice.wav` etc.

## Optional Pre-Processing
Had some great results using Sononym to sort the exported slices by brightness, then use the Sononym batch rename feature with a brightness advanced pattern. 

`%basename%-%brightness:range(0:1:0:127):floor()%`

## 3. Scripted Processing

Use two folders. One is the `incoming/Sliced` folder, the other is the `incoming/RN` folder.

The `incoming/Sliced` folder is where the slices from ReNoise are placed. The `incoming/RN` folder is where the slices will be output after the first script stage. 

Run `sortByNameAndResampleTo2048.py` on the `incoming/Sliced` folder. This will sort the slices by leading number on the filename and resample them to 2048 samples. This is the first stage of the processing.

Next, run `fastMake.bash` with the option of final name for the WT. This will create the WT from the slices in the `incoming/RN` folder and move it to the shared Google Drive folder for delivery. 







