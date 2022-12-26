import string, secrets, pyotp, qrcodeT, keyboard, os, socket

def GeneratePassword():
    # 32 string password from pool "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    characters =string.ascii_letters + string.digits + string.punctuation

    password = "".join(secrets.choice(characters) for i in range(32))
    print(password)
    
    # # saving password to a file
    # f = open("file path", "w")
    # f.write("Identifiers like Url, Username and the password itself")
    # f.close()

# ten 8-digit numeric(integers) codes 
def GenerateBackupCodes():
    numbers  = string.digits
    backupCodeList = [] # should be global

    for i in range(10):
        backupCode = "".join(secrets.choice(numbers) for j in range(8))
        backupCodeList.append(backupCode)

    print("Save these \033[1mBACKUP CODES\033[0m somewhere safe but accessible!")
    
    f = open(".backupCodes", "w")
    
    for item in backupCodeList:
        # print out contents of backupCodeList line by line
        print(item)
    
        # write each item in backupCodeList to .backupCodes file
        f.write(f"{item}\n")
    
    f.close()

# 32-character base32 secret key that is compatible with Google Authenticator and other OTP apps
base32Secret = None
# some auth apps want the secret key to be formatted as a hex-encoded string
hexSecret = None

# create an authentication link and qrcode to add an authenticator app
def CreateAuth():
    # globarize these variables to enable their usage in other functions
    global base32Secret
    base32Secret = pyotp.random_base32()
    global hexSecret
    hexSecret = pyotp.random_hex()

    # generate url credentials for connection to an authenticator app
    authLink = pyotp.totp.TOTP(base32Secret).provisioning_uri(name="CLI Authentication", issuer_name=f"{os.getlogin()}@{socket.gethostname()}")
    # url can be parsed with pyotp.parse_uri(authLink)

    # write authLink to .backupCodes file
    f = open(".backupCodes", "w")
    f.write(f"Authentication Link: {authLink}")
    f.close()
    
    print("Scan the qrcode below with Google Authenticator, Microsoft Authenticator or any other Authenticator app of your choice")
    # print out qrcode of url to terminal
    qrcodeT.qrcodeT(authLink) 
    print(f"Use secret key \033[1m{base32Secret}\033[0m if you cannot scan the qrcode\nPress Enter to continue...")
    # there is a bug here that causes the system to hold any chars (except enter) and then feed into input() if called immediately after
    keyboard.wait("enter")

def Authenticate():
    # check if an autheticator app has already be added otherwise run CreateAuth()
    if (base32Secret == None and hexSecret == None):
        print("You have not registered an authenticator app")
        CreateAuth()
    # instance of time based authentication
    totp = pyotp.TOTP(base32Secret)

    # check and verify that user input is of integer type
    while True:
        try:
            authCode = int(input("Enter the code from your authenticator app: "))
        except ValueError:
            print("Invalid authentication code!!! Only integers allowed")
            continue
        break

    # verify inputted code is correct
    match totp.verify(authCode):
        case True:
            print("You have been authenticated")
            return True
        
        case False:
            print("Failed to authenticate, try again")
            Authenticate()
            return False    
 
# GenerateBackupCodes()
GeneratePassword()
# CreateAuth()
# print("Just joking around a little bit")
# Authenticate()
# print("Just joking around a lot more")
# Authenticate()