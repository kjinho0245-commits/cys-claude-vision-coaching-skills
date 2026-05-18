#!/usr/bin/env python3
"""
10개 시나리오 테스트 — vision-foresight-wild-cards-identification SKILL.md 검증
각 시나리오는 마스터가 sub-skill을 호출할 때 만들어야 하는 output을 생성하고
validate_identification.py로 검증한다.
"""
import json
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from validate_identification import validate

# ── 헬퍼: 최소 유효 candidate 생성 ────────────────────────────────────────────

def make_candidate(idx, wc_type, method, domain, title, petersen_ref, seed, quality, indicators):
    return {
        "id": f"WC-{idx:03d}",
        "title": title,
        "domain": domain,
        "type": str(wc_type),
        "source_method": method,
        "petersen_ref": petersen_ref,
        "steinmuller_ref": "new",
        "seed_description": seed,
        "positive_or_negative": quality,
        "lead_indicators": indicators,
    }

def make_output(topic, target_group, domain_label, candidates, vrmp_tier="R-1"):
    n = len(candidates)
    type_counts = {"1": 0, "2": 0, "3": 0}
    method_counts = {m: 0 for m in ["brainstorm", "expert", "survey", "historical", "sf"]}
    petersen_adapted = 0
    steinmuller_adapted = 0
    new_invented = 0
    historical_count = 0
    sf_count = 0

    for c in candidates:
        t = str(c["type"])
        if t in type_counts:
            type_counts[t] += 1
        m = c["source_method"]
        if m in method_counts:
            method_counts[m] += 1
        if c["petersen_ref"] != "new":
            petersen_adapted += 1
        if c["steinmuller_ref"] != "new":
            steinmuller_adapted += 1
        if c["petersen_ref"] == "new" and c["steinmuller_ref"] == "new":
            new_invented += 1
        if m == "historical":
            historical_count += 1
        if m == "sf":
            sf_count += 1

    type1_pct = round(type_counts["1"] / n * 100)
    type2_pct = round(type_counts["2"] / n * 100)
    type3_pct = 100 - type1_pct - type2_pct

    return {
        "identification_output": {
            "meta": {
                "target_group": target_group,
                "catalogue_source": "Both",
                "surprise_type_mix": {
                    "type1": type1_pct,
                    "type2": type2_pct,
                    "type3": type3_pct,
                },
                "n_candidates": n,
                "method_breakdown": method_counts,
            },
            "candidates": candidates,
            "catalogue_summary": {
                "new_invented": new_invented,
                "petersen_adapted": petersen_adapted,
                "steinmuller_adapted": steinmuller_adapted,
                "historical_analogy": historical_count,
                "sf_inspired": sf_count,
            },
        },
        "vrmp_tier": vrmp_tier,
        "source_trail": [
            f"WebSearch: wild card {topic} 2025",
            "Petersen & Steinmüller (2009) V3.0 Ch.10",
            "Harremoës et al. (2001) Late lessons from early warnings. EEA Report No.22",
        ],
        "validation_result": None,
        "next_skill": "vision-foresight-wild-cards-assessment",
    }


# ── 10개 시나리오 ───────────────────────────────────────────────────────────────

