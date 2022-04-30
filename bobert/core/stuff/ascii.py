from pyfiglet import Figlet


fig = Figlet(font="standard")
fig_small = Figlet(font="small")


def to_ascii(_input, small=False):
    if small:
        ascii_text = fig_small.renderText(_input)
    else:
        ascii_text = fig.renderText(_input)
    ascii_text = ascii_text.replace('```', '```')
    return'```\n' + ascii_text + '\n```'