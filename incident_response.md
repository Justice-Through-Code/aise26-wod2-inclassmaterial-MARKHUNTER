# My Emergency Plan - I Accidentally Put Secrets on GitHub!

**What Happened:** I put my secret API keys in my code and pushed it to GitHub  
**My Name:** Mark Hunter  
**Date:** December 4, 2025  

---

## 🚨 OH NO! WHAT HAPPENED

**The Problem:** I accidentally put my secret API keys in my code 3 commits ago  
**Where:** My code is on GitHub where EVERYONE can see it  
**The Keys:** They're still being used on my real website right now  
**When I Found Out:** 2 hours after I did it  
**How Bad Is It:** REALLY BAD - I need to fix this NOW!

---

## STEP 1: FIX THE PROBLEM RIGHT NOW! (First 15 minutes)

### What I Do FIRST: Change All My Passwords/Keys ⚡

**Why I do this first:**
Even if I delete the keys from my code, bad guys might have already seen them (my code was public for 2 hours!). Robots scan GitHub looking for keys all the time.

**What I need to do:**

#### First: Figure out what secrets I exposed (2 minutes)
```bash
# Look at the bad commit to see what I put in there
git show i7j8k9l

# Search for all the secrets I might have exposed
grep -r "api_key\|API_KEY\|secret\|password" <commit-hash>
```

**I need to write down everything I exposed:**
- [ ] API keys
- [ ] Database passwords
- [ ] Secret tokens
- [ ] Other passwords
- [ ] Anything else that should be secret

#### Second: Change All My Secrets Right Now! (5 minutes)

**For each thing I exposed, I need to:**

**If it's an API Key (like Stripe, AWS, etc.):**
```bash
# 1. Log into the website (like stripe.com or aws.amazon.com)
# 2. Find the "API Keys" or "Credentials" page
# 3. Click "Delete" or "Revoke" on the old key
# 4. Click "Create New Key" to get a new one
# 5. Copy the new key (I'll need it in a minute)
```

**If it's a Database Password:**
```sql
-- I need to log into my database and change the password
ALTER USER my_database_user WITH PASSWORD 'my_new_password_here';

-- Or I can make a whole new user:
CREATE USER new_user WITH PASSWORD 'my_new_password';
GRANT ALL PRIVILEGES ON DATABASE my_db TO new_user;
-- Then later delete the old user:
DROP USER old_user;
```

**If it's something else:**
```bash
# I need to find where I got the key/password and change it there
# Every website is different, but usually there's a "Security" or "API" section
```

#### Third: Update My Real Website with the New Keys (5 minutes)
```bash
# I need to tell my website to use the new keys instead of the old ones
# How I do this depends on where my website is hosted

# If I'm using Heroku:
heroku config:set API_KEY=my_new_key_here --app my-app
heroku config:set DATABASE_URL=my_new_database_url --app my-app

# Then I need to restart my website so it uses the new keys:
heroku restart --app my-app
```

#### Fourth: Make Sure My Website Still Works (3 minutes)
```bash
# I need to check that my website is still working with the new keys

# Look at my website's logs to see if there are errors:
heroku logs --tail --app my-app

# Try visiting my website to make sure it works:
# Open it in my browser or use:
curl https://my-website.com

# If everything looks good, I'm done with the emergency part!
```

**✅ GOOD NEWS:** My website is now using the new keys and the old keys can't hurt me anymore!

---

## STEP 2: CLEAN UP MY GIT CODE (Next 15-30 minutes)

### Should I Remove It or Hide It?

Now I need to get the secrets out of my code. I have two choices:

