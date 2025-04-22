import locale


lang = locale.getlocale()[0]
print(lang)

if lang == "zh_CN":
    print("中文")
elif lang == "en_US":
    print("英文")
else:
    print("其他")