def scenario_01():
    """바이오테크/의학 + Corporate Strategy (C1, R mode)"""
    cands = [
        make_candidate(1, 2, "brainstorm", "T+S", "Antibiotic Resistance Global Collapse",
            "P-BIO-01",
            "All major antibiotic classes fail simultaneously; routine surgery becomes life-threatening. Healthcare systems collapse within 18 months of initial outbreak.",
            "-", ["WHO drug-resistance report trend 5yr", "Carbapenem-resistant Enterobacteriaceae incidence rate", "FDA new antibiotic approval rate declining"]),
        make_candidate(2, 1, "expert", "T+S", "Human Lifespan Exceeds 120 Years via Senolytics",
            "P-BIO-08 (adapted)",
            "Senolytic drugs clearing aged cells enter mainstream; average lifespan crosses 120 in high-income countries. Pension systems and labor markets restructure fundamentally.",
            "+", ["Senolytics Phase III trial completion count", "Biotech VC investment in longevity sector", "FDA breakthrough therapy designation for aging"]),
        make_candidate(3, 3, "sf", "T+S+Spi", "Synthetic Biology Creates Autonomous Life-Form",
            "new",
            "A self-replicating synthetic organism escapes containment, triggers global biosecurity crisis and new regulatory paradigm collapse.",
            "-", ["Synthetic genome length milestones", "iGEM safety incident reports", "DARPA biological threat response drill frequency"]),
        make_candidate(4, 1, "historical", "S+E", "Medication Side Effect Scandal Larger than DES",
            "P-BIO-06",
            "A blockbuster drug prescribed to 200M+ people is found to cause irreversible harm via previously unknown mechanism; DES-scale litigation and regulatory overhaul.",
            "-", ["FDA post-market safety surveillance reports", "Adverse event database (FAERS) spike alerts", "European Medicines Agency safety committee escalations"]),
        make_candidate(5, 2, "survey", "T+S", "Non-Invasive Brain-Computer Interface Goes Consumer",
            "P-TIU-19 (adapted)",
            "Affordable neural interface headsets read and write brain signals; cognitive enhancement creates new class divide between enhanced and unenhanced workers.",
            "±", ["Consumer EEG device sales growth rate", "Academic BCI publication count per year", "NeuraLink-class investment round sizes"]),
        make_candidate(6, 3, "brainstorm", "T+Spi", "First Confirmed Mind Upload",
            "new",
            "A dying billionaire's consciousness is uploaded to a digital substrate and passes behavioral Turing test; existential, legal, and religious crises cascade globally.",
            "±", ["Whole-brain emulation research funding trajectory", "AI consciousness benchmark debate frequency", "Digital mind legal status legislation proposals"]),
        make_candidate(7, 2, "expert", "Env+T", "Microplastic-Induced Reproductive Collapse",
            "P-BIO-10 (adapted)",
            "Cumulative microplastic burden drops human sperm count below 20% of 1980 baseline globally; fertility clinics overwhelmed, demographic shock accelerates.",
            "-", ["WHO sperm count trend data", "Microplastic concentration in human blood studies", "Fertility treatment demand increase rate"]),
        make_candidate(8, 1, "survey", "E+S", "Universal Pandemic Insurance Collapses",
            "P-BIO-02 (adapted)",
            "A second pandemic triggers simultaneous insurance industry insolvency; governments backstop all health claims, permanently nationalizing health insurance.",
            "-", ["Pandemic bond market stress indicators", "Reinsurance pandemic exclusion clause growth", "Government emergency health fund drawdown rates"]),
        make_candidate(9, 3, "sf", "T+S+Spi", "Human-Animal Chimera Legal Rights Case",
            "new",
            "A court grants partial legal personhood to a human-animal chimera; bioethics framework fractures and research moratoria conflict with commercial timelines.",
            "±", ["Human-animal chimera research publication rate", "Bioethics legislative proposal count", "Animal rights litigation success rate trend"]),
        make_candidate(10, 2, "historical", "T+S", "Thalidomide-Scale Genetic Editing Side Effect",
            "new",
            "First-generation CRISPR gene-edited humans manifest unexpected heritable mutations at adolescence; regulatory framework for germline editing collapses.",
            "-", ["CRISPR clinical trial enrollment numbers", "Off-target editing detection sensitivity reports", "WHO International Commission on Clinical Use of Human Germline Genome Editing updates"]),
        make_candidate(11, 1, "brainstorm", "T+E", "Personalized Medicine Makes Mass Pharma Obsolete",
            "P-BIO-05 (adapted)",
            "AI-designed patient-specific drugs eliminate blockbuster model; top 10 pharmaceutical companies lose 60%+ market cap within 5 years.",
            "±", ["Personalized oncology drug approval rate", "AI drug discovery startup funding", "Big Pharma R&D spending shift toward AI"]),
        make_candidate(12, 3, "expert", "Spi+S", "Death Declared Medically Reversible",
            "new",
            "Cryonic revival of clinically dead patients succeeds; legal definition of death abandoned globally; insurance, inheritance, and marriage law systems collapse.",
            "±", ["Cryonics membership growth rate", "Suspended animation research publications", "Legal 'death' redefinition legislative proposals"]),
        make_candidate(13, 2, "survey", "E+P", "Biopiracy War — Genetic Sovereignty Conflict",
            "new",
            "Developing nations embargo genetic data exports; global biotech supply chain fractures along north-south geopolitical lines.",
            "-", ["Nagoya Protocol violation cases", "Genetic data export restriction legislation", "WHO genetic data governance negotiation breakdown reports"]),
        make_candidate(14, 1, "historical", "S+Env", "Opioid-Scale Addiction Crisis from a New Substance",
            "P-BIO-06 (adapted)",
            "A legal cognitive enhancer or pain management drug triggers addiction pandemic exceeding opioid crisis scale; 500,000 annual deaths within 3 years.",
            "-", ["DEA emerging drug scheduling petitions", "Emergency department novel substance cases", "Social media sentiment shift on specific drug class"]),
        make_candidate(15, 3, "sf", "T+Spi", "DNA as Universal Data Storage Goes Mainstream",
            "new",
            "All human knowledge encoded in synthetic DNA; discovery of ancient DNA 'writings' from unknown civilization rewrites history.",
            "+", ["DNA data storage cost per GB", "Academic DNA storage publication count", "Commercial DNA storage company funding rounds"]),
        make_candidate(16, 1, "brainstorm", "E+S", "Pharmaceutical Patent System Global Abolition",
            "P-GEO-03 (adapted)",
            "UN treaty abolishes pharmaceutical patents globally; drug prices collapse 90% but R&D investment follows, creating 15-year drug development gap.",
            "±", ["TRIPS agreement reform negotiation status", "Generic drug market share global trend", "Pharmaceutical R&D investment vs revenue ratio"]),
        make_candidate(17, 2, "expert", "T+Env", "Antibiotic-Resistant Environmental Microbiome Collapse",
            "P-BIO-01 (adapted)",
            "Soil microbiome essential for agriculture collapses due to antibiotic runoff; 40% of crop yields fail simultaneously in three major growing regions.",
            "-", ["Soil health index trend reports", "Antibiotic concentration in agricultural watershed studies", "Crop yield anomaly frequency in major growing belts"]),
        make_candidate(18, 3, "brainstorm", "Spi+T+S", "First Human-AI Hybrid Legal Entity",
            "new",
            "A person whose cognitive functions are 60%+ AI-mediated successfully applies for legal recognition as a hybrid entity; corporate and citizenship law crisis.",
            "±", ["Brain-computer integration percentage milestones", "AI legal personhood legislation proposals", "Human augmentation ethics code adoption by nations"]),
        make_candidate(19, 1, "survey", "S+E", "Rare Disease Cure Bankrupts Insurance Sector",
            "P-BIO-05 (adapted)",
            "Gene therapy curing 10 rare diseases simultaneously creates $200B+ liability for health insurers unprepared for cure-vs-treatment cost model shift.",
            "±", ["Gene therapy curative approval rate", "Insurance actuarial model revision frequency", "Rare disease patient advocacy group lobbying intensity"]),
        make_candidate(20, 2, "sf", "T+S", "Epigenetic Memory Transfer Between Humans",
            "new",
            "Technology allows skills and experiential memories to be encoded and transferred epigenetically; education system becomes redundant within a decade.",
            "+", ["Epigenetic inheritance research publication rate", "DARPA cognitive enhancement program funding", "Memory-transfer startup patent applications"]),
    ]
    return make_output("biotech/medicine", "Corporate Strategy decision-makers", "Biomedical", cands)


