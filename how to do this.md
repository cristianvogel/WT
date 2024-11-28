# WAVETABLE PROCESSING WORKFLOW
## For BitWig WT Format
##  Documentation 27th November 2024

## 1. Source Requirements

`WAV mono 44.1 kHz 16-bit`

For simple single cycle interpolated WTs, load cycles into the `Sonic Academy Node 2` plug in and export the WT with suggested fixed size of 2048 samples. This wavetable output should then be sliced into individual cycles using `ReNoise` and the `Simple Slicer` tool. Jump straight to [Scripted Processing](#3.-Scripted-Processing) when you have the slices ready.

## 2. Pre-Processing
First step is to slice into zero crossing segments. Best tool to do this is `ReNoise`. Use the `Zero Crossing Slicer` tool from the sampler context menu, under `Slices`.

Suggested settings are:
```
Exact Crossings: 1
Min.size: 512
```

Adjust as needed. Main goal is to keep the slices as small as possible whilst containing mostly about one cycle of the waveform.

At this point, its a good idea to run Reaper batch script on the exported slices, no normalisation, but add the extra `bext` chunk that seems to get dropped on export from ReNoise. Also double conforms the mono, 16bit 44.1kHz format.

Ideally, the desired sort order should be set by the first two digits of the filename. This is because the slices will be sorted by filename in the next step.   eg. `01-MySlice.wav`, `02-MySlice.wav`, `03-MySlice.wav` etc.

## Optional Pre-Processing
Had some great results using Sononym to sort the exported slices by brightness, then use the Sononym batch rename feature with a brightness advanced pattern. 

`%basename%-%brightness:range(0:1:0:127):floor()%`

## 3. Scripted Processing

Use two folders. One is the `incoming/Sliced` folder, the other is the `incoming/RN` folder.

The `incoming/Sliced` folder is where the slices from ReNoise are placed. The `incoming/RN` folder is where the slices will be output after the first script stage. 

Run `sortByNameAndResampleTo2048.py` on the `incoming/Sliced` folder. This will sort the slices by leading number on the filename and resample them to 2048 samples. This is the first stage of the processing.

Next, run `fastMake.bash` with the option of final name for the WT. This will create the WT from the slices in the `incoming/RN` folder and move it to the shared Google Drive folder for delivery. 







