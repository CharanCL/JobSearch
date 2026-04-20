

def get_mock_jobs():
    return [
        {
            "title": "Business Analyst",
            "company": "ConsultCorp",
            "description": "Business analysis, stakeholder management, data analysis, strategy"
        },
        {
            "title": "Product Manager",
            "company": "GrowthTech",
            "description": "Product strategy, market research, customer insights, roadmap planning"
        },
        {
            "title": "Operations Manager",
            "company": "GlobalLogistics",
            "description": "Operations, process improvement, supply chain, team leadership"
        },
        {
            "title": "Marketing Manager",
            "company": "BrandWorks",
            "description": "Marketing strategy, digital campaigns, customer acquisition, analytics"
        }
    ]



if __name__ == "__main__":
    for job in get_mock_jobs():
        print(job["title"], "-", job["company"])
