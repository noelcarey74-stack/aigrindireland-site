from pathlib import Path
import subprocess
p=Path(__file__).parent
inputs=[]
for i in range(1,9):
    inputs+=['-loop','1','-framerate','24','-t','5','-i',str(p/f'frame_{i:02}.png')]
inputs+=['-i',str(p/'voiceover.mp3')]
filters=[]
for i in range(8):filters.append(f'[{i}:v]setpts=PTS-STARTPTS,format=yuv420p[v{i}]')
last='v0'
for i in range(1,8):
    out='fade'+str(i)
    filters.append(f'[{last}][v{i}]xfade=transition=fade:duration=0.6:offset={4.4*i:.1f}[{out}]')
    last=out
args=['ffmpeg','-hide_banner','-y','-loglevel','error']+inputs+['-filter_complex',';'.join(filters),
      '-map',f'[{last}]','-map','8:a','-c:v','libx264','-preset','veryfast','-crf','22',
      '-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','160k','-movflags','+faststart',
      '-shortest',str(p/'AIGrindIreland_Homepage_Preview.mp4')]
print('Rendering screenshot-led video with Irish study app narration...')
r=subprocess.run(args)
print('ffmpeg exit:',r.returncode)
raise SystemExit(r.returncode)