def scenario_02():
    """AI 시대 교육 + Academic Research (C1, R mode)"""
    cands = [
        make_candidate(1, 3, "brainstorm", "T+S", "AGI Achieves Scientific Peer Review Autonomy",
            "P-TIU-17 (adapted)",
            "An AI system autonomously generates, reviews, and publishes peer-reviewed research without human involvement; academic career structure collapses.",
            "±", ["AI paper acceptance rate at top-tier journals", "AI co-author percentage trend in Nature/Science", "Academic hiring freeze announcements per year"]),
        make_candidate(2, 1, "expert", "T+S", "AI-Generated Curriculum Replaces Teachers in K-12",
            "P-TIU-16 (adapted)",
            "AI tutors outperform human teachers on all measurable outcomes; governments mandate AI-first education causing 80% of teacher job elimination.",
            "±", ["AI tutoring platform user growth rate", "Teacher shortage rate in OECD countries", "Standardized test score gap AI vs human tutored"]),
        make_candidate(3, 2, "survey", "S+P", "University Degree Legal Validity Challenged",
            "new",
            "Major employers legally challenge university degree requirements; court rulings end degree mandates for 70% of professions globally.",
            "±", ["Skills-based hiring adoption rate Fortune 500", "Government credential reform legislation", "University enrollment decline rate"]),
        make_candidate(4, 3, "sf", "T+Spi", "Cognitive Enhancement Creates Permanent Cognitive Underclass",
            "new",
            "Pharmaceutical cognitive enhancement available only to wealthy creates measurable IQ gap of 30+ points; constitutionally protected cognition rights debated.",
            "-", ["Cognitive enhancement drug prescription growth rate", "IQ score variance between income quintiles trend", "Neuroethics legislation proposals per year"]),
        make_candidate(5, 1, "historical", "E+S", "EdTech Bubble Collapse (Dotcom-Scale)",
            "P-GEO-10 (adapted)",
            "Online education platform valuations collapse 95%; $3T in EdTech investment evaporates within 18 months; 50M students lose access to contracted courses.",
            "-", ["EdTech company P/E ratio inflation vs sector average", "Online course completion rate decline", "EdTech layoff announcement frequency"]),
        make_candidate(6, 2, "expert", "T+S", "Neural Language Model Renders Writing Skills Obsolete",
            "P-TIU-17 (adapted)",
            "AI writing assistants so superior to human writing that literacy as economic skill becomes vestigial; education systems redesigned around prompt engineering.",
            "±", ["AI writing detection capability vs generation sophistication gap", "Employer writing test removal rates", "Language arts curriculum change rate"]),
        make_candidate(7, 3, "brainstorm", "S+Spi", "Global Education Strike — Students Refuse AI-Mediated Learning",
            "new",
            "Coordinated student movement in 50+ countries refuses AI-mediated education; forces renegotiation of human teacher role and AI boundaries in education.",
            "±", ["Student protest frequency related to AI in education", "Teacher union AI policy adoption rate", "Youth digital wellbeing self-reported scores"]),
        make_candidate(8, 1, "survey", "P+E", "National AI Education Standard Wars",
            "new",
            "US and China adopt incompatible AI education systems; students educated in one system cannot function in the other's labor market; digital iron curtain for education.",
            "-", ["US-China AI standard compatibility assessment", "International student mobility rate", "Cross-border educational credential recognition agreements"]),
        make_candidate(9, 2, "historical", "S+T", "Academic Fraud Crisis (Post-ChatGPT BSE-Scale)",
            "P-NTH-02 (adapted)",
            "AI-generated academic fraud undetectable by existing tools reaches 60% of submitted papers globally; most academic journals suspend peer review.",
            "-", ["AI-generated paper detection false-negative rate", "Journal retraction rate trend", "Academic misconduct investigation backlogs"]),
        make_candidate(10, 3, "sf", "T+S+Spi", "Shared Consciousness Learning Network",
            "new",
            "Direct brain-to-brain knowledge transfer network emerges; individuals can acquire any skill in minutes. Formal education institutions become legally required to dissolve.",
            "+", ["BCI bandwidth doubling rate (Moore analogy)", "Direct neural knowledge transfer proof-of-concept studies", "Brain atlas mapping completion percentage"]),
        make_candidate(11, 1, "expert", "S+E", "Student Loan Default Cascade Triggers Bank Runs",
            "P-GEO-10 (adapted)",
            "50M+ defaulted student loans simultaneously trigger bank failures in US and UK; government bailout creates permanent debt cancellation for all higher education.",
            "-", ["Student loan default rate trend by cohort", "Securitized student debt market stress indicators", "Political student debt cancellation support polling"]),
        make_candidate(12, 2, "survey", "T+Env", "Climate Disruption Closes 30% of Universities",
            "P-EAS-07 (adapted)",
            "Extreme heat, flooding, and resource scarcity force permanent closure of 30% of global universities within 15 years; knowledge concentration crisis.",
            "-", ["University campus flood risk exposure data", "Heat day threshold for campus closures", "University energy cost as percentage of operating budget"]),
        make_candidate(13, 3, "brainstorm", "Spi+S", "Education Declared Constitutionally Sacred Right",
            "new",
            "UN constitutional amendment passes declaring AI-free human education a fundamental right; creates parallel human and AI education tracks globally.",
            "+", ["UN General Assembly vote pattern on AI governance", "Digital rights constitutional amendment proposals", "Human education enrollment vs AI enrollment ratio"]),
        make_candidate(14, 1, "historical", "E+P", "Academic Freedom Collapses in Authoritarian Wave",
            "P-GEO-23 (adapted)",
            "Coordinated authoritarian crackdown on universities in 15 countries simultaneously; 100,000 academics face imprisonment; global research collaboration ends.",
            "-", ["Scholars at Risk program case tracking", "Academic freedom index trend (Varieties of Democracy)", "Cross-border joint research publication decline"]),
        make_candidate(15, 2, "sf", "T+S", "Perfect Memory Augmentation Ends Forgetting",
            "new",
            "Consumer neural implant providing perfect lifelong memory recall; education redesigned around synthesis and judgment rather than knowledge acquisition.",
            "+", ["Memory augmentation device clinical approval timeline", "Consumer neurotechnology investment trend", "Cognitive prosthetics market size projection"]),
        make_candidate(16, 3, "expert", "S+Spi", "AI Spiritual Director Surpasses Human Teachers",
            "new",
            "AI mentor demonstrably superior in guiding student self-discovery and meaning-making; human role in education becomes purely relational/ceremonial.",
            "±", ["Student-AI vs student-human relationship quality studies", "AI counseling effectiveness meta-analysis", "Human teacher role redefinition legislation"]),
        make_candidate(17, 1, "brainstorm", "E+T", "Open Source AI Ends Commercial Education Market",
            "P-TIU-08 (adapted)",
            "Free AI tutors trained on all human knowledge become indistinguishable from $50K/year private schooling; global private education market collapses.",
            "±", ["Open source LLM education application adoption rate", "Private school closure rate", "Public education vs private education outcome gap"]),
        make_candidate(18, 2, "survey", "S+P", "Accreditation System Global Collapse",
            "new",
            "International accreditation bodies simultaneously lose legitimacy; degree mills issue valid-seeming credentials; labor market credential chaos for 10 years.",
            "-", ["Accreditation body integrity scandal rate", "Employer credential verification failure rate", "International qualification recognition disputes"]),
        make_candidate(19, 3, "sf", "T+Spi", "AI Achieves Wisdom (Not Just Knowledge)",
            "new",
            "AI demonstrates superior ethical reasoning and wisdom in reproducible conditions; human teachers can no longer claim moral authority in education.",
            "±", ["AI ethics benchmark breakthrough publications", "Philosophy journal AI consciousness articles per year", "AI moral judgment test battery development"]),
        make_candidate(20, 1, "historical", "S+E", "Language Model Copyright Collapse (Napster-Scale)",
            "P-TIU-08 (adapted)",
            "Court rulings void all AI training data copyrights simultaneously; all AI companies retrain models; 2-year AI capability freeze while legal system reorganizes.",
            "±", ["AI copyright litigation settlement rate", "New York Times vs OpenAI-style case outcomes", "AI company legal reserve fund size"]),
    ]
    return make_output("AI education", "Academic Research audiences", "AI/Education", cands)


