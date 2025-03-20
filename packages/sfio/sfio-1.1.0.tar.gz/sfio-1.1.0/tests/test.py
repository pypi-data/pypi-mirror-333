import io

import sfio

# print(sfio.logger.level, sfio.logfile.level, sfio.screen.level)
sfio.logger.setLevel(10)
import mmap
from pathlib import Path

import pyarrow as pa

# print(sfio.logger.level, sfio.logfile.level, sfio.screen.level)
import pyarrow.csv as csv
import pyarrow.parquet as pq

# to parquet
# Path("./.sfio_cache").parent.mkdir(exist_ok=True)
# f = sfio.read(sfio.rootdir/'data/gold_fcc.dump')
fpath = sfio.rootdir / 'data/gold_fcc.dump'
# fpath = '/home/henry/projects_wsl/aicdi_defect/figure/data/c0_[110][-112][-11-1]_screw_deform.dump'
f = sfio.read(fpath)
# f = sfio.read(sfio.rootdir/'data/gold_fcc.atsk')
# f = sfio.read('NaCl.atsk')
print(f[0].section('box').obj)
# for header in f.section('frame'):
#    print(header.section('atoms'))
#    print(header.df)
# print(f.section('header').dict) #('frame'))
# print(f[...])
# print(f.section('header')[1].dict)
# print(f[1].section('header')) #.section('header')[1].dict)
# print(f.section('box').dict)
# print(f.section('atoms').df)
# a = f.section('ionic_shells').df
# print(a)
# print(f.section('properties').df)
# print(f.section('comments').dict)
# print(f.section('atom',0).dict)

# print(f[...])
# print(f.frame(0))
# print(f.frames)
# print(f.section('atom',0))

# section('frame')[1].section('header').text)
# print(f.section('frame',0,190).section('tom').text)
# print(sfio.base.Sectioned.get_section(f, 'header', 0, 404))
# print(f[:4:2][0]) #.section('atom')[0].text)
raise SystemExit
# for fr in f[5]:
#    print(fr)
# print(f.text)
# with f.open() as a:
#    print(a.readline())
#    print(a.readline())
# print(a.readline())

# with f.open():
#    print(f.readline())
# for line in f:
#    print(line)
#    print(f.sections)
#    for line in f:
#        print(line)

# print(f.fileno())
# print(dir(f))
# print(f)
# a = f.read()
# print(a)
# a = f.read()
# print(a)
# print(f.scanned)
#    for line in f:
#        print(line)
#        print(f.size)
# print(f)
# print(f.mode)
# print(f.name)
# print(dir(f))
# print(f.sections)
# print(f.readline())
# print(f.__class__.mro())
# f[] or f.frame() for frame, f.section()
# print(f['a'])
# print(f[0])
# print(f[0:3])
# print(f[2].dict)
# print(f.sections)
# print(f['atom':'aa', 1:3])
# for i in range(4):
# print(f[:2][1])
# print(sfio.base.Ditto(f.read_section('frame',1)).text)
# print(fh[0])
raise SystemExit

fpath = sfio.rootdir / 'data/gold_fcc.dump'

with open(fpath, 'rb') as f:
    mf = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    for line in iter(mf.readline, b""):
        #    for line in f:
        print(line)

raise SystemExit

mmap = pa.memory_map(str(fpath), 'r')

print(mmap.read(4))

reader = csv.open_csv(mmap)
with pq.ParquetWriter("test.parquet", reader.schema) as writer:
    while True:
        try:
            chunk = reader.read_next_batch()
            writer.write_batch(chunk)
        except StopIteration:
            break

data = pq.read_table("test.parquet")
print(data)

# for line in reader.read_next_batch():
#    print(line)

raise SystemExit

f = io.BytesIO(fh[0].encode())
for _ in range(8):
    f.readline()

col_labels = f.readline().decode().split()[2:]
print(col_labels)
f.seek(0)
read_options = pa_csv.ReadOptions(skip_rows=9, column_names=col_labels)
parse_options = pa_csv.ParseOptions(delimiter=' ')
table = pa_csv.read_csv(f, read_options, parse_options)
print(table)
# for line in f:
#    print(line)

#
# from sfio.lmpdump import Lmpdump
#
# with open(sfio.rootdir/'data/gold_fcc.dump', 'r') as f:
#    print(f.mode)
#    data = sfio.read(f)
#    data = sfio.read(f)
# data = sfio.read(sfio.rootdir/'data/gold_fcc.atsk')
# print(f)

# with open(sfio.rootdir/'data/gold_fcc.atsk') as f:
#    print(sfio.read(f))

# f = sfio.read(sfio.rootdir/'data/gold_fcc.atsk')


# with sfio.open(sfio.rootdir/'data/gold_fcc.atsk') as f:
#    pass
#    a = sfio.read(f)
#    print(f.fh)
#    pass
#    print(a)

# with sfio.read(sfio.rootdir/'data/gold_fcc.atsk'):
#    print(f)
#
# f = Lmpdump.read(sfio.rootdir/'data/gold_fcc.dump.gz')
# print(f[0].attrs)

# a = sfio.read(sfio.rootdir/'data/gold_fcc.dump')
# print(a)
