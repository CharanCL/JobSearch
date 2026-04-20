
COMMON_PREFIXES = [
    "careers",
    "recruitment",
    "jobs",
    "hr",
    "talent"
]

def normalize_company_name(company_name: str) -> str:
    """
    Convert company name to a likely domain base.
    Example: 'ITS (Cheltenham) Ltd' -> 'its'
    """
    name = company_name.lower()
    name = re.sub(r"\(.*?\)", "", name)
    name = re.sub(r"\b(ltd|limited|plc|group|inc)\b", "", name)
    name = re.sub(r"[^a-z0-9 ]", "", name)
    name = name.strip().replace(" ", "")
    return name


def suggest_hr_emails(company_name: str, domain="com"):
    base = normalize_company_name(company_name)
    return [f"{prefix}@{base}.{domain}" for prefix in COMMON_PREFIXES]