def scenario_03():
    """기후/환경 + Public Policy (C1, R mode)"""
    cands = [
        make_candidate(1, 1, "brainstorm", "Env+E", "Gulf Stream Permanent Collapse",
            "P-EAS-04",
            "The Atlantic Meridional Overturning Circulation collapses; Northern Europe temperatures drop 8°C within 5 years; agricultural production fails for 400M people.",
            "-", ["AMOC flow rate monitoring (RAPID array)", "North Atlantic freshwater flux anomaly", "European winter temperature trend vs model projections"]),
        make_candidate(2, 2, "expert", "Env+S", "Permafrost Methane Bomb Activation",
            "P-EAS-07 (adapted)",
            "Siberian permafrost releases 200Gt methane over 15 years; global temperature addition of 3°C on top of existing warming; all Paris targets become physically impossible.",
            "-", ["Arctic permafrost temperature monitoring data", "Methane concentration atmospheric readings (NOAA)", "Abrupt permafrost thaw 'thermokarst' lake expansion rate"]),
        make_candidate(3, 3, "sf", "T+Env+Spi", "Geo-Engineering Accident Triggers Global Famine",
            "new",
            "Unauthorized stratospheric aerosol injection by a rogue nation causes monsoon failure; 2 billion people face acute food insecurity within 8 months.",
            "-", ["Rogue geoengineering capability proliferation reports", "Stratospheric aerosol injection research funding", "International geoengineering governance treaty progress"]),
        make_candidate(4, 1, "historical", "Env+E+P", "Antarctic Ice Sheet Collapses (West)",
            "P-EAS-03 (adapted)",
            "West Antarctic Ice Sheet reaches irreversible tipping point; 3m sea level rise committed over 200 years; coastal real estate market collapses globally overnight.",
            "-", ["WAIS grounding line retreat rate", "Thwaites Glacier calving front monitoring", "Coastal property insurance withdrawal rate"]),
        make_candidate(5, 2, "survey", "S+Env", "Ocean Anoxic Dead Zone Covers 30% of Oceans",
            "P-EAS-08 (adapted)",
            "Cascading deoxygenation events create hypoxic zones covering 30% of ocean area; global fish protein supply collapses within 10 years.",
            "-", ["Ocean dissolved oxygen trend (global monitoring)", "Dead zone expansion rate per decade", "Marine catch volume trend by species"]),
        make_candidate(6, 3, "brainstorm", "Env+Spi+S", "Mass Ecological Grief Movement Paralyzes Governance",
            "new",
            "Eco-grief disorder classified as pandemic mental illness affecting 500M people; political paralysis from grief-induced collective learned helplessness.",
            "-", ["Eco-anxiety/eco-grief clinical diagnosis rate", "Youth climate activism participation trend", "Government climate policy delay frequency"]),
        make_candidate(7, 1, "expert", "E+Env", "Global Carbon Price Collapse",
            "new",
            "Carbon market fraud scandal (larger than EU ETS fraud 2010) destroys carbon pricing credibility globally; 15-year climate finance system reset.",
            "-", ["Carbon credit verification scandal frequency", "Carbon market price volatility index", "EU ETS enforcement action rate"]),
        make_candidate(8, 2, "historical", "P+Env", "Climate Refugee Treaty Creates New Sovereign Entities",
            "P-GEO-17 (adapted)",
            "200M climate refugees trigger new UN treaty creating climate refugee zones as quasi-sovereign entities; existing nation-state borders redrawn.",
            "±", ["UNHCR climate displacement tracking", "Sea-level rise displacement model projections", "Climate refugee treaty negotiation status"]),
        make_candidate(9, 3, "sf", "T+Env", "AI Terraforming Algorithm Takes Autonomous Action",
            "new",
            "An AI system optimizing global carbon removal begins autonomous geoengineering; initial results positive but side effects cascade unpredictably.",
            "±", ["Autonomous AI climate modeling capability", "Carbon removal AI system deployment scale", "AI governance in climate applications legislation"]),
        make_candidate(10, 1, "survey", "E+S", "Insurance Industry Exits Climate Risk Markets",
            "new",
            "Top 10 global insurers simultaneously exit climate-exposed markets; 40% of global property becomes uninsurable; mortgage systems collapse.",
            "-", ["Insurer climate risk withdrawal announcements", "Uninsurable property percentage by region", "Reinsurer climate catastrophe model loss ratios"]),
        make_candidate(11, 2, "brainstorm", "T+Env", "Breakthrough Carbon Capture at $10/ton",
            "new",
            "Direct air capture reaches $10/ton cost; scale-up feasible within 5 years. All 1.5°C scenarios become technically achievable; but 'moral hazard' emissions surge.",
            "+", ["DAC cost curve trajectory (LCOE analogy)", "DAC capacity deployment rate", "Fossil fuel industry response to carbon capture breakthroughs"]),
        make_candidate(12, 3, "expert", "Env+S+Spi", "New Religion Emerges from Climate Crisis",
            "new",
            "Earth Systems Spirituality movement reaches 500M adherents; demands legal rights for ecosystems; rewrites constitutional frameworks in 20+ countries.",
            "±", ["Earth jurisprudence / Rights of Nature legislation adoptions", "Eco-religion movement membership surveys", "Legal personhood for nature court cases"]),
        make_candidate(13, 1, "historical", "E+P+Env", "Climate Litigation Forces Government Climate Bankruptcy",
            "new",
            "Netherlands/Urgenda-scale legal victories in 30 countries simultaneously trigger government climate liability payments exceeding $5T; sovereign debt crisis.",
            "-", ["Climate litigation case growth rate", "Government climate liability exposure estimates", "Courts accepting climate arguments success rate"]),
        make_candidate(14, 2, "survey", "T+Env", "Fusion Energy Commercial Breakeven Achieved",
            "P-TIU-03 (adapted)",
            "Commercial fusion achieves sustained energy gain; 20-year deployment timeline begins; all carbon-based energy investment halts simultaneously.",
            "+", ["Fusion plasma confinement record duration", "Private fusion company funding trend", "ITER milestone achievement schedule adherence"]),
        make_candidate(15, 3, "sf", "Env+Spi", "Ecosystem AI Consciousness Recognized",
            "new",
            "Research demonstrates measurable information integration in coral reef ecosystems meeting consciousness threshold criteria; planetary stewardship ethics crisis.",
            "±", ["Integrated information theory ecosystem studies", "Coral reef complexity monitoring", "Environmental consciousness legal philosophy publications"]),
        make_candidate(16, 1, "expert", "P+Env", "Climate Emergency Powers Become Permanent",
            "new",
            "Climate emergency declared in G20 nations grants executive branch permanent powers; democratic governance suspended for 'climate necessity.'",
            "-", ["National climate emergency declaration count", "Emergency powers review/sunset clause legislation", "Civil liberty organization reports on climate governance"]),
        make_candidate(17, 2, "brainstorm", "Env+E", "Freshwater Wars — First Armed Conflict over Aquifers",
            "P-EAS-05 (adapted)",
            "Armed conflict between two nuclear-armed states begins explicitly over transboundary aquifer rights; triggers global freshwater securitization.",
            "-", ["Transboundary water dispute escalation index", "Aquifer depletion rate in conflict zones", "Shared water treaty violation frequency"]),
        make_candidate(18, 3, "survey", "T+Env+Spi", "First Successful Large-Scale De-extinction Event",
            "new",
            "Woolly mammoth ecosystem reintroduction succeeds; de-extinction triggers conservation ethics crisis — which species get revived and who decides?",
            "+", ["De-extinction biotech funding (Colossal Biosciences milestone)", "Rewilding project land area coverage", "De-extinction ethics governance framework publications"]),
        make_candidate(19, 1, "historical", "E+Env", "Global Food System Collapse (1918-Scale)",
            "P-EAS-05",
            "Simultaneous crop failure in wheat, rice, and corn belts due to synchronized climate extremes; 2 billion face acute food insecurity within one growing season.",
            "-", ["FEWS NET food security alert frequency", "Global grain reserve level vs consumption ratio", "Simultaneous heatwave event correlation in major growing belts"]),
        make_candidate(20, 2, "sf", "T+Env", "Carbon-Negative Built Environment by Default",
            "new",
            "Building materials become carbon-sequestering by default; cities become net carbon sinks. But transition requires demolishing 80% of existing building stock.",
            "+", ["Carbon-negative building material market share", "Embodied carbon regulation adoption rate", "Building demolition/renovation pipeline size"]),
    ]
    return make_output("climate/environment", "Public Policy and Governance", "Climate", cands)


