import streamlit as st
from sentinai.core import SentinAICore

st.set_page_config(page_title="SentinAI", layout="wide")

st.title("SentinAI — Automated Code Review & Security Auditor")
st.markdown("Upload Python or JavaScript files and receive a comprehensive security and quality report.")

core = SentinAICore()
validation_error = None
fallback_notice = None
try:
    fallback_notice = core.validate()
except RuntimeError as exc:
    validation_error = str(exc)

if validation_error:
    st.error(validation_error)
else:
    if fallback_notice:
        st.warning(fallback_notice)
    uploaded_files = st.file_uploader("Upload source code files", type=["py", "js"], accept_multiple_files=True)

    if uploaded_files:
        source_files = []
        for uploaded_file in uploaded_files:
            content = uploaded_file.read().decode("utf-8", errors="ignore")
            source_files.append({
                "name": uploaded_file.name,
                "content": content,
                "language": "python" if uploaded_file.name.endswith(".py") else "javascript"
            })

        report = None
        with st.spinner("Analyzing code with SentinAI Multi-Agent Workflow..."):
            try:
                report = core.analyze(source_files)
            except RuntimeError as exc:
                st.error(str(exc))
                report = None

        if report:
            if report.get("llm_fallback_reason"):
                st.warning(report["llm_fallback_reason"])
            st.success("Analysis complete")

            # Provide download buttons for the full documentation
            final_md_report = report.get("final_report", "No report generated.")
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Download Documentation (Markdown)",
                    data=final_md_report,
                    file_name="sentinai_analysis_report.md",
                    mime="text/markdown"
                )
            
            with col2:
                try:
                    from markdown_pdf import MarkdownPdf, Section
                    import tempfile
                    import os
                    
                    pdf = MarkdownPdf(toc_level=2)
                    pdf.add_section(Section(final_md_report, toc=False))
                    
                    # Save to a temporary file
                    temp_pdf_path = os.path.join(tempfile.gettempdir(), "sentinai_report.pdf")
                    pdf.save(temp_pdf_path)
                    
                    with open(temp_pdf_path, "rb") as f:
                        pdf_bytes = f.read()
                        
                    st.download_button(
                        label="📄 Download Documentation (PDF)",
                        data=pdf_bytes,
                        file_name="sentinai_analysis_report.pdf",
                        mime="application/pdf"
                    )
                except ImportError:
                    st.warning("Install `markdown-pdf` to enable PDF downloads.")


            # Extract structured data from the LLM's JSON response
            json_data = report.get("final_json", {})
            health_score = json_data.get("health_score", 0)
            sec_findings = json_data.get("security_findings", [])
            bug_findings = json_data.get("bug_findings", [])
            docs = json_data.get("documentation", [])
            refs = json_data.get("references", [])

            st.subheader("Overall Code Health")
            st.metric("Health Score", f"{health_score} / 100")
            st.markdown(
                f"**Security issues:** {len(sec_findings)}, "
                f"**Bug findings:** {len(bug_findings)}, "
                f"**Documentation suggestions:** {len(docs)}"
            )

            tabs = st.tabs(["Security Audit", "Bug Analysis", "Documentation", "RAG References", "Raw Report"])

            with tabs[0]:
                for issue in sec_findings:
                    st.markdown(f"### {issue.get('title', 'Issue')}")
                    st.write(issue.get("description", ""))
                    st.markdown(f"- Severity: **{issue.get('severity', 'Unknown')}**")
                    st.markdown(f"- File: `{issue.get('file', 'Unknown')}`")
                    if issue.get("reference"):
                        st.markdown(f"- Reference: {issue['reference']}")

            with tabs[1]:
                for issue in bug_findings:
                    st.markdown(f"### {issue.get('title', 'Bug')}")
                    st.write(issue.get("description", ""))
                    st.markdown(f"- Severity: **{issue.get('severity', 'Unknown')}**")
                    st.markdown(f"- File: `{issue.get('file', 'Unknown')}`")
                    if issue.get("recommendation"):
                        st.markdown(f"- Recommendation: {issue['recommendation']}")

            with tabs[2]:
                for doc in docs:
                    st.markdown(f"### {doc.get('file', 'File')} — {doc.get('type', 'Summary').capitalize()}")
                    st.code(doc.get("content", ""), language="markdown")

            with tabs[3]:
                for ref in refs:
                    st.markdown(f"- **{ref.get('title', 'Reference')}**: {ref.get('snippet', '')}")

            with tabs[4]:
                st.markdown(report.get("final_report", "No report generated."))

