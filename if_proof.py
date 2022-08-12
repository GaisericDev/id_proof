from cryptography.fernet import Fernet

global key
key = Fernet.generate_key()

# team member enters user and creates a fernet token to send to the user, Bob, who wants to know if the team member is legit
def createkey(user):
    user = bytes(user, "utf8")
    f = Fernet(key)
    token = f.encrypt(user)
    return token

# user Bob enters his name (Bob) and the provided hash - backend will decrypt using the current key and return the message after verification
def decryptmsg(token, user):
    f = Fernet(key)
    try:
        msg = f.decrypt(token)
        if(bytes(user, "utf8")) == msg:
            return True
        else:
            return False
    except Exception:
        # invalid key
        print("Invalid key")
        return False

def main():
    # key should be regenerated every x amount of time
    global key
    token = createkey("Bob")
    print(f"Token: {token}")
    # Below should return false - Bob22 is not Bob, the team member's proof of identity is only valid when talking to Bob.
    # This is important because otherwise Bob can pretend to be a team member by sending a legit fernet token to Bob22.
    is_valid = decryptmsg(token, "Bob22") 
    print(f"Bob - Bob22, valid key, should return False; Returned {is_valid}")
    is_valid = decryptmsg(token, "Bob") # Should return true - Bob is Bob
    print(f"Bob - Bob, valid key, should return True; Returned {is_valid}")
    # line below simulates key changed after x seconds
    key = Fernet.generate_key()
    print(f"Token changed: {key}")
    is_valid = decryptmsg(token, "Bob") # Should return false - Bob is Bob, but the key used is no longer valid
    print(f"Bob - Bob, invalid key, should return False; Returned {is_valid}")

if __name__ == "__main__":
    main()