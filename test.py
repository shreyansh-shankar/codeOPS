from datetime import datetime
formatted_time = datetime.fromisoformat(datetime.now().isoformat()).strftime("%Y-%m-%d %H:%M:%S")
print(formatted_time)
print(type(formatted_time))