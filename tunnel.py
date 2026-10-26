"""인터넷 통로 열기 (start_internet.bat 이 실행해요)
cloudflared 통로를 열고, 주소가 나오면 진행자 화면(/host)을 자동으로 브라우저에 열어줘요.
이 창을 닫거나 Ctrl + C 를 누르면 통로가 닫혀요."""
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import webbrowser

def find_cloudflared():
    path = shutil.which("cloudflared")
    if path:
        return path
    for base in (os.environ.get("ProgramFiles(x86)"), os.environ.get("ProgramFiles"),
                 os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Links")):
        if base:
            for name in ("cloudflared.exe", os.path.join("cloudflared", "cloudflared.exe")):
                cand = os.path.join(base, name)
                if os.path.exists(cand):
                    return cand
    return None


def port_in_use(port=8080):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def ensure_quiz_running():
    """퀴즈가 안 켜져 있으면 새 창으로 켜고, 이미 켜져 있으면 그대로 써요"""
    if port_in_use():
        print("이미 켜져 있는 퀴즈 프로그램이 있어서, 그 프로그램에 통로를 연결해요.")
        print("(다른 폴더나 예전 버전이면 문제가 다르게 보일 수 있어요. 그럴 땐 모든 퀴즈 창을 닫고 다시 실행하세요.)\n")
        return True
    here = os.path.dirname(os.path.abspath(__file__))
    print("퀴즈 프로그램을 새 창으로 켜는 중이에요...")
    if os.name == "nt":
        subprocess.Popen(["cmd", "/c", "start", "Quiz server - keep open", "cmd", "/k",
                          sys.executable, "quiz_game.py"], cwd=here)
    else:
        subprocess.Popen([sys.executable, "quiz_game.py"], cwd=here)
    for _ in range(80):                      # 최대 40초 기다리기
        if port_in_use():
            print("퀴즈 프로그램이 켜졌어요.\n")
            return True
        time.sleep(0.5)
    print("[!] 퀴즈 프로그램이 켜지지 않았어요. 'Quiz server' 창의 빨간 글씨를 확인해주세요.")
    return False


def main():
    if not ensure_quiz_running():
        return
    exe = find_cloudflared()
    if not exe:
        print("\n[!] 통로 도구(cloudflared)가 없어요. install_tunnel.bat 을 먼저 더블클릭해주세요.")
        print("    설치 직후라면 이 창을 닫고 start_internet.bat 을 다시 실행해보세요.")
        return
    proc = subprocess.Popen([exe, "tunnel", "--url", "http://localhost:8080"],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                            encoding="utf-8", errors="replace")
    url, opened = None, False
    print("통로를 여는 중이에요... (10초 정도 걸려요)")
    for line in proc.stdout:
        if not url:
            m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", line)
            if m:
                url = m.group(0)
        if url and not opened and "Registered tunnel connection" in line:
            opened = True
            time.sleep(2)
            print("\n" + "=" * 60)
            print("  인터넷 통로가 열렸어요!")
            print(f"  진행자 화면: {url}/host")
            print("  QR코드에도 이 주소가 자동으로 들어가요.")
            print("  이 창은 게임이 끝날 때까지 닫지 마세요. (Ctrl + C 누르지 않기!)")
            print("=" * 60 + "\n")
            webbrowser.open(url + "/host")
        if "ERR" in line and not opened:
            print("  " + line.strip())
    print("\n통로가 닫혔어요.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n통로를 닫았어요.")
