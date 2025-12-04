# My Merge Conflict Resolution

**Date:** December 4, 2025  
**What I'm Doing:** Combining two different versions of code  
**My Name:** Mark Hunter

---

## What Happened

Two people worked on the same file at the same time and now I need to combine their work.

**Person A's Work:** Added login stuff and password security  
**Person B's Work:** Added database to save users

I need to put both of these together so we have both features working.

---

## Looking at What Each Person Did

### Person A: Login Features
**What they added:**
- Way to create login tokens (JWT)
- Better password scrambling (bcrypt)
- Checks to make sure username and password are okay
- Good error messages

### Person B: Database Features
**What they added:**
- Database to save users permanently
- User table in the database
- Way to see list of all users
- Tools to manage database connections

---

## The Problems I Found

### Problem 1: Different Imports
- **Person A** needed: `jwt`, `bcrypt`, `datetime`, `timedelta`
- **Person B** needed: SQLAlchemy stuff for database
- **What I'll do:** I'll keep all the imports from both people

### Problem 2: Creating Users
- **Person A** checks if the username and password are okay, scrambles the password
- **Person B** saves to the database but doesn't scramble the password (bad!)
- **What I'll do:** Use Person A's checking and scrambling, but save to Person B's database

### Problem 3: App Settings
- **Person A** added a secret key for login tokens
- **Person B** added database setup
- **What I'll do:** Keep both settings

### Problem 4: Missing Features
- Person A has a login page but it doesn't check the database
- Person B has a "show all users" page that's fine
- **What I'll do:** Make the login check the database, keep the "show all users" page

---

## How I Fixed It

I looked at both versions and thought about what to keep:

1. **For creating users:** I used Person A's safety checks and Person B's database
2. **For passwords:** I used Person A's bcrypt (it's safer than what Person B had)
3. **For login:** I combined Person A's token with Person B's database lookup
4. **For listing users:** I kept Person B's code (no problems there)

---

## My Decisions

### Decision 1: Password Safety
**What I chose:** Use bcrypt from Person A  
**Why:** Person B was saving passwords without scrambling them. That's really bad! Anyone who sees the database could read all the passwords.

### Decision 2: Checking Inputs
**What I chose:** Keep all the checks from Person A  
**Why:** We need to make sure usernames and passwords make sense before saving them.

### Decision 3: Database
**What I chose:** Use Person B's database setup  
**Why:** It's organized better and safer than just writing SQL by hand.

### Decision 4: Login
**What I chose:** Use both - Person A's tokens and Person B's database  
**Why:** We need to check the database to see if the password is right, then give them a token to stay logged in.

---

## What I Kept from Each Person

### From Person A:
- ✅ Kept: Login tokens (JWT), password scrambling (bcrypt), input checking
- ✅ Changed: Now saves to database instead of just pretending to work
- ✅ Changed: Login now actually checks the database

### From Person B:
- ✅ Kept: Database setup, User table, "show all users" page
- ✅ Changed: Now checks if username and password are valid before saving
- ✅ Changed: Now scrambles passwords before saving them
- ✅ Added: Password checking when logging in

---

## How I Tested It

### Test 1: Create a User
I tried creating a user with a good username and password.
**What should happen:** User gets saved with scrambled password  
**What happened:** ✅ It worked!

### Test 2: Try a Bad Username
I tried creating a user with username "ab" (too short).
**What should happen:** Error message saying username is too short  
**What happened:** ✅ It worked!

### Test 3: Try a Bad Password
I tried password "short" (not 8 characters).
**What should happen:** Error message saying password is too short  
**What happened:** ✅ It worked!

### Test 4: Login with Right Password
I tried logging in with the correct password.
**What should happen:** Get a login token back  
**What happened:** ✅ It worked!

### Test 5: Login with Wrong Password
I tried logging in with the wrong password.
**What should happen:** Error message  
**What happened:** ✅ It worked!

### Test 6: See All Users
I tried getting the list of all users.
**What should happen:** See usernames but NOT passwords  
**What happened:** ✅ It worked!

---

## What I Learned

### What Went Well
1. I planned it out before I started coding
2. I kept all the good features from both people
3. I made security a priority
4. I tested everything to make sure it works

### What Was Hard
1. Figuring out how to combine bcrypt (Person A) with the database (Person B)
2. Making login work with both tokens and the database
3. Organizing all the imports

### Good Practices I Used
1. ✅ Tested everything thoroughly
2. ✅ Kept the security stuff from Person A
3. ✅ Kept the database organization from Person B
4. ✅ Wrote clear notes about what I did

---

## The Final Result

My merged code has:
- ✅ Safe password storage (bcrypt)
- ✅ Input checking
- ✅ Database to save users permanently
- ✅ Login tokens (JWT)
- ✅ All the features we need
- ✅ Good error messages

This shows that when I have to merge code, I need to understand what both people did and combine the best parts, not just pick one or the other.

---

*Completed with the help of AI*
