
def ParseSeconds(seconds: int) -> str:
    time = ''
    if seconds // 86400:
        time += f'{seconds // 86400} д. '
    if  (seconds % 86400)// 3600:
        time += f'{(seconds % 86400)// 3600} ч. '
    if (seconds % 3600)// 60:
        time += f'{(seconds % 3600)// 60} м. '
    if time == '':
        time = 'мгновенно'
    return time