**Choice A: The Safe Way (I should probably do this)**
- ✅ Safe if other people have downloaded my code
- ✅ Keeps the full history so I can see what happened
- ✅ Won't break anyone else's work
- ❌ The secrets are still in the history (but that's okay because I already changed them!)

**Choice B: The Risky Way (only if I'm really sure)**
- ✅ Completely removes secrets from history
- ❌ DANGEROUS if anyone else has downloaded my code
- ❌ Requires force push (scary!)
- ❌ Could break other people's work

### I'll Use the Safe Way (Choice A)

Since I already changed all my keys, it doesn't matter if the old keys are in my Git history. The old keys don't work anymore!

#### How to Do It: Remove Secrets from My Code (5 minutes)
```bash
# First, make sure I'm working on the main code
git checkout main
git pull origin main

# Now I need to edit my code to remove the hardcoded secrets
# I'll open the file and change it

# Before (BAD - secret in the code):
API_KEY = "sk-live-1234567890abcdef"

# After (GOOD - get secret from environment):
import os
API_KEY = os.getenv('API_KEY')

# After I fix the code, I save my changes:
git add my_config_file.py
git commit -m "Security fix: Removed hardcoded API keys

I accidentally put API keys in the code and pushed them to GitHub.
I've now:
- Changed all the API keys (the old ones don't work anymore)
- Removed the keys from the code
- Made the code get keys from environment variables instead

The old keys are still in Git history but they're useless now."

# Push my fix to GitHub:
git push origin main
```

#### Make Sure I Fixed It (2 minutes)
```bash
# Search my code to make sure there are no more secrets:
grep -r "api_key.*=.*sk-" .
grep -r "password.*=.*" . --include="*.py"

# If nothing shows up, I'm good!

# Make sure I'm using environment variables now:
grep -r "os.getenv\|os.environ" . --include="*.py"
# I should see where I'm getting the keys from environment
```

### The Risky Way (Only If I'm Really Sure)

**⚠️ I should ONLY do this if:**
- I'm 100% sure nobody else has downloaded my code
- My team said it's okay
- I understand this could break things

```bash
# Step 1: Save my work just in case
git checkout main
git branch my-backup-just-in-case

# Step 2: Look at my recent commits to find the bad one
git log --oneline -5
# I'll see something like:
# a1b2c3d Fix user authentication bug
# e4f5g6h Update README
# i7j8k9l Add production config  <- This one has the secrets!
# m1n2o3p Add user features
# q4r5s6t Initial setup

# Step 3: Remove the bad commit from history
git rebase -i HEAD~3
# This opens a text editor
# I need to DELETE the line with i7j8k9l (or change 'pick' to 'drop')
# Then save and close

# Step 4: Force push (SCARY!)
git push --force-with-lease origin main

# Step 5: Tell everyone on my team RIGHT NOW!
# I need to send a message saying:
# "URGENT: I changed Git history. You need to:
#  1. Delete your local copy
#  2. Download it again fresh
#  rm -rf project-name
#  git clone <repo-url>"
```

**I probably shouldn't do this.** The safe way is usually better!

---

## STEP 3: MAKE SURE THIS NEVER HAPPENS AGAIN (Next 30-60 minutes)

Now I need to set up safety measures so I don't accidentally commit secrets again!

### Part 1: Tell Git to Ignore Secret Files (5 minutes)

```bash
# I need to add stuff to my .gitignore file
# This tells Git to never save these files

cat >> .gitignore << EOF

# Never save these files - they have secrets!
.env
.env.*
!.env.example
*.key
*.pem
secrets/
config/secrets/
credentials.json

EOF

# Now save this to Git:
git add .gitignore
git commit -m "Add .gitignore to prevent committing secrets"
git push origin main
```

### Part 2: Create an Example File (5 minutes)

```bash
# I'll make a file that shows what secrets I need, but without the real values

cat > .env.example << EOF
# Copy this file to .env and fill in your real values
# NEVER commit the .env file!

# Your API keys (get these from your service websites)
API_KEY=put_your_key_here
STRIPE_KEY=put_your_stripe_key_here

# Your database info
DATABASE_URL=postgresql://user:password@localhost/dbname

# Other secrets
SECRET_KEY=make_a_random_string_here

# How to use this:
# 1. Copy this file: cp .env.example .env
# 2. Edit .env and put in your real keys
# 3. The .env file won't be saved to Git (it's in .gitignore)
EOF

git add .env.example
git commit -m "Add .env.example to show what secrets are needed"
git push origin main
```

### Part 3: Basic Safety Tools (Optional)\n\nI can install tools that check for secrets, but the simple stuff above (.gitignore and .env.example) is the most important!

---

## MY CHECKLIST\n\n### Emergency Steps (Did I do these?) ✅
- [ ] Changed all my API keys and passwords
- [ ] Updated my website with new keys
- [ ] Checked that my website still works
- [ ] Removed secrets from my current code

### Prevention Steps (Did I do these?) ✅
- [ ] Updated .gitignore to ignore secret files
- [ ] Created .env.example template
- [ ] Tested that secrets don't show up in my code

### Communication (Did I tell people?) ✅
- [ ] Told my team about the problem
- [ ] Wrote down what happened
- [ ] Made a plan so it doesn't happen again

---

## SOME HELPFUL GIT COMMANDS

```bash
# Find when I added a secret:
git log -S "api_key" --source --all

# Look at what changed in a commit:
git show <commit-number>

# Undo my last commit but keep my changes:
git reset --soft HEAD~1

# Undo my last commit and throw away changes:
git reset --hard HEAD~1

# See everything I've done recently:
git reflog
```

---

## WHAT I LEARNED

This was scary but now I know what to do if it happens again!

**The most important things:**
1. **Change passwords FIRST** - before I do anything else!
2. **Don't panic** - follow my plan step by step
3. **Use .gitignore** - tell Git to never save secret files
4. **Use environment variables** - never put secrets in my code
5. **It's okay** - everyone makes mistakes, just fix it fast!

**Never put these things in my code:**
- ❌ API keys
- ❌ Passwords
- ❌ Database connection strings
- ❌ Secret tokens
- ❌ Any kind of password or key

**Always do this instead:**
- ✅ Put secrets in a .env file
- ✅ Add .env to .gitignore
- ✅ Use os.getenv() to read secrets
- ✅ Create .env.example to show what secrets are needed

---

## IF THIS HAPPENS AGAIN

1. Don't panic!
2. Change all the passwords/keys RIGHT NOW
3. Remove secrets from my code
4. Check that everything still works
5. Learn from it and move on

The good news: If I change the keys fast enough, the old ones become useless and can't hurt me!

---

*Completed with the help of AI*
