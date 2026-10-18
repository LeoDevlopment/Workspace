import glob, os, subprocess, numpy as np

BIN = './lab2'

def sobel_ref(rgb):
    Y = rgb @ np.array([0.299, 0.587, 0.114])
    P = np.pad(Y, 1, mode='edge')
    gx = (P[:-2, 2:] + 2*P[1:-1, 2:] + P[2:, 2:]) - (P[:-2, :-2] + 2*P[1:-1, :-2] + P[2:, :-2])
    gy = (P[2:, :-2] + 2*P[2:, 1:-1] + P[2:, 2:]) - (P[:-2, :-2] + 2*P[:-2, 1:-1] + P[:-2, 2:])
    return np.minimum(np.sqrt(gx*gx + gy*gy), 255).astype(int)

def load(path):
    d = open(path, 'rb').read()
    w, h = np.frombuffer(d[:8], dtype='<i4')
    px = np.frombuffer(d[8:], dtype=np.uint8)
    assert len(px) == 4*w*h, 'размер файла не сходится с заголовком'
    return int(w), int(h), px.reshape(h, w, 4)

for f in sorted(glob.glob('*.data')):
    if f.startswith(('out', 'chk')):
        continue
    w, h, img = load(f)
    r = subprocess.run([BIN], input=f'{f}\nchk_out.data\n', text=True, capture_output=True)
    if r.returncode != 0 or r.stderr.strip():
        print(f'{f:12} {w}x{h}: ОШИБКА  rc={r.returncode} stderr={r.stderr.strip()}'); continue
    ow, oh, out = load('chk_out.data')
    exp = sobel_ref(img[:, :, :3].astype(float))
    diff = np.abs(out[:, :, 0].astype(int) - exp).max()
    gray = (out[:, :, 0] == out[:, :, 1]).all() and (out[:, :, 1] == out[:, :, 2]).all()
    ok = (ow, oh) == (w, h) and diff <= 1 and gray
    print(f'{f:12} {w}x{h}: {"OK" if ok else "FAIL"}  макс.отклонение={diff}  r=g=b: {gray}')
if os.path.exists('chk_out.data'):
    os.remove('chk_out.data')
