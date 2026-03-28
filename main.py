from datetime import datetime

import gifos
from zoneinfo import ZoneInfo

FONT_FILE_LOGO = "./fonts/vtks-blocketo.regular.ttf"
FONT_FILE_BITMAP = "./fonts/gohufont-uni-14.pil"
FONT_FILE_TRUETYPE = "./fonts/IosevkaTermNerdFont-Bold.ttf"


def main():
    t = gifos.Terminal(750, 500, 15, 15, FONT_FILE_BITMAP, 15)

    # Boot sequence — minimal frames
    t.gen_text("", 1, count=1)
    t.toggle_show_cursor(False)
    year_now = datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y")
    t.gen_text("SPIDEY_OS Modular BIOS v4.2.0", 1)
    t.gen_text(f"Copyright (C) {year_now}, \x1b[31mspideystreet systems\x1b[0m", 2)
    t.gen_text("\x1b[94mGitHub Profile Terminal, Rev 420\x1b[0m", 4)
    t.gen_text("Krypton(tm) GIFCPU - 250Hz", 6)
    t.gen_text(
        "Press \x1b[94mDEL\x1b[0m to enter SETUP, \x1b[94mESC\x1b[0m to cancel Memory Test",
        t.num_rows,
    )
    for i in range(0, 65653, 32000):  # 2 steps only
        t.delete_row(7)
        t.gen_text(f"Memory Test: {i}", 7, contin=True)
    t.delete_row(7)
    t.gen_text("Memory Test: 64KB OK", 7, count=1, contin=True)
    t.gen_text("", 11, count=1, contin=True)

    # OS logo scramble
    t.clear_frame()
    t.gen_text("Initiating Boot Sequence .....", 1, contin=True)
    t.gen_text("\x1b[96m", 1, count=0, contin=True)
    t.set_font(FONT_FILE_LOGO, 66)
    os_logo_text = "SPIDEY"
    mid_row = (t.num_rows + 1) // 2
    mid_col = (t.num_cols - len(os_logo_text) + 1) // 2
    effect_lines = gifos.effects.text_scramble_effect_lines(
        os_logo_text, 3, include_special=False
    )
    for i in range(len(effect_lines)):
        t.delete_row(mid_row + 1)
        t.gen_text(effect_lines[i], mid_row + 1, mid_col + 1)

    # Login — 1 frame per step
    t.set_font(FONT_FILE_BITMAP, 15)
    t.clear_frame()
    t.clone_frame(1)
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[93mSPIDEY OS v4.2.0 (tty1)\x1b[0m", 1, count=1)
    t.gen_text("login: ", 3, count=1)
    t.toggle_show_cursor(True)
    t.gen_typing_text("spidey", 3, contin=True)
    t.gen_text("", 4, count=1)
    t.toggle_show_cursor(False)
    t.gen_text("password: ", 4, count=1)
    t.toggle_show_cursor(True)
    t.gen_typing_text("*********", 4, contin=True)
    t.toggle_show_cursor(False)
    time_now = datetime.now(ZoneInfo("Europe/Paris")).strftime(
        "%a %b %d %I:%M:%S %p %Z %Y"
    )
    t.gen_text(f"Last login: {time_now} on tty1", 6)

    # Clear command
    t.gen_prompt(7, count=1)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mclea", 7, contin=True)
    t.delete_row(7, prompt_col)
    t.gen_text("\x1b[92mclear\x1b[0m", 7, count=1, contin=True)

    # Fetch user age
    user_age = gifos.utils.calc_age(5, 3, 2001)
    user_details_lines = f"""
    \x1b[30;101mspidey@GitHub\x1b[0m
    --------------
    \x1b[96mOS:     \x1b[93mmacOS\x1b[0m
    \x1b[96mHost:   \x1b[93mSecret Organization\x1b[0m
    \x1b[96mKernel: \x1b[93mData & AI Engineering\x1b[0m
    \x1b[96mUptime: \x1b[93m{user_age.years} years, {user_age.months} months, {user_age.days} days\x1b[0m
    \x1b[96mIDE:    \x1b[93mCursor, Claude Code, Mistral Vibes\x1b[0m

    \x1b[30;101mSetup:\x1b[0m
    --------------
    \x1b[96mDaily:   \x1b[93mMacBook Air M3 16GB/512GB\x1b[0m
    \x1b[96mCompute: \x1b[93mMac Mini M4 16GB/512GB\x1b[0m
    \x1b[96mNetwork: \x1b[93mSosh Orange Fiber 1 Gb/s\x1b[0m
    """

    t.clear_frame()
    t.gen_prompt(1)
    prompt_col = t.curr_col
    t.clone_frame(1)
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mfetch.s", 1, contin=True)
    t.delete_row(1, prompt_col)
    t.gen_text("\x1b[92mfetch.sh\x1b[0m", 1, contin=True)
    t.gen_typing_text(" -u spidey", 1, contin=True)

    t.toggle_show_cursor(False)
    t.gen_text(user_details_lines, 3, 5, count=1, contin=True)
    t.toggle_show_cursor(True)
    t.gen_prompt(t.curr_row)
    t.gen_typing_text(
        "\x1b[92m# Building things in the dark...",
        t.curr_row,
        contin=True,
    )
    # Hold final frame
    t.gen_text("", t.curr_row, count=1, contin=True)

    # Generate GIF with no loop (play once, freeze on last frame)
    import os
    fps = t._Terminal__fps
    frame_count = t._Terminal__frame_count
    os.system(
        f"ffmpeg -hide_banner -loglevel error -y -r {fps} "
        f"-i './frames/frame_%d.png' "
        f"-filter_complex '[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse' "
        f"-loop -1 output.gif"
    )
    print(f"INFO: Generated output.gif approximately {round(frame_count / fps, 2)}s long (no loop)")


if __name__ == "__main__":
    main()
