# Digital internship portfolio

A rubric-aligned Streamlit e-portfolio for CIT2C27 Guided Work-Based Learning 1.

## What is included

- Clear landing page for role, company, department, job scope and projects
- At least two structured evidence/artefact case studies
- Knowledge, skills and attitudes mapped to TSC/CCS-style competency evidence
- Rigorous reflection covering work, challenge, action, result, critique, alternatives, growth and accomplishments
- Responsive navigation, interactive evidence details and a pre-publication placeholder check

## Personalise the portfolio

1. Open `portfolio_content.json`.
2. Replace every value beginning with `[REPLACE: ...]`.
3. Add a clear profile photo at `assets/profile.png`.
4. Add only approved/redacted evidence links and short non-confidential code excerpts.
5. Check the Skills Framework for Infocomm Technology and use the exact TSC/CCS names and proficiency levels relevant to your job role.
6. Set `show_editor_checklist` to `false` before final submission.

## Run locally

PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then open the local URL printed in the terminal, normally `http://localhost:8501`.

## Put the app on GitHub

Create a new, empty repository on GitHub first. Do not add a README, licence or `.gitignore` on the GitHub form because those files already exist here.

```powershell
git init
git add .
git commit -m "Create digital portfolio"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

## Deploy on Streamlit Community Cloud

1. Sign in at `https://share.streamlit.io` with the GitHub account that owns the repository.
2. Select **Create app** and then **Yup, I have an app**.
3. Choose your repository and the `main` branch.
4. Set the entrypoint file to `streamlit_app.py`.
5. Choose an optional memorable app URL and select **Deploy**.
6. Test the public URL in a signed-out/private browser window before submitting it to the LMS.

Every later push to GitHub will update the deployed app. If you add secrets in the future, enter them in Streamlit Community Cloud's secret settings and never commit `.streamlit/secrets.toml`.

## Final submission check

- No `[REPLACE: ...]` placeholders remain.
- Profile photo, email and professional links work.
- The company, department, job role, job scope and projects are clear.
- At least two relevant artefacts explain deliverable, contribution, use, skill level, action, result and corrective action.
- KSA statements point to specific evidence.
- Reflection includes critique, a practical alternative and self-introspection.
- Company clearance has been obtained for every workplace artefact.
- The Streamlit link is public and works without signing in.
- The academic integrity declaration has been submitted separately to the LMS.
