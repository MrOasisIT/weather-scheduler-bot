def weather_formatter(intro:str,api_data:dict):
    data = {"temp":"Текущая температруа на улице - ","wind_speed":"Скорость ветра составляет -","humidity":"Влажность воздуха -"}
    letter = f"{intro}"
    for key,value in api_data.items():
        if value == None:
            continue
        
        text = data.get(key)
        letter = f"{letter},{text} {value},"

    if letter == f"{intro}":
        return "Извините мы не нашли данных"
    return letter    
