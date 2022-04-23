import discord
import os
import subprocess
import signal

TOKEN    = "1234"          # put discord api token here
FILENAME = "tmp.py"        # put filename for the program here
SHELLCMD = "python tmp.py" # put command to run the file here
BOTCMD   = "!python"       # put command to invoke the bot here
TIMEOUT  = 2

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not(BOTCMD in message.content):
        return
    program = BOTCMD.join(message.content.split(BOTCMD)[1:]).strip().strip("```") + "\n"
    source = open(FILENAME, "w")
    source.write(program)
    source.close()

    try:
        p = subprocess.run(
            args=[SHELLCMD],
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            timeout=TIMEOUT,
            universal_newlines=True
        )
    except subprocess.TimeoutExpired:
        stdout, stderr = p.stdout, p.stderr
        embed = discord.Embed(title="process timed out", color=0xff0000)
        await message.reply(embed=embed)
        return

    stdout, stderr = p.stdout, p.stderr

    if stdout == "" or stdout.isspace():
        stdout = "no output"
    else:
        stdout = f"```ansi\n{stdout[:1000]}\n```"

    if stderr == "" or stderr.isspace():
        stderr = "no output"
    else:
        stderr = f"```ansi\n{stderr[:1000]}\n```"

    if p.returncode != 0:
        colour = 0xff0000
    else:
        colour = 0x00ff00

    embed = discord.Embed(color=colour,description=f"process returned {p.returncode}")
    embed.add_field(name="stdout", value=stdout, inline=False)
    embed.add_field(name="stderr", value=stderr, inline=False)
    await message.reply(embed=embed)

client.run(TOKEN)
