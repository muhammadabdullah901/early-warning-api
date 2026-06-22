# Deployment Guide — Render.com (free)

Goal: put the API on the internet so anyone can open
`https://<your-app>.onrender.com/docs`.

---

## Step 1 — Put the code on GitHub

Open PowerShell **in the project folder** and run these one by one:

```powershell
git init
git add .
git commit -m "Early Warning System API"
git branch -M main
```

Now create an empty repo on GitHub (github.com → New repository → do NOT add a
README). Copy its URL, then:

```powershell
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

(GitHub will ask you to log in the first time.)

---

## Step 2 — Deploy on Render

1. Go to **https://render.com** and sign up / log in (use "Sign in with GitHub").
2. Click **New +**  →  **Blueprint**.
3. Select your repository. Render finds `render.yaml` and shows the service.
4. Click **Apply** / **Create**.
5. Wait 2–4 minutes for the build to finish.

When it's done you get a URL like:

```
https://early-warning-api.onrender.com
```

Your docs are at:

```
https://early-warning-api.onrender.com/docs
```

Share THAT link with the frontend developer — it works from any computer.

---

## If you prefer the manual way (no render.yaml)

New + → **Web Service** → pick the repo, then set:

| Setting        | Value                                                   |
|----------------|---------------------------------------------------------|
| Runtime        | Python                                                  |
| Build Command  | `pip install -r requirements.txt`                       |
| Start Command  | `uvicorn app.main:app --host 0.0.0.0 --port $PORT`      |
| Instance Type  | Free                                                    |

Add environment variable `ERP_MOCK_MODE = true`.

---

## Good to know

- **Free tier sleeps:** after ~15 min of no traffic the app sleeps. The next
  request takes ~50 seconds to wake it up, then it's fast again. This is normal
  for the free plan.
- **Updating later:** just `git push` again — Render redeploys automatically.
- **Real ERP:** in the Render dashboard → Environment, set `ERP_MOCK_MODE=false`
  and add `ERP_BASE_URL` and `ERP_API_KEY`. No code change needed.
