r"""
    Generate Static HTML required to post on github
"""

from os import listdir,remove,path
import argparse

front_matter = r"""
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<!-- Automaticaly generated content, please update scripts/htmlgen.py for any change -->
   <head>
      <meta charset="UTF-8">
      <title align="center">blah blah"</title>
      <style type="text/css">
        body, input, select, td, li, div, textarea, p {
        	font-size: 11px;
        	line-height: 16px;
        	font-family: verdana, arial, sans-serif;
        }

        body {
        	margin:5px;
        	background-color:white;
        }

        h1 {
        	font-size:16px;
        	font-weight:bold;
        }

        h2 {
        	font-size:14px;
        	font-weight:bold;
        }
      </style>
   </head>
   <body>
      <article>
         <header>
            <h1>Ultra-Lightweight Neural Differential DSP Vocoder for High Quality Speech Synthesis</h1>
         </header>
      </article>


      <div>
        <h2>Abstract</h2>
        <p>During recent advances in speech synthesis, several vocoders have been proposed using purely neural networks to produce raw waveforms. Although, such methods produce audio with high quality, but even the most efficient works like MB-MelGAN fail to achieve the performance constraints on low end embedded devices such as a smart-glass or a watch. A pure digital signal processing based vocoder can be implemented via using fast fourier transforms and therefore is a magnitude faster than any neural vocoder, but often gets a lower quality. Combining the best of both worlds, we propose an ultra-lightweight differential DSP system, that uses a jointly optimized acoustic model with DSP vocoder, and achieves audio quality comparable to neural vocoders, while being efficient as a DSP vocoder. Our C++ implementation, without any hardware specific optimization, is at 15 MFLOPS, and achieves a vocoder only RTF of 0.003 and overall RTF 0.044 on CPU, surpassing MB-MelGAN by 350 times.</p>
      </div>

      <h2> Supplementary audio samples </h2>
"""

back_matter = r"""
   </body>
</html>
"""


def get_row_column(root='./Long'):
    Columns = [x for x in listdir(root) if x[0] != '.']
    assert len(Columns) > 0, f"No subfolders under {root}/"
    Rows = set(listdir(f"{root}/{Columns[0]}"))
    for c in Columns:
        Rows = Rows.intersection(set(listdir(f"{root}/{c}")))

    cleanup(root,Rows,Columns)

    return list(Rows), Columns

def cleanup(root,rows,columns):
    for c in columns:
        for r in listdir(f"{root}/{c}"):
            if r not in rows:
                fpath = f"{root}/{c}/{r}"
                if args.delete:
                    assert path.isfile(fpath),f"{fpath} not single file"
                    remove(fpath)
                else:
                    print(f"would delete {fpath}")

def gen_table_header(name='noname', cols=["nothing"], file=None):
    print(f"""
    <div>
    <h2> {name} </h2>
      <table border = "1" class="inlineTable">
    """, file=file)
    print(
        ''.join([r"""
        <col width="300">""" for _ in cols]),
        file=file)
    print(
        """     <tr> """, file=file)
    print(
        ''.join([f"""
        <th>{col}</th>""" for col in cols]) +
        """
</tr>""", file=file)


def audio_entry(audio, file=None):
    print(
        f"""
    <td>
        <audio controls style="width: 200px;">
        <source src={audio} type="audio/wav">
            Your browser does not support the audio element.
        </audio>
    </td>""", file=file)


def text_entry(text, file=None):
    print(
        f"""
        <th>{text}</th>""",
        file=file)


def single_row(columns, text=True, file=None):
    print("<tr>", file=file)
    for c in columns:
        if(text):
            text_entry(c, file=file)
        else:
            audio_entry(c, file=file)
    print("</tr>", file=file)


def gen_table(args, file=None):
    A = ['Female Speaker', 'Male Speaker']
    rows_list = [['nicole_base_a_00013.wav', 'nicole_base_a_00041.wav', 'nicole_base_a_00125.wav', 'nicole_base_a_00170.wav',
                'nicole_base_a_00316.wav', 'nicole_base_a_00326.wav', 'nicole_base_a_00355.wav', 'nicole_base_a_00433.wav'], 
                ['donny_base_c_00045.wav', 'donny_base_c_00167.wav', 'donny_base_c_00204.wav', 'donny_base_c_00354.wav',
             'donny_base_c_00366.wav', 'donny_base_c_00594.wav', 'donny_base_c_00643.wav', 'donny_base_c_00981.wav']]
    i = 0
    for t in args.table:
        t = path.join(t, "audio")
        # rows, _ = get_row_column(root=t)
        rows = rows_list[i]
        print("rows = ", rows)
        cols=['GroundTruth','WaveRNN','HifiGAN','MB-MelGAN','DSP Vocoder','DSP Vocoder Adv', 'DDSP Vocoder']
        gen_table_header(name=A[i], cols=cols, file=file)

        cols=['gt','wavernn', 'hifigan', 'mbmelgan', 'dsp', 'dspgan', 'ddspgan']
        for r in rows:
            c = [f"./{t}/{x}/{r}" for x in cols]
            single_row(c, text=args.name_only, file=file)

        print("""
            </table>
        </div>
        """, file=file)
        i += 1


def main(args):
    fname = args.output
    with open(fname, 'w') as f:
        print(front_matter, file=f)
        gen_table(args, file=f)
        print(back_matter, file=f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-o', '--output', type=str,
                        default='index.html', help='output name')
    parser.add_argument('-n', '--name_only',
                        action="store_true", help='put file names only')
    parser.add_argument('-t', '--table', type=str, action="append",
                        nargs='+', help='names of tables', default=['nicole', 'donny'])
    parser.add_argument('-del', '--delete',
                        action="store_true", help='delete files')



    global args
    args = parser.parse_args()

    main(args)
