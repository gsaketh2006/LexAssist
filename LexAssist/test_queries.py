"""
Test queries and responses for StartupLex Backend
This file contains test data for developing and testing the RAG API integration
"""

TEST_QUERIES = [
    {
        "id": 1,
        "question": "What documents do I need to incorporate my startup?",
        "category": "Incorporation",
        "sample_rag_response": "To incorporate your startup, you'll need: 1) Articles of Incorporation (or Certificate of Incorporation) - filed with the state; 2) Corporate Bylaws - internal governance rules; 3) Board Resolutions - documenting initial corporate actions; 4) Founder Stock Agreements - outlining equity distribution and vesting schedules; 5) 83(b) Election Forms - for tax purposes if receiving restricted stock. You'll also need to obtain an EIN from the IRS."
    },
    {
        "id": 2,
        "question": "How should I structure equity for my first employees?",
        "category": "Equity & Compensation",
        "sample_rag_response": "For early employees, consider: 1) Create an option pool of 10-20% of fully diluted shares; 2) Use 4-year vesting schedules with 1-year cliffs; 3) ISOs for US employees (up to $100k/year), NSOs for contractors and international staff; 4) Typical equity ranges: First Engineer/CTO 0.5-2%, VP-level 0.3-1%, Senior Engineers 0.1-0.5%, Mid-level 0.05-0.2%; 5) Include acceleration provisions and post-termination exercise windows."
    },
    {
        "id": 3,
        "question": "What is a SAFE and when should we use it?",
        "category": "Fundraising",
        "sample_rag_response": "A SAFE (Simple Agreement for Future Equity) is a convertible instrument used in early-stage fundraising. Benefits: 1) Simpler than equity issuance, reducing legal costs; 2) Faster closing process; 3) No voting rights or board seat given; 4) Converts to equity on future funding round or acquisition. Use SAFEs when: raising seed rounds under $2M, maintaining founder control, moving quickly with angel investors. Key terms: Valuation cap, discount rate, and MFN (Most Favored Nation) clause."
    },
    {
        "id": 4,
        "question": "What GDPR compliance do we need for our SaaS?",
        "category": "Privacy & Compliance",
        "sample_rag_response": "Key GDPR requirements: 1) Legal basis for processing (consent, contract, legitimate interest); 2) Privacy Policy and Data Processing Agreements; 3) Implement data minimization and purpose limitation principles; 4) User rights: access, deletion, correction, portability, objection; 5) Data breach notification within 72 hours; 6) Data Protection Impact Assessments for high-risk processing; 7) Appoint DPO if required. Penalties up to €20M or 4% of global revenue. Non-compliance can halt operations in EU."
    },
    {
        "id": 5,
        "question": "How do we protect our intellectual property?",
        "category": "IP Protection",
        "sample_rag_response": "Multi-layered IP protection strategy: 1) Patents - protect inventions, typically 20 years; 2) Trademarks - protect brand names and logos; 3) Copyrights - protect original works (automatic, covers code, content); 4) Trade Secrets - protect confidential processes; 5) Proper IP assignment agreements with all founders and employees; 6) Non-disclosure agreements (NDAs) with third parties; 7) Document all creative work and development; 8) Consider provisional patents before full patent filing."
    },
    {
        "id": 6,
        "question": "What's the standard vesting schedule for founders?",
        "category": "Founder Agreement",
        "sample_rag_response": "Industry standard founder vesting: 1) 4-year total vesting period; 2) 1-year cliff - no shares vest until 12 months of service; 3) Monthly vesting after cliff (1/48th per month for remaining 36 months); 4) Single or double-trigger acceleration on acquisition (single = automatic, double = requires job loss); 5) Clawback rights if founder leaves during cliff; 6) Good leaver vs bad leaver provisions affecting unvested shares. This protects investors and ensures founder commitment."
    },
    {
        "id": 7,
        "question": "What should be in our operating agreement?",
        "category": "Governance",
        "sample_rag_response": "Essential provisions in an LLC Operating Agreement: 1) Member ownership percentages and capital contributions; 2) Profit/loss distribution rules; 3) Management structure and decision-making; 4) Voting requirements for major decisions; 5) Admission/withdrawal of members; 6) Dissolution procedures; 7) Transfer restrictions and buy-sell provisions; 8) Non-compete and non-solicitation clauses; 9) Dispute resolution mechanisms; 10) Amendment procedures. This document governs internal operations and protects all members."
    },
    {
        "id": 8,
        "question": "Do we need employment agreements?",
        "category": "Employment",
        "sample_rag_response": "Yes, employment agreements are essential and should include: 1) Position, duties, and compensation; 2) At-will employment clause; 3) Confidentiality and NDA provisions; 4) Intellectual property assignment; 5) Non-compete and non-solicitation clauses (reasonableness varies by state); 6) Benefits and leave policies; 7) Termination procedures and notice periods; 8) Dispute resolution; 9) Stock option/equity grant details; 10) At-will employment statement. Proper agreements protect both employer and employee."
    },
    {
        "id": 9,
        "question": "What licenses do we need for our startup?",
        "category": "Compliance",
        "sample_rag_response": "Licenses depend on your business type: 1) General Business License - required in most jurisdictions; 2) Industry-specific licenses (healthcare, financial services, etc.); 3) Professional licenses if offering professional services; 4) SaaS/Software - usually minimal, focus on IP and terms of service; 5) E-commerce - sales tax permits, consumer protection compliance; 6) Data handling - GDPR, CCPA compliance; 7) Food/Beverage - health department licenses; 8) Check federal, state, and local requirements; 9) Renew licenses on schedule; 10) Budget for licensing costs in operations."
    },
    {
        "id": 10,
        "question": "What's the difference between a C-corp and S-corp?",
        "category": "Business Structure",
        "sample_rag_response": "Key differences: C-Corp: 1) Double taxation (corporate + individual level); 2) Unlimited shareholders; 3) Preferred for VC funding; 4) More administrative requirements. S-Corp: 1) Pass-through taxation (no double taxation); 2) Limited to 100 shareholders; 3) Restricted shareholder types; 4) Elections required with IRS; 5) Can reduce self-employment taxes. For startups seeking VC funding, C-Corp is standard. S-Corp election useful for profitable startups with high owner income."
    }
]

def get_test_query(query_id):
    """Get a test query by ID"""
    for q in TEST_QUERIES:
        if q["id"] == query_id:
            return q
    return None

def get_test_queries_by_category(category):
    """Get all test queries for a specific category"""
    return [q for q in TEST_QUERIES if q["category"].lower() == category.lower()]

def get_all_test_queries():
    """Get all test queries"""
    return TEST_QUERIES

if __name__ == "__main__":
    # Example usage
    print("StartupLex Test Queries\n")
    print("=" * 80)
    
    for query in TEST_QUERIES:
        print(f"\n[{query['id']}] {query['question']}")
        print(f"Category: {query['category']}")
        print(f"Sample Response:\n{query['sample_rag_response']}")
        print("-" * 80)
