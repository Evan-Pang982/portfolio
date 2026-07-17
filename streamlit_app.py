"""Rubric-aligned digital internship portfolio built with Streamlit.

Edit portfolio_content.json to replace the bracketed placeholders with your
own approved internship content. The application deliberately keeps content
separate from presentation so that updates do not require Python changes.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st


ROOT = Path(__file__).parent
CONTENT_FILE = ROOT / "portfolio_content.json"


st.set_page_config(
    page_title="Digital Portfolio",
    page_icon="DP",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def load_content(path: Path) -> dict:
    """Load portfolio content and surface a useful error for invalid JSON."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        st.error(f"Missing content file: {path.name}")
        st.stop()
    except json.JSONDecodeError as exc:
        st.error(f"Fix the JSON in {path.name}: line {exc.lineno}, column {exc.colno}.")
        st.stop()


def clean(value: object) -> str:
    """Escape content before placing it inside custom HTML."""
    return html.escape(str(value or ""))


def safe_link(url: str) -> str:
    """Allow only links appropriate for a public portfolio."""
    parsed = urlparse(url.strip())
    if parsed.scheme in {"https", "http", "mailto"}:
        return url.strip()
    return ""


def is_placeholder(value: object) -> bool:
    if not isinstance(value, str):
        return False
    upper_value = value.upper()
    return "[REPLACE" in upper_value or "REPLACE-ME" in upper_value


def count_placeholders(value: object) -> int:
    if isinstance(value, dict):
        return sum(count_placeholders(item) for item in value.values())
    if isinstance(value, list):
        return sum(count_placeholders(item) for item in value)
    return int(is_placeholder(value))


def pill(text: str, tone: str = "teal") -> str:
    return f'<span class="pill pill-{clean(tone)}">{clean(text)}</span>'


