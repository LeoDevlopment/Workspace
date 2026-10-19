"""Самопроверка ЛР 3, вариант 4. Запуск: python3 check_lab3.py (рядом должен лежать ./lab3)."""
import os, struct, subprocess, numpy as np

BIN = './lab3'

EX1_IMG = "A2DF4C00 F7C9FE00 9ED84500 B4E85300 99D14D00 92DD5600 A9E04C00 F7D1FA00 D4D0E900"
EX1_SAMPLES = "2\n4 1 2 1 0 2 2 2 1\n4 0 0 0 1 1 1 2 0\n"
EX1_CLASSES = "01 00 01 01 01 01 01 00 00"

EX2_IMG = """D2E27500 CFF65200 D3ED5700 D6E76900 C8F35B00 8E168200 CFF45000 AE977600
D3DC7100 7D1E7B00 AB9A8000 D9E58600 AB967E00 AE9D8000 87058200 D0F95B00
74148000 D0F55900 86136C00 85077400 D6E27700 D3609F00 D1609F00 CC5EA100
CC739D00 7C127F00 AA988800 AFA07D00 D0E37700 7D117A00 D6EB5900 D6E37C00
C9F85700 D655A100 D7EA7400 93127D00 D35BA400 D4DD7900 B0A18400 D6DE7500
D765A900 AD928400 D0D87C00 D7E97F00 CD509E00 CAF85200 CFF75600 CEF45E00
D0E86900 D1D17F00 AD928100 AFA18300 D4DB5C00 88077D00 C6F75700 7D127D00
A99A8E00 C8609E00 D15DA500 AB957E00 AE9A8000 79218100 D065A100 A99E9A00"""
EX2_SAMPLES = """5
4 5 0 0 2 6 1 1 1
6 2 0 7 1 1 0 1 2 6 0 4 0
4 3 0 3 1 0 1 0 0
4 0 3 6 2 5 2 7 2
9 6 4 5 1 7 0 2 1 2 3 4 1 1 5 3 3 2 6
"""
EX2_CLASSES = """02 01 01 02 01 00 01 04 02 00 04 02 04 04 00 01
00 01 00 00 02 03 03 03 03 00 04 04 02 00 01 02
01 03 02 00 03 02 04 02 03 04 02 02 03 01 01 01
02 02 04 04 02 00 01 00 04 03 03 04 04 00 03 04"""
# (классы выше -- ожидание из PDF, разложенное по строкам изображения)

def hexpx(s):
    return [bytes.fromhex(t) for t in s.split()]

def parse_samples(txt):
    nums = [int(x) for x in txt.split()]
    nc, i, res = nums[0], 1, []
    for _ in range(nc):
        n = nums[i]; i += 1
        res.append([(nums[i + 2*k], nums[i + 2*k + 1]) for k in range(n)]); i += 2*n
    return res

def reference(px, samples):
    A = np.array([np.mean([px[y, x] for x, y in s], axis=0) for s in samples], dtype=float)
    n = np.linalg.norm(A, axis=1); n[n == 0] = 1
    return (px.reshape(-1, 3).astype(float) @ (A / n[:, None]).T).argmax(axis=1).reshape(px.shape[:2])

def run(px, samples_txt):
    h, w, _ = px.shape
    a = np.zeros((h, w, 4), dtype=np.uint8); a[:, :, :3] = px
    open('chk_in.data', 'wb').write(struct.pack('<ii', w, h) + a.tobytes())
    r = subprocess.run([BIN], input=f'chk_in.data\nchk_out.data\n{samples_txt}', text=True, capture_output=True)
    if r.returncode != 0 or r.stderr.strip():
        return None, f'rc={r.returncode} stderr={r.stderr.strip()}'
    d = open('chk_out.data', 'rb').read()
    ow, oh = struct.unpack('<ii', d[:8])
    out = np.frombuffer(d[8:], dtype=np.uint8).reshape(oh, ow, 4)
    return out, None

def report(name, ok, extra=''):
    print(f'{name:34} {"OK" if ok else "FAIL"} {extra}')

# --- примеры из условия (сравнение с PDF) ---
for name, img, smp, cls, side in [('Пример 1 из PDF (3x3)', EX1_IMG, EX1_SAMPLES, EX1_CLASSES, 3),
                                  ('Пример 2 из PDF (8x8)', EX2_IMG, EX2_SAMPLES, EX2_CLASSES, 8)]:
    px = np.array([list(p[:3]) for p in hexpx(img)], dtype=np.uint8).reshape(side, side, 3)
    out, err = run(px, smp)
    if err: report(name, False, err); continue
    exp = np.array([int(c) for c in cls.split()]).reshape(side, side)
    report(name, (out[:, :, 3] == exp).all() and (out[:, :, :3] == px).all())

# --- случайные тесты против независимой реализации на numpy ---
rng = np.random.default_rng(2024)
bad = 0
for _ in range(50):
    w, h, nc = int(rng.integers(1, 200)), int(rng.integers(1, 200)), int(rng.integers(1, 33))
    px = rng.integers(0, 256, (h, w, 3), dtype=np.uint8)
    smp = [[(int(rng.integers(0, w)), int(rng.integers(0, h))) for _ in range(int(rng.integers(1, 50)))] for _ in range(nc)]
    txt = f'{nc}\n' + ''.join(f'{len(s)} ' + ' '.join(f'{x} {y}' for x, y in s) + '\n' for s in smp)
    out, err = run(px, txt)
    if err or not (out[:, :, 3] == reference(px, smp)).all(): bad += 1
report('50 случайных тестов (nc до 32)', bad == 0, f'ошибок: {bad}')

# --- проверка ошибок: ERROR в stderr и код 0 ---
px = np.zeros((2, 2, 3), dtype=np.uint8)
for name, txt in [('Пиксель выборки вне картинки', '1\n1 5 5\n'), ('Число классов 0', '0\n'), ('Пустой ввод', '')]:
    out, err = run(px, txt)
    report(name, err is not None and 'ERROR:' in err and 'rc=0' in err)

for f in ('chk_in.data', 'chk_out.data'):
    if os.path.exists(f): os.remove(f)
