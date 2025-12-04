# My Code Review - auth_system.py

**My Name:** Mark Hunter  
**Date:** December 4, 2025  
**What I'm Looking At:** auth_system.py  

---

## What I Found

I looked at this code and found a lot of problems that could let hackers into the system. I found **10 really bad security issues** that need to be fixed before anyone uses this code.

---

## Problems I Found

### 🔴 PROBLEM #1: The Secret Key is Written Right in the Code
**Where I Found It:** Lines 6-7  
**What's Wrong:** The API key is sitting right there in the code where anyone can see it.  
**Why This is Bad:** If I put this code on GitHub, everyone on the internet can see my secret key. Then bad guys can pretend to be me and use my account.

**How I Would Fix It:**
```python
# Don't do this - anyone can see the key:
API_KEY = "sk-live-1234567890abcdef"

# Instead, I'll hide it in a secret place:
import os
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    print("Error! I need to set up my API key first!")
```
**How Bad Is It:** Really bad - fix this first!

---
### 🔴 PROBLEM #2: Database Password is Written in Plain Text
**Where I Found It:** Line 7  
**What's Wrong:** The database username and password are just sitting there in the code.  
**Why This is Bad:** Anyone who sees this code can log into my database! They could steal all my user data or delete everything.

**How I Would Fix It:**
```python
# Don't do this - the password is visible:
DATABASE_URL = "postgresql://admin:password123@localhost/prod"

# Instead, I'll keep it secret:
import os
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print("Error! I need to set up my database connection first!")
```
**How Bad Is It:** Really bad - fix this first!
**Priority:** Critical

---
### 🔴 PROBLEM #3: Debug Mode is Turned On
**Where I Found It:** Line 8  
**What's Wrong:** Debug mode is set to True.  
**Why This is Bad:** When debug mode is on, my app shows detailed error messages to users. Hackers can use these messages to figure out how my app works and find ways to break in.

**How I Would Fix It:**
```python
# Don't do this - too much information shown:
DEBUG_MODE = True

# Instead, I'll only turn it on when I'm testing:
import os
DEBUG_MODE = False  # Keep it off for real users
```
**How Bad Is It:** Pretty bad - fix this soon!
**Priority:** High

### 🔴 PROBLEM #4: Hackers Can Trick the Database with Fake Usernames
**Where I Found It:** Line 12  
**What's Wrong:** I'm putting the username directly into my database search without checking it first.  
**Why This is Bad:** A hacker could type something like `admin' OR '1'='1` as their username and trick the database into letting them in without a password!

**How I Would Fix It:**
```python
# Don't do this - hackers can mess with the query:
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
result = conn.execute(query).fetchone()

# Instead, I'll use the safe way with question marks:
query = "SELECT * FROM users WHERE username=? AND password=?"
result = conn.execute(query, (username, password)).fetchone()
```
**How Bad Is It:** Really bad - fix this first!query, (username, password)).fetchone()
```
**Priority:** Critical

### 🔴 PROBLEM #5: I'm Printing Out People's Passwords!
**Where I Found It:** Line 16  
**What's Wrong:** The code prints the password to the screen/log files.  
**Why This is Bad:** Passwords should be secret! If I print them out, they get saved in log files that lots of people can see. That's like writing down everyone's password on a sticky note.

**How I Would Fix It:**
```python
# Don't do this - never print passwords:
print(f"Login attempt: {username}:{password}")

# Instead, I'll only print the username:
print(f"Login attempt for user: {username}")
```
**How Bad Is It:** Really bad - fix this first!ttempt for user: {username}")
```
**Priority:** Critical

### 🔴 PROBLEM #6: Hackers Can Trick the Database Again (Password Reset)
**Where I Found It:** Line 24  
**What's Wrong:** I'm doing the same mistake again when resetting passwords.  
**Why This is Bad:** A hacker could type weird stuff and mess with my database. They could even delete my whole user table!

**How I Would Fix It:**
```python
# Don't do this - same problem as before:
query = f"UPDATE users SET password='{new_password}' WHERE id={user_id}"
conn.execute(query)

# Instead, I'll use the safe way again:
query = "UPDATE users SET password=? WHERE id=?"
conn.execute(query, (new_password, user_id))
```
**How Bad Is It:** Really bad - fix this first!ew_password, user_id))
```
**Priority:** Critical

### 🔴 PROBLEM #7: The Password Protection is Too Weak
**Where I Found It:** Line 28  
**What's Wrong:** I'm using MD5 to scramble passwords, but MD5 is old and easy to crack.  
**Why This is Bad:** Hackers have lists of already-cracked MD5 passwords. They can look up the scrambled password and find the real one in seconds!

**How I Would Fix It:**
```python
# Don't do this - MD5 is too easy to crack:
import hashlib
return hashlib.md5(password.encode()).hexdigest()

# Instead, I'll use bcrypt which is much stronger:
import bcrypt

