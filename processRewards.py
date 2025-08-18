def processRewards(rewards):
    sumLightning = 0
    for item in rewards:
        if item['type'] == 'coins':
            sumLightning += int(item['value'])
            print(f"Начислено {item['value']} молний")
        else:
            print('Ого, ничего себе, бог удачи соизволил тебе подарить карту')
    return sumLightning
