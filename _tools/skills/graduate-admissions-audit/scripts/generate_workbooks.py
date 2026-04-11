#!/usr/bin/env python3
"""Generate XLSX workbook assets for the graduate-admissions-audit skill.

This script uses only the Python standard library so it can run in minimal
environments without openpyxl or xlsxwriter.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape
import zipfile


ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"


@dataclass(frozen=True)
class Sheet:
    name: str
    rows: list[list[str]]


def col_name(index: int) -> str:
    result = []
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        result.append(chr(65 + remainder))
    return "".join(reversed(result))


def xml_cell(ref: str, value: str, style_id: int = 0) -> str:
    escaped = escape("" if value is None else str(value))
    return (
        f'<c r="{ref}" t="inlineStr" s="{style_id}">'
        f"<is><t>{escaped}</t></is></c>"
    )


def sheet_xml(sheet: Sheet) -> str:
    max_cols = max((len(row) for row in sheet.rows), default=1)
    max_rows = max(len(sheet.rows), 1)
    end_ref = f"{col_name(max_cols)}{max_rows}"
    cols = "".join(
        f'<col min="{idx}" max="{idx}" width="{width}" customWidth="1"/>'
        for idx, width in enumerate(column_widths(max_cols, sheet.rows), start=1)
    )
    rows_xml = []
    for r_idx, row in enumerate(sheet.rows, start=1):
        cells = []
        style_id = 1 if r_idx == 1 else 0
        for c_idx, value in enumerate(row, start=1):
            ref = f"{col_name(c_idx)}{r_idx}"
            cells.append(xml_cell(ref, value, style_id))
        rows_xml.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
    auto_filter = (
        f'<autoFilter ref="A1:{end_ref}"/>' if sheet.rows and len(sheet.rows[0]) > 0 else ""
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<sheetViews><sheetView workbookViewId="0">'
        '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
        '<selection pane="bottomLeft" activeCell="A2" sqref="A2"/>'
        "</sheetView></sheetViews>"
        f"<dimension ref=\"A1:{end_ref}\"/>"
        f"<cols>{cols}</cols>"
        '<sheetFormatPr defaultRowHeight="15"/>'
        f"<sheetData>{''.join(rows_xml)}</sheetData>"
        f"{auto_filter}"
        "</worksheet>"
    )


def column_widths(max_cols: int, rows: list[list[str]]) -> Iterable[int]:
    widths = []
    for c_idx in range(max_cols):
        content_width = max(
            (display_len(row[c_idx]) for row in rows if c_idx < len(row)),
            default=12,
        )
        widths.append(min(max(content_width + 2, 12), 36))
    return widths


def display_len(value: str) -> int:
    return len(str(value or ""))


def content_types_xml(sheet_count: int) -> str:
    overrides = "".join(
        f'<Override PartName="/xl/worksheets/sheet{idx}.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for idx in range(1, sheet_count + 1)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/styles.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        '<Override PartName="/docProps/core.xml" '
        'ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        f"{overrides}</Types>"
    )


def root_rels_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        '<Relationship Id="rId2" '
        'Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" '
        'Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" '
        'Target="docProps/app.xml"/>'
        "</Relationships>"
    )


def workbook_xml(sheets: list[Sheet]) -> str:
    sheet_tags = "".join(
        f'<sheet name="{escape(sheet.name)}" sheetId="{idx}" r:id="rId{idx}"/>'
        for idx, sheet in enumerate(sheets, start=1)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<bookViews><workbookView xWindow="0" yWindow="0" windowWidth="24000" windowHeight="12000"/></bookViews>'
        f"<sheets>{sheet_tags}</sheets>"
        "</workbook>"
    )


def workbook_rels_xml(sheet_count: int) -> str:
    sheet_rels = "".join(
        f'<Relationship Id="rId{idx}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
        f'Target="worksheets/sheet{idx}.xml"/>'
        for idx in range(1, sheet_count + 1)
    )
    style_rid = sheet_count + 1
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f"{sheet_rels}"
        f'<Relationship Id="rId{style_rid}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
        'Target="styles.xml"/>'
        "</Relationships>"
    )


def styles_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="2">'
        '<font><sz val="11"/><name val="Aptos"/></font>'
        '<font><b/><sz val="11"/><name val="Aptos"/></font>'
        '</fonts>'
        '<fills count="3">'
        '<fill><patternFill patternType="none"/></fill>'
        '<fill><patternFill patternType="gray125"/></fill>'
        '<fill><patternFill patternType="solid"><fgColor rgb="FFD9EAF7"/><bgColor indexed="64"/></patternFill></fill>'
        '</fills>'
        '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="2">'
        '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
        '<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>'
        '</cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
        "</styleSheet>"
    )


def app_xml(sheet_count: int) -> str:
    heading_pairs = (
        '<vt:vector size="2" baseType="variant">'
        '<vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant>'
        f'<vt:variant><vt:i4>{sheet_count}</vt:i4></vt:variant>'
        "</vt:vector>"
    )
    titles = "".join(
        f"<vt:lpstr>{escape(sheet)}</vt:lpstr>"
        for sheet in [
            "README",
            "applicant_snapshot",
            "program_facts",
            "community_cases",
            "assessment",
            "review_queue",
            "source_registry",
        ][:sheet_count]
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        '<Application>Codex</Application>'
        f"<HeadingPairs>{heading_pairs}</HeadingPairs>"
        f'<TitlesOfParts><vt:vector size="{sheet_count}" baseType="lpstr">{titles}</vt:vector></TitlesOfParts>'
        "</Properties>"
    )


def core_xml() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:creator>Codex</dc:creator>'
        '<cp:lastModifiedBy>Codex</cp:lastModifiedBy>'
        '<dc:title>Graduate Admissions Audit Workbook</dc:title>'
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
        "</cp:coreProperties>"
    )


def write_workbook(path: Path, sheets: list[Sheet]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml(len(sheets)))
        zf.writestr("_rels/.rels", root_rels_xml())
        zf.writestr("docProps/app.xml", app_xml(len(sheets)))
        zf.writestr("docProps/core.xml", core_xml())
        zf.writestr("xl/workbook.xml", workbook_xml(sheets))
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml(len(sheets)))
        zf.writestr("xl/styles.xml", styles_xml())
        for idx, sheet in enumerate(sheets, start=1):
            zf.writestr(f"xl/worksheets/sheet{idx}.xml", sheet_xml(sheet))


def template_sheets() -> list[Sheet]:
    return [
        Sheet("README", [
            ["section", "content"],
            ["workbook_purpose", "Delivery-ready admissions audit workbook. Official facts, community evidence, and judgement stay in separate sheets."],
            ["grain_rule", "One row per program + intake + study mode in program_facts and assessment."],
            ["status_rule", "Use unknown, n/a, or a labeled risk instead of silent blanks for checked fields."],
        ]),
        Sheet("applicant_snapshot", [[
            "assessment_run_id", "applicant_profile_version", "target_intake", "target_countries",
            "target_directions", "identity_status", "highest_degree", "current_or_last_institution",
            "institution_country", "major", "minor_or_second_major", "gpa_value", "gpa_scale",
            "average_score", "grading_formula_status", "language_tests", "internship_summary",
            "research_summary", "work_experience_summary", "portfolio_status", "budget_range",
            "missing_critical_info", "snapshot_notes",
        ]]),
        Sheet("program_facts", [[
            "program_id", "program_country", "university_name", "faculty_or_school", "program_name_en",
            "program_name_zh", "degree_award", "study_mode", "duration", "intake_term", "project_status",
            "teaching_language", "teaching_language_basis", "language_requirement_summary", "ielts_requirement",
            "ielts_subscore_requirement", "toefl_requirement", "toefl_subscore_requirement", "other_language_requirement",
            "language_waiver_policy", "academic_requirement_summary", "degree_class_requirement", "major_restriction",
            "preferred_background", "prerequisite_courses", "minimum_core_courses", "work_experience_requirement",
            "portfolio_requirement", "test_requirement", "interview_requirement", "supervisor_requirement",
            "other_hard_requirements", "application_open_date", "application_deadline", "deadline_type",
            "tuition_local_or_domestic", "tuition_non_local_or_international", "tuition_currency", "tuition_basis_year",
            "tuition_notes", "admission_source_id", "tuition_source_id", "deadline_source_id", "captured_at",
            "fact_quality_status", "fact_notes",
        ]]),
        Sheet("community_cases", [[
            "evidence_id", "program_id", "source_id", "source_type", "source_url", "page_title", "post_date",
            "intake_if_known", "result_type", "applicant_background_summary", "gpa_or_average_if_stated",
            "language_score_if_stated", "soft_background_if_stated", "credibility_score", "similarity_score", "evidence_notes",
        ]]),
        Sheet("assessment", [[
            "program_id", "university_name", "program_name_en", "intake_term", "eligibility_status",
            "competitiveness_band", "estimated_probability_range", "assessment_confidence", "evidence_sufficiency",
            "direction_fit", "budget_fit", "key_risks", "manual_review_required", "action_recommendation",
            "judgement_reason", "supporting_fact_refs", "supporting_case_refs", "assessor_notes",
        ]]),
        Sheet("review_queue", [[
            "issue_id", "program_id", "issue_type", "severity", "blocking", "description",
            "required_human_action", "owner", "status",
        ]]),
        Sheet("source_registry", [[
            "source_id", "program_id", "source_category", "source_tier", "page_title", "source_url",
            "captured_at", "applicable_intake", "freshness_status", "notes",
        ]]),
    ]


def sample_sheets() -> list[Sheet]:
    sheets = template_sheets()
    sheets[1].rows.append([
        "RUN-EXAMPLE-001", "AP-V1", "2027 Fall", "Hong Kong; United Kingdom",
        "Cultural Heritage; Museum Studies", "HK local", "Bachelor's", "Example Metropolitan University",
        "Hong Kong", "Cultural Industries Management", "unknown", "unknown", "unknown",
        "unknown", "unknown", "IELTS 6.5 overall, no subscore below 6.0", "Museum internship at city museum",
        "Course-based dissertation on heritage policy", "n/a", "n/a", "HKD 250000 tuition cap",
        "GPA conversion formula; final average", "Illustrative example only",
    ])
    sheets[2].rows.extend([
        [
            "HK-EXU-MUS-2027FT", "Hong Kong", "Example University Hong Kong", "School of Arts and Heritage",
            "MA Museum and Heritage Practice", "博物馆与文化遗产实践文学硕士", "MA", "full-time", "1 year",
            "2027 Fall", "open", "Chinese", "inferred from Chinese proficiency requirement on official admission page",
            "Chinese proficiency required; IELTS not explicitly listed", "unknown", "unknown", "n/a", "n/a",
            "Chinese proficiency", "unknown", "Bachelor's degree in relevant or related discipline", "unknown",
            "Arts, culture, heritage, history, related fields preferred", "unknown", "n/a", "n/a",
            "no", "no", "no", "possible", "n/a", "2026-10-01", "2027-03-15", "fixed deadline",
            "HKD 138000", "HKD 172000", "HKD", "2027/28", "Identity status affects fee band", "SRC-001",
            "SRC-002", "SRC-001", "2026-11-01", "inferred", "Teaching language should be manually confirmed",
        ],
        [
            "UK-EXU-HER-2027FT", "United Kingdom", "Example University UK", "School of Public Culture",
            "MA Heritage Policy and Practice", "n/a", "MA", "full-time", "1 year",
            "2027 Fall", "open", "English", "explicit on official admission page",
            "IELTS 6.5 overall", "IELTS 6.5 overall", "no band below 6.0", "TOEFL 90", "minimum 20 in each component",
            "n/a", "pre-sessional available", "2:1 equivalent in relevant subject area", "2:1 equivalent", "Relevant subject area",
            "heritage, history, policy, museum studies", "n/a", "n/a", "n/a", "no", "no", "no", "possible", "n/a",
            "2026-09-15", "rolling", "rolling", "not separated", "GBP 24900", "GBP", "2027/28",
            "International fee shown on official page", "SRC-003", "SRC-004", "SRC-003", "2026-11-01", "complete", "Apply early because the programme is rolling",
        ],
    ])
    sheets[3].rows.extend([
        [
            "CASE-001", "HK-EXU-MUS-2027FT", "SRC-101", "forum", "https://example.com/case-1",
            "HK local heritage offer timeline", "2026-12-08", "2027 Fall", "offer",
            "HK local, humanities major, museum internship", "83/100", "not stated", "museum internship",
            "0.68", "0.72", "Detailed timeline post, no screenshot",
        ],
        [
            "CASE-002", "UK-EXU-HER-2027FT", "SRC-102", "forum", "https://example.com/case-2",
            "Heritage policy rejection note", "2026-11-20", "2027 Fall", "reject",
            "Mainland applicant, arts management major", "78/100", "IELTS 6.5", "one internship",
            "0.74", "0.51", "Included decision email date",
        ],
    ])
    sheets[4].rows.extend([
        [
            "HK-EXU-MUS-2027FT", "Example University Hong Kong", "MA Museum and Heritage Practice", "2027 Fall",
            "likely_eligible", "主申", "60-80%", "medium", "moderate", "high", "within_budget",
            "Teaching language is inferred; GPA unknown; local-case data remains thin", "yes",
            "manual_review_before_decision",
            "Official degree baseline appears reachable, but language interpretation and missing GPA detail keep this at medium confidence.",
            "SRC-001; SRC-002", "CASE-001", "Illustrative sample row",
        ],
        [
            "UK-EXU-HER-2027FT", "Example University UK", "MA Heritage Policy and Practice", "2027 Fall",
            "eligible", "主申偏冲刺", "40-55%", "medium", "moderate", "medium_high", "stretch",
            "Rolling admissions timing; GPA conversion still unconfirmed", "yes",
            "apply_after_prerequisite_check",
            "Published degree and language thresholds are visible, but competitiveness should stay conservative until GPA comparability is verified.",
            "SRC-003; SRC-004", "CASE-002", "Illustrative sample row",
        ],
    ])
    sheets[5].rows.extend([
        [
            "ISSUE-001", "HK-EXU-MUS-2027FT", "language-rule-interpretation", "medium", "no",
            "Teaching language is inferred from Chinese proficiency wording rather than stated directly.",
            "Re-open the official page or contact admissions for confirmation.", "consultant", "open",
        ],
        [
            "ISSUE-002", "UK-EXU-HER-2027FT", "gpa-conversion", "high", "yes",
            "Applicant GPA conversion formula is unknown, so competitiveness cannot be upgraded confidently.",
            "Confirm the applicant's official undergraduate grading policy.", "consultant", "open",
        ],
    ])
    sheets[6].rows.extend([
        [
            "SRC-001", "HK-EXU-MUS-2027FT", "official_admission", "program_official", "Museum and Heritage Practice Admissions",
            "https://example.edu.hk/museum/admissions", "2026-11-01", "2027 Fall", "current", "Illustrative source only",
        ],
        [
            "SRC-002", "HK-EXU-MUS-2027FT", "official_tuition", "program_official", "Museum and Heritage Practice Fees",
            "https://example.edu.hk/museum/fees", "2026-11-01", "2027 Fall", "current", "Illustrative source only",
        ],
        [
            "SRC-003", "UK-EXU-HER-2027FT", "official_admission", "program_official", "Heritage Policy and Practice Entry Requirements",
            "https://example.ac.uk/heritage/entry", "2026-11-01", "2027 Fall", "current", "Illustrative source only",
        ],
        [
            "SRC-004", "UK-EXU-HER-2027FT", "official_tuition", "university_official", "Postgraduate Tuition Fees",
            "https://example.ac.uk/pg/fees", "2026-11-01", "2027 Fall", "current", "Illustrative source only",
        ],
        [
            "SRC-101", "HK-EXU-MUS-2027FT", "community_case", "community", "HK local heritage offer timeline",
            "https://example.com/case-1", "2026-12-08", "2027 Fall", "recent", "Illustrative source only",
        ],
        [
            "SRC-102", "UK-EXU-HER-2027FT", "community_case", "community", "Heritage policy rejection note",
            "https://example.com/case-2", "2026-11-20", "2027 Fall", "recent", "Illustrative source only",
        ],
    ])
    return sheets


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    write_workbook(ASSETS_DIR / "graduate-admissions-template.xlsx", template_sheets())
    write_workbook(ASSETS_DIR / "graduate-admissions-sample.xlsx", sample_sheets())
    print(f"Wrote workbook assets to {ASSETS_DIR}")


if __name__ == "__main__":
    main()
