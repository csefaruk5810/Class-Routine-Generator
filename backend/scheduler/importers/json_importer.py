from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime


VALID_TYPES = {"Theory", "Lab"}


@dataclass(slots=True)
class ImportIssue:
    level: str
    code: str
    message: str
    context: dict


@dataclass(slots=True)
class ImportPreview:
    department: str
    year: str
    section: str
    days: list[str]
    entries: int
    unique_rooms: list[str]
    unique_courses: list[str]
    issues: list[ImportIssue]


class RoutineJSONImporter:
    def validate_and_preview(self, payload: dict) -> ImportPreview:
        issues: list[ImportIssue] = []
        required_fields = ("department", "year", "section", "days")
        for field in required_fields:
            if field not in payload:
                issues.append(ImportIssue("error", "missing_field", f"Missing required field: {field}", {"field": field}))

        days = payload.get("days", {})
        unique_rooms: set[str] = set()
        unique_courses: set[str] = set()
        entries = 0
        course_name_map: dict[str, set[str]] = defaultdict(set)

        for day_name, day_entries in days.items():
            if not isinstance(day_entries, list):
                issues.append(ImportIssue("error", "invalid_day_entries", "Day entries must be a list.", {"day": day_name}))
                continue

            for entry in day_entries:
                entries += 1
                course_code = (entry.get("courseCode") or "").strip()
                course_name = (entry.get("courseName") or "").strip()
                entry_type = (entry.get("type") or "").strip()
                time_range = (entry.get("time") or "").strip()
                room = (entry.get("room") or "").strip()

                if not course_code:
                    issues.append(ImportIssue("error", "missing_course_code", "Course code is required.", {"day": day_name}))
                if not course_name:
                    issues.append(ImportIssue("error", "missing_course_name", "Course name is required.", {"day": day_name, "courseCode": course_code}))
                if entry_type not in VALID_TYPES:
                    issues.append(ImportIssue("error", "invalid_type", "Type must be Theory or Lab.", {"day": day_name, "type": entry_type}))
                if not self._is_valid_time_range(time_range):
                    issues.append(ImportIssue("error", "invalid_time_range", "Time range is invalid.", {"day": day_name, "time": time_range}))
                if not room:
                    issues.append(ImportIssue("warning", "blank_room", "Room is blank and needs manual review.", {"day": day_name, "courseCode": course_code}))
                if "/" in room:
                    issues.append(ImportIssue("warning", "composite_room", "Room contains multiple values.", {"day": day_name, "room": room}))
                if "/" in course_code:
                    issues.append(ImportIssue("warning", "composite_course_code", "Course code contains multiple values.", {"day": day_name, "courseCode": course_code}))

                if course_code:
                    unique_courses.add(course_code)
                    course_name_map[course_code].add(course_name)
                if room:
                    unique_rooms.add(room)

        for course_code, names in course_name_map.items():
            normalized_names = {name for name in names if name}
            if len(normalized_names) > 1:
                issues.append(
                    ImportIssue(
                        "warning",
                        "course_name_mismatch",
                        "The same course code appears with multiple course names.",
                        {"courseCode": course_code, "courseNames": sorted(normalized_names)},
                    )
                )

        return ImportPreview(
            department=str(payload.get("department", "")),
            year=str(payload.get("year", "")),
            section=str(payload.get("section", "")),
            days=list(days.keys()),
            entries=entries,
            unique_rooms=sorted(unique_rooms),
            unique_courses=sorted(unique_courses),
            issues=issues,
        )

    @staticmethod
    def _is_valid_time_range(value: str) -> bool:
        parts = [part.strip() for part in value.split("-")]
        if len(parts) != 2:
            return False
        try:
            start = datetime.strptime(parts[0], "%I:%M %p")
            end = datetime.strptime(parts[1], "%I:%M %p")
        except ValueError:
            return False
        return end > start

