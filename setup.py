import sys
import os
from cx_Freeze import setup, Executable

files = [
    'resources/ui/main.ui',
    "resources/ui/menu.ui",
    "resources/ui/pro.ui",
    "resources/ui/statis.ui",
    "resources/statistics.json",
    "resources/statistics_cpy.json",
    "resources/wins_stats.json",
    "resources/wins_stats_cpy.json",
]

if sys.platform == "win32":
    base = "Win32GUI"
if sys.platform == "linux":
    base = "linux"

target = Executable(
    script="main.py",
    base=base,
    icon="resources/shleppa.jpg"
)

setup(
    name="Таблица умножения!",
    version="0.1",
    description="Таблица умножения, что бы запомнить!",
    author="Кирилл Ненашев",
    option={'build_exe': {'include_files': files}},
    executables=[target]
)
