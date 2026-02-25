# ADORE (Autonomous Data Operations and Recovery Engine)

**Status:** 🏗️ *In Progress / Active Development*

---

**ADORE** is a source-agnostic autonomous pipeline operations framework. It is demonstrated through a multi-source city data pipeline (**Weather, Transit, and Incident data**) ingesting into **Google BigQuery**.

The framework features **AI agents** that autonomously investigate pipeline failures end-to-end:

* **Investigate:** Identifies root cause, impact, exact fix, and prevention.
* **Propose:** Presents a complete repair package to the user.
* **Human-in-the-Loop:** User approves, rejects, or modifies the fix.
* **Execute:** After approval, the agent implements and documents the fix.

> **Note:** The Human-in-the-Loop design is an intentional architectural choice, not a limitation.
