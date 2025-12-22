import os
from agents.mcq_agent import generate_questions as base_generate

LINUX_INSTRUCTION = """
You are an expert in Linux and shell programming.
Generate questions ONLY about Linux:

    -Baisc Questions about linux.
    -Basic Commands: ls, cd, pwd, mkdir, rm, cp, mv, touch, cat, wc, find, locate
    -File Permissions and Ownership: chmod, chown, chgrp, umask.
    -Text Processing: grep, sed, awk, cut, sort, uniq, nl.
    -Process Management: ps, top, kill, bg, fg, jobs.
    -System Administration: user management (useradd, usermod, passwd), service management (systemctl, service), package management (apt, yum, pacman).
    -Shell Scripting: variables, loops, conditionals, functions, positional parameters.
    -File System Structure: /bin, /etc, /home, /var, /tmp, /usr.
    -Networking: ifconfig, netstat, ping, ssh, scp.
    -Environment Variables: export, PATH, env.
    -Input/Output Redirection: >, <, >>, |, tee.
    -Metacharacterss: ?, *, [], [-]
    -System Monitoring: df, du, free, uptime.
    -Cron Jobs and Scheduling: crontab.
    -Permissions and Security: sudo, su, groups, visudo.
    -System Logs: /var/log, journalctl.
    -Archive and Compression: tar, gzip, zip.
    -Text Editors: vim, nano.
    -Kernel and System Information: uname, lscpu, lsblk, dmesg.

Do NOT include questions about Python, Java, or other programming languages. Use small shell command snippets when useful.
"""

async def generate_linux_questions(
    difficulty: str,
    num_questions: int,
    api_key: str | None = None,
    fallback_api_key: str | None = None,
    fallback_model: str = "gpt-3.5-turbo"
) -> str:
    return await base_generate(
        subject="linux",
        difficulty=difficulty,
        num_questions=num_questions,
        api_key=api_key,
        fallback_api_key=fallback_api_key,
        fallback_model=fallback_model,
        extra_instruction=LINUX_INSTRUCTION,
    )

import asyncio

async def _test():
    text = await generate_linux_questions(
        difficulty="easy",
        num_questions=5,
        api_key=None,
    )
    print(text)

if __name__ == "__main__" and os.getenv("ENV") == "local":
    asyncio.run(_test())
