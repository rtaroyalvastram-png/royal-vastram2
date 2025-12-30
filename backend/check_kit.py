import pywhatkit
print(dir(pywhatkit))
try:
    help(pywhatkit.sendwhatdoc)
    print("HAS_SENDWHATDOC")
except:
    print("NO_SENDWHATDOC")