def section_intro(kicker: str, title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="section-intro">
          <div class="eyebrow">{clean(kicker)}</div>
          <h1>{clean(title)}</h1>
          <p>{clean(copy)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_bullets(items: list[str]) -> str:
    return "".join(f"<li>{clean(item)}</li>" for item in items)


def render_level(level: str) -> None:
    mapping = {"Foundational": 34, "Intermediate": 62, "Advanced": 86}
    width = mapping.get(level, 50)
    st.markdown(
        f"""
        <div class="level-row">
          <span>{clean(level)}</span>
          <div class="level-track"><div style="width:{width}%"></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home(data: dict) -> None:
    profile = data["profile"]
    company = data["company"]
    projects = data["projects"]
    artifacts = data["artifacts"]

    left, right = st.columns([1.55, 0.8], gap="large")
    with left:
        st.markdown(
            f"""
            <div class="hero-copy">
              <div class="eyebrow">DIGITAL INTERNSHIP PORTFOLIO · {clean(profile['period'])}</div>
              <h1>Hi, I'm {clean(profile['name'])}.</h1>
              <p class="hero-role">{clean(profile['role'])} at {clean(company['name'])}</p>
              <p class="hero-summary">{clean(profile['summary'])}</p>
              <div class="hero-pills">
                {pill(company['department'])}
                {pill(profile['course'], 'navy')}
                {pill(profile['location'], 'coral')}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        button_cols = st.columns([0.26, 0.28, 0.46])
        email = safe_link(f"mailto:{profile['email']}")
        linkedin = safe_link(profile["linkedin"])
        with button_cols[0]:
            if email:
                st.link_button("Email me", email, use_container_width=True)
        with button_cols[1]:
            if linkedin:
                st.link_button("LinkedIn", linkedin, use_container_width=True)
    with right:
        photo_path = ROOT / profile.get("photo", "")
        if profile.get("photo") and photo_path.exists():
            st.image(str(photo_path), caption=profile["name"], use_container_width=True)
        else:
            initials = "".join(part[:1] for part in profile["name"].split()[:2]).upper() or "ME"
            st.markdown(
                f"""
                <div class="portrait-placeholder">
                  <div class="portrait-initials">{clean(initials)}</div>
                  <div><strong>Add your clear profile photo</strong><br>
                  Save it as <code>assets/profile.jpg</code>.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    metric_cols = st.columns(3, gap="medium")
    metrics = [
        (str(len(projects)), "Projects documented"),
        (str(len(artifacts)), "Evidence artefacts"),
        (str(len(data["ksa"]["skills"])), "Technical skills mapped"),
    ]
    for column, (value, label) in zip(metric_cols, metrics):
        with column:
            st.markdown(
                f'<div class="metric-card"><strong>{clean(value)}</strong><span>{clean(label)}</span></div>',
                unsafe_allow_html=True,
            )

    section_intro(
        "01 · CONTEXT",
        "Where I worked and what I was trusted to do",
        "A concise overview of the company, department, job role and project scope.",
    )
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(
            f"""
            <div class="content-card accent-teal">
              <div class="card-label">COMPANY & DEPARTMENT</div>
              <h3>{clean(company['name'])}</h3>
              <p>{clean(company['description'])}</p>
              <div class="mini-rule"></div>
              <p><strong>{clean(company['department'])}</strong><br>{clean(company['department_description'])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="content-card accent-coral">
              <div class="card-label">JOB SCOPE</div>
              <h3>{clean(profile['role'])}</h3>
              <ul>{render_bullets(data['job_scope'])}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="quote-card">
          <span>PORTFOLIO THESIS</span>
          <blockquote>{clean(data['portfolio_thesis'])}</blockquote>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_projects(data: dict) -> None:
    section_intro(
        "02 · EXPERIENCE",
        "Role, responsibilities & projects",
        "The work is organised by outcomes, with enough context to understand my contribution.",
    )

    profile = data["profile"]
    st.markdown(
        f"""
        <div class="role-banner">
          <div><span>ROLE</span><strong>{clean(profile['role'])}</strong></div>
          <div><span>PERIOD</span><strong>{clean(profile['period'])}</strong></div>
          <div><span>TEAM</span><strong>{clean(data['company']['department'])}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for index, project in enumerate(data["projects"], start=1):
        st.markdown(
            f"""
            <div class="project-heading">
              <div class="project-number">{index:02d}</div>
              <div>
                <div class="card-label">{clean(project['period'])} · {clean(project['status'])}</div>
                <h2>{clean(project['title'])}</h2>
                <p>{clean(project['summary'])}</p>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        cols = st.columns(3, gap="medium")
        blocks = [
            ("My responsibility", project["responsibility"]),
            ("Approach", project["approach"]),
            ("Outcome", project["outcome"]),
        ]
        for col, (title, body) in zip(cols, blocks):
            with col:
                st.markdown(
                    f'<div class="mini-card"><span>{clean(title)}</span><p>{clean(body)}</p></div>',
                    unsafe_allow_html=True,
                )
        st.markdown(
            '<div class="tag-row">' + "".join(pill(tag, "navy") for tag in project["skills"]) + "</div>",
            unsafe_allow_html=True,
        )


def render_artifact(data: dict, artifact: dict, index: int) -> None:
    title_col, status_col = st.columns([0.76, 0.24], vertical_alignment="center")
    with title_col:
        st.markdown(
            f"""
            <div class="artifact-title">
              <span>ARTEFACT {index:02d} · {clean(artifact['type'])}</span>
              <h2>{clean(artifact['title'])}</h2>
              <p>{clean(artifact['summary'])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with status_col:
        st.markdown(
            f'<div class="status-badge">{clean(artifact["clearance_status"])}</div>',
            unsafe_allow_html=True,
        )

    overview, impact = st.columns([1, 1], gap="large")
    with overview:
        st.markdown("#### Deliverable and contribution")
        st.markdown(
            f"""
            **What I produced**  
            {artifact['deliverable']}

            **My contribution**  
            {artifact['contribution']}

            **How it is used**  
            {artifact['use']}
            """
        )
    with impact:
        st.markdown("#### Actions, evidence and result")
        st.markdown(
            f"""
            **Action taken**  
            {artifact['action']}

            **Measured or observed result**  
            {artifact['result']}

            **Corrective action / next iteration**  
            {artifact['corrective_action']}
            """
        )

    st.markdown("#### Competencies demonstrated")
    skill_cols = st.columns(min(3, max(1, len(artifact["skills"]))))
    for col, skill in zip(skill_cols, artifact["skills"]):
        with col:
            st.markdown(
                f"""
                <div class="skill-card">
                  <span>{clean(skill['framework'])}</span>
                  <h4>{clean(skill['name'])}</h4>
                  <p>{clean(skill['evidence'])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            render_level(skill["level"])

    if artifact.get("code_snippet"):
        with st.expander("View a short, non-confidential code excerpt"):
            st.code(artifact["code_snippet"], language=artifact.get("code_language", "python"))

    artifact_link = safe_link(artifact.get("link", ""))
    if artifact_link:
        st.link_button("Open supporting evidence", artifact_link)
    st.markdown('<div class="artifact-divider"></div>', unsafe_allow_html=True)


def render_evidence(data: dict) -> None:
    section_intro(
        "03 · PROOF OF WORK",
        "Evidence & artefacts",
        "Each case study explains the deliverable, my contribution, its use, the competencies demonstrated and the result.",
    )
    st.info(
        "Confidentiality first: publish only company-approved or redacted evidence. "
        "Never upload credentials, customer data, internal URLs, proprietary source code or unapproved screenshots."
    )
    if len(data["artifacts"]) < 2:
        st.warning("The assessment checklist requires at least two digital evidence artefacts.")
    for index, artifact in enumerate(data["artifacts"], start=1):
        render_artifact(data, artifact, index)


def render_ksa_group(title: str, intro: str, items: list[dict], tone: str) -> None:
    st.markdown(
        f"""
        <div class="ksa-heading ksa-{clean(tone)}">
          <span>{clean(title[0])}</span>
          <div><h2>{clean(title)}</h2><p>{clean(intro)}</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for item in items:
        with st.container(border=True):
            name_col, detail_col = st.columns([0.34, 0.66], gap="large")
            with name_col:
                st.markdown(f"### {item['name']}")
                st.caption(f"{item['framework']} · Evidence: {item['evidence_ref']}")
                render_level(item["level"])
            with detail_col:
                st.write(item["explanation"])
                st.markdown(f"**How I demonstrated it:** {item['demonstration']}")


def render_ksa(data: dict) -> None:
    section_intro(
        "04 · CAPABILITY",
        "Knowledge, skills & attitudes",
        "A transparent KSA map connecting workplace tasks to proficiency and evidence.",
    )
    ksa = data["ksa"]
    render_ksa_group("Knowledge", "What I came to understand more deeply.", ksa["knowledge"], "navy")
    render_ksa_group("Skills", "What I can now do with greater independence.", ksa["skills"], "teal")
    render_ksa_group("Attitudes", "How I behaved while doing the work.", ksa["attitudes"], "coral")


def render_reflection(data: dict) -> None:
    reflection = data["reflection"]
    section_intro(
        "05 · REFLECTIVE PRACTICE",
        "Learning, critique & future work self",
        "Reflection moves beyond description: it examines decisions, limitations, alternatives, growth and next steps.",
    )

    prompt_blocks = [
        ("Nature of work", reflection["nature_of_work"], "What responsibilities defined the role?"),
        ("Challenge faced", reflection["challenge"], "What made the situation difficult?"),
        ("Action & rationale", reflection["action"], "What did I do, and why did I choose that response?"),
        ("Result", reflection["result"], "What changed, and what evidence supports that?"),
        ("Critical evaluation", reflection["critical_evaluation"], "What was limited or could have been stronger?"),
        ("Practical alternative", reflection["alternative"], "What would I try next time?"),
        ("Learning & growth", reflection["learning_growth"], "How did my KSA broaden or deepen?"),
        ("Accomplishment", reflection["accomplishment"], "Why does this outcome matter?"),
    ]
    for index in range(0, len(prompt_blocks), 2):
        cols = st.columns(2, gap="large")
        for col, (title, body, prompt) in zip(cols, prompt_blocks[index : index + 2]):
            with col:
                st.markdown(
                    f"""
                    <div class="reflection-card">
                      <span>{clean(prompt)}</span>
                      <h3>{clean(title)}</h3>
                      <p>{clean(body)}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown(
        f"""
        <div class="future-card">
          <div class="eyebrow">MY FUTURE WORK SELF</div>
          <h2>{clean(reflection['future_self_title'])}</h2>
          <p>{clean(reflection['future_self'])}</p>
          <div class="next-steps"><strong>Next 90 days</strong><ul>{render_bullets(reflection['next_steps'])}</ul></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_contact(data: dict) -> None:
    profile = data["profile"]
    section_intro(
        "06 · CONNECT",
        "Thank you for viewing my portfolio",
        "I welcome conversations about my work, learning journey and future opportunities.",
    )
    st.markdown(
        f"""
        <div class="contact-card">
          <div class="contact-mark">{clean(''.join(part[:1] for part in profile['name'].split()[:2]).upper())}</div>
          <div>
            <h2>{clean(profile['name'])}</h2>
            <p>{clean(profile['role'])} · {clean(data['company']['name'])}</p>
            <p class="contact-note">{clean(data['contact_note'])}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    links = [
        ("Email", safe_link(f"mailto:{profile['email']}")),
        ("LinkedIn", safe_link(profile["linkedin"])),
        ("GitHub", safe_link(profile["github"])),
    ]
    for col, (label, link) in zip(cols, links):
        with col:
            if link:
                st.link_button(label, link, use_container_width=True)
            else:
                st.button(f"Add {label} link", disabled=True, use_container_width=True)
    st.caption(data["privacy_note"])


CUSTOM_CSS = """
<style>
  :root {
    --ink: #17213b;
    --muted: #5f6b7a;
    --paper: #f7f5ef;
    --white: #ffffff;
    --teal: #0e8176;
    --teal-soft: #dff3ee;
    --navy: #233b73;
    --navy-soft: #e7ebf7;
    --coral: #d86d51;
    --coral-soft: #f8e7df;
    --line: #d9dedc;
  }
  .stApp { background: var(--paper); color: var(--ink); }
  [data-testid="stHeader"] { background: rgba(247, 245, 239, .88); }
  [data-testid="stSidebar"] { background: #17213b; }
  [data-testid="stSidebar"] * { color: #f7f5ef; }
  [data-testid="stSidebar"] [role="radiogroup"] label {
    padding: .65rem .8rem; border-radius: 10px; margin-bottom: .18rem;
  }
  [data-testid="stSidebar"] [role="radiogroup"] label:hover { background: rgba(255,255,255,.08); }
  .block-container { max-width: 1180px; padding-top: 2.4rem; padding-bottom: 4rem; }
  h1, h2, h3, h4 { color: var(--ink); letter-spacing: -.025em; }
  p, li { line-height: 1.65; }
  .eyebrow, .card-label, .artifact-title > span {
    color: var(--teal); font-size: .76rem; font-weight: 800; letter-spacing: .14em;
  }
  .hero-copy { padding: 2.8rem 0 1.5rem; }
  .hero-copy h1 { font-size: clamp(3rem, 7vw, 5.7rem); line-height: .96; margin: .7rem 0 1rem; }
  .hero-role { font-size: 1.35rem; font-weight: 700; margin: 0 0 .9rem; }
  .hero-summary { max-width: 720px; color: var(--muted); font-size: 1.06rem; }
  .hero-pills, .tag-row { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1.2rem; }
  .pill { display: inline-block; border-radius: 999px; padding: .38rem .72rem; font-size: .78rem; font-weight: 700; }
  .pill-teal { background: var(--teal-soft); color: #086158; }
  .pill-navy { background: var(--navy-soft); color: var(--navy); }
  .pill-coral { background: var(--coral-soft); color: #a54631; }
  .portrait-placeholder {
    min-height: 370px; margin-top: 1rem; padding: 2rem; border-radius: 28px;
    background: linear-gradient(150deg, #203967 0%, #0e8176 100%); color: white;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    text-align: center; box-shadow: 0 18px 45px rgba(23,33,59,.16);
  }
  .portrait-placeholder code { color: white; }
  .portrait-initials { font-size: 5.4rem; font-weight: 800; line-height: 1; margin-bottom: 1.4rem; }
  .spacer { height: 1.4rem; }
  .metric-card { background: var(--white); border: 1px solid var(--line); border-radius: 18px; padding: 1.4rem; }
  .metric-card strong { display: block; color: var(--navy); font-size: 2.3rem; line-height: 1; }
  .metric-card span { color: var(--muted); font-size: .88rem; }
  .section-intro { border-top: 1px solid var(--line); margin: 5rem 0 2rem; padding-top: 1.5rem; }
  .section-intro h1 { font-size: clamp(2.25rem, 5vw, 3.7rem); margin: .55rem 0 .6rem; }
  .section-intro p { color: var(--muted); max-width: 760px; font-size: 1.05rem; }
  .content-card { height: 100%; background: var(--white); border-radius: 20px; padding: 1.7rem; border-top: 5px solid; }
  .accent-teal { border-color: var(--teal); } .accent-coral { border-color: var(--coral); }
  .content-card h3 { font-size: 1.55rem; margin: .65rem 0; }
  .content-card p, .content-card li { color: var(--muted); }
  .mini-rule { width: 45px; border-top: 2px solid var(--line); margin: 1.2rem 0; }
  .quote-card { margin-top: 2rem; background: var(--ink); color: white; border-radius: 20px; padding: 2rem; }
  .quote-card span { color: #79d9cc; font-size: .72rem; font-weight: 800; letter-spacing: .14em; }
  .quote-card blockquote { font-size: 1.35rem; line-height: 1.55; margin: .7rem 0 0; }
  .role-banner { background: var(--ink); color: white; border-radius: 20px; padding: 1.4rem 1.6rem; display: grid; grid-template-columns: repeat(3,1fr); gap: 1rem; }
  .role-banner div { border-left: 2px solid var(--teal); padding-left: 1rem; }
  .role-banner span, .role-banner strong { display: block; }
  .role-banner span { color: #aeb8d0; font-size: .68rem; letter-spacing: .12em; font-weight: 800; }
  .project-heading { display: grid; grid-template-columns: 80px 1fr; gap: 1rem; margin: 4rem 0 1.2rem; }
  .project-number { color: var(--coral); font-size: 2.4rem; font-weight: 800; }
  .project-heading h2 { margin: .25rem 0 .4rem; font-size: 2rem; }
  .project-heading p { color: var(--muted); max-width: 830px; }
  .mini-card { min-height: 190px; background: white; border: 1px solid var(--line); border-radius: 16px; padding: 1.25rem; }
  .mini-card span { color: var(--teal); font-weight: 800; font-size: .82rem; }
  .mini-card p { color: var(--muted); }
  .artifact-title h2 { font-size: 2.2rem; margin: .4rem 0; }
  .artifact-title p { color: var(--muted); }
  .status-badge { background: var(--teal-soft); color: #086158; padding: .7rem 1rem; border-radius: 999px; text-align: center; font-weight: 800; font-size: .78rem; }
  .skill-card { background: var(--navy-soft); border-radius: 14px; padding: 1rem; min-height: 170px; }
  .skill-card span { color: var(--navy); font-size: .7rem; font-weight: 800; letter-spacing: .08em; }
  .skill-card h4 { margin: .5rem 0; }
  .skill-card p { color: var(--muted); font-size: .88rem; }
  .level-row { display: flex; align-items: center; gap: .7rem; margin: .7rem 0; font-size: .76rem; font-weight: 800; }
  .level-track { flex: 1; height: 7px; background: #d5dbe4; border-radius: 99px; overflow: hidden; }
  .level-track div { height: 100%; background: var(--teal); border-radius: 99px; }
  .artifact-divider { border-bottom: 1px solid var(--line); margin: 4rem 0; }
  .ksa-heading { display: flex; gap: 1rem; align-items: center; margin: 3.4rem 0 1rem; }
  .ksa-heading > span { width: 58px; height: 58px; border-radius: 16px; display: grid; place-items: center; color: white; font-weight: 900; font-size: 1.6rem; }
  .ksa-heading h2, .ksa-heading p { margin: 0; }
  .ksa-heading p { color: var(--muted); }
  .ksa-navy > span { background: var(--navy); } .ksa-teal > span { background: var(--teal); } .ksa-coral > span { background: var(--coral); }
  .reflection-card { min-height: 275px; background: white; border: 1px solid var(--line); border-radius: 18px; padding: 1.5rem; margin-bottom: 1rem; }
  .reflection-card span { color: var(--teal); font-size: .75rem; font-weight: 800; }
  .reflection-card h3 { margin: .55rem 0; }
  .reflection-card p { color: var(--muted); }
  .future-card { margin-top: 2rem; background: linear-gradient(135deg, #17213b, #263f76); color: white; border-radius: 24px; padding: 2.2rem; }
  .future-card h2 { color: white; font-size: 2rem; }
  .future-card p, .future-card li { color: #e2e7f2; }
  .next-steps { background: rgba(255,255,255,.08); border-radius: 14px; padding: 1rem 1.2rem; margin-top: 1.2rem; }
  .contact-card { display: flex; gap: 1.5rem; align-items: center; background: white; border: 1px solid var(--line); border-radius: 24px; padding: 2rem; margin-bottom: 1.4rem; }
  .contact-mark { min-width: 96px; height: 96px; border-radius: 50%; display: grid; place-items: center; background: var(--teal); color: white; font-size: 2rem; font-weight: 900; }
  .contact-card h2, .contact-card p { margin: .2rem 0; }
  .contact-note { color: var(--muted); }
  @media (max-width: 720px) {
    .block-container { padding: 1.2rem 1rem 3rem; }
    .hero-copy { padding-top: 1.2rem; }
    .role-banner { grid-template-columns: 1fr; }
    .project-heading { grid-template-columns: 54px 1fr; }
    .contact-card { align-items: flex-start; flex-direction: column; }
  }
</style>
"""


data = load_content(CONTENT_FILE)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## DIGITAL PORTFOLIO")
    st.caption(data["profile"]["name"])
    st.markdown("---")
    page = st.radio(
        "Portfolio navigation",
        ["Home", "Role & Projects", "Evidence", "KSA", "Reflection", "Contact"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    if data.get("show_editor_checklist", True):
        remaining = count_placeholders(data)
        with st.expander("Before publishing"):
            if remaining:
                st.warning(f"{remaining} placeholder fields remain.")
            else:
                st.success("No bracketed placeholders remain.")
            st.caption("Add a profile photo, test every evidence link, confirm company clearance, and set show_editor_checklist to false before submission.")
    st.caption("CIT2C27 · Guided Work-Based Learning 1")

pages = {
    "Home": render_home,
    "Role & Projects": render_projects,
    "Evidence": render_evidence,
    "KSA": render_ksa,
    "Reflection": render_reflection,
    "Contact": render_contact,
}
pages[page](data)

st.markdown("---")
st.caption(
    f"© {data['profile']['name']} · Public portfolio · "
    "All workplace artefacts are published only with appropriate clearance."
)