def hash_password(password):
    # This scrambles the password really well
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password, hashed):
    # This checks if the password is correct
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
```
**How Bad Is It:** Really bad - fix this first!kpw(password.encode('utf-8'), hashed)
```
### 🔴 PROBLEM #8: The Admin Check is Confusing and Easy to Trick
**Where I Found It:** Lines 31-33  
**What's Wrong:** The function checks if someone is an admin in a weird way.  
**Why This is Bad:** It's checking if the user_id is the number 1 OR the word "admin". This is confusing and a hacker might be able to trick it.

**How I Would Fix It:**
```python
# Don't do this - too easy to trick:
def admin_check(user_id):
    if user_id == 1 or user_id == "admin":
        return True
    return False

# Instead, I'll check the database to see if they're really an admin:
def admin_check(user_id):
    # Make sure we got a number
    if not isinstance(user_id, int):
        print("Error! user_id should be a number")
        return False
    
    # Ask the database if this user is an admin
    conn = sqlite3.connect("users.db")
    query = "SELECT is_admin FROM users WHERE id=?"
    result = conn.execute(query, (user_id,)).fetchone()
    conn.close()
    
    # Return True if they're an admin, False if not
    if result and result[0] == 1:
        return True
### 🔴 PROBLEM #9: Not Checking If the Input Makes Sense
**Where I Found It:** All over the code  
**What's Wrong:** I'm not checking if the username and password are valid before using them.  
**Why This is Bad:** Someone could type really long usernames, or weird characters, or nothing at all, and break my program.

**How I Would Fix It:**
```python
# I'll add checks to make sure the input is okay:
def validate_username(username):
    # Check if username exists and is the right length
    if not username or len(username) < 3 or len(username) > 50:
        print("Error! Username must be between 3 and 50 characters")
        return False
    
    # Check if username only has letters and numbers
    if not username.isalnum():
        print("Error! Username can only have letters and numbers")
        return False
    
    return True

def validate_password(password):
    # Check if password exists and is long enough
### 🔴 PROBLEM #10: Not Closing the Database Connection
**Where I Found It:** All over the code  
**What's Wrong:** I open connections to the database but sometimes forget to close them.  
**Why This is Bad:** If my code crashes, the database connection stays open. If this happens too many times, my database runs out of connections and stops working.

**How I Would Fix It:**
```python
# Don't do this - might not close the connection:
conn = sqlite3.connect("users.db")
result = conn.execute(query).fetchone()
# What if there's an error? Connection stays open!

# Instead, I'll make sure it always closes:
try:
    conn = sqlite3.connect("users.db")
    result = conn.execute(query).fetchone()
    conn.close()  # Always close it
except Exception as e:
    print(f"Oops! Something went wrong: {e}")
    if conn:
        conn.close()  # Close even if there's an error
```
---

## What I Need to Do Now

### Fix Right Away (Before Anyone Uses This Code):
1. ✅ Take out all the passwords and keys from the code - put them in a secret file
2. ✅ Fix the database searches so hackers can't trick them
3. ✅ Use bcrypt instead of MD5 for passwords
4. ✅ Stop printing out passwords

### Fix Soon:
5. ✅ Check if usernames and passwords make sense before using them
6. ✅ Make sure I close database connections properly
7. ✅ Fix the admin check to be more secure
8. ✅ Turn off debug mode

### Other Good Ideas:
- Add a limit so people can't try to log in 1000 times
- Lock accounts after too many wrong passwords
- Make people use their phone to log in too (extra security)
- Make sure my website uses HTTPS (the lock icon)

---

## How I'll Test My Fixes

After I fix everything, I need to test:
1. **Login still works** with my new safe database searches
2. **Hackers can't trick it** (I'll try typing `' OR '1'='1` and it should NOT work)
3. **Passwords are scrambled** with bcrypt
4. **No passwords show up** when I print stuff
5. **My secret keys are hidden** in environment variables
6. **Bad usernames get rejected** (like really short ones)
7. **Admin check works right** and can't be tricked
8. **Database connections close** even when something goes wrong

---

## What I Learned

This code has a lot of security problems that could let hackers steal user data or break my app. I learned that I should never:
- Write passwords or secret keys in my code
- Trust what users type without checking it first
- Use old password scramblers like MD5
- Print out passwords

I need to fix all these problems before anyone can use this code. Once I fix them, the code will be much safer, but I should also add extra security like login limits and better logging.

**My Plan:** Fix all the "Really Bad" problems first, then fix the "Pretty Bad" ones, then add extra security features.

---

*Completed with the help of AI*

---

## Testing Recommendations

After implementing fixes, verify:
1. **Authentication works** with parameterized queries
2. **SQL injection attempts fail** (test with `' OR '1'='1`)
3. **Passwords are properly hashed** with bcrypt
4. **No credentials appear in logs**
5. **Environment variables are required** and validated
6. **Input validation rejects** invalid usernames/passwords
7. **Admin checks work correctly** with proper role validation
8. **Database connections close** even when errors occur

---

## Conclusion

This code contains multiple critical security vulnerabilities that would result in complete system compromise if deployed. None of these issues should reach production. Implementing the suggested fixes will bring the code up to basic security standards, but additional security measures (rate limiting, MFA, security monitoring) should also be considered for a production system.

**Recommendation:** Do not deploy until all Critical and High priority issues are resolved and tested.