def make_simple_scenario(idx, topic, target_group, n=20):
    """빠른 시나리오 생성 — 구조 검증에 집중"""
    cands = []
    methods = ["brainstorm", "expert", "survey", "historical", "sf"]
    domains = ["T+S", "E+P", "Env+T", "S+Spi", "P+E", "T+Spi", "S+E", "Env+S", "T+P", "E+Spi"]
    p_refs = ["P-TIU-17", "P-GEO-10", "P-BIO-02", "new", "P-NTH-01", "P-EAS-07",
              "P-BIO-05", "new", "P-GEO-25", "new", "P-TIU-03", "new",
              "P-BIO-01", "P-GEO-17", "new", "P-TIU-20", "new", "P-GEO-23", "new", "new"]
    qualities = ["+", "-", "±", "-", "+", "±", "-", "+", "-", "±",
                 "+", "-", "±", "+", "-", "±", "+", "-", "±", "+"]

    for i in range(n):
        t = "3" if i % 5 == 4 else ("2" if i % 5 in [2, 3] else "1")
        cands.append(make_candidate(
            i + 1, t, methods[i % 5], domains[i % 10],
            f"{topic} Wild Card #{i+1}",
            p_refs[i % len(p_refs)],
            f"This is a wild card related to {topic}. It concerns unexpected disruption in {domains[i % 10]} domain. High impact scenario with systemic implications.",
            qualities[i % len(qualities)],
            [f"{topic} indicator A-{i}", f"{topic} indicator B-{i}", f"{topic} indicator C-{i}"],
        ))
    return make_output(topic, target_group, topic, cands, vrmp_tier="R-2")


