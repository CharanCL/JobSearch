
def get_manual_approval(job_title, company_name, subject, body):
    print("\n================= EMAIL PREVIEW =================\n")
    print(f"Job Title : {job_title}")
    print(f"Company   : {company_name}")
    print(f"Subject   : {subject}")
    print("\n--- Email Body ---\n")
    print(body)
    print("\n=================================================\n")

    decision = input("✅ Send this email? (yes/no): ").strip().lower()
    return decision == "yes"
