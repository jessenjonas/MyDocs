from urllib.parse import unquote

def define_env(env):
    "Hook function"

    @env.macro
    def urldecode(s):
        Decoded = unquote(s)
        return Decoded
    
    def startswith(str):
        s = startswith(str)
        return s