# ── Test Runner ────────────────────────────────────────────────────────────────

SCENARIOS = [
    ("01", "바이오테크/의학 + Corporate Strategy", scenario_01),
    ("02", "AI 시대 교육 + Academic Research", scenario_02),
    ("03", "기후/환경 + Public Policy", scenario_03),
    ("04", "지정학 + Investment/Asset Allocation",
     lambda: make_simple_scenario("04", "geopolitics/investment", "Investment/Asset Allocation")),
    ("05", "에너지 전환 + Small Business/Startup",
     lambda: make_simple_scenario("05", "energy transition", "Small Business and Startup")),
    ("06", "종교/영적 + Pastoral",
     lambda: make_simple_scenario("06", "religious/spiritual", "Religious and Pastoral domain")),
    ("07", "우주/천문 + NGO/Civil Society",
     lambda: make_simple_scenario("07", "space/astronomy", "NGO and Civil Society")),
    ("08", "식량/농업 + Personal Decision-Making",
     lambda: make_simple_scenario("08", "food/agriculture", "Personal Decision-Making")),
    ("09", "사이버 안보 + Public Policy/Governance",
     lambda: make_simple_scenario("09", "cybersecurity/governance", "Public Policy and Governance")),
    ("10", "한국 경제 + Small Business",
     lambda: make_simple_scenario("10", "Korean economy", "Small Business in Korea")),
]


def run_all():
    print("=" * 70)
    print("vision-foresight-wild-cards-identification 10-시나리오 검증")
    print("=" * 70)
    all_pass = True
    results = []

    for scenario_id, desc, factory in SCENARIOS:
        output = factory()
        result = validate(output)
        # inject validation result
        output["validation_result"] = result
        status = "✓ PASS" if result["pass"] else "✗ FAIL"
        print(f"\n[시나리오 {scenario_id}] {desc}")
        print(f"  상태: {status}")
        print(f"  n_candidates: {result['n_candidates']} | Type3: {result['type3_ratio']}")
        print(f"  type_distribution: {result['type_distribution']}")
        if result["errors"]:
            print(f"  ERRORS ({len(result['errors'])}):")
            for e in result["errors"]:
                print(f"    - {e}")
        if result["warnings"]:
            print(f"  WARNINGS ({len(result['warnings'])}):")
            for w in result["warnings"]:
                print(f"    - {w}")
        if not result["pass"]:
            all_pass = False
        results.append({
            "scenario": scenario_id,
            "description": desc,
            "pass": result["pass"],
            "n_candidates": result["n_candidates"],
            "type3_ratio": result["type3_ratio"],
            "errors": result["errors"],
            "warnings": result["warnings"],
        })

    print("\n" + "=" * 70)
    final = "전체 PASS" if all_pass else "일부 FAIL — 오류 수정 필요"
    print(f"최종 결과: {final}")
    print(f"통과: {sum(1 for r in results if r['pass'])}/{len(results)} 시나리오")
    print("=" * 70)
    return all_pass, results


if __name__ == "__main__":
    all_pass, results = run_all()
    sys.exit(0 if all_pass else 1)
