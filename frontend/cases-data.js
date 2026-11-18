(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.SherpaCasesData = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const CASE_IDS = ["michael-carter","samantha-lewis","timothy-melanie-weah","daniel-emily-johnson"];
  const CASES_DATA = {
  "michael-carter": {
    "meta": {
      "slug": "michael-carter",
      "household": "Michael",
      "city": "Austin",
      "state": "TX",
      "tax_filing_status": "SINGLE",
      "isCouple": false,
      "owners": [
        {
          "key": "A",
          "name": "Michael",
          "role": "client",
          "age": 37,
          "retirement_age": 58,
          "risk_profile": "Growth"
        }
      ]
    },
    "score": {
      "published_score": 26,
      "scale": "0 to 100",
      "band": "critical",
      "colour": "red",
      "message": "Given your score of 26, financial concerns are significantly impacting your overall well-being and preventing you from achieving a fulfilling life. Your financial health is essential for your overall wellness, and it's crucial to seek expert guidance now to manage stress and regain control over your financial decisions.",
      "pillars": [
        {
          "pillar": "Savings and cash flow",
          "score": 0,
          "points_shown_in_app": "0/25"
        },
        {
          "pillar": "Debt",
          "score": 78,
          "points_shown_in_app": "8/10"
        },
        {
          "pillar": "Investments",
          "score": 42,
          "points_shown_in_app": "11/25"
        },
        {
          "pillar": "Liquidity and emergency fund",
          "score": 22,
          "points_shown_in_app": "4/20"
        },
        {
          "pillar": "Insurance and protection",
          "score": 18,
          "points_shown_in_app": "4/20"
        }
      ],
      "caps_applied": [],
      "top_moves": [
        {
          "title": "Add umbrella cover",
          "action": "Add $1M of umbrella to raise the liability shield",
          "effort": "low",
          "target_amount": 1000000,
          "score_before": 26,
          "score_after": 31,
          "lifts_a_cap": false
        },
        {
          "title": "Lower the withdrawal rate",
          "action": "Cutting withdrawals to $10,300/year (6.0%) reaches the sustainable band",
          "effort": "high",
          "target_amount": 10300,
          "score_before": 26,
          "score_after": 62,
          "lifts_a_cap": false
        },
        {
          "title": "Raise growth allocation toward glide",
          "action": "Move the invested mix from 74% to 88% growth (glide 98%) for the next horizon-fit band — about $19,900 of the invested book",
          "effort": "high",
          "target_amount": 19900,
          "score_before": 26,
          "score_after": 31,
          "lifts_a_cap": false
        }
      ],
      "combined_moves": [],
      "explainer": "## Key takeaways\n- The published score is 26, in the critical band. Nothing separate caps it; weakness across several areas, led by cash flow, sets the number.\n- Debt is the most solid area. Withdrawals of about 84% of investable assets, against a sustainable 4%, hold the household back most.\n- Protection also weighs on the score: the mortality ratio is 30%, and no umbrella cover is in place.\n- The top move is to add $1M of umbrella cover, for a $1,000,000 total. The published score moves from 26 to 31.\n\n## Cash flow\n- Withdrawals run at about 84% of investable assets, far above the 4% sustainable rate. This is why cash flow is the weakest area.\n- Cutting withdrawals to $10,300 a year (6.0%) would move the published score from 26 to 62, the largest gain available.\n\n## Debt\n- Debt is the strongest area. Debt payments are a manageable share of income, which supports the score.\n- A revolving card balance at 20% APR is the main drag, so clearing it would help most.\n\n## Protection\n- Protection holds the score back. The mortality ratio is 30%, which signals a large life-cover shortfall against need.\n- No umbrella cover is in place, so the liability shield is absent. The BMW 3 Series also lacks auto cover in the data.\n\n## Liquidity\n- Cash is $27,000, about 2.9 months of spending. That is thin against annual withdrawals of roughly $145,000.\n- Liquid assets are small against near-term commitments, so a shock could force the sale of investments.\n\n## Investing\n- Growth assets are about 74% of the invested mix, below the 98% glide target. Moving toward 88%, about $19,900 of the book, lifts the published score from 26 to 31.\n- VTI is the largest position at $60,000, about 35% of investable assets. That concentration also weighs on the score.\n- Tax-inefficient holdings total $36,500, including $15,000 in JNK held outside tax-advantaged accounts."
    },
    "persona": {
      "D0": "EMERGING. Investable assets are $145,000, held in a 401(k) ($80,000), a taxable brokerage account ($60,000) and an HSA ($5,000). Investable assets leave out cash and real estate and are well under the $500K line. Bank cash is $27,000 (checking $12,000, savings $15,000), so investable assets plus bank cash come to $172,000. RSUs of $35,000 and a BMW 3 Series worth $40,000 sit outside both figures. Total assets are $247,000 and debts $28,500, so net worth is $218,500.\r\n\r\nHis $180,000 salary is about the 90th income percentile in Texas. High income against modest savings so far is the defining profile.",
      "D1": "MID ACCUMULATION. Michael is 37, single, with no children and no co-client. He is employed and rents in Austin, TX ($2,800 a month). His target retirement age is 58, which is 20 years away, and the plan runs to age 91.\r\n\r\nThe plan has him buying a $550,000 home in January 2027 (see the transition alert).",
      "D2": "MODERATE. There is one salary, no business and no real estate yet. He holds a traditional 401(k) with a fixed $7,000 yearly employer match, an HSA, a taxable brokerage account, and checking and savings accounts. He has whole life, long-term disability and renter insurance. He has three debts: an Amex Platinum card, a federal student loan and a car loan on the BMW. The taxable brokerage account holds a $15,000 high-yield bond fund (JNK) taxed at 24%, and investment income costs him about $527 a year in tax.",
      "D3": "SIGNIFICANT GAPS. The published Financial Health score is 26 out of 100, in the critical band. Several weak areas add up, led by cash flow (0 of 25 points). Investments score 11 of 25, liquidity 4 of 20, insurance 4 of 20 and debt 8 of 10, the strongest. He saves $43,000 a year (23.9% of income, including the $7,000 employer match), so these are gaps in how the money is sequenced, not a lack of effort.\r\n\r\n- **Retirement:** retiring at 58 falls short. Savings and investments run out at age 85, six years before the plan ends at 91, and $32,439 of planned spending would go unpaid by then. The gap at retirement is $1,177,586 in today's dollars, and closing it would take about $20,231 more per year. Social Security is the only guaranteed income and covers 34% of the $89,649 yearly spending need, so savings must supply about $59,613 a year, a 5.6% average draw. At 58 his net worth would be $1,535,457, of which $1,071,095 is liquid. The plan does not include long-term care costs.\r\n- **Cash flow:** net cash flow is -$8,336 a year (-4.63% of gross income). Taxes ($40,664), rent and renter insurance ($34,272), living expenses ($66,000), debt payments ($11,400) and $36,000 of his own savings use more than his $180,000 income.\r\n- **Liquidity:** accessible cash is $30,000 (bank cash plus $3,000 of money market inside the brokerage account). Against monthly expenses of $9,306 it covers about 3.2 months. The recommended reserve is 5 to 6 months ($46,530 to $55,836), so he is $16,530 short of the minimum. Add the January 2027 goals (the $113,300 down payment and a $3,500 vacation) and the cash target is $163,330 to $172,636. Set against that, cash covers 0 months.\r\n- **Protection:** life insurance is $180,000 against a recommended $900,000 to $1,800,000, a $720,000 shortfall. There is no umbrella liability policy against a recommended minimum of $1,000,000.\r\n- **Debt:** total debt is $28,500, or 15.83% of gross income. Debt payments are 6.33% of income, and rent plus renter insurance plus debt payments make up 25.37% of income, below the 36% first threshold. The debts are the Amex card ($3,500 at 20%), the student loan ($10,000 at 5.8%) and the BMW loan ($15,000 at 5%).",
      "D4a": "- **D4a stated:** AGGRESSIVE. His chosen risk profile is Growth (4).\r",
      "D4b": "- **D4b revealed:** AGGRESSIVE, with a caveat. In the long-term accounts (the $145,000 of investable assets) about 72.1% is in stocks and 25.1% in bonds, against a Growth target of 80.0% stocks and 17.8% bonds. Counting the cash as well, stocks are about 58.7% of the $172,000 total. Over the three years to November 2026 the portfolio returned about 13.6% a year, with a worst fall of 10.2% that recovered in 62 days. A simple mix with the same stock share returned 15.3% a year.\r",
      "D4c": "- **D4c inferred:** AGGRESSIVE. A thin cash cushion, no umbrella cover, a life policy well below need, and a salary and RSUs tied to one employer all point to someone comfortable carrying risk.\r\n\r\nThe result is ALIGNED. Stated, revealed and inferred risk all sit near the Growth end.",
      "D4": "- **D4a stated:** AGGRESSIVE. His chosen risk profile is Growth (4).\r\n- **D4b revealed:** AGGRESSIVE, with a caveat. In the long-term accounts (the $145,000 of investable assets) about 72.1% is in stocks and 25.1% in bonds, against a Growth target of 80.0% stocks and 17.8% bonds. Counting the cash as well, stocks are about 58.7% of the $172,000 total. Over the three years to November 2026 the portfolio returned about 13.6% a year, with a worst fall of 10.2% that recovered in 62 days. A simple mix with the same stock share returned 15.3% a year.\r\n- **D4c inferred:** AGGRESSIVE. A thin cash cushion, no umbrella cover, a life policy well below need, and a salary and RSUs tied to one employer all point to someone comfortable carrying risk.\r\n\r\nThe result is ALIGNED. Stated, revealed and inferred risk all sit near the Growth end.",
      "D5": "COLLABORATOR, CONFIDENCE: LOW. There are no interview notes or free text from Michael, so this is inferred from the shape of his accounts. He picks his own ETFs, uses an HSA and a taxable account, and captures the full employer match. That looks like an engaged person who still seeks advice.",
      "D6": "FREEDOM, CONFIDENCE: LOW and PROVISIONAL. This is inferred from structure only: a high savings rate, a retirement target of 58 and a yearly $3,500 vacation planned until 2047. Nothing in his own words confirms it.",
      "transitionAlerts": "- **Home purchase in January 2027 (within 12 months).** Michael plans to buy a $550,000 home ($566,500 at purchase) with a $113,300 down payment and a 30-year loan of $453,200 at 7%. The monthly payment is $3,015.15, against $2,800 of rent today. The home would also add property taxes of $5,665 a year, home insurance of $2,832.50 a year and $9,464 of closing costs. Housing costs, cash, the debt load and retirement saving all change at once. The yearly projection shows investable assets of $178,717 in 2026 and $81,172 in 2027.\r\n- The $3,500 vacation also falls in January 2027 and repeats every year until 2047.",
      "subjectiveConcerns": "None detected. There is no interview or free text from Michael.",
      "objectiveConcerns": [
        {
          "id": "O1",
          "detail": "- **O1 SIGNIFICANT: Retirement shortfall.** Savings run out at 85 against a plan to 91, with $32,439 of planned spending unpaid and a $1,177,586 gap at retirement. The average draw is 5.6%. Connected: D3, D1."
        },
        {
          "id": "O2",
          "detail": "- **O2 SIGNIFICANT: Cash for the home purchase and a thin reserve.** Cash of $30,000 covers about 3.2 months, $16,530 short of the 5 to 6 month reserve. Counting the January 2027 goals, the target is $163,330 to $172,636, and the plan's cash covers 0 months after them. Connected: D1, D3."
        },
        {
          "id": "O3",
          "detail": "- **O3 SIGNIFICANT: Life insurance shortfall of $720,000.** He has $180,000 of whole life cover against $900,000 to $1,800,000 recommended. His salary is the only income. Connected: D3."
        },
        {
          "id": "O4",
          "detail": "- **O4 MODERATE: No umbrella cover.** The recommended minimum is $1,000,000. A claim could reach $172,000 of liquid assets and a $218,500 net worth. Connected: D3, D4c."
        },
        {
          "id": "O5",
          "detail": "- **O5 MODERATE: Negative cash flow.** Net cash flow is -$8,336 a year (-4.63% of gross income), even with $43,000 a year going to savings. Connected: D3."
        },
        {
          "id": "O6",
          "detail": "- **O6 MINOR: High-interest card.** The Amex Platinum balance is $3,500 at 20%, with $200 paid each month. It is small but his most expensive debt. Connected: D3."
        },
        {
          "id": "O7",
          "detail": "- **O7 MINOR: Unused savings room.** He defers $17,000 to the 401(k) against a $24,500 limit, so $7,500 more is possible (worth about $1,800 in tax at 24%). He could contribute up to $4,500 to a Roth IRA (estimate) and has put in $0. His HSA has $4,000 of a $4,400 limit, leaving $400. Connected: D3."
        },
        {
          "id": "O8",
          "detail": "- **O8 MINOR: One employer and concentrated holdings.** His $180,000 salary equals 82.4% of his net worth, and the $35,000 of RSUs adds to that. Technology is his largest sector. Connected: D4c, D4b."
        }
      ],
      "tensions": [
        {
          "id": "T1",
          "detail": "- **T1 (HIGH):** O2 against O1. The $113,300 down payment competes with retirement saving for the same dollars, and the plan has only $30,000 in cash for it. The projection implies the purchase is paid mostly from investments, which cuts the base that has to carry retirement."
        },
        {
          "id": "T2",
          "detail": "- **T2 (MEDIUM):** O1 against O5. Closing the retirement gap would take about $20,231 more a year, while cash flow is already -$8,336 a year. Both claim the same dollars."
        },
        {
          "id": "T3",
          "detail": "- **T3 (MEDIUM):** O3 and O4 against O5 and O2. Closing the insurance gaps adds premiums while cash flow is negative and cash is thin."
        },
        {
          "id": "T4",
          "detail": "- **T4 (MEDIUM):** O2 against D4a and D4b. A Growth profile suits a 20-year retirement horizon, but money needed in January 2027 is short-term money. Rebuilding cash by $16,530 or more, and setting aside the down payment, competes with staying invested."
        },
        {
          "id": "T5",
          "detail": "- **T5 (LOW):** O6 against O2 and O7. Paying off a 20% card faster is a guaranteed return, but it uses cash that is already thin and competes with retirement saving. At $200 a month it is projected paid off by July 2028."
        }
      ]
    },
    "projections": {
      "yearly": [
        {
          "year": 2026,
          "age_client": 37,
          "age_co_client": null,
          "net_worth": 226457,
          "net_worth_todays_dollars": 225892,
          "total_debts": 26933,
          "investable_assets": 178717,
          "net_worth_needed": 226457
        },
        {
          "year": 2027,
          "age_client": 38,
          "age_co_client": null,
          "net_worth": 268863,
          "net_worth_todays_dollars": 260276,
          "total_debts": 465676,
          "investable_assets": 81172,
          "net_worth_needed": 268863
        },
        {
          "year": 2028,
          "age_client": 39,
          "age_co_client": null,
          "net_worth": 312877,
          "net_worth_todays_dollars": 293944,
          "total_debts": 451100,
          "investable_assets": 95902,
          "net_worth_needed": 312877
        },
        {
          "year": 2029,
          "age_client": 40,
          "age_co_client": null,
          "net_worth": 369712,
          "net_worth_todays_dollars": 337086,
          "total_debts": 439977,
          "investable_assets": 125852,
          "net_worth_needed": 369712
        },
        {
          "year": 2030,
          "age_client": 41,
          "age_co_client": null,
          "net_worth": 436175,
          "net_worth_todays_dollars": 385945,
          "total_debts": 432691,
          "investable_assets": 168253,
          "net_worth_needed": 436175
        },
        {
          "year": 2031,
          "age_client": 42,
          "age_co_client": null,
          "net_worth": 512602,
          "net_worth_todays_dollars": 440183,
          "total_debts": 426604,
          "investable_assets": 220835,
          "net_worth_needed": 512602
        },
        {
          "year": 2032,
          "age_client": 43,
          "age_co_client": null,
          "net_worth": 596065,
          "net_worth_todays_dollars": 496745,
          "total_debts": 420078,
          "investable_assets": 279056,
          "net_worth_needed": 596065
        },
        {
          "year": 2033,
          "age_client": 44,
          "age_co_client": null,
          "net_worth": 687042,
          "net_worth_todays_dollars": 555662,
          "total_debts": 413080,
          "investable_assets": 343382,
          "net_worth_needed": 687042
        },
        {
          "year": 2034,
          "age_client": 45,
          "age_co_client": null,
          "net_worth": 785804,
          "net_worth_todays_dollars": 616779,
          "total_debts": 405576,
          "investable_assets": 414064,
          "net_worth_needed": 785804
        },
        {
          "year": 2035,
          "age_client": 46,
          "age_co_client": null,
          "net_worth": 892222,
          "net_worth_todays_dollars": 679634,
          "total_debts": 397530,
          "investable_assets": 490947,
          "net_worth_needed": 892222
        },
        {
          "year": 2036,
          "age_client": 47,
          "age_co_client": null,
          "net_worth": 1006692,
          "net_worth_todays_dollars": 744195,
          "total_debts": 388902,
          "investable_assets": 574395,
          "net_worth_needed": 1006692
        },
        {
          "year": 2037,
          "age_client": 48,
          "age_co_client": null,
          "net_worth": 1129782,
          "net_worth_todays_dollars": 810536,
          "total_debts": 379650,
          "investable_assets": 664934,
          "net_worth_needed": 1129782
        },
        {
          "year": 2038,
          "age_client": 49,
          "age_co_client": null,
          "net_worth": 1262107,
          "net_worth_todays_dollars": 878741,
          "total_debts": 369730,
          "investable_assets": 763133,
          "net_worth_needed": 1262107
        },
        {
          "year": 2039,
          "age_client": 50,
          "age_co_client": null,
          "net_worth": 1404332,
          "net_worth_todays_dollars": 948903,
          "total_debts": 359092,
          "investable_assets": 869605,
          "net_worth_needed": 1404332
        },
        {
          "year": 2040,
          "age_client": 51,
          "age_co_client": null,
          "net_worth": 1557175,
          "net_worth_todays_dollars": 1021120,
          "total_debts": 347685,
          "investable_assets": 985008,
          "net_worth_needed": 1557175
        },
        {
          "year": 2041,
          "age_client": 52,
          "age_co_client": null,
          "net_worth": 1721325,
          "net_worth_todays_dollars": 1095443,
          "total_debts": 335454,
          "investable_assets": 1110046,
          "net_worth_needed": 1721325
        },
        {
          "year": 2042,
          "age_client": 53,
          "age_co_client": null,
          "net_worth": 1898486,
          "net_worth_todays_dollars": 1172524,
          "total_debts": 322338,
          "investable_assets": 1245478,
          "net_worth_needed": 1898486
        },
        {
          "year": 2043,
          "age_client": 54,
          "age_co_client": null,
          "net_worth": 2088678,
          "net_worth_todays_dollars": 1251911,
          "total_debts": 308275,
          "investable_assets": 1392123,
          "net_worth_needed": 2088678
        },
        {
          "year": 2044,
          "age_client": 55,
          "age_co_client": null,
          "net_worth": 2292877,
          "net_worth_todays_dollars": 1333736,
          "total_debts": 293194,
          "investable_assets": 1550861,
          "net_worth_needed": 2292877
        },
        {
          "year": 2045,
          "age_client": 56,
          "age_co_client": null,
          "net_worth": 2512135,
          "net_worth_todays_dollars": 1418142,
          "total_debts": 277024,
          "investable_assets": 1722644,
          "net_worth_needed": 2512135
        },
        {
          "year": 2046,
          "age_client": 57,
          "age_co_client": null,
          "net_worth": 2747584,
          "net_worth_todays_dollars": 1505272,
          "total_debts": 259684,
          "investable_assets": 1908497,
          "net_worth_needed": 2747584
        },
        {
          "year": 2047,
          "age_client": 58,
          "age_co_client": null,
          "net_worth": 2840681,
          "net_worth_todays_dollars": 1510337,
          "total_debts": 241092,
          "investable_assets": 1949763,
          "net_worth_needed": 2840681
        },
        {
          "year": 2048,
          "age_client": 59,
          "age_co_client": null,
          "net_worth": 2860262,
          "net_worth_todays_dollars": 1475859,
          "total_debts": 221155,
          "investable_assets": 1915159,
          "net_worth_needed": 2860262
        },
        {
          "year": 2049,
          "age_client": 60,
          "age_co_client": null,
          "net_worth": 2875133,
          "net_worth_todays_dollars": 1439741,
          "total_debts": 199776,
          "investable_assets": 1873361,
          "net_worth_needed": 2875133
        },
        {
          "year": 2050,
          "age_client": 61,
          "age_co_client": null,
          "net_worth": 2884734,
          "net_worth_todays_dollars": 1401908,
          "total_debts": 176853,
          "investable_assets": 1823675,
          "net_worth_needed": 2884734
        },
        {
          "year": 2051,
          "age_client": 62,
          "age_co_client": null,
          "net_worth": 2883613,
          "net_worth_todays_dollars": 1359998,
          "total_debts": 152272,
          "investable_assets": 1760504,
          "net_worth_needed": 2883613
        },
        {
          "year": 2052,
          "age_client": 63,
          "age_co_client": null,
          "net_worth": 2852014,
          "net_worth_todays_dollars": 1305390,
          "total_debts": 125914,
          "investable_assets": 1663937,
          "net_worth_needed": 2852014
        },
        {
          "year": 2053,
          "age_client": 64,
          "age_co_client": null,
          "net_worth": 2805065,
          "net_worth_todays_dollars": 1246003,
          "total_debts": 97651,
          "investable_assets": 1548941,
          "net_worth_needed": 2805065
        },
        {
          "year": 2054,
          "age_client": 65,
          "age_co_client": null,
          "net_worth": 2732940,
          "net_worth_todays_dollars": 1178131,
          "total_debts": 67345,
          "investable_assets": 1405516,
          "net_worth_needed": 2732940
        },
        {
          "year": 2055,
          "age_client": 66,
          "age_co_client": null,
          "net_worth": 2639563,
          "net_worth_todays_dollars": 1104290,
          "total_debts": 34847,
          "investable_assets": 1237402,
          "net_worth_needed": 2639563
        },
        {
          "year": 2056,
          "age_client": 67,
          "age_co_client": null,
          "net_worth": 2606011,
          "net_worth_todays_dollars": 1058071,
          "total_debts": 1,
          "investable_assets": 1125478,
          "net_worth_needed": 2606011
        },
        {
          "year": 2057,
          "age_client": 68,
          "age_co_client": null,
          "net_worth": 2592063,
          "net_worth_todays_dollars": 1021342,
          "total_debts": 0,
          "investable_assets": 1066679,
          "net_worth_needed": 2592063
        },
        {
          "year": 2058,
          "age_client": 69,
          "age_co_client": null,
          "net_worth": 2580056,
          "net_worth_todays_dollars": 986603,
          "total_debts": 0,
          "investable_assets": 1008458,
          "net_worth_needed": 2580056
        },
        {
          "year": 2059,
          "age_client": 70,
          "age_co_client": null,
          "net_worth": 2568194,
          "net_worth_todays_dollars": 953078,
          "total_debts": 0,
          "investable_assets": 948978,
          "net_worth_needed": 2568194
        },
        {
          "year": 2060,
          "age_client": 71,
          "age_co_client": null,
          "net_worth": 2550203,
          "net_worth_todays_dollars": 918465,
          "total_debts": 0,
          "investable_assets": 881919,
          "net_worth_needed": 2550203
        },
        {
          "year": 2061,
          "age_client": 72,
          "age_co_client": null,
          "net_worth": 2524019,
          "net_worth_todays_dollars": 882202,
          "total_debts": 0,
          "investable_assets": 805174,
          "net_worth_needed": 2524019
        },
        {
          "year": 2062,
          "age_client": 73,
          "age_co_client": null,
          "net_worth": 2488464,
          "net_worth_todays_dollars": 844101,
          "total_debts": 0,
          "investable_assets": 717522,
          "net_worth_needed": 2488464
        },
        {
          "year": 2063,
          "age_client": 74,
          "age_co_client": null,
          "net_worth": 2448011,
          "net_worth_todays_dollars": 805868,
          "total_debts": 0,
          "investable_assets": 623386,
          "net_worth_needed": 2448011
        },
        {
          "year": 2064,
          "age_client": 75,
          "age_co_client": null,
          "net_worth": 2439767,
          "net_worth_todays_dollars": 779446,
          "total_debts": 0,
          "investable_assets": 559828,
          "net_worth_needed": 2439767
        },
        {
          "year": 2065,
          "age_client": 76,
          "age_co_client": null,
          "net_worth": 2434784,
          "net_worth_todays_dollars": 754894,
          "total_debts": 0,
          "investable_assets": 497847,
          "net_worth_needed": 2434784
        },
        {
          "year": 2066,
          "age_client": 77,
          "age_co_client": null,
          "net_worth": 2432200,
          "net_worth_todays_dollars": 731833,
          "total_debts": 0,
          "investable_assets": 436531,
          "net_worth_needed": 2432200
        },
        {
          "year": 2067,
          "age_client": 78,
          "age_co_client": null,
          "net_worth": 2432298,
          "net_worth_todays_dollars": 710259,
          "total_debts": 0,
          "investable_assets": 376111,
          "net_worth_needed": 2432298
        },
        {
          "year": 2068,
          "age_client": 79,
          "age_co_client": null,
          "net_worth": 2435388,
          "net_worth_todays_dollars": 690169,
          "total_debts": 0,
          "investable_assets": 316843,
          "net_worth_needed": 2435388
        },
        {
          "year": 2069,
          "age_client": 80,
          "age_co_client": null,
          "net_worth": 2441807,
          "net_worth_todays_dollars": 671562,
          "total_debts": 0,
          "investable_assets": 259007,
          "net_worth_needed": 2441807
        },
        {
          "year": 2070,
          "age_client": 81,
          "age_co_client": null,
          "net_worth": 2451923,
          "net_worth_todays_dollars": 654439,
          "total_debts": 0,
          "investable_assets": 202914,
          "net_worth_needed": 2451923
        },
        {
          "year": 2071,
          "age_client": 82,
          "age_co_client": null,
          "net_worth": 2466135,
          "net_worth_todays_dollars": 638802,
          "total_debts": 0,
          "investable_assets": 148903,
          "net_worth_needed": 2466135
        },
        {
          "year": 2072,
          "age_client": 83,
          "age_co_client": null,
          "net_worth": 2484879,
          "net_worth_todays_dollars": 624658,
          "total_debts": 0,
          "investable_assets": 97348,
          "net_worth_needed": 2484879
        },
        {
          "year": 2073,
          "age_client": 84,
          "age_co_client": null,
          "net_worth": 2508628,
          "net_worth_todays_dollars": 612013,
          "total_debts": 0,
          "investable_assets": 48660,
          "net_worth_needed": 2508628
        },
        {
          "year": 2074,
          "age_client": 85,
          "age_co_client": null,
          "net_worth": 2537895,
          "net_worth_todays_dollars": 600877,
          "total_debts": 0,
          "investable_assets": 3288,
          "net_worth_needed": 2537895
        },
        {
          "year": 2075,
          "age_client": 86,
          "age_co_client": null,
          "net_worth": 2573241,
          "net_worth_todays_dollars": 591262,
          "total_debts": 0,
          "investable_assets": -38276,
          "net_worth_needed": 2573241
        },
        {
          "year": 2076,
          "age_client": 87,
          "age_co_client": null,
          "net_worth": 2615271,
          "net_worth_todays_dollars": 583181,
          "total_debts": 0,
          "investable_assets": -75495,
          "net_worth_needed": 2615271
        },
        {
          "year": 2077,
          "age_client": 88,
          "age_co_client": null,
          "net_worth": 2664646,
          "net_worth_todays_dollars": 576652,
          "total_debts": 0,
          "investable_assets": -107780,
          "net_worth_needed": 2664646
        },
        {
          "year": 2078,
          "age_client": 89,
          "age_co_client": null,
          "net_worth": 2722081,
          "net_worth_todays_dollars": 571693,
          "total_debts": 0,
          "investable_assets": -134488,
          "net_worth_needed": 2722081
        },
        {
          "year": 2079,
          "age_client": 90,
          "age_co_client": null,
          "net_worth": 2788353,
          "net_worth_todays_dollars": 568325,
          "total_debts": 0,
          "investable_assets": -154919,
          "net_worth_needed": 2788353
        },
        {
          "year": 2080,
          "age_client": 90,
          "age_co_client": null,
          "net_worth": 2812003,
          "net_worth_todays_dollars": 567450,
          "total_debts": 0,
          "investable_assets": -160752,
          "net_worth_needed": 2812003
        }
      ],
      "firstNegativeInvestableYear": 2075,
      "firstNegativeNetWorthYear": null,
      "peakInvestable": 1949763,
      "endOfPlan": {
        "year": 2080,
        "age_client": 90,
        "age_co_client": null,
        "net_worth": 2812003,
        "net_worth_todays_dollars": 567450,
        "total_debts": 0,
        "investable_assets": -160752,
        "net_worth_needed": 2812003
      }
    },
    "goals": {
      "goalsSummary": [
        {
          "amount": 3500,
          "goalType": "VACATION",
          "value": "Going on a $3,500 vacation every year."
        },
        {
          "amount": 550000,
          "goalType": "PURCHASE",
          "subType": "REAL_ESTATE_PURCHASE",
          "value": "Plan to purchase a home for $550,000 in 2027."
        }
      ],
      "chartGoals": [
        {
          "date": "2027-01-01T00:00:00.000Z",
          "goalType": "VACATION",
          "name": "Take a vacation",
          "termDate": "2047-04-01T00:00:00.000Z"
        },
        {
          "date": "2027-01-01T00:00:00.000Z",
          "goalType": "PURCHASE",
          "name": "Purchase a home",
          "subType": "REAL_ESTATE_PURCHASE",
          "termDate": "2027-01-01T00:00:00.000Z"
        },
        {
          "date": "2047-04-01T00:00:00.000Z",
          "goalType": "RETIREMENT",
          "name": "Michael's Retirement"
        },
        {
          "date": "2075-01-01T00:00:00.000Z",
          "goalType": "BANKRUPTCY_ZEROCASH"
        }
      ]
    },
    "facts": {
      "facts": {
        "cash": {
          "monthsCovered": {
            "unit": "months",
            "basis": "n/a",
            "label": "Months of essential expenses accessible cash covers",
            "value": "3.2",
            "period": "today, before near-term goals",
            "replaces": [
              "ratios.emergencyFund.emergencyFundMonths (capped at \"+12\")",
              "savingsAndExpenses.liquidityContext.emergencyFundInMonths",
              "protection.emergencyFund.emergencyFundCoverageEvaluation.monthsCovered"
            ],
            "notToBeConfusedWith": [
              "the recommended number of months"
            ]
          },
          "nearTermGoals": [
            {
              "note": "A goal payment, not a down payment unless the goal is a purchase.",
              "unit": "USD",
              "basis": "as entered",
              "label": "Take a vacation: cash to hold for its next payment",
              "value": 3500,
              "period": "next payment January 2027, then every year",
              "replaces": [
                "extraCashOutflows[].downpayment (holds any goal payment)"
              ]
            },
            {
              "note": "A goal payment, not a down payment unless the goal is a purchase.",
              "unit": "USD",
              "basis": "as entered",
              "label": "Purchase a home: cash to hold for its next payment",
              "value": 113300,
              "period": "next payment January 2027",
              "replaces": [
                "extraCashOutflows[].downpayment (holds any goal payment)"
              ]
            }
          ],
          "accessibleCash": {
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Accessible cash (bank accounts plus taxable money market)",
            "value": 30000,
            "period": "balance today",
            "notToBeConfusedWith": [
              "bank cash alone (excludes money market)",
              "cash inside retirement accounts, which is not accessible"
            ]
          },
          "totalCashNeeded": {
            "max": 172636,
            "min": 163330,
            "note": "Never call this the emergency reserve.",
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Cash target: emergency reserve plus near-term goals",
            "period": "target balance today",
            "replaces": [
              "ratios.emergencyFund.adjustedRecommendedMin/MaxAmount",
              "savingsAndExpenses.liquidityContext.min/maxEmergencyFundTargetAndShortTermNeeds",
              "cashNeeds.cashTarget"
            ],
            "notToBeConfusedWith": [
              "emergencyReserve"
            ]
          },
          "emergencyReserve": {
            "max": 55836,
            "min": 46530,
            "note": "Excludes near-term goals. This alone is the emergency reserve.",
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Recommended emergency reserve (5–6 months of essential expenses)",
            "period": "target balance today",
            "replaces": [
              "ratios.emergencyFund.min/maxRecommendedEmergencyFund",
              "savingsAndExpenses.liquidityContext.min/maxEmergencyFundTargetInCash",
              "protection.emergencyFund.recommendedEmergencyFundLevels.minimum/maximumAmountRecommended",
              "cashNeeds.emergencyFund"
            ],
            "notToBeConfusedWith": [
              "totalCashNeeded"
            ]
          },
          "monthsCoveredAfterNearTermGoals": {
            "unit": "months",
            "basis": "n/a",
            "label": "Months of essential expenses covered after setting aside near-term goals",
            "value": "0",
            "period": "today",
            "replaces": [
              "ratios.emergencyFund.adjustedMonthsCoveredAfterShortTermCashNeeds"
            ]
          }
        },
        "rules": [
          "These facts are the only figures to quote for these concepts. Quote the label's meaning with the number; never relabel a fact as another one.",
          "Each fact names the facts it must not be confused with. Never call one by the other's name.",
          "Keep the unit: a USD/yr figure is always said per year, a lump sum never is.",
          "Do not add, subtract or compare two facts unless a fact says how they relate.",
          "Never quote a date that is before the plan date.",
          "Write a date as month and year (August 2039), never as an ISO date (2039-08-01).",
          "Write a ratio or rate as a percentage (55%), never as a decimal (0.551).",
          "A fact's `replaces` lists key-metric fields that hold the same or a confusable figure under a misleading name. When you see one of those fields in your other inputs, quote the fact with its label instead. Field names are never labels."
        ],
        "retirement": {
          "spendingGap": {
            "note": "Savings, cash and required IRA withdrawals included, pay this each year on average. It is what the plan asks of savings.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Yearly retirement spending that income does not cover, paid from savings",
            "value": 59612.79,
            "period": "average over the 33 years of retirement",
            "notToBeConfusedWith": [
              "averagePortfolioDraw"
            ]
          },
          "spendingNeed": {
            "note": "Includes taxes, debt payments and goals after retirement; do not add those on top. annualTotalIncomeNeeded adds an estimated long-term care cost: do not quote it.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Yearly retirement spending need (excluding estimated long-term care)",
            "value": 89648.57,
            "period": "average over the 33 years of retirement",
            "replaces": [
              "retirementAndOtherGoals.incomeNeedsAndWithdrawals.annualTotalIncomeNeeded (adds estimated long-term care)"
            ]
          },
          "savingsRunOut": {
            "note": "Never write a negative balance or a debt. Say when savings run out and how much planned spending would go unpaid. Net worth stays positive only because it includes the home.",
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Savings and investments run out at age 85",
            "value": 32439.08,
            "period": "planned spending left unpaid by the end of the plan",
            "replaces": [
              "assetDepletion.liquidAssetsAtEndOfPlan",
              "capacity.liquidAssetsAtEndOfPlan"
            ]
          },
          "guaranteedIncome": {
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Guaranteed income in retirement (Social Security, annuities, pensions)",
            "value": 30035.78,
            "period": "average over the 33 years of retirement; years before a benefit starts count as zero"
          },
          "incomeShareOfNeed": {
            "unit": "percent",
            "basis": "today's dollars at the plan date",
            "label": "Share of the yearly retirement spending need that income covers (guaranteed and other income)",
            "value": "34%",
            "period": "average over the 33 years of retirement",
            "replaces": [
              "retirementAndOtherGoals.incomeVsIncomeNeeds.allIncomesVsIncomeNeededExLtcCosts",
              "ratios.guaranteedIncomeRatio.allIncomesVsIncomeNeededExLtcCosts"
            ]
          },
          "netCashFlowThisYear": {
            "note": "The outflow table counts the employer 401(k) match of 7000 as household savings; the employer pays it, so this figure does not subtract it. Income 180000 minus outflows 195336 is -15336: never present that subtraction as this figure.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Net cash flow this year",
            "value": -8336,
            "period": "the plan year",
            "notToBeConfusedWith": [
              "averagePortfolioDraw",
              "withdrawalRateThisYear",
              "savingsCapacity"
            ]
          },
          "averagePortfolioDraw": {
            "note": "Counts only the months when spending exceeds every inflow. Required IRA withdrawals and other inflows drawn from savings are not in it, so savings pay more than this. Draws are concentrated in fewer years and are larger in those years. It is not the spending gap: never present it as filling that gap, and never use it to say the plan leans little on savings.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Average yearly draw from savings in retirement",
            "value": 59612.79,
            "period": "average over the 33 years of retirement, counting years with no draw as zero",
            "replaces": [
              "retirementAndOtherGoals.withdrawals.supplementalAnnualWithdrawals"
            ],
            "notToBeConfusedWith": [
              "spendingGap"
            ]
          },
          "withdrawalRateAverage": {
            "note": "A lifetime average. Do not compare it with the 4% sustainable rate.",
            "unit": "percent",
            "basis": "today's dollars at the plan date",
            "label": "Average yearly draw as a share of savings at the start of retirement",
            "value": "5.6%",
            "period": "average over the 33 years of retirement",
            "replaces": [
              "retirementAndOtherGoals.withdrawals.withdrawalRatio"
            ],
            "notToBeConfusedWith": [
              "withdrawalRateThisYear"
            ]
          }
        }
      },
      "ratios": {
        "umbrella": {
          "claim": "No coverage",
          "color": "R",
          "currentCoverage": 0,
          "recommendedCoverage": 1000000
        },
        "currentDPD": {
          "debtLastPayment": "2030-07-01T00:00:00.000Z",
          "beforeRetirement": true,
          "yearsInRetirement": 0,
          "avgDTIInRetirement": 0,
          "howMuchInRetirement": "Less than 5 years",
          "avgDTIInRetirementLevel": "<10%"
        },
        "vehiclePRI": {
          "vehiclesPri": 0.0333,
          "monthlyGrossIncome": 15000,
          "doTheyHaveAnyVehicle": true,
          "vehiclesMonthlyPayments": 500,
          "doTheyHaveAnyVehicleLoan": true,
          "vehiclesPriFirstThreshold": 0.1,
          "vehiclesPriSecondThreshold": 0.15
        },
        "debtToIncome": {
          "ratio": 0.2537,
          "debtOnlyDti": 0.0633,
          "grossIncome": 180000,
          "rentalPayment": 33600,
          "mortgagesPayments": 0,
          "monthlyDebtPayments": 950,
          "otherHousingExpenses": 672,
          "totalMonthlyObligations": 3806,
          "debtPaymentExcludingMortgages": 11400
        },
        "housingRatio": {
          "ratio": 0.1904,
          "grossIncome": 180000,
          "rentalPayment": 33600,
          "housingExpenses": 34272,
          "mortgagePayment": 0,
          "otherHousingExpenses": 672
        },
        "indebtedness": {
          "debt": true,
          "housing": "rent",
          "debtBalance": 28500,
          "monthlyDebtPayment": 950,
          "totalMonthlyObligations": 3806
        },
        "savingsLevel": {
          "ratio": 0.2389,
          "grossIncome": 180000,
          "savingAmount": 43000
        },
        "emergencyFund": {
          "claim": "Not enough",
          "color": "Y",
          "nrOfEarners": 1,
          "emergencyFund": 30000,
          "incomeDisparity": "",
          "monthlyExpenses": 9306,
          "totalCashAmount": 27000,
          "inaccessibleCash": 3500,
          "excessOverBaseMax": "Not applicable",
          "extraCashOutflows": [
            {
              "amount": 0,
              "description": "Take a vacation",
              "downpayment": 3500
            },
            {
              "amount": 566500,
              "description": "Purchase a home",
              "downpayment": 113300
            }
          ],
          "shortfallToBaseMin": 16530,
          "emergencyFundMonths": "3",
          "highestEarningsLevel": "High",
          "shortTermGoalsNeeded": [
            {
              "date": "2027-01-01T00:00:00.000Z",
              "amount": 3500,
              "description": "Take a vacation",
              "paymentFrequency": "ANNUAL"
            },
            {
              "date": "2027-01-01T00:00:00.000Z",
              "amount": 113300,
              "description": "Purchase a home",
              "paymentFrequency": "ONE_TIME"
            }
          ],
          "excessOverAdjustedMax": "Not applicable",
          "maxRecommendedEFMonths": 6,
          "minRecommendedEFMonths": 5,
          "shortfallToAdjustedMin": 133330,
          "totalMoneyMarketAmount": 3000,
          "deltaToMaxEmergencyFund": "Not applicable",
          "moneyMarketFundAccounts": [
            {
              "accountName": "Taxable Brokerage",
              "accountType": "Brokerage account",
              "cashBalance": 3000
            }
          ],
          "extraEmergencyFundNeeded": 116800,
          "maxRecommendedEmergencyFund": 55836,
          "maximumEmergencyFundPlusStg": 172636,
          "minRecommendedEmergencyFund": 46530,
          "adjustedRecommendedMaxAmount": 172636,
          "adjustedRecommendedMinAmount": 163330,
          "deltaToMaxEmergencyFundPlusStg": "Not applicable",
          "extraCashAboveMaxEmergencyFund": "Not applicable",
          "extraCashAboveMinEmergencyFund": "Not applicable",
          "cashReservesAfterShortTermCashNeeds": -86800,
          "extraCashAboveMaxEmergencyFundPlusStg": "Not applicable",
          "adjustedMonthsCoveredAfterShortTermCashNeeds": 0
        },
        "lifeInsurance": {
          "scenario": {
            "kids": false,
            "earners": 1,
            "spouses": 1,
            "scenario": 20,
            "debtBurden": "Low",
            "incomeDisparity": ""
          },
          "clientEarner": {
            "overInsured": 12,
            "isHighEarner": true,
            "underInsured": -1,
            "adequatelyInsured": 5,
            "slightlyOverInsured": 10,
            "slightlyUnderInsured": 0
          },
          "clientCoverage": 180000,
          "coClientCoverage": 0,
          "clientCoverageKey": "Slightly under insured",
          "clientEarnedIncome": 180000,
          "clientCoverageColor": "Y",
          "coClientCoverageKey": "",
          "coClientEarnedIncome": 0,
          "clientReplacementValue": 0,
          "clientCoverageOverIncome": 1,
          "coClientReplacementValue": 0,
          "coClientCoverageOverIncome": 0,
          "recommendedClientMaxCoverage": 1800000,
          "recommendedClientMinCoverage": 900000,
          "recommendedCoClientMaxCoverage": 0,
          "recommendedCoClientMinCoverage": 0,
          "lifeInsuranceCoverageGapsAndExcess": {
            "clientExcess": 0,
            "clientShortfall": 720000
          }
        },
        "creditCardDebt": {
          "balance": 3500,
          "hasDebt": true,
          "ccPayoffDate": "2028-07-01T00:00:00.000Z",
          "monthlyPayment": 200,
          "retirementDate": "2047-04-01T00:00:00.000Z",
          "yearsInRetirement": "Not applicable",
          "maxCCPaymentNormal": 130.07,
          "minCCPaymentNormal": 92.73,
          "yearsToCcPayoffDate": 1,
          "paymentsEqualToInterest": 58.33,
          "percentageOfCCOverGrossIncome": 0.0194
        },
        "educationSavings": {
          "totalGAP": 0,
          "savingsIncrease": 0,
          "expectedPerformance": 0,
          "totalRequiredSavings": 0,
          "current529AccountsBalance": 0,
          "totalEducationGoalsAmount": 0,
          "totalRequiredExtraSavings": 0,
          "annualSavingsGoingTo529Accounts": 0,
          "doTheyHaveEducationFundingGoals": false,
          "totalEducationGoalRequiredAmountAtToday": 0
        },
        "incomePercentile": {
          "state": "TX",
          "hasSpouse": false,
          "percentile": 0.9,
          "grossIncome": 180000
        },
        "realEstateEquity": {
          "ratio": 0,
          "realEstateAssets": 0,
          "realEstateEquity": 0,
          "realEstateMortgages": 0,
          "realEstateEquityThreshold1": 0.2,
          "realEstateEquityThreshold2": 0.5
        },
        "retirementSavings": {
          "generalInflation": 0.03,
          "yearsToRetirement": 20,
          "averagePerformance": 0.0776,
          "requiredExtraSavings": 20231.12,
          "planningGapAtRetirementAge": 4180127.36,
          "supplementalTotalWithdrawals": 5606298.21,
          "planningGapAtRetirementAgeInTodaysDollars": 1177585.95,
          "balanceInRetirementAccountsAtRetirementAge": 1426170.85,
          "supplementalTotalWithdrawalsInTodaysDollars": 1967222.17,
          "balanceInRetirementAccountsAtRetirementAgeInTodaysDollars": 789636.22
        },
        "withdrawalRateRatio": {
          "withdrawalRate": 0.0862,
          "withdrawalRateToday": 0.8412,
          "annualWithdrawalsToday": 144693.29,
          "annualWithdrawalsOnAverage": 169887.82,
          "withdrawalRateAtTodaysValue": 0.0559,
          "totalWithdrawalsDuringRetirement": 5606298.21,
          "investableAssetsAtFirstInRetireYrs": 1971752.82,
          "investableAssetsAt2050YrsAtTodaysValue": 1066828.66,
          "annualWithdrawalsOnAverageAtTodaysValue": 59612.79,
          "totalWithdrawalsDuringRetirementAtTodaysValue": 1967222.17
        },
        "investableAssetLevel": {
          "basis": "income",
          "ratio": 0.9556,
          "cashBalance": 27000,
          "grossIncome": 180000,
          "annualExpenses": 111672,
          "investableAssets": 145000,
          "portfolioSustainabilityMultiple": 0.9556
        },
        "guaranteedIncomeRatio": {
          "inflowsSummary": {
            "name": "All inflows",
            "total": 3501038.36,
            "guaranteedIncome": {
              "name": "Guaranteed income",
              "total": 3501038.36,
              "ANNUITY_INCOME": {
                "name": "Annuity income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "SOCIAL_SECURITY": {
                "name": "Social security",
                "total": 3501038.36,
                "totalAtTodaysValue": 991180.76,
                "yearlyAverageTotal": 106092.07,
                "yearlyAverageTotalAtTodaysValue": 30035.78
              },
              "totalAtTodaysValue": 991180.76,
              "yearlyAverageTotal": 106092.07,
              "PENSION_AND_DEFINED_BENEFIT": {
                "name": "Pension / defined benefit",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "yearlyAverageTotalAtTodaysValue": 30035.78
            },
            "otherIncomeSources": {
              "name": "Other income sources",
              "total": 0,
              "STOCK_COMP": {
                "name": "Stock compensation",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "OTHER_INFLOW": {
                "name": "Other income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "DEFERRED_COMP": {
                "name": "Deferred compensation",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "EARNED_INCOME": {
                "name": "Earned income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "RENTAL_INCOME": {
                "name": "Rental income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "ROYALTY_AND_IP": {
                "name": "Royalty & IP",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "SUPPORT_TRANSFER": {
                "name": "Support & transfer",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "GOVERNMENT_BENEFIT": {
                "name": "Government benefit",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "totalAtTodaysValue": 0,
              "yearlyAverageTotal": 0,
              "BUSINESS_PASSIVE_INCOME": {
                "name": "Business passive income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "PROPERTY_LIQUIDATION_EVENT": {
                "name": "Property liquidation event",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "yearlyAverageTotalAtTodaysValue": 0
            },
            "totalAtTodaysValue": 991180.76,
            "yearlyAverageTotal": 106092.07,
            "yearlyAverageTotalAtTodaysValue": 30035.78
          },
          "outflowsSummary": {
            "name": "Outflows",
            "total": 10879432.82,
            "ltcCosts": {
              "name": "LTC Costs",
              "total": 1772096.24,
              "totalAtTodaysValue": 378738.68,
              "yearlyAverageTotal": 53699.89,
              "yearlyAverageTotalAtTodaysValue": 189369.34
            },
            "excludingLtcCosts": {
              "name": "Excluding LTC Costs",
              "total": 9107336.57,
              "totalAtTodaysValue": 2958402.93,
              "yearlyAverageTotal": 275979.9,
              "yearlyAverageTotalAtTodaysValue": 89648.57
            },
            "totalAtTodaysValue": 3337141.61,
            "yearlyAverageTotal": 329679.78,
            "yearlyAverageTotalAtTodaysValue": 101125.5
          },
          "ltcCostsAreEstimated": true,
          "allIncomesVsIncomeNeeded": 0.297,
          "otherIncomeVsIncomeNeeded": 0,
          "guaranteedIncomeVsIncomeNeeded": 0.297,
          "allIncomesVsIncomeNeededExLtcCosts": 0.335,
          "otherIncomeVsIncomeNeededExLtcCosts": 0,
          "guaranteedIncomeVsIncomeNeededExLtcCosts": 0.335
        }
      },
      "protection": {
        "emergencyFund": {
          "clientProfile": {
            "clientAge": 37,
            "clientName": "Michael",
            "numberOfChildren": 0,
            "clientRiskProfile": "(4) Growth",
            "clientIncomeAtRisk": 180000
          },
          "cashAccountList": [
            {
              "name": "Checking account",
              "type": "Checking account",
              "owner": "Michael",
              "value": 12000
            },
            {
              "name": "Savings account",
              "type": "Savings account",
              "owner": "Michael",
              "value": 15000
            }
          ],
          "extraCashOutflows": [
            {
              "amount": 0,
              "description": "Take a vacation",
              "downpayment": 3500
            },
            {
              "amount": 566500,
              "description": "Purchase a home",
              "downpayment": 113300
            }
          ],
          "realEstateDetails": [
            [
              "Real estate",
              "Market value",
              "Mortgage balance",
              "Equity",
              "HELOC"
            ]
          ],
          "cashAndExpensesOverview": {
            "cashReserves": 30000,
            "livingExpenses": 5500,
            "housingExpenses": 2856,
            "monthlyExpenses": 9306,
            "totalCashAmount": 30000,
            "otherDebtPayment": 950,
            "totalMoneyMarketAmount": 3000,
            "cashReservesAfterShortTermCashNeeds": -86800
          },
          "otherAccountsContributions": [
            [
              "Account",
              "Holder",
              "Current contribution"
            ],
            [
              "Checking account",
              "Michael",
              0
            ],
            [
              "Savings account",
              "Michael",
              3000
            ],
            [
              "Taxable Brokerage",
              "Michael",
              12000
            ]
          ],
          "retirementAndEducationGaps": {
            "educationGap": 0,
            "retirementGap": 1177585.95
          },
          "recommendedEmergencyFundLevels": {
            "maximumAmountRecommended": 55836,
            "maximumMonthsRecommended": 6,
            "minimumAmountRecommended": 46530,
            "minimumMonthsRecommended": 5,
            "extraEmergencyFundNeededByShortTermCashNeeds": 116800,
            "maximumAmountAdjustedAfterShortTermCashNeeds": 172636,
            "minimumAmountAdjustedAfterShortTermCashNeeds": 163330
          },
          "emergencyFundCoverageEvaluation": {
            "monthsCovered": 3,
            "emergencyFundExcess": "Not applicable",
            "emergencyFundShortfall": 16530,
            "adjustedMonthsCoveredAfterShortTermCashNeeds": 0,
            "adjustedEmergencyFundExcessAfterShortTermCashNeeds": "Not applicable",
            "adjustedEmergencyFundShortfallAfterShortTermCashNeeds": 133330
          },
          "taxAdvantagedAccountsContributions": [
            [
              "Account",
              "Holder",
              "Current contribution",
              "Max contribution"
            ],
            [
              "401(k) - Michael",
              "Michael",
              24000,
              24500
            ],
            [
              "HSA",
              "Michael",
              4000,
              4400
            ]
          ]
        },
        "lifeInsurance": {
          "legacyGoal": {
            "amount": "Not applicable",
            "hasLegacyGoal": false
          },
          "educationGoal": [
            [
              "Kid name",
              "Total cost",
              "Inception Year"
            ]
          ],
          "clientDemographics": {
            "clientAge": 37,
            "clientName": "Michael",
            "numberOfChildren": 0,
            "clientRiskProfile": "(4) Growth",
            "clientIncomeAtRisk": 180000
          },
          "lifeInsuranceCoverageBasics": {
            "hasLifeInsuranceClient": true,
            "lifeInsuranceAmountClient": 180000
          },
          "lifeInsuranceCoverageGapsAndExcess": {
            "clientExcess": 0,
            "clientShortfall": 720000
          },
          "lifeInsuranceCoverageRecommendations": {
            "clientMaxRecommendedCoverage": 1800000,
            "clientMinRecommendedCoverage": 900000
          }
        },
        "umbrellaInsurance": {
          "assetExposed": {
            "netWorth": 218500,
            "totalLiquidAssets": 172000,
            "assetExposedSummary": [
              [
                "Asset",
                "Number",
                "Value",
                "Equity"
              ],
              [
                "Vehicle",
                1,
                40000,
                25000
              ],
              [
                "Other asset",
                1,
                35000,
                35000
              ],
              [
                "Total",
                2,
                75000,
                60000
              ]
            ]
          },
          "umbrellaCoverage": {
            "claim": "No coverage",
            "hasUmbrellaPolicy": false,
            "umbrellaCoverageAmount": "Not applicable"
          },
          "clientDemographics": {
            "clientAge": 37,
            "clientName": "Michael",
            "numberOfChildren": 0,
            "clientRiskProfile": "(4) Growth",
            "clientIncomeAtRisk": 180000
          },
          "assetInsuranceStatus": [
            {
              "assetName": "BMW 3 Series",
              "assetType": "Vehicle",
              "isInsured": false,
              "equityAmount": 25000
            }
          ],
          "coverageRecommendationsAndAnalysis": {
            "umbrellaCoverageGap": 1000000,
            "umbrellaCoverageExcess": "Not applicable",
            "umbrellaMinRecommendedCoverage": 1000000
          }
        }
      },
      "debtManagement": {
        "realEstate": {
          "realEstateEquity": 0,
          "realEstateEquityThreshold1": 0.2,
          "realEstateEquityThreshold2": 0.5,
          "percentageOfRealEstateEquity": 0
        },
        "listOfDebts": [
          [
            "Name",
            "Type",
            "Balance",
            "Interest rate",
            "Monthly payments",
            "Interest paid"
          ],
          [
            "BMW 3 Series loan",
            "Vehicle loan",
            15000,
            0.05,
            500,
            62.5
          ],
          [
            "Student loan - Michael",
            "Student loan",
            10000,
            0.058,
            250,
            48.33
          ],
          [
            "Amex Platinum",
            "Credit card",
            3500,
            0.2,
            200,
            58.33
          ]
        ],
        "debtOverview": {
          "debt": true,
          "debtBalance": 28500,
          "beforeRetirement": true,
          "avgDtiInRetirement": 0,
          "percentageOfDebtOverGrossIncome": 0.1583
        },
        "clientProfile": {
          "clientName": "Michael"
        },
        "creditCardDebt": {
          "ccPayoffDate": "2028-07-01T00:00:00.000Z",
          "retirementDate": "2047-04-01T00:00:00.000Z",
          "ccMonthlyPayment": 200,
          "creditCardBalance": 3500,
          "yearsInRetirement": "Not applicable",
          "maxCcPaymentNormal": 130.07,
          "minCcPaymentNormal": 92.73,
          "yearsToCcPayoffDate": 1,
          "ccPaymentEqualToInterestRate": 58.33
        },
        "vehiclePayment": {
          "vehiclesPri": 0.0333,
          "doTheyHaveAnyVehicle": true,
          "vehiclesMonthlyPayments": 500
        },
        "housingExpenses": {
          "rentVsOwn": "Rent",
          "housingRatio": 0.1904,
          "rentalPayment": 2800,
          "housingExpenses": 2856,
          "mortgagePayment": 0,
          "otherHousingExpenses": 56,
          "housingRatioFirstThreshold": 0.28,
          "housingRatioSecondThreshold": 0.32
        },
        "savingsAndCashflow": {
          "annualCashFlow": -8336,
          "annualSavingsRate": 0.2389,
          "annualSavingsAmount": 43000
        },
        "debtToIncomeAndMonthlyObligations": {
          "dti": 0.2537,
          "debtOnlyDti": 0.0633,
          "grossIncome": 180000,
          "dtiFirstThreshold": 0.36,
          "dtiThirdThreshold": 0.5,
          "dtiSecondThreshold": 0.43,
          "monthlyGrossIncome": 15000,
          "monthlyDebtPayments": 950,
          "totalMonthlyObligations": 3806,
          "percentageOfDebtOverGrossIncome": 0.1583
        }
      },
      "cashflowStatement": {
        "inflows": {
          "items": [
            {
              "name": "Earned income",
              "items": [
                {
                  "name": "Salary and wages",
                  "joint": 0,
                  "total": 180000,
                  "client": 180000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "total": 180000,
              "client": 180000,
              "coClient": 0
            }
          ],
          "joint": 0,
          "total": 180000,
          "client": 180000,
          "coClient": 0
        },
        "outflows": {
          "items": [
            {
              "name": "Expenses",
              "items": [
                {
                  "name": "Living Expenses",
                  "joint": 0,
                  "total": 66000,
                  "client": 66000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "total": 66000,
              "client": 66000,
              "coClient": 0
            },
            {
              "name": "Taxes",
              "items": [
                {
                  "name": "Federal Income Tax",
                  "joint": 0,
                  "total": 26894,
                  "client": 26894,
                  "coClient": 0
                },
                {
                  "name": "FICA tax",
                  "joint": 0,
                  "total": 13770,
                  "client": 13770,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "total": 40664,
              "client": 40664,
              "coClient": 0
            },
            {
              "name": "Savings",
              "items": [
                {
                  "name": "401k - Traditional savings",
                  "joint": 0,
                  "total": 17000,
                  "client": 17000,
                  "coClient": 0
                },
                {
                  "name": "Brokerage account savings",
                  "joint": 0,
                  "total": 12000,
                  "client": 12000,
                  "coClient": 0
                },
                {
                  "name": "HSA savings",
                  "joint": 0,
                  "total": 4000,
                  "client": 4000,
                  "coClient": 0
                },
                {
                  "name": "Cash savings",
                  "joint": 0,
                  "total": 3000,
                  "client": 3000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "total": 36000,
              "client": 36000,
              "coClient": 0
            },
            {
              "name": "Housing Expenses",
              "items": [
                {
                  "name": "Rent",
                  "joint": 0,
                  "total": 33600,
                  "client": 33600,
                  "coClient": 0
                },
                {
                  "name": "Renter insurance",
                  "joint": 0,
                  "total": 672,
                  "client": 672,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "total": 34272,
              "client": 34272,
              "coClient": 0
            },
            {
              "name": "Debt Payments",
              "items": [
                {
                  "name": "Car loan payments",
                  "joint": 0,
                  "total": 6000,
                  "client": 6000,
                  "coClient": 0
                },
                {
                  "name": "Student loan payments",
                  "joint": 0,
                  "total": 3000,
                  "client": 3000,
                  "coClient": 0
                },
                {
                  "name": "Credit card payments",
                  "joint": 0,
                  "total": 2400,
                  "client": 2400,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "total": 11400,
              "client": 11400,
              "coClient": 0
            }
          ],
          "joint": 0,
          "total": 188336,
          "client": 188336,
          "coClient": 0
        },
        "freeCashflow": {
          "joint": 0,
          "total": -8336,
          "client": -8336,
          "coClient": 0
        }
      },
      "netWorthStatement": {
        "assets": {
          "name": "Assets",
          "type": "MAIN",
          "items": [
            {
              "name": "Cash account",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Savings account",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 15000,
                  "client": 15000,
                  "coClient": 0,
                  "annualSavings": 3000,
                  "clientSavings": 3000,
                  "annualMatching": 0,
                  "portfolioTypeName": "Savings account"
                },
                {
                  "name": "Checking account",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 12000,
                  "client": 12000,
                  "coClient": 0,
                  "annualSavings": 0,
                  "clientSavings": 0,
                  "annualMatching": 0,
                  "portfolioTypeName": "Checking account"
                }
              ],
              "joint": 0,
              "order": 1,
              "total": 27000,
              "client": 27000,
              "coClient": 0,
              "totalDebts": 0
            },
            {
              "name": "Investment account",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Taxable",
                  "type": "INDIVIDUAL",
                  "items": [
                    {
                      "name": "Taxable Brokerage",
                      "type": "PORTFOLIO",
                      "joint": 0,
                      "total": 60000,
                      "client": 60000,
                      "coClient": 0,
                      "annualSavings": 12000,
                      "clientSavings": 12000,
                      "annualMatching": 0,
                      "portfolioTypeName": "Brokerage account"
                    }
                  ],
                  "joint": 0,
                  "total": 60000,
                  "client": 60000,
                  "coClient": 0
                },
                {
                  "name": "Tax-free",
                  "type": "INDIVIDUAL",
                  "items": [
                    {
                      "name": "HSA",
                      "type": "PORTFOLIO",
                      "joint": 0,
                      "total": 5000,
                      "client": 5000,
                      "coClient": 0,
                      "annualSavings": 4000,
                      "clientSavings": 4000,
                      "annualMatching": 0,
                      "portfolioTypeName": "HSA"
                    }
                  ],
                  "joint": 0,
                  "total": 5000,
                  "client": 5000,
                  "coClient": 0
                },
                {
                  "name": "Tax-deferred",
                  "type": "INDIVIDUAL",
                  "items": [
                    {
                      "name": "401(k) - Michael",
                      "type": "PORTFOLIO",
                      "joint": 0,
                      "total": 80000,
                      "client": 80000,
                      "coClient": 0,
                      "annualSavings": 24000,
                      "clientSavings": 17000,
                      "annualMatching": 7000,
                      "portfolioTypeName": "401k - Traditional"
                    }
                  ],
                  "joint": 0,
                  "total": 80000,
                  "client": 80000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 2,
              "total": 145000,
              "client": 145000,
              "coClient": 0,
              "totalDebts": 0
            },
            {
              "name": "Stock compensation",
              "type": "CATEGORY",
              "joint": 0,
              "order": 3,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Annuity",
              "type": "CATEGORY",
              "joint": 0,
              "order": 4,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Insurance (Cash value)",
              "type": "CATEGORY",
              "joint": 0,
              "order": 5,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Business",
              "type": "CATEGORY",
              "joint": 0,
              "order": 6,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Real estate",
              "type": "CATEGORY",
              "joint": 0,
              "order": 7,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "totalDebts": 0
            },
            {
              "name": "Vehicle",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "BMW 3 Series",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 40000,
                  "client": 40000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 8,
              "total": 40000,
              "client": 40000,
              "coClient": 0,
              "totalDebts": 15000
            },
            {
              "name": "Other asset",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "RSUs",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 35000,
                  "client": 35000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 9,
              "total": 35000,
              "client": 35000,
              "coClient": 0,
              "totalDebts": 0
            }
          ],
          "joint": 0,
          "total": 247000,
          "client": 247000,
          "coClient": 0,
          "totalDebts": 15000
        },
        "netWorth": {
          "joint": 0,
          "total": 218500,
          "client": 218500,
          "coClient": 0
        },
        "liabilities": {
          "name": "Liabilities",
          "type": "MAIN",
          "items": [
            {
              "name": "Credit card",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Amex Platinum",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 3500,
                  "client": 3500,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 1,
              "total": 3500,
              "client": 3500,
              "coClient": 0
            },
            {
              "name": "Student loan",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Student loan - Michael",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 10000,
                  "client": 10000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 2,
              "total": 10000,
              "client": 10000,
              "coClient": 0
            },
            {
              "name": "Business loan",
              "type": "CATEGORY",
              "joint": 0,
              "order": 3,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true
            },
            {
              "name": "Personal loan",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "BMW 3 Series loan",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 15000,
                  "client": 15000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 4,
              "total": 15000,
              "client": 15000,
              "coClient": 0
            },
            {
              "name": "Investment loan",
              "type": "CATEGORY",
              "joint": 0,
              "order": 5,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true
            },
            {
              "name": "Real estate debt",
              "type": "CATEGORY",
              "joint": 0,
              "order": 6,
              "total": 0,
              "client": 0,
              "coClient": 0
            },
            {
              "name": "Other debt",
              "type": "CATEGORY",
              "joint": 0,
              "order": 7,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true
            }
          ],
          "joint": 0,
          "total": 28500,
          "client": 28500,
          "coClient": 0
        }
      },
      "savingsAndExpenses": {
        "goals": {
          "clientRetirementAge": 58,
          "shortTermGoalsCashNeeds": 116800,
          "doTheyHaveEducationFundingGoals": false,
          "totalEducationGoalRequiredAmount": "Not applicable"
        },
        "annualSavings": {
          "currentAnnualSavingsAtHSA": 4000,
          "currentAnnualSavingsAtHSARate": 0.0222,
          "currentAnnualSavingsAt529Accounts": 0,
          "requiredRetirementExtraAnnualSavings": 20231.12,
          "currentAnnualSavingsAt529AccountsRate": 0,
          "currentAnnualSavingsAtTaxableAccounts": 12000,
          "gapInRetirementAccountsAtRetirementAge": 1177585.95,
          "requiredAnnualSavingsAtTaxableAccounts": 54000,
          "requiredExtraAnnualSavingsForEducation": "Not applicable",
          "currentAnnualSavingsAtRetirementAccounts": 24000,
          "requiredRetirementExtraAnnualSavingsRate": 0.1124,
          "currentAnnualSavingsAtTaxableAccountsRate": 0.0667,
          "requiredAnnualSavingsAtTaxableAccountsRate": 0.3,
          "requiredExtraAnnualSavingsForEducationRate": "Not applicable",
          "currentAnnualSavingsAtRetirementAccountsRate": 0.1333
        },
        "clientProfile": {
          "clientAge": 37,
          "clientName": "Michael",
          "numberOfChildren": 0,
          "stateOfResidence": "Texas",
          "clientRiskProfile": "(4) Growth",
          "maximumAgeOfChildren": "Not applicable",
          "minimumAgeOfChildren": "Not applicable"
        },
        "otherExpenses": {
          "lifeInsuranceGap": 720000,
          "umbrellaInsuranceGap": 1000000
        },
        "liquidityContext": {
          "shortTermNeeds": 116800,
          "emergencyFundInCash": 30000,
          "emergencyFundInMonths": "3",
          "maxEmergencyFundTargetInCash": 55836,
          "minEmergencyFundTargetInCash": 46530,
          "maxEmergencyFundTargetInMonths": 6,
          "minEmergencyFundTargetInMonths": 5,
          "gapWithRecommendedMinEmergencyFund": 16530,
          "excessWithRecommendedMaxEmergencyFund": "Not applicable",
          "maxEmergencyFundTargetAndShortTermNeeds": 172636,
          "minEmergencyFundTargetAndShortTermNeeds": 163330,
          "gapWithRecommendedMinEmergencyFundAndShortTermNeeds": 133330,
          "excessWithRecommendedMaxEmergencyFundAndShortTermNeeds": "Not applicable"
        },
        "advantagedSavings": {
          "hsaMaxContributions": 4400,
          "hsaClientCanContribute": true,
          "hsaClientContributions": 4000,
          "client401kCanContribute": "Yes",
          "client401kContributions": 17000,
          "iraClientMaxContributions": 7500,
          "rothIraClientCanContribute": true,
          "rothIraClientContributions": 0,
          "rothIraClientMaxContributions": 4500,
          "traditionalIraClientContributions": 0,
          "client401kContributionsMaxEmployerMatch": 10800,
          "traditionalIraClientCanDeductContributions": false,
          "client401kContributionsCurrentEmployerMatch": 7000,
          "traditionalIraClientMaxDeductibleContributions": 0
        },
        "incomeAndCashflow": {
          "incomeSummary": [
            [
              "Category",
              "Value",
              "Percentage"
            ],
            [
              "Earned income - Client",
              180000,
              1
            ],
            [
              "Total",
              180000,
              1
            ]
          ],
          "annualCashflow": -8336,
          "outflowSummary": [
            [
              "Category",
              "Value",
              "Percentage"
            ],
            [
              "Taxes",
              40664,
              0.2259
            ],
            [
              "Debt Payments",
              11400,
              0.0633
            ],
            [
              "Housing Expenses",
              34272,
              0.1904
            ],
            [
              "Savings",
              43000,
              0.2389
            ],
            [
              "Expenses",
              66000,
              0.3667
            ],
            [
              "Total",
              195336,
              1.0852
            ]
          ],
          "annualCashflowPercentage": -0.0463,
          "householdIncomePercentile": 0.9
        },
        "housingInformation": {
          "rentVsOwn": "Rent",
          "rentalPayment": 2800,
          "housingExpenses": 2856,
          "mortgagePayment": 0,
          "otherHousingExpenses": 56
        },
        "debtRatiosAndHealth": {
          "dti": 0.2537,
          "housingRatio": 0.1904,
          "housingExpenses": 2856,
          "dtiFirstThreshold": 0.36,
          "dtiThirdThreshold": 0.5,
          "dtiSecondThreshold": 0.43,
          "totalMonthlyObligations": 3806,
          "housingRatioFirstThreshold": 0.28,
          "housingRatioSecondThreshold": 0.32,
          "percentageOfDebtOverGrossIncome": 0.1583
        },
        "shortTermGoalsNeeded": [
          {
            "date": "2027-01-01T00:00:00.000Z",
            "amount": 3500,
            "description": "Take a vacation",
            "paymentFrequency": "ANNUAL"
          },
          {
            "date": "2027-01-01T00:00:00.000Z",
            "amount": 113300,
            "description": "Purchase a home",
            "paymentFrequency": "ONE_TIME"
          }
        ]
      },
      "assetsAndInvestments": {
        "withdrawals": {
          "rmdStartAge": 75,
          "rmdStartYear": 2064,
          "averageWithdrawalsDuringRmds": 38774.84,
          "yearsPayingMoreRmdsThanRequiredWithoutSavings": 0,
          "yearsPayingMoreRmdsThanRequiredWithCurrentSavings": 0
        },
        "listOfAssets": [
          [
            "Asset type",
            "Number of assets",
            "Asset value",
            "% of total assets",
            "Equity value",
            "% of Net worth"
          ],
          [
            "Cash account",
            2,
            27000,
            0.1093,
            27000,
            0.1164
          ],
          [
            "Investment account",
            3,
            145000,
            0.587,
            145000,
            0.625
          ],
          [
            "Real estate",
            0,
            0,
            0,
            0,
            0
          ],
          [
            "Vehicle",
            1,
            40000,
            0.1619,
            25000,
            0.1078
          ],
          [
            "Other asset",
            1,
            35000,
            0.1417,
            35000,
            0.1509
          ]
        ],
        "clientProfile": {
          "clientAge": 37,
          "clientName": "Michael",
          "clientRiskProfile": "(4) Growth",
          "clientRetirementAge": 58
        },
        "contributions": {
          "IRAContributions": [
            [
              "IRA contributions (Traditional + Roth)",
              "Client"
            ],
            [
              "Max IRA contribution (Traditional + Roth)",
              7500
            ],
            [
              "IRA catch-up (age 50+)",
              "Not applicable"
            ],
            [
              "Total possible IRA contribution",
              7500
            ],
            [
              "Roth IRA eligible amount (estimate)",
              4500
            ]
          ],
          "hsaContributions": {
            "catchUpForClient": "Not applicable",
            "maxContributions": 4400,
            "totalPossibleContribution": 4400
          },
          "employerPlanContributions": [
            [
              "Employer plan contributions (401k, 403b, etc)",
              "Client"
            ],
            [
              "Max employee contribution",
              24500
            ],
            [
              "Catch up (age 50+)",
              "Not applicable"
            ],
            [
              "Super catch up (age 60-63)",
              "Not applicable"
            ],
            [
              "Total possible employee contribution",
              24500
            ]
          ]
        },
        "educationGoal": {
          "hasAnEducationGoal": false
        },
        "listOfAccounts": [
          [
            "Account",
            "Client",
            "Number",
            "Balance",
            "Annual contribution"
          ],
          [
            "401k - Traditional",
            "Michael",
            1,
            80000,
            24000
          ],
          [
            "Brokerage account",
            "Michael",
            1,
            60000,
            12000
          ],
          [
            "Cash/savings",
            "Michael",
            2,
            27000,
            3000
          ],
          [
            "HSA",
            "Michael",
            1,
            5000,
            4000
          ]
        ],
        "matchGapAnalysis": [
          {
            "holder": "client",
            "accountName": "401(k) - Michael",
            "accountType": "401K",
            "grossSalary": 180000,
            "matchStructure": "FIXED_AMOUNT",
            "alertSuppressed": false,
            "matchPolicySource": "configured",
            "currentAnnualMatch": 7000,
            "fullMatchThreshold": 0,
            "activeContributions": true,
            "matchPolicyConfigured": true,
            "uncapturedAnnualMatch": 0,
            "maxPossibleAnnualMatch": 7000,
            "matchMaximizationStatus": "MAXIMIZED",
            "lifetimeUncapturedMatchEstimate": 0,
            "additionalContributionToMaximize": 0
          }
        ],
        "incomeAndTaxation": {
          "taxRates": [
            [
              "Tax rate",
              "Current",
              "Expected at retirement"
            ],
            [
              "Federal ordinary tax rate",
              0.24,
              0.12
            ],
            [
              "State tax rate",
              0,
              0
            ],
            [
              "NIIT tax rate",
              0,
              0
            ],
            [
              "Effective ordinary tax rate",
              0.24,
              0.12
            ]
          ],
          "taxableIncome": {
            "totalTaxableIncome": 142900
          },
          "totalGrossIncome": 180000,
          "clientGrossIncome": 180000,
          "coClientGrossIncome": 0
        },
        "retirementGlidePath": {
          "retirementGlidePathForClient": "98% equity and 2% fixed income",
          "retirementGlideEquityForClient": 0.9798,
          "retirementGlideFixedIncomeForClient": 0.0202
        },
        "totalAssetsAndEquity": {
          "totalAssets": 247000,
          "totalEquity": 232000
        },
        "realEstateAndMortgage": {
          "mortgageBalance": 0,
          "realEstateEquity": 0,
          "realEstateEquityThreshold1": 0.2,
          "realEstateEquityThreshold2": 0.5
        },
        "listOfRealEstateAssets": [
          [
            "Real estate",
            "Value",
            "Debt amount",
            "Debt %",
            "Equity amount",
            "Equity %"
          ]
        ],
        "percentageOfCashThreshold": 0.5,
        "listOfChildrenAndEducationGoals": [
          [
            "Student",
            "Age",
            "Education goal timeframe",
            "Years to uni",
            "Education goal ($)",
            "Target equity allocation in 529 account",
            "Target fixed income in 529 account"
          ]
        ]
      },
      "retirementAndOtherGoals": {
        "otherIncome": [
          [
            "Income source",
            "Total value",
            "Yearly average value"
          ],
          [
            "Total other income",
            0,
            0
          ]
        ],
        "withdrawals": {
          "withdrawalRatio": 0.0559,
          "supplementalTotalWithdrawals": 1967222.17,
          "supplementalAnnualWithdrawals": 59612.79
        },
        "clientProfile": {
          "clientAge": 37,
          "clientName": "Michael",
          "endOfPlanAge": 91,
          "clientRiskProfile": "(4) Growth",
          "clientRetirementAge": 58
        },
        "assetDepletion": {
          "netWorthAtEndOfPlan": 567449.78,
          "requiredRetirementAge": "Not applicable",
          "liquidAssetsAtEndOfPlan": -32439.08,
          "shortfallInNumberOfYears": "Not applicable",
          "ageWhenTheyRunOutOfNetWorth": "Not applicable",
          "ageWhenTheyRunOutOfLiquidAssets": 85
        },
        "guaranteedIncome": [
          [
            "Income source",
            "Total value",
            "Yearly average value"
          ],
          [
            "Social security",
            991180.76,
            30035.78
          ],
          [
            "Annuity income",
            0,
            0
          ],
          [
            "Pension / defined benefit",
            0,
            0
          ],
          [
            "Total guaranteed income",
            991180.76,
            30035.78
          ]
        ],
        "incomeVsIncomeNeeds": {
          "allIncomesVsIncomeNeeded": 0.297,
          "otherIncomeVsIncomeNeeded": 0,
          "guaranteedIncomeVsIncomeNeeded": 0.297,
          "allIncomesVsIncomeNeededExLtcCosts": 0.335,
          "otherIncomeVsIncomeNeededExLtcCosts": 0,
          "guaranteedIncomeVsIncomeNeededExLtcCosts": 0.335
        },
        "otherGoalsAndLegacy": {
          "legacyGoal": false,
          "legacyGoalGap": "Not applicable",
          "legacyGoalAmount": "Not applicable",
          "achievesLegacyGoals": "Not applicable",
          "otherGoalsAfterRetirement": true,
          "otherGoalsAfterRetirementAmount": 443522.22
        },
        "netWorthAtRetirement": {
          "netWorthAtRetirementAge": 1535456.66,
          "liquidAssetsAtRetirementAge": 1071095.44,
          "nonLiquidAssetsAtRetirementAge": 464361.21
        },
        "incomeNeedsAndWithdrawals": {
          "totalLtcCosts": 378738.68,
          "annualLtcCosts": 189369.34,
          "totalIncomeNeeded": 3337141.61,
          "ltcCostsAreEstimated": true,
          "annualTotalIncomeNeeded": 101125.5,
          "totalIncomeNeededExLtcCosts": 2958402.93,
          "annualTotalIncomeNeededExLtcCosts": 89648.57
        }
      },
      "taxDragAnalysis": {
        "householdRollup": [
          [
            "Metric",
            "Value",
            "Notes"
          ],
          [
            "Total annual tax cost (Table 2)",
            526.93,
            "All taxable-account rows, including money-market positions."
          ],
          [
            "Money-market drag routed to Cash sub-task",
            0,
            "Money-market positions stay visible here but are carved out of the in-scope Tax Drag total."
          ],
          [
            "In-scope tax cost (Table 2 ex-MM)",
            526.93,
            "Standalone Tax Drag total after routing money-market drag to Cash."
          ],
          [
            "Total annual tax cost saved (Table 3)",
            38.2,
            "Permanent annual tax saved if those holdings were taxable today."
          ],
          [
            "Total annual tax cost deferred (Table 4)",
            318.07,
            "Deferred, not eliminated; future withdrawals remain taxable on exit."
          ],
          [
            "NIIT contribution to Table 2",
            0,
            "Taxable net-investment components multiplied by the current NIIT rate."
          ]
        ],
        "accountTypeInputs": [
          [
            "#",
            "Account name",
            "Account type",
            "Tax treatment"
          ],
          [
            "1",
            "Checking account",
            "Checking account",
            "Taxable"
          ],
          [
            "2",
            "Savings account",
            "Savings account",
            "Taxable"
          ],
          [
            "3",
            "401(k) - Michael",
            "401k - Traditional",
            "Tax deferred"
          ],
          [
            "4",
            "HSA",
            "HSA",
            "Tax free"
          ],
          [
            "5",
            "Taxable Brokerage",
            "Brokerage account",
            "Taxable"
          ]
        ],
        "effectiveTaxMargin": [
          [
            "Component",
            "Rate",
            "Source / Trigger",
            "Applies to"
          ],
          [
            "Federal ordinary",
            "24%",
            "FH metrics — currentTaxBracket",
            "Ordinary income, ST cap gains, ST cap gain distributions, ordinary interest, non-qualified dividends"
          ],
          [
            "Federal LTCG",
            "15%",
            "PW-computed federal LTCG (2026 thresholds; taxable-income proxy)",
            "Qualified dividends, LT cap gains, LT cap gain distributions"
          ],
          [
            "State (TX)",
            "0%",
            "FH metrics — stateTaxRate (TX)",
            "All investment income (state rules)"
          ],
          [
            "NIIT",
            "0%",
            "FH metrics — niitRate",
            "All net investment income"
          ],
          [
            "Total taxable income",
            "$142,900",
            "FH metrics — taxableIncome.totalTaxableIncome",
            "Debug input for LTCG and NIIT lookups"
          ],
          [
            "MAGI proxy",
            "$142,900",
            "Current tax-margin logic — reuse taxableIncome.totalTaxableIncome as MAGI proxy",
            "Debug input for NIIT and current LTCG threshold lookup"
          ],
          [
            "State input",
            "TX — Texas",
            "PW params — state.code / state.name",
            "Debug input for state marginal-rate lookup"
          ],
          [
            "Expected retirement ordinary",
            "12%",
            "FH metrics — expectedTaxBracketInRetirement",
            "Future withdrawals from tax-deferred accounts"
          ],
          [
            "Effective ordinary rate",
            "24%",
            "24% + 0% + 0%",
            "Today's ordinary-rate income"
          ],
          [
            "Effective LTCG rate",
            "15%",
            "15% + 0% + 0%",
            "Today's LTCG-rate income"
          ]
        ],
        "fundHoldingsInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Morningstar category",
            "Balance",
            "Shares",
            "Estimated shares",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Interest income ($/share)",
            "Tax-free income ($/share)",
            "LT cap gain ($/share)",
            "ST cap gain ($/share)",
            "Ordinary-rate share (non-qual div + interest + ST cap gain) / total distribution",
            "Tax cost ratio",
            "Turnover",
            "PCGE"
          ],
          [
            "1",
            "HSA",
            "Cash (USD)",
            "Money Market-Taxable",
            1500,
            1500,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "2",
            "Taxable Brokerage",
            "JNK",
            "High Yield Bond",
            15000,
            161.99,
            "-",
            "$0",
            "$6.358",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "3",
            "401(k) - Michael",
            "SCHP",
            "Inflation-Protected Bond",
            18000,
            703.4,
            "-",
            "$0",
            "$1.075",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "4",
            "401(k) - Michael",
            "Cash (USD)",
            "Money Market-Taxable",
            2000,
            2000,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "5",
            "Taxable Brokerage",
            "SCHD",
            "Large Value",
            20000,
            568.5,
            "-",
            "$0",
            "$1.048",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "6",
            "Taxable Brokerage",
            "VWO",
            "Diversified Emerging Markets",
            22000,
            397.4,
            "-",
            "$0.168",
            "$1.329",
            "$0",
            "$0",
            "$0",
            "$0",
            "88.77%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "7",
            "Taxable Brokerage",
            "Cash (USD)",
            "Money Market-Taxable",
            3000,
            3000,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "8",
            "HSA",
            "FSTDX",
            "Inflation-Protected Bond",
            3500,
            479.45,
            "-",
            "$0",
            "$0.332",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "9",
            "401(k) - Michael",
            "VTI",
            "Large Blend",
            60000,
            165.81,
            "-",
            "$0.86",
            "$2.897",
            "$0",
            "$0",
            "$0",
            "$0",
            "77.11%",
            "[pending]",
            "[pending]",
            "[pending]"
          ]
        ],
        "stockHoldingsInputs": [
          [
            "#",
            "Account",
            "Name",
            "Ticker",
            "Sector",
            "Industry",
            "Country",
            "Balance",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Dividend yield TTM"
          ]
        ],
        "taxFreeAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable)",
            "Annual tax cost saved"
          ],
          [
            "1",
            "HSA",
            "Cash (USD)",
            1500,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "2",
            "HSA",
            "FSTDX",
            3500,
            "Non-qualified dividend",
            159.18,
            "24%",
            38.2
          ],
          [
            "Total",
            "Total tax-free",
            "-",
            5000,
            "-",
            159.18,
            "-",
            38.2
          ]
        ],
        "taxableAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate",
            "Annual tax cost"
          ],
          [
            "1",
            "Taxable Brokerage",
            "JNK",
            15000,
            "Non-qualified dividend",
            1030.01,
            "24%",
            247.2
          ],
          [
            "2",
            "Taxable Brokerage",
            "SCHD",
            20000,
            "Non-qualified dividend",
            595.57,
            "24%",
            142.94
          ],
          [
            "3a",
            "Taxable Brokerage",
            "VWO",
            22000,
            "Qualified dividend",
            66.84,
            "15%",
            10.03
          ],
          [
            "3b",
            "Taxable Brokerage",
            "VWO",
            22000,
            "Non-qualified dividend",
            528.19,
            "24%",
            126.77
          ],
          [
            "3c",
            "Taxable Brokerage",
            "VWO",
            22000,
            "Subtotal",
            595.03,
            "-",
            136.79
          ],
          [
            "4",
            "Taxable Brokerage",
            "Cash (USD)",
            3000,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "Total",
            "Total taxable",
            "-",
            60000,
            "-",
            2220.6,
            "-",
            526.93
          ]
        ],
        "costBasisBlockingNotes": [
          [
            "Account",
            "Blocking note"
          ],
          [
            "Taxable Brokerage",
            "Implementation of Taxable Brokerage cannot be responsibly sequenced without tax-lot data."
          ]
        ],
        "taxableCostBasisInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Balance (market value)",
            "Cost basis",
            "Unrealized gain",
            "Holding period",
            "Notes"
          ],
          [
            "1",
            "Taxable Brokerage",
            "JNK",
            15000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "2",
            "Taxable Brokerage",
            "SCHD",
            20000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "3",
            "Taxable Brokerage",
            "VWO",
            22000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "4",
            "Taxable Brokerage",
            "Cash (USD)",
            3000,
            3000,
            0,
            "N/A",
            "Money market — NAV $1.00, no embedded gain by design."
          ],
          [
            "Total",
            "Total taxable",
            "-",
            60000,
            "[missing cost basis]",
            "[missing cost basis]",
            "-",
            "Totals stay blocked until missing tax-lot inputs are filled."
          ]
        ],
        "taxDeferredAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable today)",
            "Annual tax cost deferred"
          ],
          [
            "1",
            "401(k) - Michael",
            "SCHP",
            18000,
            "Non-qualified dividend",
            755.87,
            "24%",
            181.41
          ],
          [
            "2",
            "401(k) - Michael",
            "Cash (USD)",
            2000,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "3a",
            "401(k) - Michael",
            "VTI",
            60000,
            "Qualified dividend",
            142.56,
            "15%",
            21.38
          ],
          [
            "3b",
            "401(k) - Michael",
            "VTI",
            60000,
            "Non-qualified dividend",
            480.3,
            "24%",
            115.27
          ],
          [
            "3c",
            "401(k) - Michael",
            "VTI",
            60000,
            "Subtotal",
            622.86,
            "-",
            136.66
          ],
          [
            "Total",
            "Total tax-deferred",
            "-",
            80000,
            "-",
            1378.74,
            "-",
            318.07
          ]
        ],
        "componentTaxTreatmentMatrix": [
          [
            "Component",
            "Federal rate type",
            "Effective household rate today",
            "Taxable accounts",
            "Tax-free accounts",
            "Tax-deferred accounts",
            "Notes"
          ],
          [
            "Qualified dividend",
            "LTCG",
            "15%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for US common stock and treaty-country foreign names; funds keep the precomputed Morningstar qualified split."
          ],
          [
            "Non-qualified dividend",
            "ORDINARY",
            "24%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for REIT and non-treaty foreign names, while MLP distributions are treated as ROC; funds keep the precomputed Morningstar non-qualified split."
          ],
          [
            "Interest income",
            "ORDINARY",
            "24%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Money-market and bond-style fund income is treated as ordinary-rate income."
          ],
          [
            "Tax-free income",
            "Tax-exempt federal",
            "0%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Current phase assumes a 0% effective rate because state-specific muni exposure is not available in the data path."
          ],
          [
            "LT cap gain distribution",
            "LTCG",
            "15%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed long-term capital gains use the LTCG household rate."
          ],
          [
            "ST cap gain distribution",
            "ORDINARY",
            "24%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed short-term capital gains use the ordinary household rate."
          ]
        ]
      },
      "realEstate": {
        "realEstateEquity": 0,
        "realEstateEquityThreshold1": 0.2,
        "realEstateEquityThreshold2": 0.5,
        "percentageOfRealEstateEquity": 0
      },
      "savingsRate": null,
      "educationGoalNeeds": null
    },
    "savingsWaterfall": [
      {
        "step": 1,
        "bucket": "Build minimum emergency threshold (3 months)",
        "current": 30000,
        "target": 27918,
        "status": "Filled",
        "delta": 2082,
        "flag": "",
        "notes": ""
      },
      {
        "step": 2,
        "bucket": "Address essential insurance gaps",
        "current": 180000,
        "target": 1900000,
        "status": "Partially filled",
        "delta": -1720000,
        "flag": "",
        "notes": ""
      },
      {
        "step": 3,
        "bucket": "Set aside cash for near-term goals",
        "current": 2082,
        "target": 116800,
        "status": "Partially filled",
        "delta": -114718,
        "flag": "",
        "notes": ""
      },
      {
        "step": 4,
        "bucket": "Maximize employer match — primary plan",
        "current": "N/A",
        "target": "",
        "status": ""
      },
      {
        "step": 5,
        "bucket": "Maximize employer match — secondary plan",
        "current": "N/A",
        "target": "",
        "status": ""
      },
      {
        "step": 6,
        "bucket": "Maximize HSA match",
        "current": 0,
        "target": "N/A",
        "status": "",
        "delta": ""
      },
      {
        "step": 7,
        "bucket": "Maximize ESPP (Employee Stock Purchase Plan)",
        "current": "N/A",
        "target": "",
        "status": ""
      },
      {
        "step": 8,
        "bucket": "Pay high-interest debt (>7%)",
        "current": 3500,
        "target": 0,
        "status": "Empty",
        "delta": 3500,
        "flag": "",
        "notes": ""
      },
      {
        "step": 9,
        "bucket": "Build toward maximum emergency threshold (6 months)",
        "current": 0,
        "target": 55836,
        "status": "Empty",
        "delta": -55836,
        "flag": "",
        "notes": ""
      },
      {
        "step": 10,
        "bucket": "Contribute to Roth IRA",
        "current": 0,
        "target": 4500,
        "status": "Empty",
        "delta": -4500,
        "flag": "",
        "notes": ""
      },
      {
        "step": 11,
        "bucket": "Maximize HSA",
        "current": 4000,
        "target": 4400,
        "status": "Partially filled",
        "delta": -400,
        "flag": "",
        "notes": ""
      },
      {
        "step": 12,
        "bucket": "Contribute to 529 accounts",
        "current": 0,
        "target": "N/A",
        "status": "",
        "delta": ""
      },
      {
        "step": 13,
        "bucket": "Maximize 401k / employer plans",
        "current": 17000,
        "target": 24500,
        "status": "Partially filled",
        "delta": -7500,
        "flag": "",
        "notes": ""
      },
      {
        "step": 14,
        "bucket": "Invest in taxable brokerage",
        "current": 12000,
        "target": "N/A",
        "status": "",
        "delta": ""
      },
      {
        "step": 15,
        "bucket": "Pay low-interest debt (personal, auto)",
        "current": 15000,
        "target": 0,
        "status": "Partially filled",
        "delta": 15000,
        "flag": "",
        "notes": ""
      },
      {
        "step": 16,
        "bucket": "Make extra mortgage payments",
        "current": "N/A",
        "target": "",
        "status": ""
      }
    ],
    "shocks": [
      {
        "assetClassesAffected": [
          "US Treasuries",
          "US equities",
          "USD",
          "rate-sensitive sectors"
        ],
        "dateLabel": "2023-07-26",
        "description": "The Fed raised rates 25bp to 5.25–5.50%, the 11th and final hike in the cycle — the highest level in 22 years. The Fed held here for 14 months before cutting in September 2024.",
        "duration": "Extended",
        "endDate": "2024-09-17",
        "impactDirection": "Rates-driven",
        "name": "Fed final hike to 5.25–5.50%",
        "portfolioImpact": "Mixed",
        "severity": "High",
        "startDate": "2023-07-23",
        "type": "Fed/Macro",
        "drawdown": {
          "severity": "major",
          "eventDate": "2023-07-26",
          "household": {
            "drawdownPct": -0.0419,
            "recoveryDays": 15,
            "returnDuringPct": 0.196
          },
          "windowEnd": "2024-09-17",
          "eventTitle": "Fed final hike to 5.25–5.50%",
          "windowStart": "2023-07-23",
          "divergencePp": 0.0044,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0463,
            "recoveryDays": 13,
            "returnDuringPct": 0.235
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "US Treasuries",
          "small caps",
          "USD",
          "rate-sensitive sectors"
        ],
        "dateLabel": "2023-12-13",
        "description": "Fed held rates steady but the dot plot signaled 75bp of cuts in 2024, marking a decisive pivot. S&P 500 surged to new highs; Russell 2000 +4%. Long-end yields fell sharply. Catalyzed a broad year-end rally across equities and bonds.",
        "duration": "Extended",
        "endDate": "2024-03-31",
        "impactDirection": "Risk-on equity",
        "name": "Fed pivot — December 2023 dot plot",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2023-12-10",
        "type": "Fed/Macro",
        "drawdown": {
          "severity": "major",
          "eventDate": "2023-12-13",
          "household": {
            "drawdownPct": -0.0141,
            "recoveryDays": 7,
            "returnDuringPct": 0.0746
          },
          "windowEnd": "2024-03-31",
          "eventTitle": "Fed pivot — December 2023 dot plot",
          "windowStart": "2023-12-10",
          "divergencePp": 0.0018,
          "sameRiskBenchmark": {
            "drawdownPct": -0.016,
            "recoveryDays": 14,
            "returnDuringPct": 0.0887
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "Japanese equities",
          "EM",
          "global equities",
          "USD/JPY"
        ],
        "dateLabel": "2024-08-05",
        "description": "Yen carry trade unwind and US recession fears triggered a global rout. Japan's TOPIX fell 12.3% — worst since 1987 Black Monday. VIX spiked above 65 intraday. S&P 500 fell ~3% at the open but recovered most losses by Friday. The episode lasted one week.",
        "duration": "Immediate (days)",
        "endDate": "2024-08-09",
        "impactDirection": "Risk-off equity",
        "name": "Global selloff — VIX spikes above 60",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2024-07-31",
        "type": "Market",
        "drawdown": {
          "severity": "major",
          "eventDate": "2024-08-05",
          "household": {
            "drawdownPct": -0.0349,
            "returnDuringPct": -0.0174
          },
          "windowEnd": "2024-08-09",
          "eventTitle": "Global selloff — VIX spikes above 60",
          "windowStart": "2024-07-31",
          "divergencePp": 0.0011,
          "sameRiskBenchmark": {
            "drawdownPct": -0.036,
            "returnDuringPct": -0.0186
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "US Treasuries",
          "USD",
          "EM",
          "rate-sensitive sectors"
        ],
        "dateLabel": "2024-09-18",
        "description": "First Fed rate cut in four years, and an outsized 50bp move, formally marking the start of the easing cycle. Signaled the Fed's confidence that inflation was heading sustainably toward 2% and opened the door to subsequent cuts.",
        "duration": "Extended",
        "endDate": "2024-12-18",
        "impactDirection": "Risk-on equity",
        "name": "Fed first rate cut — 50bp",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2024-09-15",
        "type": "Fed/Macro",
        "drawdown": {
          "severity": "major",
          "eventDate": "2024-09-18",
          "household": {
            "drawdownPct": -0.0264,
            "returnDuringPct": 0.0135
          },
          "windowEnd": "2024-12-18",
          "eventTitle": "Fed first rate cut — 50bp",
          "windowStart": "2024-09-15",
          "divergencePp": 0.0013,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0277,
            "returnDuringPct": 0.0231
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "small caps",
          "financials",
          "USD",
          "crypto"
        ],
        "dateLabel": "2024-11-05",
        "description": "Trump defeated Kamala Harris decisively. S&P 500 surged 2.5%, Dow +3.6%, Russell 2000 +5.8%. The \"Trump trade\" lifted banks, small caps, and crypto on expectations of deregulation and tax cuts. USD strengthened sharply.",
        "duration": "Short",
        "endDate": "2024-11-19",
        "impactDirection": "Risk-on equity",
        "name": "Trump election win",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2024-11-05",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2024-11-05",
          "household": {
            "drawdownPct": -0.0165,
            "returnDuringPct": 0.0059
          },
          "windowEnd": "2024-11-19",
          "eventTitle": "Trump election win",
          "windowStart": "2024-11-05",
          "divergencePp": -0.001,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0156,
            "returnDuringPct": 0.0151
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities (tech/semis)",
          "Nvidia",
          "AI-linked names"
        ],
        "dateLabel": "2025-01-27",
        "description": "Chinese startup DeepSeek released an open-source AI model rivaling GPT-4 at a fraction of the cost, questioning the US AI capex thesis. Nvidia lost $589B in market value — the largest single-day loss for any stock in history. Nasdaq fell 3.1%, S&P 500 fell 1.5%.",
        "duration": "Immediate (days)",
        "endDate": "2025-01-30",
        "impactDirection": "Sector-specific",
        "name": "DeepSeek AI shock",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2025-01-27",
        "type": "Tech/AI",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-01-27",
          "household": {
            "drawdownPct": -0.0017,
            "recoveryDays": 0,
            "returnDuringPct": 0.0045
          },
          "windowEnd": "2025-01-30",
          "eventTitle": "DeepSeek AI shock",
          "windowStart": "2025-01-27",
          "divergencePp": 0.0009,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0027,
            "recoveryDays": 0,
            "returnDuringPct": 0.0064
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "EM",
          "USD",
          "US Treasuries"
        ],
        "dateLabel": "2025-04-02",
        "description": "Trump announced sweeping reciprocal tariffs (10% baseline, 34% on China, 20% on EU, 46% on Vietnam) — the highest US tariff level since 1909. S&P 500 lost 10% in two days — the worst two-day loss in history ($6.6T erased). Long-end yields spiked on bond vigilante concerns.",
        "duration": "Short",
        "endDate": "2025-04-09",
        "impactDirection": "Risk-off equity",
        "name": "Liberation Day tariffs announced",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2025-04-02",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-04-02",
          "household": {
            "drawdownPct": -0.0841,
            "returnDuringPct": -0.0346
          },
          "windowEnd": "2025-04-09",
          "eventTitle": "Liberation Day tariffs announced",
          "windowStart": "2025-04-02",
          "divergencePp": -0.0019,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0822,
            "returnDuringPct": -0.0243
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "US Treasuries",
          "USD"
        ],
        "dateLabel": "2025-04-09",
        "description": "After the S&P 500 fell 10% in two days post-Liberation Day, Trump announced a 90-day pause on reciprocal tariffs above 10% for all countries except China (raised to 125%). S&P 500 surged 9.52% — its largest single-day gain since 2008. Nasdaq jumped 12.16%. Record 30B shares traded.",
        "duration": "Short",
        "endDate": "2025-04-22",
        "impactDirection": "Risk-on equity",
        "name": "90-day tariff pause rally",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2025-04-09",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-04-09",
          "household": {
            "drawdownPct": -0.0198,
            "returnDuringPct": -0.0053
          },
          "windowEnd": "2025-04-22",
          "eventTitle": "90-day tariff pause rally",
          "windowStart": "2025-04-09",
          "divergencePp": 0.013,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0327,
            "returnDuringPct": -0.0168
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "EM",
          "USD",
          "tech",
          "retail"
        ],
        "dateLabel": "2025-05-12",
        "description": "After two days of talks in Geneva, the US and China agreed to reduce reciprocal tariffs from 125% to 10% for 90 days. S&P 500 surged 3.3%, Nasdaq +4.4%. Apple and Amazon led gains as the deal eased supply-chain fears for import-dependent tech and retail sectors.",
        "duration": "Short",
        "endDate": "2025-05-19",
        "impactDirection": "Risk-on equity",
        "name": "US-China Geneva tariff truce",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2025-05-11",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-05-12",
          "household": {
            "drawdownPct": -0.0005,
            "recoveryDays": 0,
            "returnDuringPct": 0.0096
          },
          "windowEnd": "2025-05-19",
          "eventTitle": "US-China Geneva tariff truce",
          "windowStart": "2025-05-11",
          "divergencePp": -0.0002,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0003,
            "recoveryDays": 0,
            "returnDuringPct": 0.0123
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "USD",
          "imports-sensitive sectors"
        ],
        "dateLabel": "2026-02-01",
        "description": "The Supreme Court affirmed that the Trump administration's use of emergency powers to impose the April 2025 reciprocal tariffs was unlawful, formally unwinding the tariff regime's legal basis. (Exact date to verify on next run.)",
        "duration": "Extended",
        "endDate": "2026-02-28",
        "impactDirection": "Risk-on equity",
        "name": "Supreme Court strikes down Liberation Day tariffs",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2026-02-01",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2026-02-01",
          "household": {
            "drawdownPct": -0.0079,
            "recoveryDays": 12,
            "returnDuringPct": 0.0084
          },
          "windowEnd": "2026-02-28",
          "eventTitle": "Supreme Court strikes down Liberation Day tariffs",
          "windowStart": "2026-02-01",
          "divergencePp": 0.0061,
          "sameRiskBenchmark": {
            "drawdownPct": -0.014,
            "returnDuringPct": -0.0021
          }
        }
      },
      {
        "assetClassesAffected": [
          "Crude oil",
          "US equities",
          "international equities",
          "defense stocks",
          "US Treasuries"
        ],
        "dateLabel": "2026-02-28",
        "description": "US and Israel launched coordinated airstrikes on Iranian military and nuclear sites, with nearly 900 strikes in the first 12 hours. Iranian leadership was decapitated. Brent crude surged 10–13% immediately; global equity markets sold off sharply on escalation and energy-supply fears.",
        "duration": "Extended",
        "endDate": "2026-03-04",
        "impactDirection": "Risk-off equity",
        "name": "Operation Epic Fury — US-Israel strikes on Iran",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2026-02-28",
        "type": "Geopolitical",
        "drawdown": {
          "severity": "major",
          "eventDate": "2026-02-28",
          "household": {
            "drawdownPct": -0.0091,
            "returnDuringPct": -0.0062
          },
          "windowEnd": "2026-03-04",
          "eventTitle": "Operation Epic Fury — US-Israel strikes on Iran",
          "windowStart": "2026-02-28",
          "divergencePp": -0.0029,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0062,
            "returnDuringPct": -0.0019
          }
        }
      }
    ],
    "performanceSummary": {
      "maxDrawdown3y": -0.1021,
      "maxDrawdownRecoveryDays": 62,
      "benchmark": {
        "sharpe3y": 1.3001,
        "blendCash": 0.2013,
        "blendEquity": 0.5871,
        "volatility3y": 0.0899,
        "maxDrawdown3y": -0.1144,
        "blendFixedIncome": 0.2116,
        "return1yAnnualized": 0.0784,
        "return3yAnnualized": 0.1528,
        "return3yCumulative": 0.5325
      },
      "assetAllocation": {
        "currentEF": {
          "equity": 0.5871,
          "fixedIncome": 0.4129
        },
        "currentEFC": {
          "cash": 0.2013,
          "equity": 0.5871,
          "fixedIncome": 0.2116
        },
        "targetEF": {
          "equity": 0.6744,
          "fixedIncome": 0.3256
        },
        "targetEFC": {
          "cash": 0.1753,
          "equity": 0.6744,
          "fixedIncome": 0.1505
        }
      },
      "concentration": {
        "topSectorPct": 0.4094,
        "topSectorName": "Technology",
        "isMaterialConcentration": true
      },
      "positions": [
        {
          "account": "Taxable Brokerage",
          "ticker": "JNK",
          "name": "SPDR Bloomberg High Yield Bond ETF",
          "type": "ETF",
          "category": "High Yield Bond",
          "value": 15000,
          "weight_in_account": 0.25,
          "expense_ratio": 0.004
        },
        {
          "account": "401(k) - Michael",
          "ticker": "VTI",
          "name": "Vanguard Morningstar Total Stock Market ETF",
          "type": "ETF",
          "category": "Large Blend",
          "value": 60000,
          "weight_in_account": 0.75,
          "expense_ratio": 0.0003
        }
      ],
      "taxDragAnalysis": {
        "householdRollup": [
          [
            "Metric",
            "Value",
            "Notes"
          ],
          [
            "Total annual tax cost (Table 2)",
            526.93,
            "All taxable-account rows, including money-market positions."
          ],
          [
            "Money-market drag routed to Cash sub-task",
            0,
            "Money-market positions stay visible here but are carved out of the in-scope Tax Drag total."
          ],
          [
            "In-scope tax cost (Table 2 ex-MM)",
            526.93,
            "Standalone Tax Drag total after routing money-market drag to Cash."
          ],
          [
            "Total annual tax cost saved (Table 3)",
            38.2,
            "Permanent annual tax saved if those holdings were taxable today."
          ],
          [
            "Total annual tax cost deferred (Table 4)",
            318.07,
            "Deferred, not eliminated; future withdrawals remain taxable on exit."
          ],
          [
            "NIIT contribution to Table 2",
            0,
            "Taxable net-investment components multiplied by the current NIIT rate."
          ]
        ],
        "accountTypeInputs": [
          [
            "#",
            "Account name",
            "Account type",
            "Tax treatment"
          ],
          [
            "1",
            "Checking account",
            "Checking account",
            "Taxable"
          ],
          [
            "2",
            "Savings account",
            "Savings account",
            "Taxable"
          ],
          [
            "3",
            "401(k) - Michael",
            "401k - Traditional",
            "Tax deferred"
          ],
          [
            "4",
            "HSA",
            "HSA",
            "Tax free"
          ],
          [
            "5",
            "Taxable Brokerage",
            "Brokerage account",
            "Taxable"
          ]
        ],
        "effectiveTaxMargin": [
          [
            "Component",
            "Rate",
            "Source / Trigger",
            "Applies to"
          ],
          [
            "Federal ordinary",
            "24%",
            "FH metrics — currentTaxBracket",
            "Ordinary income, ST cap gains, ST cap gain distributions, ordinary interest, non-qualified dividends"
          ],
          [
            "Federal LTCG",
            "15%",
            "PW-computed federal LTCG (2026 thresholds; taxable-income proxy)",
            "Qualified dividends, LT cap gains, LT cap gain distributions"
          ],
          [
            "State (TX)",
            "0%",
            "FH metrics — stateTaxRate (TX)",
            "All investment income (state rules)"
          ],
          [
            "NIIT",
            "0%",
            "FH metrics — niitRate",
            "All net investment income"
          ],
          [
            "Total taxable income",
            "$142,900",
            "FH metrics — taxableIncome.totalTaxableIncome",
            "Debug input for LTCG and NIIT lookups"
          ],
          [
            "MAGI proxy",
            "$142,900",
            "Current tax-margin logic — reuse taxableIncome.totalTaxableIncome as MAGI proxy",
            "Debug input for NIIT and current LTCG threshold lookup"
          ],
          [
            "State input",
            "TX — Texas",
            "PW params — state.code / state.name",
            "Debug input for state marginal-rate lookup"
          ],
          [
            "Expected retirement ordinary",
            "12%",
            "FH metrics — expectedTaxBracketInRetirement",
            "Future withdrawals from tax-deferred accounts"
          ],
          [
            "Effective ordinary rate",
            "24%",
            "24% + 0% + 0%",
            "Today's ordinary-rate income"
          ],
          [
            "Effective LTCG rate",
            "15%",
            "15% + 0% + 0%",
            "Today's LTCG-rate income"
          ]
        ],
        "fundHoldingsInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Morningstar category",
            "Balance",
            "Shares",
            "Estimated shares",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Interest income ($/share)",
            "Tax-free income ($/share)",
            "LT cap gain ($/share)",
            "ST cap gain ($/share)",
            "Ordinary-rate share (non-qual div + interest + ST cap gain) / total distribution",
            "Tax cost ratio",
            "Turnover",
            "PCGE"
          ],
          [
            "1",
            "HSA",
            "Cash (USD)",
            "Money Market-Taxable",
            1500,
            1500,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "2",
            "Taxable Brokerage",
            "JNK",
            "High Yield Bond",
            15000,
            161.99,
            "-",
            "$0",
            "$6.358",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "3",
            "401(k) - Michael",
            "SCHP",
            "Inflation-Protected Bond",
            18000,
            703.4,
            "-",
            "$0",
            "$1.075",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "4",
            "401(k) - Michael",
            "Cash (USD)",
            "Money Market-Taxable",
            2000,
            2000,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "5",
            "Taxable Brokerage",
            "SCHD",
            "Large Value",
            20000,
            568.5,
            "-",
            "$0",
            "$1.048",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "6",
            "Taxable Brokerage",
            "VWO",
            "Diversified Emerging Markets",
            22000,
            397.4,
            "-",
            "$0.168",
            "$1.329",
            "$0",
            "$0",
            "$0",
            "$0",
            "88.77%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "7",
            "Taxable Brokerage",
            "Cash (USD)",
            "Money Market-Taxable",
            3000,
            3000,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "8",
            "HSA",
            "FSTDX",
            "Inflation-Protected Bond",
            3500,
            479.45,
            "-",
            "$0",
            "$0.332",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "9",
            "401(k) - Michael",
            "VTI",
            "Large Blend",
            60000,
            165.81,
            "-",
            "$0.86",
            "$2.897",
            "$0",
            "$0",
            "$0",
            "$0",
            "77.11%",
            "[pending]",
            "[pending]",
            "[pending]"
          ]
        ],
        "stockHoldingsInputs": [
          [
            "#",
            "Account",
            "Name",
            "Ticker",
            "Sector",
            "Industry",
            "Country",
            "Balance",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Dividend yield TTM"
          ]
        ],
        "taxFreeAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable)",
            "Annual tax cost saved"
          ],
          [
            "1",
            "HSA",
            "Cash (USD)",
            1500,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "2",
            "HSA",
            "FSTDX",
            3500,
            "Non-qualified dividend",
            159.18,
            "24%",
            38.2
          ],
          [
            "Total",
            "Total tax-free",
            "-",
            5000,
            "-",
            159.18,
            "-",
            38.2
          ]
        ],
        "taxableAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate",
            "Annual tax cost"
          ],
          [
            "1",
            "Taxable Brokerage",
            "JNK",
            15000,
            "Non-qualified dividend",
            1030.01,
            "24%",
            247.2
          ],
          [
            "2",
            "Taxable Brokerage",
            "SCHD",
            20000,
            "Non-qualified dividend",
            595.57,
            "24%",
            142.94
          ],
          [
            "3a",
            "Taxable Brokerage",
            "VWO",
            22000,
            "Qualified dividend",
            66.84,
            "15%",
            10.03
          ],
          [
            "3b",
            "Taxable Brokerage",
            "VWO",
            22000,
            "Non-qualified dividend",
            528.19,
            "24%",
            126.77
          ],
          [
            "3c",
            "Taxable Brokerage",
            "VWO",
            22000,
            "Subtotal",
            595.03,
            "-",
            136.79
          ],
          [
            "4",
            "Taxable Brokerage",
            "Cash (USD)",
            3000,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "Total",
            "Total taxable",
            "-",
            60000,
            "-",
            2220.6,
            "-",
            526.93
          ]
        ],
        "costBasisBlockingNotes": [
          [
            "Account",
            "Blocking note"
          ],
          [
            "Taxable Brokerage",
            "Implementation of Taxable Brokerage cannot be responsibly sequenced without tax-lot data."
          ]
        ],
        "taxableCostBasisInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Balance (market value)",
            "Cost basis",
            "Unrealized gain",
            "Holding period",
            "Notes"
          ],
          [
            "1",
            "Taxable Brokerage",
            "JNK",
            15000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "2",
            "Taxable Brokerage",
            "SCHD",
            20000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "3",
            "Taxable Brokerage",
            "VWO",
            22000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "4",
            "Taxable Brokerage",
            "Cash (USD)",
            3000,
            3000,
            0,
            "N/A",
            "Money market — NAV $1.00, no embedded gain by design."
          ],
          [
            "Total",
            "Total taxable",
            "-",
            60000,
            "[missing cost basis]",
            "[missing cost basis]",
            "-",
            "Totals stay blocked until missing tax-lot inputs are filled."
          ]
        ],
        "taxDeferredAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable today)",
            "Annual tax cost deferred"
          ],
          [
            "1",
            "401(k) - Michael",
            "SCHP",
            18000,
            "Non-qualified dividend",
            755.87,
            "24%",
            181.41
          ],
          [
            "2",
            "401(k) - Michael",
            "Cash (USD)",
            2000,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "3a",
            "401(k) - Michael",
            "VTI",
            60000,
            "Qualified dividend",
            142.56,
            "15%",
            21.38
          ],
          [
            "3b",
            "401(k) - Michael",
            "VTI",
            60000,
            "Non-qualified dividend",
            480.3,
            "24%",
            115.27
          ],
          [
            "3c",
            "401(k) - Michael",
            "VTI",
            60000,
            "Subtotal",
            622.86,
            "-",
            136.66
          ],
          [
            "Total",
            "Total tax-deferred",
            "-",
            80000,
            "-",
            1378.74,
            "-",
            318.07
          ]
        ],
        "componentTaxTreatmentMatrix": [
          [
            "Component",
            "Federal rate type",
            "Effective household rate today",
            "Taxable accounts",
            "Tax-free accounts",
            "Tax-deferred accounts",
            "Notes"
          ],
          [
            "Qualified dividend",
            "LTCG",
            "15%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for US common stock and treaty-country foreign names; funds keep the precomputed Morningstar qualified split."
          ],
          [
            "Non-qualified dividend",
            "ORDINARY",
            "24%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for REIT and non-treaty foreign names, while MLP distributions are treated as ROC; funds keep the precomputed Morningstar non-qualified split."
          ],
          [
            "Interest income",
            "ORDINARY",
            "24%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Money-market and bond-style fund income is treated as ordinary-rate income."
          ],
          [
            "Tax-free income",
            "Tax-exempt federal",
            "0%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Current phase assumes a 0% effective rate because state-specific muni exposure is not available in the data path."
          ],
          [
            "LT cap gain distribution",
            "LTCG",
            "15%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed long-term capital gains use the LTCG household rate."
          ],
          [
            "ST cap gain distribution",
            "ORDINARY",
            "24%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed short-term capital gains use the ordinary household rate."
          ]
        ]
      }
    }
  },
  "samantha-lewis": {
    "meta": {
      "slug": "samantha-lewis",
      "household": "Samantha",
      "city": "Miami",
      "state": "FL",
      "tax_filing_status": "SINGLE",
      "isCouple": false,
      "owners": [
        {
          "key": "A",
          "name": "Samantha",
          "role": "client",
          "age": 47,
          "retirement_age": 65,
          "risk_profile": "Growth"
        }
      ]
    },
    "score": {
      "published_score": 82,
      "scale": "0 to 100",
      "band": "strong",
      "colour": "green",
      "message": "A score of 82 places you above average, with some strong areas in your financial life but lacking a cohesive strategy for achieving your goals. Don't settle for just above average; develop a plan to make informed decisions and optimize your financial resources.",
      "pillars": [
        {
          "pillar": "Savings and cash flow",
          "score": 75,
          "points_shown_in_app": "22/30"
        },
        {
          "pillar": "Debt",
          "score": 100,
          "points_shown_in_app": "20/20"
        },
        {
          "pillar": "Investments",
          "score": 66,
          "points_shown_in_app": "10/15"
        },
        {
          "pillar": "Liquidity and emergency fund",
          "score": 100,
          "points_shown_in_app": "15/15"
        },
        {
          "pillar": "Insurance and protection",
          "score": 71,
          "points_shown_in_app": "14/20"
        }
      ],
      "caps_applied": [],
      "top_moves": [
        {
          "title": "Close a coverage gap",
          "action": "Add homeowners insurance on Primary home so coverage integrity clears that gap",
          "effort": "medium",
          "target_amount": null,
          "score_before": 82,
          "score_after": 84,
          "lifts_a_cap": false
        },
        {
          "title": "Reduce single-name concentration",
          "action": "Bring VTI from 39% to 25% of investable for the next concentration band — about $58,300 of that line",
          "effort": "high",
          "target_amount": 58300,
          "score_before": 82,
          "score_after": 83,
          "lifts_a_cap": false
        },
        {
          "title": "Reduce growth allocation toward glide",
          "action": "Move the invested mix from 85% to 80% growth (glide 80%) for the next horizon-fit band — about $17,100 of the invested book",
          "effort": "high",
          "target_amount": 17100,
          "score_before": 82,
          "score_after": 83,
          "lifts_a_cap": false
        }
      ],
      "combined_moves": [],
      "explainer": "## Key takeaways\n- The published score is 82, in the strong band. Liquidity, debt and protection are solid, and no binding limit caps the score. The score before the limit is the same.\n- Protection does not hold the score back. The weaker areas are cash flow and investing, mainly one large VTI position.\n- The top move is homeowners insurance on the primary home to close a coverage gap. The published score moves from 82 to 84 after that move.\n- Cutting VTI concentration is the next move. Adding $58,300 toward that change lifts the published score from 82 to 83.\n\n## Cash flow\n- The savings rate is 24%, but retirement accounts receive none of it.\n- Housing obligations are 5.4% of income, which is light and does not strain the household.\n- College payments begin in August 2026 and August 2028, so these goals draw on the same cash as everyday savings.\n\n## Debt\n- The household has no debt. Debt-only DTI is 0% and the home is owned outright.\n- Debt is a strength and does not drag on the score.\n\n## Protection\n- Life cover of $2,000,000 gives a 193% mortality ratio, and an umbrella policy is in place. Protection does not hold the score back.\n- The primary home and the Porsche Cayenne still show as uninsured. Homeowners cover on the home is the top move.\n\n## Liquidity\n- Cash is $80,000, covering 7.9 months of essential expenses. That falls to 6.1 months after near-term goals of $18,500.\n- Cash above the reserve and goals is only $750, so the cushion is thin.\n\n## Investing\n- VTI is 39% of investable assets. Technology is 30.6% of equity and US exposure is 92.6%, so the mix is concentrated.\n- The invested mix is about 85% growth. Moving to 80% growth, about $17,100 of the invested book, is another listed move.\n- Retirement accounts hold 0. Projected savings run out at age 73, with guaranteed income covering 25% of the spending need."
    },
    "persona": {
      "D0": "EMERGING. Samantha's investable assets are $335,000, below the $500,000 line for the next tier. That figure leaves out her $80,000 of cash and her $900,000 home. Investments plus cash come to $415,000, still under $500,000, so the tier is the same whether or not cash is counted. Her net worth is $1,395,000 and she owes nothing. About 65% of it is the house, which she cannot easily spend. Her $250,000 salary is about the 90th percentile of household incomes in Florida.",
      "D1": "LATE ACCUMULATION. Samantha is 47, single, and works full time. She is the only adult and the only earner. She plans to retire at 65, which is 17 years away. Her children are Ethan (18) and Ava (16). Ethan's college started in August 2026 and his next $12,500 payment is due in August 2027. Ava starts in August 2028. Her plan also includes a $6,000 vacation every year and a $500,000 home purchase in 2030, which change her cash needs but not her life stage.",
      "D2": "MODERATE. She has one source of earned income, no stock compensation and no business. Her accounts are:\r\n\r\n- checking $30,000 and savings $50,000;\r\n- a taxable brokerage account of $300,000;\r\n- two custodial accounts held for the children, $20,000 for Ethan and $15,000 for Ava.\r\n\r\nThe investments are eight broad, low-cost ETFs (funds that trade like stocks), with no individual stocks. She owns her $900,000 home outright and an $80,000 Porsche Cayenne, with no loans on either. She has no retirement accounts, and whether her employer offers a 401(k) is not known. She pays $8,100 a year for three policies: term life, long-term disability and umbrella liability. Cost basis and purchase dates (what she paid and when) are missing for all taxable holdings. The structure is simple, with some added complexity from the custodial accounts, taxes and insurance.",
      "D3": "SIGNIFICANT GAPS. Her Financial Health score is 82 out of 100, in the strong band, and nothing caps it. Debt and liquidity score 100, savings and cash flow 75, insurance 71 and investments 66. The score is high because protection, debt and cash are solid. The remaining gaps are retirement funding and a thin yearly cash flow.\r\n\r\n- **Protection:** Term life is $2,000,000, inside the recommended range of $1,250,000 to $2,500,000, so there is no shortfall. Umbrella coverage is $2,000,000, which meets the recommended minimum. Long-term disability pays $12,500 a month if she cannot work. No homeowners or auto policy is recorded, and the home and car are flagged as uninsured.\r\n- **Retirement:** Retirement accounts hold $0. The projection shows her savings running out at age 73, with $1,448,673 of planned spending unpaid by the end of the plan at age 91. Her yearly spending need in retirement is $153,672. Social Security, her only guaranteed income, averages $38,336 a year and covers 25% of it. That leaves about $115,335 a year to come from savings, an average draw of 12.2% of savings at the start of retirement.\r\n- **Cash flow:** After taxes, $129,600 of yearly expenses and $60,000 of savings (24% of her income), she is $6,418 a year short, about 2.6% of income. None of her savings goes to retirement accounts: $50,000 a year goes to taxable and cash accounts and $10,000 to the custodial accounts.\r\n- **Education:** College costs $12,500 a year per child, $50,000 each. The plan counts $0 in 529 college savings plans and shows $98,838 of the $100,000 total cost still needed.\r\n- **Liquidity and debt:** Cash is $80,000, which covers 7.9 months of essential expenses. The recommended reserve is 5 to 6 months, $50,625 to $60,750. After $18,500 of near-term goals (the vacation and Ethan's payment) it covers 6.1 months, with only $750 above both. She has no debt, and housing costs are 5.4% of income.\r\n\r\nLong-term care costs are only estimates, so they are not treated as a driver.",
      "D4a": "- **D4a stated:** AGGRESSIVE. Her risk profile is Growth (4).\r",
      "D4b": "- **D4b revealed:** AGGRESSIVE. Her long-term taxable accounts hold about 85% stocks against an 80% target, and the children's accounts are almost entirely stocks. Counting cash, the mix is 68.3% stocks, 12.0% bonds and 19.7% cash. VTI, a total US stock market fund, is the largest position, about 39% of her investments plus cash ($162,000 of $415,000). Technology is 30.6% of her stock holdings and 92.6% are in the US.\r",
      "D4c": "- **D4c inferred:** MODERATE. Cautious signs: $80,000 of cash, no debt, an owned home, and life, disability and umbrella cover. Riskier signs: all her income comes from one employer, her yearly cash flow is negative, she has no retirement accounts, and the home and car show as uninsured.\r\n\r\nAlignment: ALIGNED. Her stated and actual investing both lean toward growth.",
      "D4": "- **D4a stated:** AGGRESSIVE. Her risk profile is Growth (4).\r\n- **D4b revealed:** AGGRESSIVE. Her long-term taxable accounts hold about 85% stocks against an 80% target, and the children's accounts are almost entirely stocks. Counting cash, the mix is 68.3% stocks, 12.0% bonds and 19.7% cash. VTI, a total US stock market fund, is the largest position, about 39% of her investments plus cash ($162,000 of $415,000). Technology is 30.6% of her stock holdings and 92.6% are in the US.\r\n- **D4c inferred:** MODERATE. Cautious signs: $80,000 of cash, no debt, an owned home, and life, disability and umbrella cover. Riskier signs: all her income comes from one employer, her yearly cash flow is negative, she has no retirement accounts, and the home and car show as uninsured.\r\n\r\nAlignment: ALIGNED. Her stated and actual investing both lean toward growth.",
      "D5": "VALIDATOR, CONFIDENCE: LOW. Inferred from the structure of her plan only. She built a simple set of broad ETFs, chose a clear Growth target, holds a large cash reserve and has protection policies in place. That fits someone who checks and confirms.",
      "D6": "DUTY, CONFIDENCE: LOW and PROVISIONAL. The evidence is structural. She funds custodial accounts for both children, holds a college goal for each, and carries life, disability and umbrella cover so Ethan and Ava stay protected if her income stops.",
      "transitionAlerts": "None detected. Ethan's August 2027 payment, Ava's August 2028 start and a January 2027 vacation will press on her cash, but change no label within 12 to 24 months. The home purchase is in 2030.",
      "subjectiveConcerns": "None detected. The plan holds no interview notes or statements from Samantha, so her own worries are not recorded.",
      "objectiveConcerns": [
        {
          "id": "O1",
          "detail": "- **O1: Retirement plan runs out of savings at age 73 (CRITICAL).** Retirement accounts hold $0, Social Security covers only 25% of the $153,672 yearly need, and $1,448,673 of planned spending goes unpaid by the end of the plan. Net worth, which includes the home, lasts until about age 90. Connected: D1, D3."
        },
        {
          "id": "O2",
          "detail": "- **O2: Yearly cash flow is negative (SIGNIFICANT).** She is $6,418 a year short after expenses and savings. Connected: D3."
        },
        {
          "id": "O3",
          "detail": "- **O3: College funding gap (MODERATE).** $98,838 is still needed and the 529 balance is $0. Connected: D1, D3."
        },
        {
          "id": "O4",
          "detail": "- **O4: No home or auto insurance recorded (MODERATE).** The plan flags the $900,000 home and the $80,000 Porsche Cayenne as uninsured, and adding homeowners cover is its top-ranked move (score 82 to 84). Her budget does include $4,500 a year for home insurance, so the data does not settle whether the home is covered. Connected: D3, D4c."
        },
        {
          "id": "O5",
          "detail": "- **O5: Thin cash after near-term goals (MINOR).** Only $750 sits above the reserve once $18,500 of goals are set aside. Connected: D3."
        },
        {
          "id": "O6",
          "detail": "- **O6: Concentration and home bias (MINOR).** Technology is 30.6% of her stocks, US exposure is 92.6%, and VTI is the largest position. Her salary is 17.9% of net worth. The plan lists cutting VTI from 39% to 25% and moving from 85% to 80% growth. Connected: D4b."
        },
        {
          "id": "O7",
          "detail": "- **O7: Tax-advantaged limits unused (MODERATE).** She could put up to $4,400 a year in an HSA (about $1,408 of tax saved at her 32% bracket) if her health plan qualifies, and up to $7,500 in a deductible traditional IRA. She has contributed $0 to each. Whether she has a 401(k) is unknown, and Roth IRA contributions are not permitted for her. Connected: D2, D3."
        },
        {
          "id": "O8",
          "detail": "- **O8: Tax cost on taxable holdings (MINOR).** Tax on her investments costs about $3,032 a year, mostly from dividends taxed at 35.8%. The bond fund JNK costs $1,229 and the dividend fund SCHD in the brokerage account $853. Missing cost basis blocks a sale-by-sale review. Connected: D2."
        },
        {
          "id": "O9",
          "detail": "- **O9: Home purchase planned for 2030 (MODERATE).** The plan assumes a $500,000 purchase (about $562,754 by then): a $112,551 down payment, $9,404 of closing costs and a $450,204 mortgage at 7% over 30 years, $2,995 a month. Connected: D1, D3."
        }
      ],
      "tensions": [
        {
          "id": "T1",
          "detail": "- **T1: Retirement shortfall, college funding and negative cash flow (HIGH).** Her savings go to taxable and cash accounts while retirement accounts hold $0. The $98,838 college gap, the age 73 depletion and the $6,418 yearly shortfall compete for the same dollars (O1, O2, O3), and the 2030 home purchase adds another call on cash (O9). Urgency is high because college payments are under way."
        },
        {
          "id": "T2",
          "detail": "- **T2: Growth portfolio against early depletion and negative cash flow (MEDIUM).** Stated and actual risk are both aggressive, yet the plan runs out at 73 and cash flow is negative (O1, O2). A market drop would hit a household with a 12.2% starting draw and a thin cushion."
        },
        {
          "id": "T3",
          "detail": "- **T3: Cash reserve against near-term goals (LOW).** Only $750 sits above the reserve after $18,500 of goals, and the $6,418 yearly shortfall would erode it (O5, O2)."
        }
      ]
    },
    "projections": {
      "yearly": [
        {
          "year": 2026,
          "age_client": 47,
          "age_co_client": null,
          "net_worth": 1401427,
          "net_worth_todays_dollars": 1397932,
          "total_debts": 0,
          "investable_assets": 420006,
          "net_worth_needed": 1402014
        },
        {
          "year": 2027,
          "age_client": 48,
          "age_co_client": null,
          "net_worth": 1479965,
          "net_worth_todays_dollars": 1432697,
          "total_debts": 0,
          "investable_assets": 480397,
          "net_worth_needed": 1487592
        },
        {
          "year": 2028,
          "age_client": 49,
          "age_co_client": null,
          "net_worth": 1553297,
          "net_worth_todays_dollars": 1459301,
          "total_debts": 0,
          "investable_assets": 533657,
          "net_worth_needed": 1567964
        },
        {
          "year": 2029,
          "age_client": 50,
          "age_co_client": null,
          "net_worth": 1634586,
          "net_worth_todays_dollars": 1490341,
          "total_debts": 0,
          "investable_assets": 593049,
          "net_worth_needed": 1656293
        },
        {
          "year": 2030,
          "age_client": 51,
          "age_co_client": null,
          "net_worth": 1694917,
          "net_worth_todays_dollars": 1499733,
          "total_debts": 445630,
          "investable_assets": 496954,
          "net_worth_needed": 1723666
        },
        {
          "year": 2031,
          "age_client": 52,
          "age_co_client": null,
          "net_worth": 1770779,
          "net_worth_todays_dollars": 1520607,
          "total_debts": 440726,
          "investable_assets": 525022,
          "net_worth_needed": 1806567
        },
        {
          "year": 2032,
          "age_client": 53,
          "age_co_client": null,
          "net_worth": 1868772,
          "net_worth_todays_dollars": 1557387,
          "total_debts": 435468,
          "investable_assets": 572728,
          "net_worth_needed": 1911601
        },
        {
          "year": 2033,
          "age_client": 54,
          "age_co_client": null,
          "net_worth": 1973991,
          "net_worth_todays_dollars": 1596514,
          "total_debts": 429830,
          "investable_assets": 625175,
          "net_worth_needed": 2023860
        },
        {
          "year": 2034,
          "age_client": 55,
          "age_co_client": null,
          "net_worth": 2086828,
          "net_worth_todays_dollars": 1637954,
          "total_debts": 423783,
          "investable_assets": 682749,
          "net_worth_needed": 2143737
        },
        {
          "year": 2035,
          "age_client": 56,
          "age_co_client": null,
          "net_worth": 2207715,
          "net_worth_todays_dollars": 1681688,
          "total_debts": 417300,
          "investable_assets": 745865,
          "net_worth_needed": 2271665
        },
        {
          "year": 2036,
          "age_client": 57,
          "age_co_client": null,
          "net_worth": 2337149,
          "net_worth_todays_dollars": 1727732,
          "total_debts": 410348,
          "investable_assets": 814995,
          "net_worth_needed": 2408139
        },
        {
          "year": 2037,
          "age_client": 58,
          "age_co_client": null,
          "net_worth": 2475655,
          "net_worth_todays_dollars": 1776100,
          "total_debts": 402894,
          "investable_assets": 890624,
          "net_worth_needed": 2553686
        },
        {
          "year": 2038,
          "age_client": 59,
          "age_co_client": null,
          "net_worth": 2623807,
          "net_worth_todays_dollars": 1826824,
          "total_debts": 394901,
          "investable_assets": 973281,
          "net_worth_needed": 2708878
        },
        {
          "year": 2039,
          "age_client": 60,
          "age_co_client": null,
          "net_worth": 2782229,
          "net_worth_todays_dollars": 1879944,
          "total_debts": 386330,
          "investable_assets": 1063532,
          "net_worth_needed": 2874340
        },
        {
          "year": 2040,
          "age_client": 61,
          "age_co_client": null,
          "net_worth": 2951617,
          "net_worth_todays_dollars": 1935529,
          "total_debts": 377139,
          "investable_assets": 1162011,
          "net_worth_needed": 3050769
        },
        {
          "year": 2041,
          "age_client": 62,
          "age_co_client": null,
          "net_worth": 3132533,
          "net_worth_todays_dollars": 1993529,
          "total_debts": 367284,
          "investable_assets": 1269362,
          "net_worth_needed": 3238725
        },
        {
          "year": 2042,
          "age_client": 63,
          "age_co_client": null,
          "net_worth": 3327534,
          "net_worth_todays_dollars": 2055119,
          "total_debts": 356716,
          "investable_assets": 1386319,
          "net_worth_needed": 3440767
        },
        {
          "year": 2043,
          "age_client": 64,
          "age_co_client": null,
          "net_worth": 3535731,
          "net_worth_todays_dollars": 2119245,
          "total_debts": 345385,
          "investable_assets": 1513656,
          "net_worth_needed": 3656004
        },
        {
          "year": 2044,
          "age_client": 65,
          "age_co_client": null,
          "net_worth": 3628794,
          "net_worth_todays_dollars": 2110822,
          "total_debts": 333234,
          "investable_assets": 1522924,
          "net_worth_needed": 3753174
        },
        {
          "year": 2045,
          "age_client": 66,
          "age_co_client": null,
          "net_worth": 3522479,
          "net_worth_todays_dollars": 1988498,
          "total_debts": 320205,
          "investable_assets": 1329758,
          "net_worth_needed": 3646859
        },
        {
          "year": 2046,
          "age_client": 67,
          "age_co_client": null,
          "net_worth": 3443976,
          "net_worth_todays_dollars": 1886793,
          "total_debts": 306234,
          "investable_assets": 1161215,
          "net_worth_needed": 3568356
        },
        {
          "year": 2047,
          "age_client": 68,
          "age_co_client": null,
          "net_worth": 3396943,
          "net_worth_todays_dollars": 1806092,
          "total_debts": 291253,
          "investable_assets": 1020820,
          "net_worth_needed": 3521323
        },
        {
          "year": 2048,
          "age_client": 69,
          "age_co_client": null,
          "net_worth": 3336412,
          "net_worth_todays_dollars": 1721546,
          "total_debts": 275190,
          "investable_assets": 863460,
          "net_worth_needed": 3460792
        },
        {
          "year": 2049,
          "age_client": 70,
          "age_co_client": null,
          "net_worth": 3261023,
          "net_worth_todays_dollars": 1632978,
          "total_debts": 257964,
          "investable_assets": 687623,
          "net_worth_needed": 3385403
        },
        {
          "year": 2050,
          "age_client": 71,
          "age_co_client": null,
          "net_worth": 3169301,
          "net_worth_todays_dollars": 1540200,
          "total_debts": 239494,
          "investable_assets": 491677,
          "net_worth_needed": 3293680
        },
        {
          "year": 2051,
          "age_client": 72,
          "age_co_client": null,
          "net_worth": 3059645,
          "net_worth_todays_dollars": 1443020,
          "total_debts": 219689,
          "investable_assets": 273853,
          "net_worth_needed": 3184024
        },
        {
          "year": 2052,
          "age_client": 73,
          "age_co_client": null,
          "net_worth": 2930320,
          "net_worth_todays_dollars": 1341231,
          "total_debts": 198452,
          "investable_assets": 32242,
          "net_worth_needed": 3054699
        },
        {
          "year": 2053,
          "age_client": 74,
          "age_co_client": null,
          "net_worth": 2787255,
          "net_worth_todays_dollars": 1238092,
          "total_debts": 175679,
          "investable_assets": -227414,
          "net_worth_needed": 2911635
        },
        {
          "year": 2054,
          "age_client": 75,
          "age_co_client": null,
          "net_worth": 2641557,
          "net_worth_todays_dollars": 1138737,
          "total_debts": 151260,
          "investable_assets": -494204,
          "net_worth_needed": 2765937
        },
        {
          "year": 2055,
          "age_client": 76,
          "age_co_client": null,
          "net_worth": 2493280,
          "net_worth_todays_dollars": 1043090,
          "total_debts": 125077,
          "investable_assets": -768277,
          "net_worth_needed": 2617660
        },
        {
          "year": 2056,
          "age_client": 77,
          "age_co_client": null,
          "net_worth": 2342408,
          "net_worth_todays_dollars": 951045,
          "total_debts": 97000,
          "investable_assets": -1049868,
          "net_worth_needed": 2466788
        },
        {
          "year": 2057,
          "age_client": 78,
          "age_co_client": null,
          "net_worth": 2188929,
          "net_worth_todays_dollars": 862497,
          "total_debts": 66893,
          "investable_assets": -1339219,
          "net_worth_needed": 2313309
        },
        {
          "year": 2058,
          "age_client": 79,
          "age_co_client": null,
          "net_worth": 2032834,
          "net_worth_todays_dollars": 777347,
          "total_debts": 34611,
          "investable_assets": -1636578,
          "net_worth_needed": 2157214
        },
        {
          "year": 2059,
          "age_client": 80,
          "age_co_client": null,
          "net_worth": 1874122,
          "net_worth_todays_dollars": 695502,
          "total_debts": 0,
          "investable_assets": -1942197,
          "net_worth_needed": 1998502
        },
        {
          "year": 2060,
          "age_client": 81,
          "age_co_client": null,
          "net_worth": 1711618,
          "net_worth_todays_dollars": 616446,
          "total_debts": 0,
          "investable_assets": -2220413,
          "net_worth_needed": 1835998
        },
        {
          "year": 2061,
          "age_client": 82,
          "age_co_client": null,
          "net_worth": 1543826,
          "net_worth_todays_dollars": 539602,
          "total_debts": 0,
          "investable_assets": -2507437,
          "net_worth_needed": 1668206
        },
        {
          "year": 2062,
          "age_client": 83,
          "age_co_client": null,
          "net_worth": 1370568,
          "net_worth_todays_dollars": 464904,
          "total_debts": 0,
          "investable_assets": -2803553,
          "net_worth_needed": 1494948
        },
        {
          "year": 2063,
          "age_client": 84,
          "age_co_client": null,
          "net_worth": 1191661,
          "net_worth_todays_dollars": 392286,
          "total_debts": 0,
          "investable_assets": -3109054,
          "net_worth_needed": 1316041
        },
        {
          "year": 2064,
          "age_client": 85,
          "age_co_client": null,
          "net_worth": 1006916,
          "net_worth_todays_dollars": 321685,
          "total_debts": 0,
          "investable_assets": -3424245,
          "net_worth_needed": 1131295
        },
        {
          "year": 2065,
          "age_client": 86,
          "age_co_client": null,
          "net_worth": 816135,
          "net_worth_todays_dollars": 253039,
          "total_debts": 0,
          "investable_assets": -3749439,
          "net_worth_needed": 940515
        },
        {
          "year": 2066,
          "age_client": 87,
          "age_co_client": null,
          "net_worth": 619115,
          "net_worth_todays_dollars": 186288,
          "total_debts": 0,
          "investable_assets": -4084960,
          "net_worth_needed": 743495
        },
        {
          "year": 2067,
          "age_client": 88,
          "age_co_client": null,
          "net_worth": 415647,
          "net_worth_todays_dollars": 121374,
          "total_debts": 0,
          "investable_assets": -4431142,
          "net_worth_needed": 540027
        },
        {
          "year": 2068,
          "age_client": 89,
          "age_co_client": null,
          "net_worth": 205512,
          "net_worth_todays_dollars": 58240,
          "total_debts": 0,
          "investable_assets": -4788332,
          "net_worth_needed": 329892
        },
        {
          "year": 2069,
          "age_client": 90,
          "age_co_client": null,
          "net_worth": -11516,
          "net_worth_todays_dollars": -3167,
          "total_debts": 0,
          "investable_assets": -5156887,
          "net_worth_needed": 112864
        },
        {
          "year": 2070,
          "age_client": 90,
          "age_co_client": null,
          "net_worth": -124380,
          "net_worth_todays_dollars": -33615,
          "total_debts": 0,
          "investable_assets": -5360262,
          "net_worth_needed": 0
        }
      ],
      "firstNegativeInvestableYear": 2053,
      "firstNegativeNetWorthYear": 2069,
      "peakInvestable": 1522924,
      "endOfPlan": {
        "year": 2070,
        "age_client": 90,
        "age_co_client": null,
        "net_worth": -124380,
        "net_worth_todays_dollars": -33615,
        "total_debts": 0,
        "investable_assets": -5360262,
        "net_worth_needed": 0
      }
    },
    "goals": {
      "goalsSummary": [
        {
          "amount": 6000,
          "goalType": "VACATION",
          "value": "Going on a $6,000 vacation every year."
        },
        {
          "amount": 50000,
          "goalType": "COLLEGE",
          "value": "Finance education for 2 children ($50,000 in total for each child)."
        },
        {
          "amount": 500000,
          "goalType": "PURCHASE",
          "subType": "REAL_ESTATE_PURCHASE",
          "value": "Plan to purchase a home for $500,000 in 2030."
        }
      ],
      "chartGoals": [
        {
          "date": "2027-01-01T00:00:00.000Z",
          "goalType": "VACATION",
          "name": "Take a vacation",
          "termDate": "2044-07-01T00:00:00.000Z"
        },
        {
          "date": "2028-08-01T00:00:00.000Z",
          "goalType": "COLLEGE",
          "name": "College Ava",
          "termDate": "2032-01-01T00:00:00.000Z"
        },
        {
          "date": "2030-01-01T00:00:00.000Z",
          "goalType": "PURCHASE",
          "name": "Purchase a home",
          "subType": "REAL_ESTATE_PURCHASE",
          "termDate": "2030-01-01T00:00:00.000Z"
        },
        {
          "date": "2044-07-01T00:00:00.000Z",
          "goalType": "RETIREMENT",
          "name": "Samantha's Retirement"
        },
        {
          "date": "2053-02-01T00:00:00.000Z",
          "goalType": "BANKRUPTCY_ZEROCASH"
        },
        {
          "date": "2069-12-01T00:00:00.000Z",
          "goalType": "BANKRUPTCY"
        }
      ]
    },
    "facts": {
      "facts": {
        "cash": {
          "monthsCovered": {
            "unit": "months",
            "basis": "n/a",
            "label": "Months of essential expenses accessible cash covers",
            "value": "7.9",
            "period": "today, before near-term goals",
            "replaces": [
              "ratios.emergencyFund.emergencyFundMonths (capped at \"+12\")",
              "savingsAndExpenses.liquidityContext.emergencyFundInMonths",
              "protection.emergencyFund.emergencyFundCoverageEvaluation.monthsCovered"
            ],
            "notToBeConfusedWith": [
              "the recommended number of months"
            ]
          },
          "nearTermGoals": [
            {
              "note": "A goal payment, not a down payment unless the goal is a purchase.",
              "unit": "USD",
              "basis": "as entered",
              "label": "Take a vacation: cash to hold for its next payment",
              "value": 6000,
              "period": "next payment January 2027, then every year",
              "replaces": [
                "extraCashOutflows[].downpayment (holds any goal payment)"
              ]
            },
            {
              "note": "A goal payment, not a down payment unless the goal is a purchase.",
              "unit": "USD",
              "basis": "as entered",
              "label": "College Ethan: cash to hold for its next payment",
              "value": 12500,
              "period": "next payment August 2027, then every year",
              "replaces": [
                "extraCashOutflows[].downpayment (holds any goal payment)"
              ]
            }
          ],
          "accessibleCash": {
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Accessible cash (bank accounts plus taxable money market)",
            "value": 80000,
            "period": "balance today",
            "notToBeConfusedWith": [
              "bank cash alone (excludes money market)",
              "cash inside retirement accounts, which is not accessible"
            ]
          },
          "totalCashNeeded": {
            "max": 79250,
            "min": 69125,
            "note": "Never call this the emergency reserve.",
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Cash target: emergency reserve plus near-term goals",
            "period": "target balance today",
            "replaces": [
              "ratios.emergencyFund.adjustedRecommendedMin/MaxAmount",
              "savingsAndExpenses.liquidityContext.min/maxEmergencyFundTargetAndShortTermNeeds",
              "cashNeeds.cashTarget"
            ],
            "notToBeConfusedWith": [
              "emergencyReserve"
            ]
          },
          "cashAboveReserve": {
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Cash above the top of the emergency reserve, before near-term goals",
            "value": 19250,
            "period": "today",
            "notToBeConfusedWith": [
              "cashAboveTotalNeeded"
            ]
          },
          "emergencyReserve": {
            "max": 60750,
            "min": 50625,
            "note": "Excludes near-term goals. This alone is the emergency reserve.",
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Recommended emergency reserve (5–6 months of essential expenses)",
            "period": "target balance today",
            "replaces": [
              "ratios.emergencyFund.min/maxRecommendedEmergencyFund",
              "savingsAndExpenses.liquidityContext.min/maxEmergencyFundTargetInCash",
              "protection.emergencyFund.recommendedEmergencyFundLevels.minimum/maximumAmountRecommended",
              "cashNeeds.emergencyFund"
            ],
            "notToBeConfusedWith": [
              "totalCashNeeded"
            ]
          },
          "cashAboveTotalNeeded": {
            "note": "This is the cash that is free after the reserve and the near-term goals. Say it is above both; never call it the amount above the reserve or the reserve target.",
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Cash above the emergency reserve and near-term goals",
            "value": 750,
            "period": "today",
            "replaces": [
              "ratios.emergencyFund.excessOverAdjustedMax",
              "ratios.emergencyFund.extraCashAboveMaxEmergencyFundPlusStg",
              "savingsAndExpenses.liquidityContext.excessWithRecommendedMaxEmergencyFundAndShortTermNeeds",
              "protection.emergencyFund.emergencyFundCoverageEvaluation.adjustedEmergencyFundExcessAfterShortTermCashNeeds",
              "cashNeeds.accessibleCashExcess"
            ],
            "notToBeConfusedWith": [
              "cashAboveReserve"
            ]
          },
          "monthsCoveredAfterNearTermGoals": {
            "unit": "months",
            "basis": "n/a",
            "label": "Months of essential expenses covered after setting aside near-term goals",
            "value": "6.1",
            "period": "today",
            "replaces": [
              "ratios.emergencyFund.adjustedMonthsCoveredAfterShortTermCashNeeds"
            ]
          }
        },
        "rules": [
          "These facts are the only figures to quote for these concepts. Quote the label's meaning with the number; never relabel a fact as another one.",
          "Each fact names the facts it must not be confused with. Never call one by the other's name.",
          "Keep the unit: a USD/yr figure is always said per year, a lump sum never is.",
          "Do not add, subtract or compare two facts unless a fact says how they relate.",
          "Never quote a date that is before the plan date.",
          "Write a date as month and year (August 2039), never as an ISO date (2039-08-01).",
          "Write a ratio or rate as a percentage (55%), never as a decimal (0.551).",
          "A fact's `replaces` lists key-metric fields that hold the same or a confusable figure under a misleading name. When you see one of those fields in your other inputs, quote the fact with its label instead. Field names are never labels."
        ],
        "education": {
          "fundingGap": {
            "note": "Not the amount to invest today and not the goal. It is larger than the total cost because college costs are inflated to the years they are paid.",
            "unit": "USD",
            "basis": "engine estimate: inflated college costs valued at college start, restated in today's dollars",
            "label": "College funding still needed beyond current 529 balances",
            "value": 98837.55,
            "period": "one lump sum for all college years",
            "notToBeConfusedWith": [
              "totalCostAllGoals",
              "combinedAnnualCost"
            ]
          },
          "totalCostPerGoal": [
            {
              "unit": "USD",
              "basis": "today's dollars at the plan date, before education inflation",
              "label": "College Ethan: total college cost, whole program",
              "value": 50000,
              "period": "4 years of college",
              "notToBeConfusedWith": [
                "annualCostPerGoal"
              ]
            },
            {
              "unit": "USD",
              "basis": "today's dollars at the plan date, before education inflation",
              "label": "College Ava: total college cost, whole program",
              "value": 50000,
              "period": "4 years of college",
              "notToBeConfusedWith": [
                "annualCostPerGoal"
              ]
            }
          ],
          "annualCostPerGoal": [
            {
              "unit": "USD/yr",
              "basis": "today's dollars at the plan date",
              "label": "College Ethan: yearly college cost",
              "value": 12500,
              "period": "each year of college, 2026–2029 (4 payments); college starts August 2026, about 0 years from now",
              "replaces": [
                "listOfChildrenAndEducationGoals column \"Years to uni\" (rounded down)",
                "listOfChildrenAndEducationGoals column \"Education goal ($)\" (a yearly cost)",
                "protection.lifeInsurance.educationGoal column \"Total cost\" (a yearly cost)"
              ],
              "notToBeConfusedWith": [
                "totalCostPerGoal",
                "fundingGap"
              ]
            },
            {
              "unit": "USD/yr",
              "basis": "today's dollars at the plan date",
              "label": "College Ava: yearly college cost",
              "value": 12500,
              "period": "each year of college, 2028–2031 (4 payments); college starts August 2028, about 2 years from now",
              "replaces": [
                "listOfChildrenAndEducationGoals column \"Years to uni\" (rounded down)",
                "listOfChildrenAndEducationGoals column \"Education goal ($)\" (a yearly cost)",
                "protection.lifeInsurance.educationGoal column \"Total cost\" (a yearly cost)"
              ],
              "notToBeConfusedWith": [
                "totalCostPerGoal",
                "fundingGap"
              ]
            }
          ],
          "extraYearlySaving": {
            "unit": "USD/yr",
            "basis": "engine estimate",
            "label": "Extra yearly saving needed for college (first year)",
            "value": -179275.57,
            "period": "per year from now until each child starts college, rising each year",
            "notToBeConfusedWith": [
              "annualCostPerGoal"
            ]
          },
          "totalCostAllGoals": {
            "note": "This is the education goal when one total is needed.",
            "unit": "USD",
            "basis": "today's dollars at the plan date, before education inflation",
            "label": "Total college cost, all children, whole programs",
            "value": 100000,
            "period": "all college years",
            "notToBeConfusedWith": [
              "fundingGap",
              "combinedAnnualCost"
            ]
          },
          "combinedAnnualCost": {
            "note": "Not the education goal and not a yearly household bill. Prefer per-child yearly costs; for one total use totalCostAllGoals.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Sum of each child's yearly college cost",
            "value": 25000,
            "period": "one year per child added together; their college years do not overlap",
            "replaces": [
              "assetsAndInvestments.educationGoalNeeds.educationGoalAmount",
              "savingsAndExpenses.goals.totalEducationGoalRequiredAmount",
              "ratios.educationSavings.totalEducationGoalsAmount"
            ]
          }
        },
        "retirement": {
          "spendingGap": {
            "note": "Savings, cash and required IRA withdrawals included, pay this each year on average. It is what the plan asks of savings.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Yearly retirement spending that income does not cover, paid from savings",
            "value": 115335.47,
            "period": "average over the 26 years of retirement",
            "notToBeConfusedWith": [
              "averagePortfolioDraw"
            ]
          },
          "spendingNeed": {
            "note": "Includes taxes, debt payments and goals after retirement; do not add those on top. annualTotalIncomeNeeded adds an estimated long-term care cost: do not quote it.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Yearly retirement spending need (excluding estimated long-term care)",
            "value": 153671.62,
            "period": "average over the 26 years of retirement",
            "replaces": [
              "retirementAndOtherGoals.incomeNeedsAndWithdrawals.annualTotalIncomeNeeded (adds estimated long-term care)"
            ]
          },
          "savingsRunOut": {
            "note": "Never write a negative balance or a debt. Say when savings run out and how much planned spending would go unpaid. Net worth stays positive only because it includes the home.",
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Savings and investments run out at age 73",
            "value": 1448672.53,
            "period": "planned spending left unpaid by the end of the plan",
            "replaces": [
              "assetDepletion.liquidAssetsAtEndOfPlan",
              "capacity.liquidAssetsAtEndOfPlan"
            ]
          },
          "guaranteedIncome": {
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Guaranteed income in retirement (Social Security, annuities, pensions)",
            "value": 38336.15,
            "period": "average over the 26 years of retirement; years before a benefit starts count as zero"
          },
          "incomeShareOfNeed": {
            "unit": "percent",
            "basis": "today's dollars at the plan date",
            "label": "Share of the yearly retirement spending need that income covers (guaranteed and other income)",
            "value": "25%",
            "period": "average over the 26 years of retirement",
            "replaces": [
              "retirementAndOtherGoals.incomeVsIncomeNeeds.allIncomesVsIncomeNeededExLtcCosts",
              "ratios.guaranteedIncomeRatio.allIncomesVsIncomeNeededExLtcCosts"
            ]
          },
          "netCashFlowThisYear": {
            "note": "Income minus outflows for the plan year.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Net cash flow this year",
            "value": -6417.99,
            "period": "the plan year",
            "notToBeConfusedWith": [
              "averagePortfolioDraw",
              "withdrawalRateThisYear",
              "savingsCapacity"
            ]
          },
          "averagePortfolioDraw": {
            "note": "Counts only the months when spending exceeds every inflow. Required IRA withdrawals and other inflows drawn from savings are not in it, so savings pay more than this. Draws are concentrated in fewer years and are larger in those years. It is not the spending gap: never present it as filling that gap, and never use it to say the plan leans little on savings.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Average yearly draw from savings in retirement",
            "value": 115335.47,
            "period": "average over the 26 years of retirement, counting years with no draw as zero",
            "replaces": [
              "retirementAndOtherGoals.withdrawals.supplementalAnnualWithdrawals"
            ],
            "notToBeConfusedWith": [
              "spendingGap"
            ]
          },
          "withdrawalRateAverage": {
            "note": "A lifetime average. Do not compare it with the 4% sustainable rate.",
            "unit": "percent",
            "basis": "today's dollars at the plan date",
            "label": "Average yearly draw as a share of savings at the start of retirement",
            "value": "12.2%",
            "period": "average over the 26 years of retirement",
            "replaces": [
              "retirementAndOtherGoals.withdrawals.withdrawalRatio"
            ],
            "notToBeConfusedWith": [
              "withdrawalRateThisYear"
            ]
          }
        }
      },
      "ratios": {
        "umbrella": {
          "claim": "Adequately insured",
          "color": "G",
          "currentCoverage": 2000000,
          "recommendedCoverage": 2000000
        },
        "currentDPD": {
          "beforeRetirement": true,
          "yearsInRetirement": 0,
          "avgDTIInRetirement": 0,
          "howMuchInRetirement": "Less than 5 years",
          "avgDTIInRetirementLevel": "<10%"
        },
        "vehiclePRI": {
          "vehiclesPri": 0,
          "monthlyGrossIncome": 20833.33,
          "doTheyHaveAnyVehicle": true,
          "vehiclesMonthlyPayments": 0,
          "doTheyHaveAnyVehicleLoan": false,
          "vehiclesPriFirstThreshold": 0.1,
          "vehiclesPriSecondThreshold": 0.15
        },
        "debtToIncome": {
          "ratio": 0.054,
          "debtOnlyDti": 0,
          "grossIncome": 250000,
          "rentalPayment": 0,
          "mortgagesPayments": 0,
          "monthlyDebtPayments": 0,
          "otherHousingExpenses": 13500,
          "totalMonthlyObligations": 1125,
          "debtPaymentExcludingMortgages": 0
        },
        "housingRatio": {
          "ratio": 0.054,
          "grossIncome": 250000,
          "rentalPayment": 0,
          "housingExpenses": 13500,
          "mortgagePayment": 0,
          "otherHousingExpenses": 13500
        },
        "indebtedness": {
          "debt": false,
          "housing": "own",
          "debtBalance": 0,
          "monthlyDebtPayment": 0,
          "totalMonthlyObligations": 1125
        },
        "savingsLevel": {
          "ratio": 0.24,
          "grossIncome": 250000,
          "savingAmount": 60000
        },
        "emergencyFund": {
          "claim": "Over-reserved",
          "color": "Y",
          "nrOfEarners": 1,
          "emergencyFund": 80000,
          "incomeDisparity": "",
          "monthlyExpenses": 10125,
          "totalCashAmount": 80000,
          "inaccessibleCash": 0,
          "excessOverBaseMax": 19250,
          "extraCashOutflows": [
            {
              "amount": 0,
              "description": "Take a vacation",
              "downpayment": 6000
            },
            {
              "amount": 0,
              "description": "College Ethan",
              "downpayment": 12500
            }
          ],
          "shortfallToBaseMin": "Not applicable",
          "emergencyFundMonths": "8",
          "highestEarningsLevel": "High",
          "shortTermGoalsNeeded": [
            {
              "date": "2027-01-01T00:00:00.000Z",
              "amount": 6000,
              "description": "Take a vacation",
              "paymentFrequency": "ANNUAL"
            },
            {
              "date": "2027-08-01T00:00:00.000Z",
              "amount": 12500,
              "description": "College Ethan",
              "paymentFrequency": "ANNUAL"
            }
          ],
          "excessOverAdjustedMax": 750,
          "maxRecommendedEFMonths": 6,
          "minRecommendedEFMonths": 5,
          "shortfallToAdjustedMin": "Not applicable",
          "totalMoneyMarketAmount": 0,
          "deltaToMaxEmergencyFund": "Not applicable",
          "extraEmergencyFundNeeded": 18500,
          "maxRecommendedEmergencyFund": 60750,
          "maximumEmergencyFundPlusStg": 79250,
          "minRecommendedEmergencyFund": 50625,
          "adjustedRecommendedMaxAmount": 79250,
          "adjustedRecommendedMinAmount": 69125,
          "deltaToMaxEmergencyFundPlusStg": "Not applicable",
          "extraCashAboveMaxEmergencyFund": 19250,
          "extraCashAboveMinEmergencyFund": 29375,
          "cashReservesAfterShortTermCashNeeds": 61500,
          "extraCashAboveMaxEmergencyFundPlusStg": 750,
          "adjustedMonthsCoveredAfterShortTermCashNeeds": 6
        },
        "lifeInsurance": {
          "scenario": {
            "kids": true,
            "earners": 1,
            "spouses": 1,
            "scenario": 22,
            "debtBurden": "",
            "incomeDisparity": ""
          },
          "clientEarner": {
            "overInsured": 12,
            "isHighEarner": true,
            "underInsured": -1,
            "adequatelyInsured": 5,
            "slightlyOverInsured": 10,
            "slightlyUnderInsured": 0
          },
          "clientCoverage": 2000000,
          "coClientCoverage": 0,
          "clientCoverageKey": "Adequately insured",
          "clientEarnedIncome": 250000,
          "clientCoverageColor": "G",
          "coClientCoverageKey": "",
          "coClientEarnedIncome": 0,
          "clientReplacementValue": 0,
          "clientCoverageOverIncome": 8,
          "coClientReplacementValue": 0,
          "coClientCoverageOverIncome": 0,
          "recommendedClientMaxCoverage": 2500000,
          "recommendedClientMinCoverage": 1250000,
          "recommendedCoClientMaxCoverage": 0,
          "recommendedCoClientMinCoverage": 0,
          "lifeInsuranceCoverageGapsAndExcess": {
            "clientExcess": 0,
            "clientShortfall": 0
          }
        },
        "creditCardDebt": {
          "balance": 0,
          "hasDebt": false,
          "monthlyPayment": 0,
          "retirementDate": "2044-07-01T00:00:00.000Z",
          "yearsInRetirement": "Not applicable",
          "maxCCPaymentNormal": 0,
          "minCCPaymentNormal": 0,
          "paymentsEqualToInterest": 0,
          "percentageOfCCOverGrossIncome": 0
        },
        "educationSavings": {
          "totalGAP": 98837.55,
          "goalsSummary": [
            {
              "date": "2026-08-01T00:00:00.000Z",
              "weight": 0.5279,
              "kidsAge": 18,
              "goalName": "College Ethan",
              "termDate": "2030-01-01T00:00:00.000Z",
              "totalGAP": 48468.5,
              "goalAmount": 12500,
              "yearsToStart": -0.25,
              "accountBalance": 0,
              "accountSavings": 0,
              "requiredSavings": -206949.06,
              "requiredExtraSavings": -206949.06,
              "goalRequiredAmountAtToday": 48468.5,
              "expectedCapitalizationAmount": 447.23
            },
            {
              "date": "2028-08-01T00:00:00.000Z",
              "weight": 0.4721,
              "kidsAge": 16,
              "goalName": "College Ava",
              "termDate": "2032-01-01T00:00:00.000Z",
              "totalGAP": 50369.05,
              "goalAmount": 12500,
              "yearsToStart": 1.75,
              "accountBalance": 0,
              "accountSavings": 0,
              "requiredSavings": 27673.49,
              "requiredExtraSavings": 27673.49,
              "goalRequiredAmountAtToday": 50369.05,
              "expectedCapitalizationAmount": 399.93
            }
          ],
          "savingsIncrease": 0.03,
          "expectedPerformance": 0.0776,
          "totalRequiredSavings": -179275.57,
          "current529AccountsBalance": 0,
          "totalEducationGoalsAmount": 25000,
          "totalRequiredExtraSavings": -179275.57,
          "annualSavingsGoingTo529Accounts": 0,
          "doTheyHaveEducationFundingGoals": true,
          "totalEducationGoalRequiredAmountAtToday": 98837.55
        },
        "incomePercentile": {
          "state": "FL",
          "hasSpouse": false,
          "percentile": 0.9,
          "grossIncome": 250000
        },
        "realEstateEquity": {
          "ratio": 1,
          "realEstateAssets": 900000,
          "realEstateEquity": 900000,
          "realEstateMortgages": 0,
          "realEstateEquityThreshold1": 0.2,
          "realEstateEquityThreshold2": 0.5
        },
        "retirementSavings": {
          "generalInflation": 0.03,
          "yearsToRetirement": 17,
          "averagePerformance": 0,
          "requiredExtraSavings": 0,
          "planningGapAtRetirementAge": 0,
          "supplementalTotalWithdrawals": 7521255.19,
          "planningGapAtRetirementAgeInTodaysDollars": 0,
          "balanceInRetirementAccountsAtRetirementAge": 0,
          "supplementalTotalWithdrawalsInTodaysDollars": 2998722.12,
          "balanceInRetirementAccountsAtRetirementAgeInTodaysDollars": 0
        },
        "withdrawalRateRatio": {
          "withdrawalRate": 0.1803,
          "withdrawalRateToday": 0.0727,
          "annualWithdrawalsToday": 30172.67,
          "annualWithdrawalsOnAverage": 289279.05,
          "withdrawalRateAtTodaysValue": 0.1223,
          "totalWithdrawalsDuringRetirement": 7521255.19,
          "investableAssetsAtFirstInRetireYrs": 1604510.57,
          "investableAssetsAt2050YrsAtTodaysValue": 942691.01,
          "annualWithdrawalsOnAverageAtTodaysValue": 115335.47,
          "totalWithdrawalsDuringRetirementAtTodaysValue": 2998722.12
        },
        "investableAssetLevel": {
          "basis": "income",
          "ratio": 1.66,
          "cashBalance": 80000,
          "grossIncome": 250000,
          "annualExpenses": 129600,
          "investableAssets": 335000,
          "portfolioSustainabilityMultiple": 1.66
        },
        "guaranteedIncomeRatio": {
          "inflowsSummary": {
            "name": "All inflows",
            "total": 2628774.08,
            "guaranteedIncome": {
              "name": "Guaranteed income",
              "total": 2628774.08,
              "ANNUITY_INCOME": {
                "name": "Annuity income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "SOCIAL_SECURITY": {
                "name": "Social security",
                "total": 2628774.08,
                "totalAtTodaysValue": 996739.95,
                "yearlyAverageTotal": 101106.7,
                "yearlyAverageTotalAtTodaysValue": 38336.15
              },
              "totalAtTodaysValue": 996739.95,
              "yearlyAverageTotal": 101106.7,
              "PENSION_AND_DEFINED_BENEFIT": {
                "name": "Pension / defined benefit",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "yearlyAverageTotalAtTodaysValue": 38336.15
            },
            "otherIncomeSources": {
              "name": "Other income sources",
              "total": 0,
              "STOCK_COMP": {
                "name": "Stock compensation",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "OTHER_INFLOW": {
                "name": "Other income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "DEFERRED_COMP": {
                "name": "Deferred compensation",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "EARNED_INCOME": {
                "name": "Earned income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "RENTAL_INCOME": {
                "name": "Rental income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "ROYALTY_AND_IP": {
                "name": "Royalty & IP",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "SUPPORT_TRANSFER": {
                "name": "Support & transfer",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "GOVERNMENT_BENEFIT": {
                "name": "Government benefit",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "totalAtTodaysValue": 0,
              "yearlyAverageTotal": 0,
              "BUSINESS_PASSIVE_INCOME": {
                "name": "Business passive income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "PROPERTY_LIQUIDATION_EVENT": {
                "name": "Property liquidation event",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "yearlyAverageTotalAtTodaysValue": 0
            },
            "totalAtTodaysValue": 996739.95,
            "yearlyAverageTotal": 101106.7,
            "yearlyAverageTotalAtTodaysValue": 38336.15
          },
          "outflowsSummary": {
            "name": "Outflows",
            "total": 11283272.36,
            "ltcCosts": {
              "name": "LTC Costs",
              "total": 1133243.09,
              "totalAtTodaysValue": 324375.51,
              "yearlyAverageTotal": 43586.27,
              "yearlyAverageTotalAtTodaysValue": 162187.75
            },
            "excludingLtcCosts": {
              "name": "Excluding LTC Costs",
              "total": 10150029.27,
              "totalAtTodaysValue": 3995462.07,
              "yearlyAverageTotal": 390385.74,
              "yearlyAverageTotalAtTodaysValue": 153671.62
            },
            "totalAtTodaysValue": 4319837.58,
            "yearlyAverageTotal": 433972.01,
            "yearlyAverageTotalAtTodaysValue": 166147.6
          },
          "ltcCostsAreEstimated": true,
          "allIncomesVsIncomeNeeded": 0.2307,
          "otherIncomeVsIncomeNeeded": 0,
          "guaranteedIncomeVsIncomeNeeded": 0.2307,
          "allIncomesVsIncomeNeededExLtcCosts": 0.2495,
          "otherIncomeVsIncomeNeededExLtcCosts": 0,
          "guaranteedIncomeVsIncomeNeededExLtcCosts": 0.2495
        }
      },
      "protection": {
        "emergencyFund": {
          "clientProfile": {
            "kids": [
              {
                "age": 18,
                "name": "Ethan"
              },
              {
                "age": 16,
                "name": "Ava"
              }
            ],
            "clientAge": 47,
            "clientName": "Samantha",
            "numberOfChildren": 2,
            "clientRiskProfile": "(4) Growth",
            "clientIncomeAtRisk": 250000
          },
          "cashAccountList": [
            {
              "name": "Checking Account",
              "type": "Checking account",
              "owner": "Samantha",
              "value": 30000
            },
            {
              "name": "Savings account",
              "type": "Savings account",
              "owner": "Samantha",
              "value": 50000
            }
          ],
          "extraCashOutflows": [
            {
              "amount": 0,
              "description": "Take a vacation",
              "downpayment": 6000
            },
            {
              "amount": 0,
              "description": "College Ethan",
              "downpayment": 12500
            }
          ],
          "realEstateDetails": [
            [
              "Real estate",
              "Market value",
              "Mortgage balance",
              "Equity",
              "HELOC"
            ],
            [
              "Primary home",
              900000,
              0,
              1,
              0
            ]
          ],
          "cashAndExpensesOverview": {
            "cashReserves": 80000,
            "livingExpenses": 9000,
            "housingExpenses": 1125,
            "monthlyExpenses": 10125,
            "totalCashAmount": 80000,
            "otherDebtPayment": 0,
            "totalMoneyMarketAmount": 0,
            "cashReservesAfterShortTermCashNeeds": 61500
          },
          "otherAccountsContributions": [
            [
              "Account",
              "Holder",
              "Current contribution"
            ],
            [
              "Checking Account",
              "Samantha",
              0
            ],
            [
              "Custodial Account (Ava)",
              "Samantha",
              5000
            ],
            [
              "Custodial Account (Ethan)",
              "Samantha",
              5000
            ],
            [
              "Savings account",
              "Samantha",
              10000
            ],
            [
              "Taxable Brokerage",
              "Samantha",
              40000
            ]
          ],
          "retirementAndEducationGaps": {
            "educationGap": 98837.55,
            "retirementGap": 0
          },
          "recommendedEmergencyFundLevels": {
            "maximumAmountRecommended": 60750,
            "maximumMonthsRecommended": 6,
            "minimumAmountRecommended": 50625,
            "minimumMonthsRecommended": 5,
            "extraEmergencyFundNeededByShortTermCashNeeds": 18500,
            "maximumAmountAdjustedAfterShortTermCashNeeds": 79250,
            "minimumAmountAdjustedAfterShortTermCashNeeds": 69125
          },
          "emergencyFundCoverageEvaluation": {
            "monthsCovered": 8,
            "emergencyFundExcess": 19250,
            "emergencyFundShortfall": "Not applicable",
            "adjustedMonthsCoveredAfterShortTermCashNeeds": 6,
            "adjustedEmergencyFundExcessAfterShortTermCashNeeds": 750,
            "adjustedEmergencyFundShortfallAfterShortTermCashNeeds": "Not applicable"
          },
          "taxAdvantagedAccountsContributions": [
            [
              "Account",
              "Holder",
              "Current contribution",
              "Max contribution"
            ],
            [
              "Custodial Account (Ava)",
              "Samantha",
              5000,
              0
            ],
            [
              "Custodial Account (Ethan)",
              "Samantha",
              5000,
              0
            ]
          ]
        },
        "lifeInsurance": {
          "legacyGoal": {
            "amount": "Not applicable",
            "hasLegacyGoal": false
          },
          "educationGoal": [
            [
              "Kid name",
              "Total cost",
              "Inception Year"
            ],
            [
              "Ethan",
              12500,
              "2026"
            ],
            [
              "Ava",
              12500,
              "2028"
            ]
          ],
          "clientDemographics": {
            "kids": [
              {
                "age": 18,
                "name": "Ethan"
              },
              {
                "age": 16,
                "name": "Ava"
              }
            ],
            "clientAge": 47,
            "clientName": "Samantha",
            "numberOfChildren": 2,
            "clientRiskProfile": "(4) Growth",
            "clientIncomeAtRisk": 250000
          },
          "lifeInsuranceCoverageBasics": {
            "hasLifeInsuranceClient": true,
            "lifeInsuranceAmountClient": 2000000
          },
          "lifeInsuranceCoverageGapsAndExcess": {
            "clientExcess": 0,
            "clientShortfall": 0
          },
          "lifeInsuranceCoverageRecommendations": {
            "clientMaxRecommendedCoverage": 2500000,
            "clientMinRecommendedCoverage": 1250000
          }
        },
        "umbrellaInsurance": {
          "assetExposed": {
            "netWorth": 1395000,
            "totalLiquidAssets": 415000,
            "assetExposedSummary": [
              [
                "Asset",
                "Number",
                "Value",
                "Equity"
              ],
              [
                "Real estate",
                1,
                900000,
                900000
              ],
              [
                "Vehicle",
                1,
                80000,
                80000
              ],
              [
                "Total",
                2,
                980000,
                980000
              ]
            ]
          },
          "umbrellaCoverage": {
            "claim": "Adequately insured",
            "hasUmbrellaPolicy": true,
            "umbrellaCoverageAmount": 2000000
          },
          "clientDemographics": {
            "kids": [
              {
                "age": 18,
                "name": "Ethan"
              },
              {
                "age": 16,
                "name": "Ava"
              }
            ],
            "clientAge": 47,
            "clientName": "Samantha",
            "numberOfChildren": 2,
            "clientRiskProfile": "(4) Growth",
            "clientIncomeAtRisk": 250000
          },
          "assetInsuranceStatus": [
            {
              "assetName": "Primary home",
              "assetType": "Real Estate",
              "isInsured": false,
              "equityAmount": 900000
            },
            {
              "assetName": "Porsche Cayenne",
              "assetType": "Vehicle",
              "isInsured": false,
              "equityAmount": 80000
            }
          ],
          "coverageRecommendationsAndAnalysis": {
            "umbrellaCoverageGap": "Not applicable",
            "umbrellaCoverageExcess": "Not applicable",
            "umbrellaMinRecommendedCoverage": 2000000
          }
        }
      },
      "debtManagement": {
        "realEstate": {
          "realEstateEquity": 900000,
          "realEstateEquityThreshold1": 0.2,
          "realEstateEquityThreshold2": 0.5,
          "percentageOfRealEstateEquity": 1
        },
        "listOfDebts": [
          [
            "Name",
            "Type",
            "Balance",
            "Interest rate",
            "Monthly payments",
            "Interest paid"
          ],
          [
            "Amex Gold",
            "Credit card",
            0,
            0,
            0,
            0
          ],
          [
            "Porsche Cayenne",
            "Other liability",
            0,
            0,
            0,
            0
          ]
        ],
        "debtOverview": {
          "debt": false,
          "debtBalance": 0,
          "beforeRetirement": "Not applicable",
          "avgDtiInRetirement": 0,
          "percentageOfDebtOverGrossIncome": 0
        },
        "clientProfile": {
          "clientName": "Samantha"
        },
        "creditCardDebt": {
          "retirementDate": "2044-07-01T00:00:00.000Z",
          "ccMonthlyPayment": 0,
          "creditCardBalance": 0,
          "yearsInRetirement": "Not applicable",
          "maxCcPaymentNormal": 0,
          "minCcPaymentNormal": 0,
          "ccPaymentEqualToInterestRate": 0
        },
        "vehiclePayment": {
          "vehiclesPri": 0,
          "doTheyHaveAnyVehicle": true,
          "vehiclesMonthlyPayments": 0
        },
        "housingExpenses": {
          "rentVsOwn": "Own",
          "housingRatio": 0.054,
          "rentalPayment": 0,
          "housingExpenses": 1125,
          "mortgagePayment": 0,
          "otherHousingExpenses": 1125,
          "housingRatioFirstThreshold": 0.28,
          "housingRatioSecondThreshold": 0.32
        },
        "savingsAndCashflow": {
          "annualCashFlow": -6417.99,
          "annualSavingsRate": 0.24,
          "annualSavingsAmount": 60000
        },
        "debtToIncomeAndMonthlyObligations": {
          "dti": 0.054,
          "debtOnlyDti": 0,
          "grossIncome": 250000,
          "dtiFirstThreshold": 0.36,
          "dtiThirdThreshold": 0.5,
          "dtiSecondThreshold": 0.43,
          "monthlyGrossIncome": 20833.33,
          "monthlyDebtPayments": 0,
          "totalMonthlyObligations": 1125,
          "percentageOfDebtOverGrossIncome": 0
        }
      },
      "cashflowStatement": {
        "inflows": {
          "items": [
            {
              "name": "Earned income",
              "items": [
                {
                  "name": "Salary and wages",
                  "joint": 0,
                  "total": 250000,
                  "client": 250000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "total": 250000,
              "client": 250000,
              "coClient": 0
            }
          ],
          "joint": 0,
          "total": 250000,
          "client": 250000,
          "coClient": 0
        },
        "outflows": {
          "items": [
            {
              "name": "Expenses",
              "items": [
                {
                  "name": "Living Expenses",
                  "joint": 0,
                  "total": 108000,
                  "client": 108000,
                  "coClient": 0
                },
                {
                  "name": "Insurance payments",
                  "joint": 0,
                  "total": 8100,
                  "client": 8100,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "total": 116100,
              "client": 116100,
              "coClient": 0
            },
            {
              "name": "Taxes",
              "items": [
                {
                  "name": "Federal Income Tax",
                  "joint": 0,
                  "total": 51303.99,
                  "client": 51303.99,
                  "coClient": 0
                },
                {
                  "name": "FICA tax",
                  "joint": 0,
                  "total": 15514,
                  "client": 15514,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "total": 66817.99,
              "client": 66817.99,
              "coClient": 0
            },
            {
              "name": "Savings",
              "items": [
                {
                  "name": "Brokerage account savings",
                  "joint": 0,
                  "total": 40000,
                  "client": 40000,
                  "coClient": 0
                },
                {
                  "name": "Cash savings",
                  "joint": 0,
                  "total": 10000,
                  "client": 10000,
                  "coClient": 0
                },
                {
                  "name": "Custodial UGMA savings",
                  "joint": 0,
                  "total": 10000,
                  "client": 10000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "total": 60000,
              "client": 60000,
              "coClient": 0
            },
            {
              "name": "Housing Expenses",
              "items": [
                {
                  "name": "Property Taxes",
                  "joint": 0,
                  "total": 9000,
                  "client": 9000,
                  "coClient": 0
                },
                {
                  "name": "Home Insurance",
                  "joint": 0,
                  "total": 4500,
                  "client": 4500,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "total": 13500,
              "client": 13500,
              "coClient": 0
            }
          ],
          "joint": 0,
          "total": 256417.99,
          "client": 256417.99,
          "coClient": 0
        },
        "freeCashflow": {
          "joint": 0,
          "total": -6417.99,
          "client": -6417.99,
          "coClient": 0
        }
      },
      "netWorthStatement": {
        "assets": {
          "name": "Assets",
          "type": "MAIN",
          "items": [
            {
              "name": "Cash account",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Savings account",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 50000,
                  "client": 50000,
                  "coClient": 0,
                  "annualSavings": 10000,
                  "clientSavings": 10000,
                  "annualMatching": 0,
                  "portfolioTypeName": "Savings account"
                },
                {
                  "name": "Checking Account",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 30000,
                  "client": 30000,
                  "coClient": 0,
                  "annualSavings": 0,
                  "clientSavings": 0,
                  "annualMatching": 0,
                  "portfolioTypeName": "Checking account"
                }
              ],
              "joint": 0,
              "order": 1,
              "total": 80000,
              "client": 80000,
              "coClient": 0,
              "totalDebts": 0
            },
            {
              "name": "Investment account",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Taxable",
                  "type": "INDIVIDUAL",
                  "items": [
                    {
                      "name": "Taxable Brokerage",
                      "type": "PORTFOLIO",
                      "joint": 0,
                      "total": 300000,
                      "client": 300000,
                      "coClient": 0,
                      "annualSavings": 40000,
                      "clientSavings": 40000,
                      "annualMatching": 0,
                      "portfolioTypeName": "Brokerage account"
                    },
                    {
                      "name": "Custodial Account (Ethan)",
                      "type": "PORTFOLIO",
                      "joint": 0,
                      "total": 20000,
                      "client": 20000,
                      "coClient": 0,
                      "annualSavings": 5000,
                      "clientSavings": 5000,
                      "annualMatching": 0,
                      "portfolioTypeName": "Custodial UGMA"
                    },
                    {
                      "name": "Custodial Account (Ava)",
                      "type": "PORTFOLIO",
                      "joint": 0,
                      "total": 15000,
                      "client": 15000,
                      "coClient": 0,
                      "annualSavings": 5000,
                      "clientSavings": 5000,
                      "annualMatching": 0,
                      "portfolioTypeName": "Custodial UGMA"
                    }
                  ],
                  "joint": 0,
                  "total": 335000,
                  "client": 335000,
                  "coClient": 0
                },
                {
                  "name": "Tax-free",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 0,
                  "client": 0,
                  "coClient": 0
                },
                {
                  "name": "Tax-deferred",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 0,
                  "client": 0,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 2,
              "total": 335000,
              "client": 335000,
              "coClient": 0,
              "totalDebts": 0
            },
            {
              "name": "Stock compensation",
              "type": "CATEGORY",
              "joint": 0,
              "order": 3,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Annuity",
              "type": "CATEGORY",
              "joint": 0,
              "order": 4,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Insurance (Cash value)",
              "type": "CATEGORY",
              "joint": 0,
              "order": 5,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Business",
              "type": "CATEGORY",
              "joint": 0,
              "order": 6,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Real estate",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Primary home",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 900000,
                  "client": 900000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 7,
              "total": 900000,
              "client": 900000,
              "coClient": 0,
              "totalDebts": 0
            },
            {
              "name": "Vehicle",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Porsche Cayenne",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 80000,
                  "client": 80000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 8,
              "total": 80000,
              "client": 80000,
              "coClient": 0,
              "totalDebts": 0
            },
            {
              "name": "Other asset",
              "type": "CATEGORY",
              "joint": 0,
              "order": 9,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "totalDebts": 0
            }
          ],
          "joint": 0,
          "total": 1395000,
          "client": 1395000,
          "coClient": 0,
          "totalDebts": 0
        },
        "netWorth": {
          "joint": 0,
          "total": 1395000,
          "client": 1395000,
          "coClient": 0
        },
        "liabilities": {
          "name": "Liabilities",
          "type": "MAIN",
          "items": [
            {
              "name": "Credit card",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Amex Gold",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 0,
                  "client": 0,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 1,
              "total": 0,
              "client": 0,
              "coClient": 0
            },
            {
              "name": "Student loan",
              "type": "CATEGORY",
              "joint": 0,
              "order": 2,
              "total": 0,
              "client": 0,
              "coClient": 0
            },
            {
              "name": "Business loan",
              "type": "CATEGORY",
              "joint": 0,
              "order": 3,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true
            },
            {
              "name": "Personal loan",
              "type": "CATEGORY",
              "joint": 0,
              "order": 4,
              "total": 0,
              "client": 0,
              "coClient": 0
            },
            {
              "name": "Investment loan",
              "type": "CATEGORY",
              "joint": 0,
              "order": 5,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true
            },
            {
              "name": "Real estate debt",
              "type": "CATEGORY",
              "joint": 0,
              "order": 6,
              "total": 0,
              "client": 0,
              "coClient": 0
            },
            {
              "name": "Other debt",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Porsche Cayenne",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 0,
                  "client": 0,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 7,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true
            }
          ],
          "joint": 0,
          "total": 0,
          "client": 0,
          "coClient": 0
        }
      },
      "savingsAndExpenses": {
        "goals": {
          "clientRetirementAge": 65,
          "shortTermGoalsCashNeeds": 18500,
          "doTheyHaveEducationFundingGoals": true,
          "totalEducationGoalRequiredAmount": 25000
        },
        "annualSavings": {
          "currentAnnualSavingsAtHSA": 0,
          "currentAnnualSavingsAtHSARate": 0,
          "currentAnnualSavingsAt529Accounts": 0,
          "requiredRetirementExtraAnnualSavings": 0,
          "currentAnnualSavingsAt529AccountsRate": 0,
          "currentAnnualSavingsAtTaxableAccounts": 50000,
          "gapInRetirementAccountsAtRetirementAge": 0,
          "requiredAnnualSavingsAtTaxableAccounts": 50000,
          "requiredExtraAnnualSavingsForEducation": -179275.57,
          "currentAnnualSavingsAtRetirementAccounts": 0,
          "requiredRetirementExtraAnnualSavingsRate": 0,
          "currentAnnualSavingsAtTaxableAccountsRate": 0.2,
          "requiredAnnualSavingsAtTaxableAccountsRate": 0.2,
          "requiredExtraAnnualSavingsForEducationRate": -0.7171,
          "currentAnnualSavingsAtRetirementAccountsRate": 0
        },
        "clientProfile": {
          "clientAge": 47,
          "clientName": "Samantha",
          "numberOfChildren": 2,
          "stateOfResidence": "Florida",
          "clientRiskProfile": "(4) Growth",
          "maximumAgeOfChildren": 18,
          "minimumAgeOfChildren": 16
        },
        "otherExpenses": {
          "lifeInsuranceGap": 0,
          "umbrellaInsuranceGap": 0
        },
        "liquidityContext": {
          "shortTermNeeds": 18500,
          "emergencyFundInCash": 80000,
          "emergencyFundInMonths": "8",
          "maxEmergencyFundTargetInCash": 60750,
          "minEmergencyFundTargetInCash": 50625,
          "maxEmergencyFundTargetInMonths": 6,
          "minEmergencyFundTargetInMonths": 5,
          "gapWithRecommendedMinEmergencyFund": "Not applicable",
          "excessWithRecommendedMaxEmergencyFund": 19250,
          "maxEmergencyFundTargetAndShortTermNeeds": 79250,
          "minEmergencyFundTargetAndShortTermNeeds": 69125,
          "gapWithRecommendedMinEmergencyFundAndShortTermNeeds": "Not applicable",
          "excessWithRecommendedMaxEmergencyFundAndShortTermNeeds": 750
        },
        "advantagedSavings": {
          "hsaMaxContributions": 4400,
          "hsaClientCanContribute": true,
          "hsaClientContributions": 0,
          "client401kCanContribute": "Unknown",
          "iraClientMaxContributions": 7500,
          "rothIraClientCanContribute": false,
          "rothIraClientContributions": 0,
          "rothIraClientMaxContributions": 0,
          "traditionalIraClientContributions": 0,
          "client401kContributionsMaxEmployerMatch": "Unknown",
          "traditionalIraClientCanDeductContributions": true,
          "traditionalIraClientMaxDeductibleContributions": 7500
        },
        "incomeAndCashflow": {
          "incomeSummary": [
            [
              "Category",
              "Value",
              "Percentage"
            ],
            [
              "Earned income - Client",
              250000,
              1
            ],
            [
              "Total",
              250000,
              1
            ]
          ],
          "annualCashflow": -6417.99,
          "outflowSummary": [
            [
              "Category",
              "Value",
              "Percentage"
            ],
            [
              "Taxes",
              66817.99,
              0.2673
            ],
            [
              "Housing Expenses",
              13500,
              0.054
            ],
            [
              "Savings",
              60000,
              0.24
            ],
            [
              "Expenses",
              116100,
              0.4644
            ],
            [
              "Total",
              256417.99,
              1.0257
            ]
          ],
          "annualCashflowPercentage": -0.0257,
          "householdIncomePercentile": 0.9
        },
        "housingInformation": {
          "rentVsOwn": "Own",
          "rentalPayment": 0,
          "housingExpenses": 1125,
          "mortgagePayment": 0,
          "otherHousingExpenses": 1125
        },
        "debtRatiosAndHealth": {
          "dti": 0.054,
          "housingRatio": 0.054,
          "housingExpenses": 1125,
          "dtiFirstThreshold": 0.36,
          "dtiThirdThreshold": 0.5,
          "dtiSecondThreshold": 0.43,
          "totalMonthlyObligations": 1125,
          "housingRatioFirstThreshold": 0.28,
          "housingRatioSecondThreshold": 0.32,
          "percentageOfDebtOverGrossIncome": 0
        },
        "shortTermGoalsNeeded": [
          {
            "date": "2027-01-01T00:00:00.000Z",
            "amount": 6000,
            "description": "Take a vacation",
            "paymentFrequency": "ANNUAL"
          },
          {
            "date": "2027-08-01T00:00:00.000Z",
            "amount": 12500,
            "description": "College Ethan",
            "paymentFrequency": "ANNUAL"
          }
        ]
      },
      "assetsAndInvestments": {
        "withdrawals": {
          "rmdStartAge": 75,
          "rmdStartYear": 2054,
          "averageWithdrawalsDuringRmds": 104125.05,
          "yearsPayingMoreRmdsThanRequiredWithoutSavings": 0,
          "yearsPayingMoreRmdsThanRequiredWithCurrentSavings": 0
        },
        "listOfAssets": [
          [
            "Asset type",
            "Number of assets",
            "Asset value",
            "% of total assets",
            "Equity value",
            "% of Net worth"
          ],
          [
            "Cash account",
            2,
            80000,
            0.0573,
            80000,
            0.0573
          ],
          [
            "Investment account",
            3,
            335000,
            0.2401,
            335000,
            0.2401
          ],
          [
            "Real estate",
            1,
            900000,
            0.6452,
            900000,
            0.6452
          ],
          [
            "Vehicle",
            1,
            80000,
            0.0573,
            80000,
            0.0573
          ],
          [
            "Other asset",
            0,
            0,
            0,
            0,
            0
          ]
        ],
        "clientProfile": {
          "clientAge": 47,
          "clientName": "Samantha",
          "clientRiskProfile": "(4) Growth",
          "clientRetirementAge": 65
        },
        "contributions": {
          "IRAContributions": [
            [
              "IRA contributions (Traditional + Roth)",
              "Client"
            ],
            [
              "Max IRA contribution (Traditional + Roth)",
              7500
            ],
            [
              "IRA catch-up (age 50+)",
              "Not applicable"
            ],
            [
              "Total possible IRA contribution",
              7500
            ],
            [
              "Roth IRA eligible amount (estimate)",
              "Not applicable"
            ]
          ],
          "hsaContributions": {
            "catchUpForClient": "Not applicable",
            "maxContributions": 4400,
            "totalPossibleContribution": 4400
          },
          "employerPlanContributions": [
            [
              "Employer plan contributions (401k, 403b, etc)",
              "Client"
            ],
            [
              "Max employee contribution",
              24500
            ],
            [
              "Catch up (age 50+)",
              "Not applicable"
            ],
            [
              "Super catch up (age 60-63)",
              "Not applicable"
            ],
            [
              "Total possible employee contribution",
              24500
            ]
          ]
        },
        "educationGoal": {
          "hasAnEducationGoal": true
        },
        "listOfAccounts": [
          [
            "Account",
            "Client",
            "Number",
            "Balance",
            "Annual contribution"
          ],
          [
            "Brokerage account",
            "Samantha",
            1,
            300000,
            40000
          ],
          [
            "Cash/savings",
            "Samantha",
            2,
            80000,
            10000
          ],
          [
            "Custodial UGMA",
            "Samantha",
            2,
            35000,
            10000
          ]
        ],
        "incomeAndTaxation": {
          "taxRates": [
            [
              "Tax rate",
              "Current",
              "Expected at retirement"
            ],
            [
              "Federal ordinary tax rate",
              0.32,
              0.24
            ],
            [
              "State tax rate",
              0,
              0
            ],
            [
              "NIIT tax rate",
              0.038,
              0.038
            ],
            [
              "Effective ordinary tax rate",
              0.358,
              0.278
            ]
          ],
          "taxableIncome": {
            "totalTaxableIncome": 233899.96
          },
          "totalGrossIncome": 250000,
          "clientGrossIncome": 250000,
          "coClientGrossIncome": 0
        },
        "educationGoalNeeds": {
          "current529Balance": 0,
          "educationGoalAmount": 25000,
          "target529Contributions": -179275.57,
          "current529Contributions": 0
        },
        "retirementGlidePath": {
          "retirementGlidePathForClient": "80% equity and 20% fixed income",
          "retirementGlideEquityForClient": 0.7999,
          "retirementGlideFixedIncomeForClient": 0.2001
        },
        "totalAssetsAndEquity": {
          "totalAssets": 1395000,
          "totalEquity": 1395000
        },
        "realEstateAndMortgage": {
          "mortgageBalance": 0,
          "realEstateEquity": 1,
          "realEstateEquityThreshold1": 0.2,
          "realEstateEquityThreshold2": 0.5
        },
        "listOfRealEstateAssets": [
          [
            "Real estate",
            "Value",
            "Debt amount",
            "Debt %",
            "Equity amount",
            "Equity %"
          ],
          [
            "Primary home",
            900000,
            0,
            0,
            900000,
            1
          ]
        ],
        "percentageOfCashThreshold": 0.5,
        "listOfChildrenAndEducationGoals": [
          [
            "Student",
            "Age",
            "Education goal timeframe",
            "Years to uni",
            "Education goal ($)",
            "Target equity allocation in 529 account",
            "Target fixed income in 529 account"
          ],
          [
            "Ethan",
            18,
            "2026 - 2030",
            0,
            12500,
            0.25,
            0.75
          ],
          [
            "Ava",
            16,
            "2028 - 2032",
            1,
            12500,
            0.25,
            0.75
          ]
        ]
      },
      "retirementAndOtherGoals": {
        "otherIncome": [
          [
            "Income source",
            "Total value",
            "Yearly average value"
          ],
          [
            "Total other income",
            0,
            0
          ]
        ],
        "withdrawals": {
          "withdrawalRatio": 0.1223,
          "supplementalTotalWithdrawals": 2998722.12,
          "supplementalAnnualWithdrawals": 115335.47
        },
        "clientProfile": {
          "clientAge": 47,
          "clientName": "Samantha",
          "endOfPlanAge": 91,
          "clientRiskProfile": "(4) Growth",
          "clientRetirementAge": 65
        },
        "assetDepletion": {
          "netWorthAtEndOfPlan": -33615.09,
          "requiredRetirementAge": 90,
          "liquidAssetsAtEndOfPlan": -1448672.53,
          "shortfallInNumberOfYears": 1,
          "ageWhenTheyRunOutOfNetWorth": 90,
          "ageWhenTheyRunOutOfLiquidAssets": 73
        },
        "guaranteedIncome": [
          [
            "Income source",
            "Total value",
            "Yearly average value"
          ],
          [
            "Social security",
            996739.95,
            38336.15
          ],
          [
            "Annuity income",
            0,
            0
          ],
          [
            "Pension / defined benefit",
            0,
            0
          ],
          [
            "Total guaranteed income",
            996739.95,
            38336.15
          ]
        ],
        "incomeVsIncomeNeeds": {
          "allIncomesVsIncomeNeeded": 0.2307,
          "otherIncomeVsIncomeNeeded": 0,
          "guaranteedIncomeVsIncomeNeeded": 0.2307,
          "allIncomesVsIncomeNeededExLtcCosts": 0.2495,
          "otherIncomeVsIncomeNeededExLtcCosts": 0,
          "guaranteedIncomeVsIncomeNeededExLtcCosts": 0.2495
        },
        "otherGoalsAndLegacy": {
          "legacyGoal": false,
          "legacyGoalGap": "Not applicable",
          "legacyGoalAmount": "Not applicable",
          "achievesLegacyGoals": "Not applicable",
          "otherGoalsAfterRetirement": true,
          "otherGoalsAfterRetirementAmount": 460651.34
        },
        "netWorthAtRetirement": {
          "netWorthAtRetirementAge": 2174335.48,
          "liquidAssetsAtRetirementAge": 954768.98,
          "nonLiquidAssetsAtRetirementAge": 1219566.5
        },
        "incomeNeedsAndWithdrawals": {
          "totalLtcCosts": 324375.51,
          "annualLtcCosts": 162187.75,
          "totalIncomeNeeded": 4319837.58,
          "ltcCostsAreEstimated": true,
          "annualTotalIncomeNeeded": 166147.6,
          "totalIncomeNeededExLtcCosts": 3995462.07,
          "annualTotalIncomeNeededExLtcCosts": 153671.62
        }
      },
      "taxDragAnalysis": {
        "householdRollup": [
          [
            "Metric",
            "Value",
            "Notes"
          ],
          [
            "Total annual tax cost (Table 2)",
            3032.2,
            "All taxable-account rows, including money-market positions."
          ],
          [
            "Money-market drag routed to Cash sub-task",
            0,
            "Money-market positions stay visible here but are carved out of the in-scope Tax Drag total."
          ],
          [
            "In-scope tax cost (Table 2 ex-MM)",
            3032.2,
            "Standalone Tax Drag total after routing money-market drag to Cash."
          ],
          [
            "Total annual tax cost saved (Table 3)",
            0,
            "Permanent annual tax saved if those holdings were taxable today."
          ],
          [
            "Total annual tax cost deferred (Table 4)",
            0,
            "Deferred, not eliminated; future withdrawals remain taxable on exit."
          ],
          [
            "NIIT contribution to Table 2",
            330.44,
            "Taxable net-investment components multiplied by the current NIIT rate."
          ]
        ],
        "accountTypeInputs": [
          [
            "#",
            "Account name",
            "Account type",
            "Tax treatment"
          ],
          [
            "1",
            "Checking Account",
            "Checking account",
            "Taxable"
          ],
          [
            "2",
            "Savings account",
            "Savings account",
            "Taxable"
          ],
          [
            "3",
            "Custodial Account (Ava)",
            "Custodial UGMA",
            "Taxable"
          ],
          [
            "4",
            "Custodial Account (Ethan)",
            "Custodial UGMA",
            "Taxable"
          ],
          [
            "5",
            "Taxable Brokerage",
            "Brokerage account",
            "Taxable"
          ]
        ],
        "effectiveTaxMargin": [
          [
            "Component",
            "Rate",
            "Source / Trigger",
            "Applies to"
          ],
          [
            "Federal ordinary",
            "32%",
            "FH metrics — currentTaxBracket",
            "Ordinary income, ST cap gains, ST cap gain distributions, ordinary interest, non-qualified dividends"
          ],
          [
            "Federal LTCG",
            "15%",
            "PW-computed federal LTCG (2026 thresholds; taxable-income proxy)",
            "Qualified dividends, LT cap gains, LT cap gain distributions"
          ],
          [
            "State (FL)",
            "0%",
            "FH metrics — stateTaxRate (FL)",
            "All investment income (state rules)"
          ],
          [
            "NIIT",
            "3.8%",
            "Triggered: income $233,900 > $200K Single",
            "All net investment income"
          ],
          [
            "Total taxable income",
            "$233,900",
            "FH metrics — taxableIncome.totalTaxableIncome",
            "Debug input for LTCG and NIIT lookups"
          ],
          [
            "MAGI proxy",
            "$233,900",
            "Current tax-margin logic — reuse taxableIncome.totalTaxableIncome as MAGI proxy",
            "Debug input for NIIT and current LTCG threshold lookup"
          ],
          [
            "State input",
            "FL — Florida",
            "PW params — state.code / state.name",
            "Debug input for state marginal-rate lookup"
          ],
          [
            "Expected retirement ordinary",
            "24%",
            "FH metrics — expectedTaxBracketInRetirement",
            "Future withdrawals from tax-deferred accounts"
          ],
          [
            "Effective ordinary rate",
            "35.8%",
            "32% + 0% + 3.8%",
            "Today's ordinary-rate income"
          ],
          [
            "Effective LTCG rate",
            "18.8%",
            "15% + 0% + 3.8%",
            "Today's LTCG-rate income"
          ]
        ],
        "fundHoldingsInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Morningstar category",
            "Balance",
            "Shares",
            "Estimated shares",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Interest income ($/share)",
            "Tax-free income ($/share)",
            "LT cap gain ($/share)",
            "ST cap gain ($/share)",
            "Ordinary-rate share (non-qual div + interest + ST cap gain) / total distribution",
            "Tax cost ratio",
            "Turnover",
            "PCGE"
          ],
          [
            "1",
            "Custodial Account (Ava)",
            "VTI",
            "Large Blend",
            10000,
            27.63,
            "-",
            "$0.86",
            "$2.897",
            "$0",
            "$0",
            "$0",
            "$0",
            "77.11%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "2",
            "Custodial Account (Ethan)",
            "VTI",
            "Large Blend",
            12000,
            33.16,
            "-",
            "$0.86",
            "$2.897",
            "$0",
            "$0",
            "$0",
            "$0",
            "77.11%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "3",
            "Taxable Brokerage",
            "VTI",
            "Large Blend",
            140000,
            386.88,
            "-",
            "$0.86",
            "$2.897",
            "$0",
            "$0",
            "$0",
            "$0",
            "77.11%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "4",
            "Taxable Brokerage",
            "VWO",
            "Diversified Emerging Markets",
            30000,
            541.91,
            "-",
            "$0.168",
            "$1.329",
            "$0",
            "$0",
            "$0",
            "$0",
            "88.77%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "5",
            "Custodial Account (Ava)",
            "SCHD",
            "Large Value",
            5000,
            142.13,
            "-",
            "$0",
            "$1.048",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "6",
            "Taxable Brokerage",
            "JNK",
            "High Yield Bond",
            50000,
            539.97,
            "-",
            "$0",
            "$6.358",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "7",
            "Custodial Account (Ethan)",
            "SCHD",
            "Large Value",
            8000,
            227.4,
            "-",
            "$0",
            "$1.048",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "8",
            "Taxable Brokerage",
            "SCHD",
            "Large Value",
            80000,
            2274.02,
            "-",
            "$0",
            "$1.048",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ]
        ],
        "stockHoldingsInputs": [
          [
            "#",
            "Account",
            "Name",
            "Ticker",
            "Sector",
            "Industry",
            "Country",
            "Balance",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Dividend yield TTM"
          ]
        ],
        "taxFreeAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable)",
            "Annual tax cost saved"
          ],
          [
            "1",
            "No Tax-Free accounts in household",
            "-",
            0,
            "-",
            0,
            "-",
            0
          ],
          [
            "Total",
            "Total tax-free",
            "-",
            0,
            "-",
            0,
            "-",
            0
          ]
        ],
        "taxableAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate",
            "Annual tax cost"
          ],
          [
            "1a",
            "Custodial Account (Ava)",
            "VTI",
            10000,
            "Qualified dividend",
            23.76,
            "18.8%",
            4.4669
          ],
          [
            "1b",
            "Custodial Account (Ava)",
            "VTI",
            10000,
            "Non-qualified dividend",
            80.05,
            "35.8%",
            28.66
          ],
          [
            "1c",
            "Custodial Account (Ava)",
            "VTI",
            10000,
            "Subtotal",
            103.81,
            "-",
            33.13
          ],
          [
            "2a",
            "Custodial Account (Ethan)",
            "VTI",
            12000,
            "Qualified dividend",
            28.51,
            "18.8%",
            5.3603
          ],
          [
            "2b",
            "Custodial Account (Ethan)",
            "VTI",
            12000,
            "Non-qualified dividend",
            96.06,
            "35.8%",
            34.39
          ],
          [
            "2c",
            "Custodial Account (Ethan)",
            "VTI",
            12000,
            "Subtotal",
            124.57,
            "-",
            39.75
          ],
          [
            "3a",
            "Taxable Brokerage",
            "VTI",
            140000,
            "Qualified dividend",
            332.64,
            "18.8%",
            62.54
          ],
          [
            "3b",
            "Taxable Brokerage",
            "VTI",
            140000,
            "Non-qualified dividend",
            1120.71,
            "35.8%",
            401.21
          ],
          [
            "3c",
            "Taxable Brokerage",
            "VTI",
            140000,
            "Subtotal",
            1453.35,
            "-",
            463.75
          ],
          [
            "4a",
            "Taxable Brokerage",
            "VWO",
            30000,
            "Qualified dividend",
            91.14,
            "18.8%",
            17.13
          ],
          [
            "4b",
            "Taxable Brokerage",
            "VWO",
            30000,
            "Non-qualified dividend",
            720.26,
            "35.8%",
            257.85
          ],
          [
            "4c",
            "Taxable Brokerage",
            "VWO",
            30000,
            "Subtotal",
            811.4,
            "-",
            274.99
          ],
          [
            "5",
            "Custodial Account (Ava)",
            "SCHD",
            5000,
            "Non-qualified dividend",
            148.89,
            "35.8%",
            53.3
          ],
          [
            "6",
            "Taxable Brokerage",
            "JNK",
            50000,
            "Non-qualified dividend",
            3433.37,
            "35.8%",
            1229.15
          ],
          [
            "7",
            "Custodial Account (Ethan)",
            "SCHD",
            8000,
            "Non-qualified dividend",
            238.23,
            "35.8%",
            85.29
          ],
          [
            "8",
            "Taxable Brokerage",
            "SCHD",
            80000,
            "Non-qualified dividend",
            2382.26,
            "35.8%",
            852.85
          ],
          [
            "Total",
            "Total taxable",
            "-",
            335000,
            "-",
            8695.88,
            "-",
            3032.2
          ]
        ],
        "costBasisBlockingNotes": [
          [
            "Account",
            "Blocking note"
          ],
          [
            "Custodial Account (Ava)",
            "Implementation of Custodial Account (Ava) cannot be responsibly sequenced without tax-lot data."
          ],
          [
            "Custodial Account (Ethan)",
            "Implementation of Custodial Account (Ethan) cannot be responsibly sequenced without tax-lot data."
          ],
          [
            "Taxable Brokerage",
            "Implementation of Taxable Brokerage cannot be responsibly sequenced without tax-lot data."
          ]
        ],
        "taxableCostBasisInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Balance (market value)",
            "Cost basis",
            "Unrealized gain",
            "Holding period",
            "Notes"
          ],
          [
            "1",
            "Custodial Account (Ava)",
            "VTI",
            10000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "2",
            "Custodial Account (Ethan)",
            "VTI",
            12000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "3",
            "Taxable Brokerage",
            "VTI",
            140000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "4",
            "Taxable Brokerage",
            "VWO",
            30000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "5",
            "Custodial Account (Ava)",
            "SCHD",
            5000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "6",
            "Taxable Brokerage",
            "JNK",
            50000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "7",
            "Custodial Account (Ethan)",
            "SCHD",
            8000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "8",
            "Taxable Brokerage",
            "SCHD",
            80000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "Total",
            "Total taxable",
            "-",
            335000,
            "[missing cost basis]",
            "[missing cost basis]",
            "-",
            "Totals stay blocked until missing tax-lot inputs are filled."
          ]
        ],
        "taxDeferredAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable today)",
            "Annual tax cost deferred"
          ],
          [
            "1",
            "No Tax-Deferred accounts in household",
            "-",
            0,
            "-",
            0,
            "-",
            0
          ],
          [
            "Total",
            "Total tax-deferred",
            "-",
            0,
            "-",
            0,
            "-",
            0
          ]
        ],
        "componentTaxTreatmentMatrix": [
          [
            "Component",
            "Federal rate type",
            "Effective household rate today",
            "Taxable accounts",
            "Tax-free accounts",
            "Tax-deferred accounts",
            "Notes"
          ],
          [
            "Qualified dividend",
            "LTCG",
            "18.8%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for US common stock and treaty-country foreign names; funds keep the precomputed Morningstar qualified split."
          ],
          [
            "Non-qualified dividend",
            "ORDINARY",
            "35.8%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for REIT and non-treaty foreign names, while MLP distributions are treated as ROC; funds keep the precomputed Morningstar non-qualified split."
          ],
          [
            "Interest income",
            "ORDINARY",
            "35.8%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Money-market and bond-style fund income is treated as ordinary-rate income."
          ],
          [
            "Tax-free income",
            "Tax-exempt federal",
            "0%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Current phase assumes a 0% effective rate because state-specific muni exposure is not available in the data path."
          ],
          [
            "LT cap gain distribution",
            "LTCG",
            "18.8%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed long-term capital gains use the LTCG household rate."
          ],
          [
            "ST cap gain distribution",
            "ORDINARY",
            "35.8%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed short-term capital gains use the ordinary household rate."
          ]
        ]
      },
      "realEstate": {
        "realEstateEquity": 900000,
        "realEstateEquityThreshold1": 0.2,
        "realEstateEquityThreshold2": 0.5,
        "percentageOfRealEstateEquity": 1
      },
      "savingsRate": null,
      "educationGoalNeeds": {
        "current529Balance": 0,
        "educationGoalAmount": 25000,
        "target529Contributions": -179275.57,
        "current529Contributions": 0
      }
    },
    "savingsWaterfall": [
      {
        "step": 1,
        "bucket": "Build minimum emergency threshold (3 months)",
        "current": 80000,
        "target": 30375,
        "status": "Filled",
        "delta": 49625,
        "flag": "",
        "notes": ""
      },
      {
        "step": 2,
        "bucket": "Address essential insurance gaps",
        "current": 4000000,
        "target": 3250000,
        "status": "Filled",
        "delta": 750000,
        "flag": "",
        "notes": ""
      },
      {
        "step": 3,
        "bucket": "Set aside cash for near-term goals",
        "current": 49625,
        "target": 18500,
        "status": "Filled",
        "delta": 31125,
        "flag": "",
        "notes": ""
      },
      {
        "step": 4,
        "bucket": "Maximize employer match — primary plan",
        "current": "N/A",
        "target": "",
        "status": ""
      },
      {
        "step": 5,
        "bucket": "Maximize employer match — secondary plan",
        "current": "N/A",
        "target": "",
        "status": ""
      },
      {
        "step": 6,
        "bucket": "Maximize HSA match",
        "current": "N/A",
        "target": "",
        "status": ""
      },
      {
        "step": 7,
        "bucket": "Maximize ESPP (Employee Stock Purchase Plan)",
        "current": "N/A",
        "target": "",
        "status": ""
      },
      {
        "step": 8,
        "bucket": "Pay high-interest debt (>7%)",
        "current": 0,
        "target": 0,
        "status": "Filled",
        "delta": 0,
        "flag": "",
        "notes": ""
      },
      {
        "step": 9,
        "bucket": "Build toward maximum emergency threshold (6 months)",
        "current": 61500,
        "target": 60750,
        "status": "Filled",
        "delta": 750,
        "flag": "",
        "notes": ""
      },
      {
        "step": 10,
        "bucket": "Contribute to Roth IRA",
        "current": 0,
        "target": "N/A",
        "status": "",
        "delta": ""
      },
      {
        "step": 11,
        "bucket": "Maximize HSA",
        "current": 0,
        "target": 4400,
        "status": "Empty",
        "delta": -4400,
        "flag": "",
        "notes": ""
      },
      {
        "step": 12,
        "bucket": "Contribute to 529 accounts",
        "current": 0,
        "target": -179276,
        "status": "N/A",
        "delta": "",
        "flag": ""
      },
      {
        "step": 13,
        "bucket": "Maximize 401k / employer plans",
        "current": 0,
        "target": 24500,
        "status": "Empty",
        "delta": -24500,
        "flag": "",
        "notes": ""
      },
      {
        "step": 14,
        "bucket": "Invest in taxable brokerage",
        "current": 50000,
        "target": "N/A",
        "status": "",
        "delta": ""
      },
      {
        "step": 15,
        "bucket": "Pay low-interest debt (personal, auto)",
        "current": 0,
        "target": "N/A",
        "status": "",
        "delta": ""
      },
      {
        "step": 16,
        "bucket": "Make extra mortgage payments",
        "current": "N/A",
        "target": "",
        "status": ""
      }
    ],
    "shocks": [
      {
        "assetClassesAffected": [
          "US Treasuries",
          "US equities",
          "USD",
          "rate-sensitive sectors"
        ],
        "dateLabel": "2023-07-26",
        "description": "The Fed raised rates 25bp to 5.25–5.50%, the 11th and final hike in the cycle — the highest level in 22 years. The Fed held here for 14 months before cutting in September 2024.",
        "duration": "Extended",
        "endDate": "2024-09-17",
        "impactDirection": "Rates-driven",
        "name": "Fed final hike to 5.25–5.50%",
        "portfolioImpact": "Mixed",
        "severity": "High",
        "startDate": "2023-07-23",
        "type": "Fed/Macro",
        "drawdown": {
          "severity": "major",
          "eventDate": "2023-07-26",
          "household": {
            "drawdownPct": -0.046,
            "recoveryDays": 13,
            "returnDuringPct": 0.2196
          },
          "windowEnd": "2024-09-17",
          "eventTitle": "Fed final hike to 5.25–5.50%",
          "windowStart": "2023-07-23",
          "divergencePp": 0.01,
          "sameRiskBenchmark": {
            "drawdownPct": -0.056,
            "recoveryDays": 17,
            "returnDuringPct": 0.2561
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "US Treasuries",
          "small caps",
          "USD",
          "rate-sensitive sectors"
        ],
        "dateLabel": "2023-12-13",
        "description": "Fed held rates steady but the dot plot signaled 75bp of cuts in 2024, marking a decisive pivot. S&P 500 surged to new highs; Russell 2000 +4%. Long-end yields fell sharply. Catalyzed a broad year-end rally across equities and bonds.",
        "duration": "Extended",
        "endDate": "2024-03-31",
        "impactDirection": "Risk-on equity",
        "name": "Fed pivot — December 2023 dot plot",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2023-12-10",
        "type": "Fed/Macro",
        "drawdown": {
          "severity": "major",
          "eventDate": "2023-12-13",
          "household": {
            "drawdownPct": -0.0131,
            "recoveryDays": 4,
            "returnDuringPct": 0.0876
          },
          "windowEnd": "2024-03-31",
          "eventTitle": "Fed pivot — December 2023 dot plot",
          "windowStart": "2023-12-10",
          "divergencePp": 0.0039,
          "sameRiskBenchmark": {
            "drawdownPct": -0.017,
            "recoveryDays": 14,
            "returnDuringPct": 0.1005
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "Japanese equities",
          "EM",
          "global equities",
          "USD/JPY"
        ],
        "dateLabel": "2024-08-05",
        "description": "Yen carry trade unwind and US recession fears triggered a global rout. Japan's TOPIX fell 12.3% — worst since 1987 Black Monday. VIX spiked above 65 intraday. S&P 500 fell ~3% at the open but recovered most losses by Friday. The episode lasted one week.",
        "duration": "Immediate (days)",
        "endDate": "2024-08-09",
        "impactDirection": "Risk-off equity",
        "name": "Global selloff — VIX spikes above 60",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2024-07-31",
        "type": "Market",
        "drawdown": {
          "severity": "major",
          "eventDate": "2024-08-05",
          "household": {
            "drawdownPct": -0.0413,
            "returnDuringPct": -0.0214
          },
          "windowEnd": "2024-08-09",
          "eventTitle": "Global selloff — VIX spikes above 60",
          "windowStart": "2024-07-31",
          "divergencePp": 0.0023,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0436,
            "returnDuringPct": -0.0227
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "US Treasuries",
          "USD",
          "EM",
          "rate-sensitive sectors"
        ],
        "dateLabel": "2024-09-18",
        "description": "First Fed rate cut in four years, and an outsized 50bp move, formally marking the start of the easing cycle. Signaled the Fed's confidence that inflation was heading sustainably toward 2% and opened the door to subsequent cuts.",
        "duration": "Extended",
        "endDate": "2024-12-18",
        "impactDirection": "Risk-on equity",
        "name": "Fed first rate cut — 50bp",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2024-09-15",
        "type": "Fed/Macro",
        "drawdown": {
          "severity": "major",
          "eventDate": "2024-09-18",
          "household": {
            "drawdownPct": -0.0303,
            "returnDuringPct": 0.0167
          },
          "windowEnd": "2024-12-18",
          "eventTitle": "Fed first rate cut — 50bp",
          "windowStart": "2024-09-15",
          "divergencePp": -0.0005,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0298,
            "returnDuringPct": 0.0311
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "small caps",
          "financials",
          "USD",
          "crypto"
        ],
        "dateLabel": "2024-11-05",
        "description": "Trump defeated Kamala Harris decisively. S&P 500 surged 2.5%, Dow +3.6%, Russell 2000 +5.8%. The \"Trump trade\" lifted banks, small caps, and crypto on expectations of deregulation and tax cuts. USD strengthened sharply.",
        "duration": "Short",
        "endDate": "2024-11-19",
        "impactDirection": "Risk-on equity",
        "name": "Trump election win",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2024-11-05",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2024-11-05",
          "household": {
            "drawdownPct": -0.0165,
            "returnDuringPct": 0.0105
          },
          "windowEnd": "2024-11-19",
          "eventTitle": "Trump election win",
          "windowStart": "2024-11-05",
          "divergencePp": 0.0007,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0172,
            "returnDuringPct": 0.018
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities (tech/semis)",
          "Nvidia",
          "AI-linked names"
        ],
        "dateLabel": "2025-01-27",
        "description": "Chinese startup DeepSeek released an open-source AI model rivaling GPT-4 at a fraction of the cost, questioning the US AI capex thesis. Nvidia lost $589B in market value — the largest single-day loss for any stock in history. Nasdaq fell 3.1%, S&P 500 fell 1.5%.",
        "duration": "Immediate (days)",
        "endDate": "2025-01-30",
        "impactDirection": "Sector-specific",
        "name": "DeepSeek AI shock",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2025-01-27",
        "type": "Tech/AI",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-01-27",
          "household": {
            "drawdownPct": -0.0021,
            "recoveryDays": 0,
            "returnDuringPct": 0.0022
          },
          "windowEnd": "2025-01-30",
          "eventTitle": "DeepSeek AI shock",
          "windowStart": "2025-01-27",
          "divergencePp": 0.0009,
          "sameRiskBenchmark": {
            "drawdownPct": -0.003,
            "recoveryDays": 0,
            "returnDuringPct": 0.0074
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "EM",
          "USD",
          "US Treasuries"
        ],
        "dateLabel": "2025-04-02",
        "description": "Trump announced sweeping reciprocal tariffs (10% baseline, 34% on China, 20% on EU, 46% on Vietnam) — the highest US tariff level since 1909. S&P 500 lost 10% in two days — the worst two-day loss in history ($6.6T erased). Long-end yields spiked on bond vigilante concerns.",
        "duration": "Short",
        "endDate": "2025-04-09",
        "impactDirection": "Risk-off equity",
        "name": "Liberation Day tariffs announced",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2025-04-02",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-04-02",
          "household": {
            "drawdownPct": -0.0987,
            "returnDuringPct": -0.0398
          },
          "windowEnd": "2025-04-09",
          "eventTitle": "Liberation Day tariffs announced",
          "windowStart": "2025-04-02",
          "divergencePp": -0.0036,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0951,
            "returnDuringPct": -0.0274
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "US Treasuries",
          "USD"
        ],
        "dateLabel": "2025-04-09",
        "description": "After the S&P 500 fell 10% in two days post-Liberation Day, Trump announced a 90-day pause on reciprocal tariffs above 10% for all countries except China (raised to 125%). S&P 500 surged 9.52% — its largest single-day gain since 2008. Nasdaq jumped 12.16%. Record 30B shares traded.",
        "duration": "Short",
        "endDate": "2025-04-22",
        "impactDirection": "Risk-on equity",
        "name": "90-day tariff pause rally",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2025-04-09",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-04-09",
          "household": {
            "drawdownPct": -0.0252,
            "returnDuringPct": -0.0098
          },
          "windowEnd": "2025-04-22",
          "eventTitle": "90-day tariff pause rally",
          "windowStart": "2025-04-09",
          "divergencePp": 0.0125,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0378,
            "returnDuringPct": -0.0194
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "EM",
          "USD",
          "tech",
          "retail"
        ],
        "dateLabel": "2025-05-12",
        "description": "After two days of talks in Geneva, the US and China agreed to reduce reciprocal tariffs from 125% to 10% for 90 days. S&P 500 surged 3.3%, Nasdaq +4.4%. Apple and Amazon led gains as the deal eased supply-chain fears for import-dependent tech and retail sectors.",
        "duration": "Short",
        "endDate": "2025-05-19",
        "impactDirection": "Risk-on equity",
        "name": "US-China Geneva tariff truce",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2025-05-11",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-05-12",
          "household": {
            "drawdownPct": -0.0021,
            "recoveryDays": 0,
            "returnDuringPct": 0.0098
          },
          "windowEnd": "2025-05-19",
          "eventTitle": "US-China Geneva tariff truce",
          "windowStart": "2025-05-11",
          "divergencePp": -0.0021,
          "sameRiskBenchmark": {
            "drawdownPct": 0,
            "returnDuringPct": 0.014
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "USD",
          "imports-sensitive sectors"
        ],
        "dateLabel": "2026-02-01",
        "description": "The Supreme Court affirmed that the Trump administration's use of emergency powers to impose the April 2025 reciprocal tariffs was unlawful, formally unwinding the tariff regime's legal basis. (Exact date to verify on next run.)",
        "duration": "Extended",
        "endDate": "2026-02-28",
        "impactDirection": "Risk-on equity",
        "name": "Supreme Court strikes down Liberation Day tariffs",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2026-02-01",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2026-02-01",
          "household": {
            "drawdownPct": -0.0096,
            "returnDuringPct": 0.0106
          },
          "windowEnd": "2026-02-28",
          "eventTitle": "Supreme Court strikes down Liberation Day tariffs",
          "windowStart": "2026-02-01",
          "divergencePp": 0.0072,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0168,
            "returnDuringPct": -0.0047
          }
        }
      },
      {
        "assetClassesAffected": [
          "Crude oil",
          "US equities",
          "international equities",
          "defense stocks",
          "US Treasuries"
        ],
        "dateLabel": "2026-02-28",
        "description": "US and Israel launched coordinated airstrikes on Iranian military and nuclear sites, with nearly 900 strikes in the first 12 hours. Iranian leadership was decapitated. Brent crude surged 10–13% immediately; global equity markets sold off sharply on escalation and energy-supply fears.",
        "duration": "Extended",
        "endDate": "2026-03-04",
        "impactDirection": "Risk-off equity",
        "name": "Operation Epic Fury — US-Israel strikes on Iran",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2026-02-28",
        "type": "Geopolitical",
        "drawdown": {
          "severity": "major",
          "eventDate": "2026-02-28",
          "household": {
            "drawdownPct": -0.0086,
            "returnDuringPct": -0.0053
          },
          "windowEnd": "2026-03-04",
          "eventTitle": "Operation Epic Fury — US-Israel strikes on Iran",
          "windowStart": "2026-02-28",
          "divergencePp": -0.0015,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0072,
            "returnDuringPct": -0.002
          }
        }
      }
    ],
    "performanceSummary": {
      "maxDrawdown3y": -0.1195,
      "maxDrawdownRecoveryDays": 78,
      "benchmark": {
        "sharpe3y": 1.298,
        "blendCash": 0.1973,
        "blendEquity": 0.683,
        "volatility3y": 0.103,
        "maxDrawdown3y": -0.1335,
        "blendFixedIncome": 0.1197,
        "return1yAnnualized": 0.0897,
        "return3yAnnualized": 0.1697,
        "return3yCumulative": 0.6009
      },
      "assetAllocation": {
        "currentEF": {
          "equity": 0.683,
          "fixedIncome": 0.317
        },
        "currentEFC": {
          "cash": 0.1973,
          "equity": 0.683,
          "fixedIncome": 0.1197
        },
        "targetEF": {
          "equity": 0.6457,
          "fixedIncome": 0.3543
        },
        "targetEFC": {
          "cash": 0.2104,
          "equity": 0.6457,
          "fixedIncome": 0.1442
        }
      },
      "concentration": {
        "topSectorPct": 0.4028,
        "topSectorName": "Technology",
        "isMaterialConcentration": true
      },
      "positions": [
        {
          "account": "Custodial Account (Ava)",
          "ticker": "VTI",
          "name": "Vanguard Morningstar Total Stock Market ETF",
          "type": "ETF",
          "category": "Large Blend",
          "value": 10000,
          "weight_in_account": 0.6667,
          "expense_ratio": 0.0003
        },
        {
          "account": "Custodial Account (Ethan)",
          "ticker": "VTI",
          "name": "Vanguard Morningstar Total Stock Market ETF",
          "type": "ETF",
          "category": "Large Blend",
          "value": 12000,
          "weight_in_account": 0.6,
          "expense_ratio": 0.0003
        },
        {
          "account": "Taxable Brokerage",
          "ticker": "VTI",
          "name": "Vanguard Morningstar Total Stock Market ETF",
          "type": "ETF",
          "category": "Large Blend",
          "value": 140000,
          "weight_in_account": 0.4667,
          "expense_ratio": 0.0003
        },
        {
          "account": "Taxable Brokerage",
          "ticker": "JNK",
          "name": "SPDR Bloomberg High Yield Bond ETF",
          "type": "ETF",
          "category": "High Yield Bond",
          "value": 50000,
          "weight_in_account": 0.1667,
          "expense_ratio": 0.004
        }
      ],
      "taxDragAnalysis": {
        "householdRollup": [
          [
            "Metric",
            "Value",
            "Notes"
          ],
          [
            "Total annual tax cost (Table 2)",
            3032.2,
            "All taxable-account rows, including money-market positions."
          ],
          [
            "Money-market drag routed to Cash sub-task",
            0,
            "Money-market positions stay visible here but are carved out of the in-scope Tax Drag total."
          ],
          [
            "In-scope tax cost (Table 2 ex-MM)",
            3032.2,
            "Standalone Tax Drag total after routing money-market drag to Cash."
          ],
          [
            "Total annual tax cost saved (Table 3)",
            0,
            "Permanent annual tax saved if those holdings were taxable today."
          ],
          [
            "Total annual tax cost deferred (Table 4)",
            0,
            "Deferred, not eliminated; future withdrawals remain taxable on exit."
          ],
          [
            "NIIT contribution to Table 2",
            330.44,
            "Taxable net-investment components multiplied by the current NIIT rate."
          ]
        ],
        "accountTypeInputs": [
          [
            "#",
            "Account name",
            "Account type",
            "Tax treatment"
          ],
          [
            "1",
            "Checking Account",
            "Checking account",
            "Taxable"
          ],
          [
            "2",
            "Savings account",
            "Savings account",
            "Taxable"
          ],
          [
            "3",
            "Custodial Account (Ava)",
            "Custodial UGMA",
            "Taxable"
          ],
          [
            "4",
            "Custodial Account (Ethan)",
            "Custodial UGMA",
            "Taxable"
          ],
          [
            "5",
            "Taxable Brokerage",
            "Brokerage account",
            "Taxable"
          ]
        ],
        "effectiveTaxMargin": [
          [
            "Component",
            "Rate",
            "Source / Trigger",
            "Applies to"
          ],
          [
            "Federal ordinary",
            "32%",
            "FH metrics — currentTaxBracket",
            "Ordinary income, ST cap gains, ST cap gain distributions, ordinary interest, non-qualified dividends"
          ],
          [
            "Federal LTCG",
            "15%",
            "PW-computed federal LTCG (2026 thresholds; taxable-income proxy)",
            "Qualified dividends, LT cap gains, LT cap gain distributions"
          ],
          [
            "State (FL)",
            "0%",
            "FH metrics — stateTaxRate (FL)",
            "All investment income (state rules)"
          ],
          [
            "NIIT",
            "3.8%",
            "Triggered: income $233,900 > $200K Single",
            "All net investment income"
          ],
          [
            "Total taxable income",
            "$233,900",
            "FH metrics — taxableIncome.totalTaxableIncome",
            "Debug input for LTCG and NIIT lookups"
          ],
          [
            "MAGI proxy",
            "$233,900",
            "Current tax-margin logic — reuse taxableIncome.totalTaxableIncome as MAGI proxy",
            "Debug input for NIIT and current LTCG threshold lookup"
          ],
          [
            "State input",
            "FL — Florida",
            "PW params — state.code / state.name",
            "Debug input for state marginal-rate lookup"
          ],
          [
            "Expected retirement ordinary",
            "24%",
            "FH metrics — expectedTaxBracketInRetirement",
            "Future withdrawals from tax-deferred accounts"
          ],
          [
            "Effective ordinary rate",
            "35.8%",
            "32% + 0% + 3.8%",
            "Today's ordinary-rate income"
          ],
          [
            "Effective LTCG rate",
            "18.8%",
            "15% + 0% + 3.8%",
            "Today's LTCG-rate income"
          ]
        ],
        "fundHoldingsInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Morningstar category",
            "Balance",
            "Shares",
            "Estimated shares",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Interest income ($/share)",
            "Tax-free income ($/share)",
            "LT cap gain ($/share)",
            "ST cap gain ($/share)",
            "Ordinary-rate share (non-qual div + interest + ST cap gain) / total distribution",
            "Tax cost ratio",
            "Turnover",
            "PCGE"
          ],
          [
            "1",
            "Custodial Account (Ava)",
            "VTI",
            "Large Blend",
            10000,
            27.63,
            "-",
            "$0.86",
            "$2.897",
            "$0",
            "$0",
            "$0",
            "$0",
            "77.11%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "2",
            "Custodial Account (Ethan)",
            "VTI",
            "Large Blend",
            12000,
            33.16,
            "-",
            "$0.86",
            "$2.897",
            "$0",
            "$0",
            "$0",
            "$0",
            "77.11%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "3",
            "Taxable Brokerage",
            "VTI",
            "Large Blend",
            140000,
            386.88,
            "-",
            "$0.86",
            "$2.897",
            "$0",
            "$0",
            "$0",
            "$0",
            "77.11%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "4",
            "Taxable Brokerage",
            "VWO",
            "Diversified Emerging Markets",
            30000,
            541.91,
            "-",
            "$0.168",
            "$1.329",
            "$0",
            "$0",
            "$0",
            "$0",
            "88.77%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "5",
            "Custodial Account (Ava)",
            "SCHD",
            "Large Value",
            5000,
            142.13,
            "-",
            "$0",
            "$1.048",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "6",
            "Taxable Brokerage",
            "JNK",
            "High Yield Bond",
            50000,
            539.97,
            "-",
            "$0",
            "$6.358",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "7",
            "Custodial Account (Ethan)",
            "SCHD",
            "Large Value",
            8000,
            227.4,
            "-",
            "$0",
            "$1.048",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "8",
            "Taxable Brokerage",
            "SCHD",
            "Large Value",
            80000,
            2274.02,
            "-",
            "$0",
            "$1.048",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ]
        ],
        "stockHoldingsInputs": [
          [
            "#",
            "Account",
            "Name",
            "Ticker",
            "Sector",
            "Industry",
            "Country",
            "Balance",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Dividend yield TTM"
          ]
        ],
        "taxFreeAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable)",
            "Annual tax cost saved"
          ],
          [
            "1",
            "No Tax-Free accounts in household",
            "-",
            0,
            "-",
            0,
            "-",
            0
          ],
          [
            "Total",
            "Total tax-free",
            "-",
            0,
            "-",
            0,
            "-",
            0
          ]
        ],
        "taxableAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate",
            "Annual tax cost"
          ],
          [
            "1a",
            "Custodial Account (Ava)",
            "VTI",
            10000,
            "Qualified dividend",
            23.76,
            "18.8%",
            4.4669
          ],
          [
            "1b",
            "Custodial Account (Ava)",
            "VTI",
            10000,
            "Non-qualified dividend",
            80.05,
            "35.8%",
            28.66
          ],
          [
            "1c",
            "Custodial Account (Ava)",
            "VTI",
            10000,
            "Subtotal",
            103.81,
            "-",
            33.13
          ],
          [
            "2a",
            "Custodial Account (Ethan)",
            "VTI",
            12000,
            "Qualified dividend",
            28.51,
            "18.8%",
            5.3603
          ],
          [
            "2b",
            "Custodial Account (Ethan)",
            "VTI",
            12000,
            "Non-qualified dividend",
            96.06,
            "35.8%",
            34.39
          ],
          [
            "2c",
            "Custodial Account (Ethan)",
            "VTI",
            12000,
            "Subtotal",
            124.57,
            "-",
            39.75
          ],
          [
            "3a",
            "Taxable Brokerage",
            "VTI",
            140000,
            "Qualified dividend",
            332.64,
            "18.8%",
            62.54
          ],
          [
            "3b",
            "Taxable Brokerage",
            "VTI",
            140000,
            "Non-qualified dividend",
            1120.71,
            "35.8%",
            401.21
          ],
          [
            "3c",
            "Taxable Brokerage",
            "VTI",
            140000,
            "Subtotal",
            1453.35,
            "-",
            463.75
          ],
          [
            "4a",
            "Taxable Brokerage",
            "VWO",
            30000,
            "Qualified dividend",
            91.14,
            "18.8%",
            17.13
          ],
          [
            "4b",
            "Taxable Brokerage",
            "VWO",
            30000,
            "Non-qualified dividend",
            720.26,
            "35.8%",
            257.85
          ],
          [
            "4c",
            "Taxable Brokerage",
            "VWO",
            30000,
            "Subtotal",
            811.4,
            "-",
            274.99
          ],
          [
            "5",
            "Custodial Account (Ava)",
            "SCHD",
            5000,
            "Non-qualified dividend",
            148.89,
            "35.8%",
            53.3
          ],
          [
            "6",
            "Taxable Brokerage",
            "JNK",
            50000,
            "Non-qualified dividend",
            3433.37,
            "35.8%",
            1229.15
          ],
          [
            "7",
            "Custodial Account (Ethan)",
            "SCHD",
            8000,
            "Non-qualified dividend",
            238.23,
            "35.8%",
            85.29
          ],
          [
            "8",
            "Taxable Brokerage",
            "SCHD",
            80000,
            "Non-qualified dividend",
            2382.26,
            "35.8%",
            852.85
          ],
          [
            "Total",
            "Total taxable",
            "-",
            335000,
            "-",
            8695.88,
            "-",
            3032.2
          ]
        ],
        "costBasisBlockingNotes": [
          [
            "Account",
            "Blocking note"
          ],
          [
            "Custodial Account (Ava)",
            "Implementation of Custodial Account (Ava) cannot be responsibly sequenced without tax-lot data."
          ],
          [
            "Custodial Account (Ethan)",
            "Implementation of Custodial Account (Ethan) cannot be responsibly sequenced without tax-lot data."
          ],
          [
            "Taxable Brokerage",
            "Implementation of Taxable Brokerage cannot be responsibly sequenced without tax-lot data."
          ]
        ],
        "taxableCostBasisInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Balance (market value)",
            "Cost basis",
            "Unrealized gain",
            "Holding period",
            "Notes"
          ],
          [
            "1",
            "Custodial Account (Ava)",
            "VTI",
            10000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "2",
            "Custodial Account (Ethan)",
            "VTI",
            12000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "3",
            "Taxable Brokerage",
            "VTI",
            140000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "4",
            "Taxable Brokerage",
            "VWO",
            30000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "5",
            "Custodial Account (Ava)",
            "SCHD",
            5000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "6",
            "Taxable Brokerage",
            "JNK",
            50000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "7",
            "Custodial Account (Ethan)",
            "SCHD",
            8000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "8",
            "Taxable Brokerage",
            "SCHD",
            80000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "Total",
            "Total taxable",
            "-",
            335000,
            "[missing cost basis]",
            "[missing cost basis]",
            "-",
            "Totals stay blocked until missing tax-lot inputs are filled."
          ]
        ],
        "taxDeferredAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable today)",
            "Annual tax cost deferred"
          ],
          [
            "1",
            "No Tax-Deferred accounts in household",
            "-",
            0,
            "-",
            0,
            "-",
            0
          ],
          [
            "Total",
            "Total tax-deferred",
            "-",
            0,
            "-",
            0,
            "-",
            0
          ]
        ],
        "componentTaxTreatmentMatrix": [
          [
            "Component",
            "Federal rate type",
            "Effective household rate today",
            "Taxable accounts",
            "Tax-free accounts",
            "Tax-deferred accounts",
            "Notes"
          ],
          [
            "Qualified dividend",
            "LTCG",
            "18.8%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for US common stock and treaty-country foreign names; funds keep the precomputed Morningstar qualified split."
          ],
          [
            "Non-qualified dividend",
            "ORDINARY",
            "35.8%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for REIT and non-treaty foreign names, while MLP distributions are treated as ROC; funds keep the precomputed Morningstar non-qualified split."
          ],
          [
            "Interest income",
            "ORDINARY",
            "35.8%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Money-market and bond-style fund income is treated as ordinary-rate income."
          ],
          [
            "Tax-free income",
            "Tax-exempt federal",
            "0%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Current phase assumes a 0% effective rate because state-specific muni exposure is not available in the data path."
          ],
          [
            "LT cap gain distribution",
            "LTCG",
            "18.8%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed long-term capital gains use the LTCG household rate."
          ],
          [
            "ST cap gain distribution",
            "ORDINARY",
            "35.8%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed short-term capital gains use the ordinary household rate."
          ]
        ]
      }
    }
  },
  "timothy-melanie-weah": {
    "meta": {
      "slug": "timothy-melanie-weah",
      "household": "Timothy & Melanie",
      "city": "San Francisco",
      "state": "CA",
      "tax_filing_status": "MARRIED_JOINTLY",
      "isCouple": true,
      "owners": [
        {
          "key": "A",
          "name": "Timothy",
          "role": "client",
          "age": 40,
          "retirement_age": 62,
          "risk_profile": "Growth"
        },
        {
          "key": "B",
          "name": "Melanie",
          "role": "co-client",
          "age": 38,
          "retirement_age": 60,
          "risk_profile": "Moderate"
        }
      ]
    },
    "score": {
      "published_score": 60,
      "scale": "0 to 100",
      "band": "stable",
      "colour": "yellow",
      "message": "Your score of 60 suggests that while you manage to get by, you aren't thriving financially, often leading to stress and financial disorganization. Enhancing your financial health and creating a strategic plan could unlock your money's potential and help you gain control of your desired life.",
      "pillars": [
        {
          "pillar": "Savings and cash flow",
          "score": 86,
          "points_shown_in_app": "26/30"
        },
        {
          "pillar": "Debt",
          "score": 58,
          "points_shown_in_app": "12/20"
        },
        {
          "pillar": "Investments",
          "score": 56,
          "points_shown_in_app": "8/15"
        },
        {
          "pillar": "Liquidity and emergency fund",
          "score": 100,
          "points_shown_in_app": "15/15"
        },
        {
          "pillar": "Insurance and protection",
          "score": 37,
          "points_shown_in_app": "7/20"
        }
      ],
      "caps_applied": [
        {
          "reason": "High revolving balance with high APR",
          "score_capped_at": 60
        },
        {
          "reason": "Mortality coverage ratio below threshold with dependents",
          "score_capped_at": 62
        }
      ],
      "top_moves": [
        {
          "title": "Pay down revolving card",
          "action": "Pay $6,800 on the 18% card from cash to remove high revolving exposure and clear the gate",
          "effort": "medium",
          "target_amount": 11200,
          "score_before": 60,
          "score_after": 62,
          "lifts_a_cap": true
        },
        {
          "title": "Add life cover",
          "action": "Add $235,000 of life cover to raise the mortality ratio and clear the gate",
          "effort": "low",
          "target_amount": 485000,
          "score_before": 60,
          "score_after": 60,
          "lifts_a_cap": true
        },
        {
          "title": "Add umbrella cover",
          "action": "Add $1M of umbrella to raise the liability shield",
          "effort": "low",
          "target_amount": 1000000,
          "score_before": 60,
          "score_after": 60,
          "lifts_a_cap": false
        }
      ],
      "combined_moves": [
        {
          "moves": [
            "Pay down revolving card",
            "Add life cover",
            "Add umbrella cover"
          ],
          "score_after": 78,
          "note": "After the card paydown, life cover must reach $491,800 to keep the mortality ratio at the gate line."
        },
        {
          "moves": [
            "Pay down revolving card",
            "Add life cover"
          ],
          "score_after": 73,
          "note": "After the card paydown, life cover must reach $491,800 to keep the mortality ratio at the gate line."
        },
        {
          "moves": [
            "Pay down revolving card",
            "Add umbrella cover"
          ],
          "score_after": 62,
          "note": "Together they raise the published score more than either move alone."
        },
        {
          "moves": [
            "Add life cover",
            "Add umbrella cover"
          ],
          "score_after": 60,
          "note": "Together they raise the published score more than either move alone."
        }
      ],
      "explainer": "## Key takeaways\n- Liquidity is a clear strength, and retirement saving is steady. Cash flow and cash reserves are doing their job for the household.\n- Two limits hold the published score at 60: an 18% revolving card balance and a life-cover gap, with a 33% mortality ratio and dependents.\n- Without those limits, the score before the limit would be about 68. The published score stays at 60 until both are addressed.\n- The first move is paying $6,800 on the 18% card from cash. The published score moves from 60 to 62, leaving $11,200 total after the move.\n\n## Cash flow\n- Retirement saving is about 14% of income, and the savings pattern is a solid part of the score.\n- Fixed obligations are a manageable share of income, which leaves the household room to act on the card.\n\n## Debt\n- The card balance is the main drag: revolving use is 80% at an 18% rate, and it caps the published score.\n- Paying $6,800 from cash clears that limit and lifts the published score from 60 to 62.\n- Other debt measures, such as the debt-service load, are comfortable and are not what holds the score back.\n\n## Protection\n- Protection is the pillar holding the score back most. The mortality ratio is 33%, with dependents in the household.\n- Adding $235,000 of life cover brings the total to $485,000. On its own, it leaves the published score at 60 while the card limit remains.\n- Once the card is paid down, life cover must reach $491,800 in total. Clearing both lifts the published score from 60 to 73.\n- An umbrella policy of $1M would add liability protection. The household has none now.\n\n## Liquidity\n- Cash covers about 16 months of spending, and total liquid assets cover about 18 months. This is the strongest area.\n- Paying $6,800 toward the card from cash still leaves a very large reserve.\n\n## Investing\n- Investing is a middle area. The largest single position, VTI, is about 16% of investable assets.\n- Growth is a large share of the portfolio's value, which weighs on this area more than concentration does.\n- Some holdings, including JNK, are tax-inefficient. They sit mostly in tax-advantaged accounts, which is a smaller issue."
    },
    "persona": {
      "D0": "EMERGING. The household earns a high income, which would suggest mass affluent, but the tier is set by investable assets, and those exclude cash and home equity. Investable assets are $210,000, under the $500,000 line for the next band, so the EMERGING label governs.\r\n\r\nCash is $150,000 on top of the $210,000 of investments, which gives $360,000 of liquid assets. Net worth is $695,500 and total assets are $788,500. Gross household income is $270,000 (Timothy $150,000, Melanie $120,000), about the 90th income percentile in California. High income against modest investable assets is the defining profile.",
      "D1": "MID ACCUMULATION. Timothy is 40 and Melanie is 38, and they live in San Francisco. Both work. They plan to retire at 62 (Timothy) and 60 (Melanie), 21 years from now. The children are Liam (6) and Josh (3). College starts for Liam in August 2038 and for Josh in August 2041, so the first college payment is about 12 years away. The plan also lists a $45,000 vehicle purchase in 2028 and a $600,000 home purchase in 2030. No stage change is likely within 24 months.",
      "D2": "MODERATE. There are two earned incomes, with no equity compensation, business or single-stock concentration. Each spouse has a traditional 401(k) and a Roth retirement account. There is also a taxable brokerage account and a large cash account. There is one home with a mortgage, two vehicles, and four debts (mortgage, credit card, student loan, vehicle loan). The portfolio holds funds and ETFs, including a leveraged ETF (UPRO) in Timothy's Roth account. Tax-aware placement is only partly in evidence: most bond funds sit in tax-deferred accounts, but a high-yield bond fund (JNK) sits in the taxable brokerage account.",
      "D3": "MODERATE GAPS. The published Financial Health score is 60 out of 100. It is capped at 60 because of a high-rate credit card balance, and a second cap at 62 applies because life cover is low for a household with young children. Without the caps the score would be about 68.\r\n\r\n- **Retirement:** the plan is sustainable. The retirement gap is 0 and income covers 93% of the yearly retirement spending need (before estimated long-term care costs). Savings left at the end of the plan are $2,371,900.89. The savings rate is 22.8% of gross income ($61,500 a year), and the employer match is fully captured for both spouses ($8,000 for Timothy, $6,000 for Melanie).\r\n- **Life insurance:** both spouses hold whole life policies. Timothy has $140,000 against a recommended minimum of $750,000, a shortfall of $610,000. Melanie has $110,000 against $600,000, a shortfall of $490,000. This is the largest protection gap.\r\n- **Umbrella:** there is no umbrella liability policy, a $1,000,000 gap.\r\n- **Debt:** total debt is $93,000. Debt payments take 13.2% of gross income, and 15.1% once housing costs are included. The Chase card carries $18,000 at 18% with $300 a month paid, of which about $270 is interest each month. At that pace the card is projected to be paid off in September 2039. The other debts are cheaper: 6% on the $50,000 mortgage, 5.5% on the $15,000 student loan, 4.5% on the $10,000 vehicle loan.\r\n- **Education:** nothing is saved in 529 accounts. The funding gap is $113,508.60, and the extra yearly saving needed is $4,609.22 in the first year, rising each year.\r\n- **Liquidity:** accessible cash is $150,800, about 16 months of essential expenses. The recommended reserve is 8 to 9 months ($75,180 to $84,577.50), so there is a surplus. Cash above the reserve and the $6,000 yearly vacation is $60,222.50.\r\n- **Cash flow reliability:** net cash flow is $36,960.75 a year, but savings capacity reads 0 and the reported expenses look understated. Confidence in the cash flow figures is low.\r\n\r\nLong-term care costs in the plan are estimates, so they are not treated as a driver. Including them, income covers about 79% of the retirement need instead of 93%.",
      "D4a": "- **D4a stated:** Timothy is Growth (4) and Melanie is Moderate (3). The household reading is MODERATE, with a split between the spouses.\r",
      "D4b": "- **D4b revealed:** about 77% of the $210,000 of investments is in stocks, which reads AGGRESSIVE (more than 70%). The Moderate target is 60%. Timothy's accounts sit close to a Growth mix, while Melanie's accounts run 70% to 81% in stocks against the Moderate target. Counting the $150,000 of cash, the household's overall stock share is about 45%. Timothy's Roth holds a leveraged ETF (UPRO) worth $12,740. That account returned about 41% a year over three years with 30% volatility, a result that may not repeat.\r",
      "D4c": "- **D4c inferred:** MODERATE. Leverage is low overall and the emergency fund is very large, but life insurance is thin, there is no umbrella policy, and a high-rate card balance is carried while a large cash balance sits idle. This is inferred from the accounts, not from a conversation.\r\n\r\nThe result is MISALIGNED. The invested portfolio runs hotter than the stated household Moderate profile, and the large cash balance and thin protection point in different directions. See T2.",
      "D4": "- **D4a stated:** Timothy is Growth (4) and Melanie is Moderate (3). The household reading is MODERATE, with a split between the spouses.\r\n- **D4b revealed:** about 77% of the $210,000 of investments is in stocks, which reads AGGRESSIVE (more than 70%). The Moderate target is 60%. Timothy's accounts sit close to a Growth mix, while Melanie's accounts run 70% to 81% in stocks against the Moderate target. Counting the $150,000 of cash, the household's overall stock share is about 45%. Timothy's Roth holds a leveraged ETF (UPRO) worth $12,740. That account returned about 41% a year over three years with 30% volatility, a result that may not repeat.\r\n- **D4c inferred:** MODERATE. Leverage is low overall and the emergency fund is very large, but life insurance is thin, there is no umbrella policy, and a high-rate card balance is carried while a large cash balance sits idle. This is inferred from the accounts, not from a conversation.\r\n\r\nThe result is MISALIGNED. The invested portfolio runs hotter than the stated household Moderate profile, and the large cash balance and thin protection point in different directions. See T2.",
      "D5": "COLLABORATOR, with low confidence. This is inferred from the accounts, not from a conversation. Two earners split the saving, each with their own accounts, and the portfolio mixes self-selected funds with broad index ETFs. The risk profiles differ between the spouses, so a plan should be explained so that both can follow the reasoning.",
      "D6": "PROTECTION, with low confidence and provisional. This rests on structure alone: very large cash reserves, two young children, and a college goal. Protection gaps remain open despite that, which suggests the anchor is not yet backed by action.",
      "transitionAlerts": "None detected within 12 to 24 months. The nearest shifts are the planned vehicle purchase in 2028, the planned home purchase in 2030, college starts in 2038 and 2041, and retirement 21 years out.",
      "subjectiveConcerns": "None recorded. There is no conversation, note or free text from the household, so their own worries are unknown. Interviews or written comments would fill this.",
      "objectiveConcerns": [
        {
          "id": "O1",
          "detail": "- **O1: Life insurance shortfall (SIGNIFICANT).** Timothy is short $610,000 and Melanie $490,000, and both have dependents. This is one of the two caps holding the published score down. Connected: D3, D4c."
        },
        {
          "id": "O2",
          "detail": "- **O2: High-rate credit card (MODERATE).** $18,000 at 18% against $150,800 of accessible cash. This is the other cap on the score. Connected: D3, D4c."
        },
        {
          "id": "O3",
          "detail": "- **O3: No umbrella coverage (MODERATE).** A $1,000,000 gap. Against a net worth of $695,500 and a 90th-percentile income, a liability claim could reach well beyond current cover. Connected: D3."
        },
        {
          "id": "O4",
          "detail": "- **O4: Education funding unfunded (MODERATE).** $0 in 529s against a $113,508.60 funding gap. Connected: D3."
        },
        {
          "id": "O5",
          "detail": "- **O5: Idle cash (MINOR).** $60,222.50 sits above the emergency reserve and near-term goals, and the cash earns about 0.1%, roughly $150 a year on $150,000. The near-term cash target counts only the $6,000 vacation, not the planned 2028 vehicle and 2030 home purchases. Connected: D3, D4c."
        },
        {
          "id": "O6",
          "detail": "- **O6: Portfolio equity above target and technology concentration (MINOR).** About 77% stocks in the long-term accounts against a 60% Moderate target, technology at about 30% of stock holdings, and a leveraged ETF (UPRO) at $12,740. Connected: D4b."
        },
        {
          "id": "O7",
          "detail": "- **O7: Unused contribution limits (MINOR).** Neither spouse has contributed to a Roth IRA (each is estimated eligible for up to $5,250.10) or to a health savings account (HSA, an $8,750 household limit, usable only if their health plan qualifies). Each spouse already defers part of their pay into a 401(k) ($14,000 for Timothy, $11,000 for Melanie), so more 401(k) saving has room of $10,500 for Timothy and $13,500 for Melanie against the $24,500 limit. The plan puts the tax saving from using that room at about $5,760 a year. Connected: D3."
        }
      ],
      "tensions": [
        {
          "id": "T1",
          "detail": "- **T1 (HIGH):** O1 against O5 and the stated Protection anchor. Large idle cash coexists with $1,100,000 of combined life insurance shortfall and no umbrella. Resources exist to close part of the gap, but the cash is sitting unused. The published score is held at 60, while the plan models 73 with a card paydown and more life cover, and 78 if an umbrella policy is added too."
        },
        {
          "id": "T2",
          "detail": "- **T2 (MEDIUM):** D4 misalignment, O6 against D4a. The spouses' stated profiles (Growth and Moderate) differ, while the invested book is about 77% stocks. Revealed risk is higher than the Moderate household reading."
        },
        {
          "id": "T3",
          "detail": "- **T3 (MEDIUM):** O2 against O5. An 18% card balance is carried while accessible cash far exceeds the reserve. The card costs about $3,240 a year in interest (18% of $18,000), against roughly $150 a year earned on the cash."
        },
        {
          "id": "T4",
          "detail": "- **T4 (LOW):** O4 against current savings priorities. The $4,609.22 yearly education need competes with 401(k), Roth and HSA contributions for the same cash flow, which is itself reported as uncertain."
        }
      ]
    },
    "projections": {
      "yearly": [
        {
          "year": 2026,
          "age_client": 40,
          "age_co_client": 38,
          "net_worth": 712086,
          "net_worth_todays_dollars": 710310,
          "total_debts": 88321,
          "investable_assets": 371588,
          "net_worth_needed": 712086
        },
        {
          "year": 2027,
          "age_client": 41,
          "age_co_client": 39,
          "net_worth": 823317,
          "net_worth_todays_dollars": 797021,
          "total_debts": 59265,
          "investable_assets": 449278,
          "net_worth_needed": 823317
        },
        {
          "year": 2028,
          "age_client": 42,
          "age_co_client": 40,
          "net_worth": 945346,
          "net_worth_todays_dollars": 888140,
          "total_debts": 63390,
          "investable_assets": 524488,
          "net_worth_needed": 945346
        },
        {
          "year": 2029,
          "age_client": 43,
          "age_co_client": 41,
          "net_worth": 1044059,
          "net_worth_todays_dollars": 951926,
          "total_debts": 51658,
          "investable_assets": 614300,
          "net_worth_needed": 1044059
        },
        {
          "year": 2030,
          "age_client": 44,
          "age_co_client": 42,
          "net_worth": 1163031,
          "net_worth_todays_dollars": 1029097,
          "total_debts": 575584,
          "investable_assets": 561863,
          "net_worth_needed": 1163031
        },
        {
          "year": 2031,
          "age_client": 45,
          "age_co_client": 43,
          "net_worth": 1307142,
          "net_worth_todays_dollars": 1122472,
          "total_debts": 558046,
          "investable_assets": 663135,
          "net_worth_needed": 1307142
        },
        {
          "year": 2032,
          "age_client": 46,
          "age_co_client": 44,
          "net_worth": 1460964,
          "net_worth_todays_dollars": 1217530,
          "total_debts": 540989,
          "investable_assets": 772423,
          "net_worth_needed": 1460964
        },
        {
          "year": 2033,
          "age_client": 47,
          "age_co_client": 45,
          "net_worth": 1621060,
          "net_worth_todays_dollars": 1311072,
          "total_debts": 528599,
          "investable_assets": 890605,
          "net_worth_needed": 1621060
        },
        {
          "year": 2034,
          "age_client": 48,
          "age_co_client": 46,
          "net_worth": 1790331,
          "net_worth_todays_dollars": 1405233,
          "total_debts": 519936,
          "investable_assets": 1018840,
          "net_worth_needed": 1790331
        },
        {
          "year": 2035,
          "age_client": 49,
          "age_co_client": 47,
          "net_worth": 1972378,
          "net_worth_todays_dollars": 1502424,
          "total_debts": 510473,
          "investable_assets": 1157086,
          "net_worth_needed": 1972378
        },
        {
          "year": 2036,
          "age_client": 50,
          "age_co_client": 48,
          "net_worth": 2167951,
          "net_worth_todays_dollars": 1602652,
          "total_debts": 500119,
          "investable_assets": 1306111,
          "net_worth_needed": 2167951
        },
        {
          "year": 2037,
          "age_client": 51,
          "age_co_client": 49,
          "net_worth": 2377773,
          "net_worth_todays_dollars": 1705877,
          "total_debts": 488768,
          "investable_assets": 1466740,
          "net_worth_needed": 2377773
        },
        {
          "year": 2038,
          "age_client": 52,
          "age_co_client": 50,
          "net_worth": 2585588,
          "net_worth_todays_dollars": 1800214,
          "total_debts": 476299,
          "investable_assets": 1622749,
          "net_worth_needed": 2585588
        },
        {
          "year": 2039,
          "age_client": 53,
          "age_co_client": 51,
          "net_worth": 2807491,
          "net_worth_todays_dollars": 1897014,
          "total_debts": 463596,
          "investable_assets": 1791106,
          "net_worth_needed": 2807491
        },
        {
          "year": 2040,
          "age_client": 54,
          "age_co_client": 52,
          "net_worth": 3042480,
          "net_worth_todays_dollars": 1995112,
          "total_debts": 452567,
          "investable_assets": 1972706,
          "net_worth_needed": 3042480
        },
        {
          "year": 2041,
          "age_client": 55,
          "age_co_client": 53,
          "net_worth": 3265261,
          "net_worth_todays_dollars": 2077997,
          "total_debts": 440741,
          "investable_assets": 2143579,
          "net_worth_needed": 3265261
        },
        {
          "year": 2042,
          "age_client": 56,
          "age_co_client": 54,
          "net_worth": 3532509,
          "net_worth_todays_dollars": 2181714,
          "total_debts": 428060,
          "investable_assets": 2351109,
          "net_worth_needed": 3532509
        },
        {
          "year": 2043,
          "age_client": 57,
          "age_co_client": 55,
          "net_worth": 3817378,
          "net_worth_todays_dollars": 2288058,
          "total_debts": 414463,
          "investable_assets": 2573911,
          "net_worth_needed": 3817378
        },
        {
          "year": 2044,
          "age_client": 58,
          "age_co_client": 56,
          "net_worth": 4121133,
          "net_worth_todays_dollars": 2397209,
          "total_debts": 399882,
          "investable_assets": 2813143,
          "net_worth_needed": 4121133
        },
        {
          "year": 2045,
          "age_client": 59,
          "age_co_client": 57,
          "net_worth": 4469226,
          "net_worth_todays_dollars": 2522952,
          "total_debts": 384247,
          "investable_assets": 3094139,
          "net_worth_needed": 4469226
        },
        {
          "year": 2046,
          "age_client": 60,
          "age_co_client": 58,
          "net_worth": 4841694,
          "net_worth_todays_dollars": 2652537,
          "total_debts": 367483,
          "investable_assets": 3396816,
          "net_worth_needed": 4841694
        },
        {
          "year": 2047,
          "age_client": 61,
          "age_co_client": 59,
          "net_worth": 5240317,
          "net_worth_todays_dollars": 2786180,
          "total_debts": 349506,
          "investable_assets": 3722822,
          "net_worth_needed": 5240317
        },
        {
          "year": 2048,
          "age_client": 62,
          "age_co_client": 60,
          "net_worth": 5442180,
          "net_worth_todays_dollars": 2808095,
          "total_debts": 330229,
          "investable_assets": 3849106,
          "net_worth_needed": 5442180
        },
        {
          "year": 2049,
          "age_client": 63,
          "age_co_client": 61,
          "net_worth": 5553124,
          "net_worth_todays_dollars": 2780762,
          "total_debts": 309560,
          "investable_assets": 3881366,
          "net_worth_needed": 5553124
        },
        {
          "year": 2050,
          "age_client": 64,
          "age_co_client": 62,
          "net_worth": 5663547,
          "net_worth_todays_dollars": 2752342,
          "total_debts": 287395,
          "investable_assets": 3909846,
          "net_worth_needed": 5663547
        },
        {
          "year": 2051,
          "age_client": 65,
          "age_co_client": 63,
          "net_worth": 5765563,
          "net_worth_todays_dollars": 2719211,
          "total_debts": 263629,
          "investable_assets": 3926498,
          "net_worth_needed": 5765563
        },
        {
          "year": 2052,
          "age_client": 66,
          "age_co_client": 64,
          "net_worth": 5862710,
          "net_worth_todays_dollars": 2683410,
          "total_debts": 238145,
          "investable_assets": 3934690,
          "net_worth_needed": 5862710
        },
        {
          "year": 2053,
          "age_client": 67,
          "age_co_client": 65,
          "net_worth": 6167559,
          "net_worth_todays_dollars": 2739614,
          "total_debts": 210818,
          "investable_assets": 4146811,
          "net_worth_needed": 6167559
        },
        {
          "year": 2054,
          "age_client": 68,
          "age_co_client": 66,
          "net_worth": 6555401,
          "net_worth_todays_dollars": 2825939,
          "total_debts": 181516,
          "investable_assets": 4437961,
          "net_worth_needed": 6555401
        },
        {
          "year": 2055,
          "age_client": 69,
          "age_co_client": 67,
          "net_worth": 6991844,
          "net_worth_todays_dollars": 2925113,
          "total_debts": 150095,
          "investable_assets": 4773543,
          "net_worth_needed": 6991844
        },
        {
          "year": 2056,
          "age_client": 70,
          "age_co_client": 68,
          "net_worth": 7458069,
          "net_worth_todays_dollars": 3028062,
          "total_debts": 116404,
          "investable_assets": 5134524,
          "net_worth_needed": 7458069
        },
        {
          "year": 2057,
          "age_client": 71,
          "age_co_client": 69,
          "net_worth": 7956228,
          "net_worth_todays_dollars": 3134967,
          "total_debts": 80276,
          "investable_assets": 5522827,
          "net_worth_needed": 7956228
        },
        {
          "year": 2058,
          "age_client": 72,
          "age_co_client": 70,
          "net_worth": 8488634,
          "net_worth_todays_dollars": 3246019,
          "total_debts": 41537,
          "investable_assets": 5940523,
          "net_worth_needed": 8488634
        },
        {
          "year": 2059,
          "age_client": 73,
          "age_co_client": 71,
          "net_worth": 9057769,
          "net_worth_todays_dollars": 3361413,
          "total_debts": 0,
          "investable_assets": 6389838,
          "net_worth_needed": 9057769
        },
        {
          "year": 2060,
          "age_client": 74,
          "age_co_client": 72,
          "net_worth": 9621762,
          "net_worth_todays_dollars": 3465315,
          "total_debts": 0,
          "investable_assets": 6873168,
          "net_worth_needed": 9621762
        },
        {
          "year": 2061,
          "age_client": 75,
          "age_co_client": 73,
          "net_worth": 10070976,
          "net_worth_todays_dollars": 3520035,
          "total_debts": 0,
          "investable_assets": 7239265,
          "net_worth_needed": 10070976
        },
        {
          "year": 2062,
          "age_client": 76,
          "age_co_client": 74,
          "net_worth": 10538674,
          "net_worth_todays_dollars": 3574776,
          "total_debts": 0,
          "investable_assets": 7621320,
          "net_worth_needed": 10538674
        },
        {
          "year": 2063,
          "age_client": 77,
          "age_co_client": 75,
          "net_worth": 10894736,
          "net_worth_todays_dollars": 3586469,
          "total_debts": 0,
          "investable_assets": 7889132,
          "net_worth_needed": 10894736
        },
        {
          "year": 2064,
          "age_client": 78,
          "age_co_client": 76,
          "net_worth": 11251414,
          "net_worth_todays_dollars": 3594553,
          "total_debts": 0,
          "investable_assets": 8154877,
          "net_worth_needed": 11251414
        },
        {
          "year": 2065,
          "age_client": 79,
          "age_co_client": 77,
          "net_worth": 11607716,
          "net_worth_todays_dollars": 3598918,
          "total_debts": 0,
          "investable_assets": 8417479,
          "net_worth_needed": 11607716
        },
        {
          "year": 2066,
          "age_client": 80,
          "age_co_client": 78,
          "net_worth": 11961193,
          "net_worth_todays_dollars": 3599044,
          "total_debts": 0,
          "investable_assets": 8674407,
          "net_worth_needed": 11961193
        },
        {
          "year": 2067,
          "age_client": 81,
          "age_co_client": 79,
          "net_worth": 12310930,
          "net_worth_todays_dollars": 3594934,
          "total_debts": 0,
          "investable_assets": 8924657,
          "net_worth_needed": 12310930
        },
        {
          "year": 2068,
          "age_client": 82,
          "age_co_client": 80,
          "net_worth": 12653482,
          "net_worth_todays_dollars": 3585894,
          "total_debts": 0,
          "investable_assets": 9164697,
          "net_worth_needed": 12653482
        },
        {
          "year": 2069,
          "age_client": 83,
          "age_co_client": 81,
          "net_worth": 12988685,
          "net_worth_todays_dollars": 3572235,
          "total_debts": 0,
          "investable_assets": 9394271,
          "net_worth_needed": 12988685
        },
        {
          "year": 2070,
          "age_client": 84,
          "age_co_client": 82,
          "net_worth": 13311338,
          "net_worth_todays_dollars": 3552908,
          "total_debts": 0,
          "investable_assets": 9608081,
          "net_worth_needed": 13311338
        },
        {
          "year": 2071,
          "age_client": 85,
          "age_co_client": 83,
          "net_worth": 13621274,
          "net_worth_todays_dollars": 3528316,
          "total_debts": 0,
          "investable_assets": 9805864,
          "net_worth_needed": 13621274
        },
        {
          "year": 2072,
          "age_client": 86,
          "age_co_client": 84,
          "net_worth": 13914178,
          "net_worth_todays_dollars": 3497798,
          "total_debts": 0,
          "investable_assets": 9983203,
          "net_worth_needed": 13914178
        },
        {
          "year": 2073,
          "age_client": 87,
          "age_co_client": 85,
          "net_worth": 14188088,
          "net_worth_todays_dollars": 3461373,
          "total_debts": 0,
          "investable_assets": 10138033,
          "net_worth_needed": 14188088
        },
        {
          "year": 2074,
          "age_client": 88,
          "age_co_client": 86,
          "net_worth": 14442231,
          "net_worth_todays_dollars": 3419371,
          "total_debts": 0,
          "investable_assets": 10269474,
          "net_worth_needed": 14442231
        },
        {
          "year": 2075,
          "age_client": 89,
          "age_co_client": 87,
          "net_worth": 14670470,
          "net_worth_todays_dollars": 3370881,
          "total_debts": 0,
          "investable_assets": 10371279,
          "net_worth_needed": 14670470
        },
        {
          "year": 2076,
          "age_client": 90,
          "age_co_client": 88,
          "net_worth": 14874373,
          "net_worth_todays_dollars": 3316848,
          "total_debts": 0,
          "investable_assets": 10444903,
          "net_worth_needed": 14874373
        },
        {
          "year": 2077,
          "age_client": null,
          "age_co_client": 89,
          "net_worth": 15334811,
          "net_worth_todays_dollars": 3318583,
          "total_debts": 0,
          "investable_assets": 10771100,
          "net_worth_needed": 15334811
        },
        {
          "year": 2078,
          "age_client": null,
          "age_co_client": 90,
          "net_worth": 15957595,
          "net_worth_todays_dollars": 3351422,
          "total_debts": 0,
          "investable_assets": 11255558,
          "net_worth_needed": 15957595
        },
        {
          "year": 2079,
          "age_client": null,
          "age_co_client": 90,
          "net_worth": 16115848,
          "net_worth_todays_dollars": 3359400,
          "total_debts": 0,
          "investable_assets": 11378578,
          "net_worth_needed": 16115848
        }
      ],
      "firstNegativeInvestableYear": null,
      "firstNegativeNetWorthYear": null,
      "peakInvestable": 11378578,
      "endOfPlan": {
        "year": 2079,
        "age_client": null,
        "age_co_client": 90,
        "net_worth": 16115848,
        "net_worth_todays_dollars": 3359400,
        "total_debts": 0,
        "investable_assets": 11378578,
        "net_worth_needed": 16115848
      }
    },
    "goals": {
      "goalsSummary": [
        {
          "goalType": "RETIREMENT",
          "value": "Both Timothy and Melanie want to retire in 2048 at ages 62 and 60."
        },
        {
          "amount": 6000,
          "goalType": "VACATION",
          "value": "Going on a $6,000 vacation every year."
        },
        {
          "amount": 45000,
          "goalType": "COLLEGE",
          "value": "Finance education for 2 children ($45,000 in total for each child)."
        },
        {
          "amount": 600000,
          "goalType": "PURCHASE",
          "subType": "REAL_ESTATE_PURCHASE",
          "value": "Plan to purchase a home for $600,000 in 2030."
        },
        {
          "amount": 45000,
          "goalType": "PURCHASE",
          "subType": "VEHICLE_PURCHASE",
          "value": "Plan to purchase a vehicle for $45,000 in 2028."
        }
      ],
      "chartGoals": [
        {
          "date": "2027-01-01T00:00:00.000Z",
          "goalType": "VACATION",
          "name": "Go on vacation",
          "termDate": "2048-04-01T00:00:00.000Z"
        },
        {
          "date": "2028-07-01T00:00:00.000Z",
          "goalType": "PURCHASE",
          "name": "Purchase a vehicle",
          "subType": "VEHICLE_PURCHASE",
          "termDate": "2079-03-01T00:00:00.000Z"
        },
        {
          "date": "2030-01-01T00:00:00.000Z",
          "goalType": "PURCHASE",
          "name": "Purchase a home",
          "subType": "REAL_ESTATE_PURCHASE",
          "termDate": "2030-01-01T00:00:00.000Z"
        },
        {
          "date": "2038-08-01T00:00:00.000Z",
          "goalType": "COLLEGE",
          "name": "College Liam",
          "termDate": "2042-01-01T00:00:00.000Z"
        },
        {
          "date": "2041-08-01T00:00:00.000Z",
          "goalType": "COLLEGE",
          "name": "College Josh",
          "termDate": "2045-01-01T00:00:00.000Z"
        },
        {
          "date": "2048-03-01T00:00:00.000Z",
          "goalType": "RETIREMENT",
          "name": "Melanie's Retirement"
        },
        {
          "date": "2048-04-01T00:00:00.000Z",
          "goalType": "RETIREMENT",
          "name": "Timothy's Retirement"
        }
      ]
    },
    "facts": {
      "facts": {
        "cash": {
          "monthsCovered": {
            "unit": "months",
            "basis": "n/a",
            "label": "Months of essential expenses accessible cash covers",
            "value": "16",
            "period": "today, before near-term goals",
            "replaces": [
              "ratios.emergencyFund.emergencyFundMonths (capped at \"+12\")",
              "savingsAndExpenses.liquidityContext.emergencyFundInMonths",
              "protection.emergencyFund.emergencyFundCoverageEvaluation.monthsCovered"
            ],
            "notToBeConfusedWith": [
              "the recommended number of months"
            ]
          },
          "nearTermGoals": [
            {
              "note": "A goal payment, not a down payment unless the goal is a purchase.",
              "unit": "USD",
              "basis": "as entered",
              "label": "Go on vacation: cash to hold for its next payment",
              "value": 6000,
              "period": "next payment January 2027, then every year",
              "replaces": [
                "extraCashOutflows[].downpayment (holds any goal payment)"
              ]
            }
          ],
          "accessibleCash": {
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Accessible cash (bank accounts plus taxable money market)",
            "value": 150800,
            "period": "balance today",
            "notToBeConfusedWith": [
              "bank cash alone (excludes money market)",
              "cash inside retirement accounts, which is not accessible"
            ]
          },
          "totalCashNeeded": {
            "max": 90577.5,
            "min": 81180,
            "note": "Never call this the emergency reserve.",
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Cash target: emergency reserve plus near-term goals",
            "period": "target balance today",
            "replaces": [
              "ratios.emergencyFund.adjustedRecommendedMin/MaxAmount",
              "savingsAndExpenses.liquidityContext.min/maxEmergencyFundTargetAndShortTermNeeds",
              "cashNeeds.cashTarget"
            ],
            "notToBeConfusedWith": [
              "emergencyReserve"
            ]
          },
          "cashAboveReserve": {
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Cash above the top of the emergency reserve, before near-term goals",
            "value": 66222.5,
            "period": "today",
            "notToBeConfusedWith": [
              "cashAboveTotalNeeded"
            ]
          },
          "emergencyReserve": {
            "max": 84577.5,
            "min": 75180,
            "note": "Excludes near-term goals. This alone is the emergency reserve.",
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Recommended emergency reserve (8–9 months of essential expenses)",
            "period": "target balance today",
            "replaces": [
              "ratios.emergencyFund.min/maxRecommendedEmergencyFund",
              "savingsAndExpenses.liquidityContext.min/maxEmergencyFundTargetInCash",
              "protection.emergencyFund.recommendedEmergencyFundLevels.minimum/maximumAmountRecommended",
              "cashNeeds.emergencyFund"
            ],
            "notToBeConfusedWith": [
              "totalCashNeeded"
            ]
          },
          "cashAboveTotalNeeded": {
            "note": "This is the cash that is free after the reserve and the near-term goals. Say it is above both; never call it the amount above the reserve or the reserve target.",
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Cash above the emergency reserve and near-term goals",
            "value": 60222.5,
            "period": "today",
            "replaces": [
              "ratios.emergencyFund.excessOverAdjustedMax",
              "ratios.emergencyFund.extraCashAboveMaxEmergencyFundPlusStg",
              "savingsAndExpenses.liquidityContext.excessWithRecommendedMaxEmergencyFundAndShortTermNeeds",
              "protection.emergencyFund.emergencyFundCoverageEvaluation.adjustedEmergencyFundExcessAfterShortTermCashNeeds",
              "cashNeeds.accessibleCashExcess"
            ],
            "notToBeConfusedWith": [
              "cashAboveReserve"
            ]
          },
          "monthsCoveredAfterNearTermGoals": {
            "unit": "months",
            "basis": "n/a",
            "label": "Months of essential expenses covered after setting aside near-term goals",
            "value": "15.4",
            "period": "today",
            "replaces": [
              "ratios.emergencyFund.adjustedMonthsCoveredAfterShortTermCashNeeds"
            ]
          }
        },
        "rules": [
          "These facts are the only figures to quote for these concepts. Quote the label's meaning with the number; never relabel a fact as another one.",
          "Each fact names the facts it must not be confused with. Never call one by the other's name.",
          "Keep the unit: a USD/yr figure is always said per year, a lump sum never is.",
          "Do not add, subtract or compare two facts unless a fact says how they relate.",
          "Never quote a date that is before the plan date.",
          "Write a date as month and year (August 2039), never as an ISO date (2039-08-01).",
          "Write a ratio or rate as a percentage (55%), never as a decimal (0.551).",
          "A fact's `replaces` lists key-metric fields that hold the same or a confusable figure under a misleading name. When you see one of those fields in your other inputs, quote the fact with its label instead. Field names are never labels."
        ],
        "education": {
          "fundingGap": {
            "note": "Not the amount to invest today and not the goal. It is larger than the total cost because college costs are inflated to the years they are paid.",
            "unit": "USD",
            "basis": "engine estimate: inflated college costs valued at college start, restated in today's dollars",
            "label": "College funding still needed beyond current 529 balances",
            "value": 113508.6,
            "period": "one lump sum for all college years",
            "notToBeConfusedWith": [
              "totalCostAllGoals",
              "combinedAnnualCost"
            ]
          },
          "totalCostPerGoal": [
            {
              "unit": "USD",
              "basis": "today's dollars at the plan date, before education inflation",
              "label": "College Liam: total college cost, whole program",
              "value": 45000,
              "period": "4 years of college",
              "notToBeConfusedWith": [
                "annualCostPerGoal"
              ]
            },
            {
              "unit": "USD",
              "basis": "today's dollars at the plan date, before education inflation",
              "label": "College Josh: total college cost, whole program",
              "value": 45000,
              "period": "4 years of college",
              "notToBeConfusedWith": [
                "annualCostPerGoal"
              ]
            }
          ],
          "annualCostPerGoal": [
            {
              "unit": "USD/yr",
              "basis": "today's dollars at the plan date",
              "label": "College Liam: yearly college cost",
              "value": 11250,
              "period": "each year of college, 2038–2041 (4 payments); college starts August 2038, about 12 years from now",
              "replaces": [
                "listOfChildrenAndEducationGoals column \"Years to uni\" (rounded down)",
                "listOfChildrenAndEducationGoals column \"Education goal ($)\" (a yearly cost)",
                "protection.lifeInsurance.educationGoal column \"Total cost\" (a yearly cost)"
              ],
              "notToBeConfusedWith": [
                "totalCostPerGoal",
                "fundingGap"
              ]
            },
            {
              "unit": "USD/yr",
              "basis": "today's dollars at the plan date",
              "label": "College Josh: yearly college cost",
              "value": 11250,
              "period": "each year of college, 2041–2044 (4 payments); college starts August 2041, about 15 years from now",
              "replaces": [
                "listOfChildrenAndEducationGoals column \"Years to uni\" (rounded down)",
                "listOfChildrenAndEducationGoals column \"Education goal ($)\" (a yearly cost)",
                "protection.lifeInsurance.educationGoal column \"Total cost\" (a yearly cost)"
              ],
              "notToBeConfusedWith": [
                "totalCostPerGoal",
                "fundingGap"
              ]
            }
          ],
          "extraYearlySaving": {
            "unit": "USD/yr",
            "basis": "engine estimate",
            "label": "Extra yearly saving needed for college (first year)",
            "value": 4609.22,
            "period": "per year from now until each child starts college, rising each year",
            "notToBeConfusedWith": [
              "annualCostPerGoal"
            ]
          },
          "totalCostAllGoals": {
            "note": "This is the education goal when one total is needed.",
            "unit": "USD",
            "basis": "today's dollars at the plan date, before education inflation",
            "label": "Total college cost, all children, whole programs",
            "value": 90000,
            "period": "all college years",
            "notToBeConfusedWith": [
              "fundingGap",
              "combinedAnnualCost"
            ]
          },
          "combinedAnnualCost": {
            "note": "Not the education goal and not a yearly household bill. Prefer per-child yearly costs; for one total use totalCostAllGoals.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Sum of each child's yearly college cost",
            "value": 22500,
            "period": "one year per child added together; their college years do not overlap",
            "replaces": [
              "assetsAndInvestments.educationGoalNeeds.educationGoalAmount",
              "savingsAndExpenses.goals.totalEducationGoalRequiredAmount",
              "ratios.educationSavings.totalEducationGoalsAmount"
            ]
          }
        },
        "retirement": {
          "spendingGap": {
            "note": "Savings, cash and required IRA withdrawals included, pay this each year on average. It is what the plan asks of savings.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Yearly retirement spending that income does not cover, paid from savings",
            "value": 12852.82,
            "period": "average over the 31 years of retirement",
            "notToBeConfusedWith": [
              "averagePortfolioDraw"
            ]
          },
          "spendingNeed": {
            "note": "Includes taxes, debt payments and goals after retirement; do not add those on top. annualTotalIncomeNeeded adds an estimated long-term care cost: do not quote it.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Yearly retirement spending need (excluding estimated long-term care)",
            "value": 184303.51,
            "period": "average over the 31 years of retirement",
            "replaces": [
              "retirementAndOtherGoals.incomeNeedsAndWithdrawals.annualTotalIncomeNeeded (adds estimated long-term care)"
            ]
          },
          "guaranteedIncome": {
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Guaranteed income in retirement (Social Security, annuities, pensions)",
            "value": 171055.83,
            "period": "average over the 31 years of retirement; years before a benefit starts count as zero"
          },
          "incomeShareOfNeed": {
            "unit": "percent",
            "basis": "today's dollars at the plan date",
            "label": "Share of the yearly retirement spending need that income covers (guaranteed and other income)",
            "value": "93%",
            "period": "average over the 31 years of retirement",
            "replaces": [
              "retirementAndOtherGoals.incomeVsIncomeNeeds.allIncomesVsIncomeNeededExLtcCosts",
              "ratios.guaranteedIncomeRatio.allIncomesVsIncomeNeededExLtcCosts"
            ]
          },
          "netCashFlowThisYear": {
            "note": "The outflow table counts the employer 401(k) match of 14000 as household savings; the employer pays it, so this figure does not subtract it. Income 270000 minus outflows 247039.25 is 22960.75: never present that subtraction as this figure.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Net cash flow this year",
            "value": 36960.75,
            "period": "the plan year",
            "notToBeConfusedWith": [
              "averagePortfolioDraw",
              "withdrawalRateThisYear",
              "savingsCapacity"
            ]
          },
          "averagePortfolioDraw": {
            "note": "Counts only the months when spending exceeds every inflow. Required IRA withdrawals and other inflows drawn from savings are not in it, so savings pay more than this. Draws are concentrated in fewer years and are larger in those years. It is not the spending gap: never present it as filling that gap, and never use it to say the plan leans little on savings.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Average yearly draw from savings in retirement",
            "value": 20687.67,
            "period": "average over the 31 years of retirement, counting years with no draw as zero",
            "replaces": [
              "retirementAndOtherGoals.withdrawals.supplementalAnnualWithdrawals"
            ],
            "notToBeConfusedWith": [
              "spendingGap"
            ]
          },
          "savingsLeftAtPlanEnd": {
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Savings and investments left at the end of the plan",
            "value": 2371900.89,
            "period": "end of plan",
            "replaces": [
              "assetDepletion.liquidAssetsAtEndOfPlan",
              "capacity.liquidAssetsAtEndOfPlan"
            ]
          },
          "withdrawalRateAverage": {
            "note": "A lifetime average. Do not compare it with the 4% sustainable rate.",
            "unit": "percent",
            "basis": "today's dollars at the plan date",
            "label": "Average yearly draw as a share of savings at the start of retirement",
            "value": "1.0%",
            "period": "average over the 31 years of retirement",
            "replaces": [
              "retirementAndOtherGoals.withdrawals.withdrawalRatio"
            ],
            "notToBeConfusedWith": [
              "withdrawalRateThisYear"
            ]
          }
        }
      },
      "ratios": {
        "umbrella": {
          "claim": "No coverage",
          "color": "R",
          "currentCoverage": 0,
          "recommendedCoverage": 1000000
        },
        "currentDPD": {
          "debtLastPayment": "2039-09-01T00:00:00.000Z",
          "beforeRetirement": true,
          "yearsInRetirement": 0,
          "avgDTIInRetirement": 0,
          "howMuchInRetirement": "Less than 5 years",
          "avgDTIInRetirementLevel": "<10%"
        },
        "vehiclePRI": {
          "vehiclesPri": 0.0178,
          "monthlyGrossIncome": 22500,
          "doTheyHaveAnyVehicle": true,
          "vehiclesMonthlyPayments": 400,
          "doTheyHaveAnyVehicleLoan": true,
          "vehiclesPriFirstThreshold": 0.1,
          "vehiclesPriSecondThreshold": 0.15
        },
        "debtToIncome": {
          "ratio": 0.151,
          "debtOnlyDti": 0.1316,
          "grossIncome": 270000,
          "rentalPayment": 0,
          "mortgagesPayments": 24000,
          "monthlyDebtPayments": 2960,
          "otherHousingExpenses": 5250,
          "totalMonthlyObligations": 3397.5,
          "debtPaymentExcludingMortgages": 11520
        },
        "housingRatio": {
          "ratio": 0.1083,
          "grossIncome": 270000,
          "rentalPayment": 0,
          "housingExpenses": 29250,
          "mortgagePayment": 24000,
          "otherHousingExpenses": 5250
        },
        "indebtedness": {
          "debt": true,
          "housing": "own",
          "debtBalance": 93000,
          "monthlyDebtPayment": 2960,
          "totalMonthlyObligations": 3397.5
        },
        "savingsLevel": {
          "ratio": 0.2278,
          "grossIncome": 270000,
          "savingAmount": 61500
        },
        "emergencyFund": {
          "claim": "Very over-reserved",
          "color": "R",
          "nrOfEarners": 2,
          "emergencyFund": 150800,
          "incomeDisparity": "Low",
          "monthlyExpenses": 9397.5,
          "totalCashAmount": 150000,
          "inaccessibleCash": 3400,
          "excessOverBaseMax": 66222.5,
          "extraCashOutflows": [
            {
              "amount": 0,
              "description": "Go on vacation",
              "downpayment": 6000
            }
          ],
          "shortfallToBaseMin": "Not applicable",
          "emergencyFundMonths": "+12",
          "highestEarningsLevel": "High",
          "shortTermGoalsNeeded": [
            {
              "date": "2027-01-01T00:00:00.000Z",
              "amount": 6000,
              "description": "Go on vacation",
              "paymentFrequency": "ANNUAL"
            }
          ],
          "excessOverAdjustedMax": 60222.5,
          "maxRecommendedEFMonths": 9,
          "minRecommendedEFMonths": 8,
          "shortfallToAdjustedMin": "Not applicable",
          "totalMoneyMarketAmount": 800,
          "deltaToMaxEmergencyFund": "Not applicable",
          "moneyMarketFundAccounts": [
            {
              "accountName": "Brokerage account",
              "accountType": "Brokerage account",
              "cashBalance": 800
            }
          ],
          "extraEmergencyFundNeeded": 6000,
          "maxRecommendedEmergencyFund": 84577.5,
          "maximumEmergencyFundPlusStg": 90577.5,
          "minRecommendedEmergencyFund": 75180,
          "adjustedRecommendedMaxAmount": 90577.5,
          "adjustedRecommendedMinAmount": 81180,
          "deltaToMaxEmergencyFundPlusStg": "Not applicable",
          "extraCashAboveMaxEmergencyFund": 66222.5,
          "extraCashAboveMinEmergencyFund": 75620,
          "cashReservesAfterShortTermCashNeeds": 144800,
          "extraCashAboveMaxEmergencyFundPlusStg": 60222.5,
          "adjustedMonthsCoveredAfterShortTermCashNeeds": 15
        },
        "lifeInsurance": {
          "scenario": {
            "kids": true,
            "earners": 2,
            "spouses": 2,
            "scenario": 9,
            "debtBurden": "Low",
            "incomeDisparity": "Low"
          },
          "clientEarner": {
            "overInsured": 12,
            "isHighEarner": true,
            "underInsured": 0,
            "adequatelyInsured": 5,
            "slightlyOverInsured": 10,
            "slightlyUnderInsured": 4
          },
          "clientCoverage": 140000,
          "coClientEarner": {
            "overInsured": 12,
            "isHighEarner": false,
            "underInsured": 0,
            "adequatelyInsured": 5,
            "slightlyOverInsured": 10,
            "slightlyUnderInsured": 4
          },
          "coClientCoverage": 110000,
          "clientCoverageKey": "Under insured",
          "clientEarnedIncome": 150000,
          "clientCoverageColor": "R",
          "coClientCoverageKey": "Under insured",
          "coClientEarnedIncome": 120000,
          "coClientCoverageColor": "R",
          "clientReplacementValue": 0,
          "clientCoverageOverIncome": 0.9333,
          "coClientReplacementValue": 0,
          "coClientCoverageOverIncome": 0.9167,
          "recommendedClientMaxCoverage": 1500000,
          "recommendedClientMinCoverage": 750000,
          "recommendedCoClientMaxCoverage": 1200000,
          "recommendedCoClientMinCoverage": 600000,
          "lifeInsuranceCoverageGapsAndExcess": {
            "clientExcess": 0,
            "coClientExcess": 0,
            "clientShortfall": 610000,
            "coClientShortfall": 490000
          }
        },
        "creditCardDebt": {
          "balance": 18000,
          "hasDebt": true,
          "ccPayoffDate": "2039-09-01T00:00:00.000Z",
          "monthlyPayment": 300,
          "retirementDate": "2048-03-01T00:00:00.000Z",
          "yearsInRetirement": "Not applicable",
          "maxCCPaymentNormal": 650.74,
          "minCCPaymentNormal": 457.08,
          "yearsToCcPayoffDate": 12,
          "paymentsEqualToInterest": 270,
          "percentageOfCCOverGrossIncome": 0.0667
        },
        "educationSavings": {
          "totalGAP": 113508.6,
          "goalsSummary": [
            {
              "date": "2038-08-01T00:00:00.000Z",
              "weight": 0.5665,
              "kidsAge": 6,
              "goalName": "College Liam",
              "termDate": "2042-01-01T00:00:00.000Z",
              "totalGAP": 55117.56,
              "goalAmount": 11250,
              "yearsToStart": 11.75,
              "accountBalance": 0,
              "accountSavings": 0,
              "requiredSavings": 2680.37,
              "requiredExtraSavings": 2680.37,
              "goalRequiredAmountAtToday": 55117.56,
              "expectedCapitalizationAmount": 186.65
            },
            {
              "date": "2041-08-01T00:00:00.000Z",
              "weight": 0.4335,
              "kidsAge": 3,
              "goalName": "College Josh",
              "termDate": "2045-01-01T00:00:00.000Z",
              "totalGAP": 58391.04,
              "goalAmount": 11250,
              "yearsToStart": 14.75,
              "accountBalance": 0,
              "accountSavings": 0,
              "requiredSavings": 1928.84,
              "requiredExtraSavings": 1928.84,
              "goalRequiredAmountAtToday": 58391.04,
              "expectedCapitalizationAmount": 142.85
            }
          ],
          "savingsIncrease": 0.03,
          "expectedPerformance": 0.0753,
          "totalRequiredSavings": 4609.22,
          "current529AccountsBalance": 0,
          "totalEducationGoalsAmount": 22500,
          "totalRequiredExtraSavings": 4609.22,
          "annualSavingsGoingTo529Accounts": 0,
          "doTheyHaveEducationFundingGoals": true,
          "totalEducationGoalRequiredAmountAtToday": 113508.6
        },
        "incomePercentile": {
          "state": "CA",
          "hasSpouse": true,
          "percentile": 0.9,
          "grossIncome": 270000
        },
        "realEstateEquity": {
          "ratio": 0.8571,
          "realEstateAssets": 350000,
          "realEstateEquity": 300000,
          "realEstateMortgages": 50000,
          "realEstateEquityThreshold1": 0.2,
          "realEstateEquityThreshold2": 0.5
        },
        "retirementSavings": {
          "generalInflation": 0.03,
          "yearsToRetirement": 21,
          "averagePerformance": 0.0756,
          "requiredExtraSavings": 0,
          "planningGapAtRetirementAge": 0,
          "supplementalTotalWithdrawals": 1316966.09,
          "planningGapAtRetirementAgeInTodaysDollars": 0,
          "balanceInRetirementAccountsAtRetirementAge": 2651947.59,
          "supplementalTotalWithdrawalsInTodaysDollars": 641317.73,
          "balanceInRetirementAccountsAtRetirementAgeInTodaysDollars": 1425552.5
        },
        "withdrawalRateRatio": {
          "withdrawalRate": 0.0111,
          "withdrawalRateToday": 0.0087,
          "annualWithdrawalsToday": 3135.59,
          "annualWithdrawalsOnAverage": 42482.78,
          "withdrawalRateAtTodaysValue": 0.0102,
          "totalWithdrawalsDuringRetirement": 1316966.09,
          "investableAssetsAtFirstInRetireYrs": 3834317.29,
          "investableAssetsAt2050YrsAtTodaysValue": 2018375.92,
          "annualWithdrawalsOnAverageAtTodaysValue": 20687.67,
          "totalWithdrawalsDuringRetirementAtTodaysValue": 641317.73
        },
        "investableAssetLevel": {
          "basis": "income",
          "ratio": 1.3333,
          "cashBalance": 150000,
          "grossIncome": 270000,
          "annualExpenses": 112774,
          "investableAssets": 210000,
          "portfolioSustainabilityMultiple": 1.3333
        },
        "guaranteedIncomeRatio": {
          "inflowsSummary": {
            "name": "All inflows",
            "total": 17685194.58,
            "guaranteedIncome": {
              "name": "Guaranteed income",
              "total": 17661940.89,
              "ANNUITY_INCOME": {
                "name": "Annuity income",
                "total": 11565912.68,
                "totalAtTodaysValue": 3469028.55,
                "yearlyAverageTotal": 373093.96,
                "yearlyAverageTotalAtTodaysValue": 111904.15
              },
              "SOCIAL_SECURITY": {
                "name": "Social security",
                "total": 6096028.22,
                "totalAtTodaysValue": 1833702.02,
                "yearlyAverageTotal": 196646.07,
                "yearlyAverageTotalAtTodaysValue": 59151.68
              },
              "totalAtTodaysValue": 5302730.58,
              "yearlyAverageTotal": 569740.03,
              "PENSION_AND_DEFINED_BENEFIT": {
                "name": "Pension / defined benefit",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "yearlyAverageTotalAtTodaysValue": 171055.83
            },
            "otherIncomeSources": {
              "name": "Other income sources",
              "total": 23253.68,
              "STOCK_COMP": {
                "name": "Stock compensation",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "OTHER_INFLOW": {
                "name": "Other income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "DEFERRED_COMP": {
                "name": "Deferred compensation",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "EARNED_INCOME": {
                "name": "Earned income",
                "total": 23253.68,
                "totalAtTodaysValue": 12240.69,
                "yearlyAverageTotal": 750.12,
                "yearlyAverageTotalAtTodaysValue": 394.86
              },
              "RENTAL_INCOME": {
                "name": "Rental income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "ROYALTY_AND_IP": {
                "name": "Royalty & IP",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "SUPPORT_TRANSFER": {
                "name": "Support & transfer",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "GOVERNMENT_BENEFIT": {
                "name": "Government benefit",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "totalAtTodaysValue": 12240.69,
              "yearlyAverageTotal": 750.12,
              "BUSINESS_PASSIVE_INCOME": {
                "name": "Business passive income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "PROPERTY_LIQUIDATION_EVENT": {
                "name": "Property liquidation event",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "yearlyAverageTotalAtTodaysValue": 394.86
            },
            "totalAtTodaysValue": 5314971.26,
            "yearlyAverageTotal": 570490.15,
            "yearlyAverageTotalAtTodaysValue": 171450.69
          },
          "outflowsSummary": {
            "name": "Outflows",
            "total": 22834895.03,
            "ltcCosts": {
              "name": "LTC Costs",
              "total": 4291352.09,
              "totalAtTodaysValue": 974057.64,
              "yearlyAverageTotal": 138430.71,
              "yearlyAverageTotalAtTodaysValue": 243514.41
            },
            "excludingLtcCosts": {
              "name": "Excluding LTC Costs",
              "total": 18543542.94,
              "totalAtTodaysValue": 5713408.75,
              "yearlyAverageTotal": 598178.8,
              "yearlyAverageTotalAtTodaysValue": 184303.51
            },
            "totalAtTodaysValue": 6687466.39,
            "yearlyAverageTotal": 736609.52,
            "yearlyAverageTotalAtTodaysValue": 215724.72
          },
          "ltcCostsAreEstimated": true,
          "allIncomesVsIncomeNeeded": 0.7948,
          "otherIncomeVsIncomeNeeded": 0.0018,
          "guaranteedIncomeVsIncomeNeeded": 0.7929,
          "allIncomesVsIncomeNeededExLtcCosts": 0.9303,
          "otherIncomeVsIncomeNeededExLtcCosts": 0.0021,
          "guaranteedIncomeVsIncomeNeededExLtcCosts": 0.9281
        }
      },
      "protection": {
        "emergencyFund": {
          "clientProfile": {
            "kids": [
              {
                "age": 6,
                "name": "Liam"
              },
              {
                "age": 3,
                "name": "Josh"
              }
            ],
            "clientAge": 40,
            "clientName": "Timothy",
            "coClientAge": 38,
            "coClientName": "Melanie",
            "numberOfChildren": 2,
            "clientRiskProfile": "(4) Growth",
            "clientIncomeAtRisk": 150000,
            "coClientRiskProfile": "(3) Moderate",
            "coClientIncomeAtRisk": 120000
          },
          "cashAccountList": [
            {
              "name": "Cash account",
              "type": "Checking account",
              "owner": "Melanie",
              "value": 150000
            }
          ],
          "extraCashOutflows": [
            {
              "amount": 0,
              "description": "Go on vacation",
              "downpayment": 6000
            }
          ],
          "realEstateDetails": [
            [
              "Real estate",
              "Market value",
              "Mortgage balance",
              "Equity",
              "HELOC"
            ],
            [
              "Primary home",
              350000,
              50000,
              0.8571,
              0
            ]
          ],
          "cashAndExpensesOverview": {
            "cashReserves": 150800,
            "livingExpenses": 6000,
            "housingExpenses": 2437.5,
            "monthlyExpenses": 9397.5,
            "totalCashAmount": 150800,
            "otherDebtPayment": 960,
            "totalMoneyMarketAmount": 800,
            "cashReservesAfterShortTermCashNeeds": 144800
          },
          "otherAccountsContributions": [
            [
              "Account",
              "Holder",
              "Current contribution"
            ],
            [
              "Brokerage account",
              "Melanie",
              15000
            ],
            [
              "Cash account",
              "Melanie",
              7500
            ]
          ],
          "retirementAndEducationGaps": {
            "educationGap": 113508.6,
            "retirementGap": 0
          },
          "recommendedEmergencyFundLevels": {
            "maximumAmountRecommended": 84577.5,
            "maximumMonthsRecommended": 9,
            "minimumAmountRecommended": 75180,
            "minimumMonthsRecommended": 8,
            "extraEmergencyFundNeededByShortTermCashNeeds": 6000,
            "maximumAmountAdjustedAfterShortTermCashNeeds": 90577.5,
            "minimumAmountAdjustedAfterShortTermCashNeeds": 81180
          },
          "emergencyFundCoverageEvaluation": {
            "monthsCovered": 16,
            "emergencyFundExcess": 66222.5,
            "emergencyFundShortfall": "Not applicable",
            "adjustedMonthsCoveredAfterShortTermCashNeeds": 15,
            "adjustedEmergencyFundExcessAfterShortTermCashNeeds": 60222.5,
            "adjustedEmergencyFundShortfallAfterShortTermCashNeeds": "Not applicable"
          },
          "taxAdvantagedAccountsContributions": [
            [
              "Account",
              "Holder",
              "Current contribution",
              "Max contribution"
            ],
            [
              "401(k) - Timothy",
              "Timothy",
              22000,
              24500
            ],
            [
              "401k - Melanie",
              "Melanie",
              17000,
              24500
            ],
            [
              "IRA - Roth Melanie",
              "Melanie",
              0,
              24500
            ],
            [
              "IRA - Roth Timothy",
              "Timothy",
              0,
              24500
            ]
          ]
        },
        "lifeInsurance": {
          "legacyGoal": {
            "amount": "Not applicable",
            "hasLegacyGoal": false
          },
          "educationGoal": [
            [
              "Kid name",
              "Total cost",
              "Inception Year"
            ],
            [
              "Liam",
              11250,
              "2038"
            ],
            [
              "Josh",
              11250,
              "2041"
            ]
          ],
          "clientDemographics": {
            "kids": [
              {
                "age": 6,
                "name": "Liam"
              },
              {
                "age": 3,
                "name": "Josh"
              }
            ],
            "clientAge": 40,
            "clientName": "Timothy",
            "coClientAge": 38,
            "coClientName": "Melanie",
            "numberOfChildren": 2,
            "clientRiskProfile": "(4) Growth",
            "clientIncomeAtRisk": 150000,
            "coClientRiskProfile": "(3) Moderate",
            "coClientIncomeAtRisk": 120000
          },
          "lifeInsuranceCoverageBasics": {
            "hasLifeInsuranceClient": true,
            "hasLifeInsuranceCoClient": true,
            "lifeInsuranceAmountClient": 140000,
            "lifeInsuranceAmountCoClient": 110000
          },
          "lifeInsuranceCoverageGapsAndExcess": {
            "clientExcess": 0,
            "coClientExcess": 0,
            "clientShortfall": 610000,
            "coClientShortfall": 490000
          },
          "lifeInsuranceCoverageRecommendations": {
            "clientMaxRecommendedCoverage": 1500000,
            "clientMinRecommendedCoverage": 750000,
            "coClientMaxRecommendedCoverage": 1200000,
            "coClientMinRecommendedCoverage": 600000
          }
        },
        "umbrellaInsurance": {
          "assetExposed": {
            "netWorth": 695500,
            "totalLiquidAssets": 360000,
            "assetExposedSummary": [
              [
                "Asset",
                "Number",
                "Value",
                "Equity"
              ],
              [
                "Real estate",
                1,
                350000,
                300000
              ],
              [
                "Vehicle",
                2,
                58500,
                48500
              ],
              [
                "Other asset",
                1,
                20000,
                20000
              ],
              [
                "Total",
                4,
                428500,
                368500
              ]
            ]
          },
          "umbrellaCoverage": {
            "claim": "No coverage",
            "hasUmbrellaPolicy": false,
            "umbrellaCoverageAmount": "Not applicable"
          },
          "clientDemographics": {
            "kids": [
              {
                "age": 6,
                "name": "Liam"
              },
              {
                "age": 3,
                "name": "Josh"
              }
            ],
            "clientAge": 40,
            "clientName": "Timothy",
            "coClientAge": 38,
            "coClientName": "Melanie",
            "numberOfChildren": 2,
            "clientRiskProfile": "(4) Growth",
            "clientIncomeAtRisk": 150000,
            "coClientRiskProfile": "(3) Moderate",
            "coClientIncomeAtRisk": 120000
          },
          "assetInsuranceStatus": [
            {
              "assetName": "Primary home",
              "assetType": "Real Estate",
              "isInsured": true,
              "equityAmount": 300000
            },
            {
              "assetName": "Ford",
              "assetType": "Vehicle",
              "isInsured": true,
              "equityAmount": 28500
            },
            {
              "assetName": "Tesla",
              "assetType": "Vehicle",
              "isInsured": true,
              "equityAmount": 20000
            }
          ],
          "coverageRecommendationsAndAnalysis": {
            "umbrellaCoverageGap": 1000000,
            "umbrellaCoverageExcess": "Not applicable",
            "umbrellaMinRecommendedCoverage": 1000000
          }
        }
      },
      "debtManagement": {
        "realEstate": {
          "realEstateEquity": 300000,
          "realEstateEquityThreshold1": 0.2,
          "realEstateEquityThreshold2": 0.5,
          "percentageOfRealEstateEquity": 0.8571
        },
        "listOfDebts": [
          [
            "Name",
            "Type",
            "Balance",
            "Interest rate",
            "Monthly payments",
            "Interest paid"
          ],
          [
            "Primary home mortgage",
            "Mortgage",
            50000,
            0.06,
            2000,
            250
          ],
          [
            "Chase CC",
            "Credit card",
            18000,
            0.18,
            300,
            270
          ],
          [
            "Melanie's student loan",
            "Student loan",
            15000,
            0.055,
            260,
            68.75
          ],
          [
            "Tesla loan",
            "Vehicle loan",
            10000,
            0.045,
            400,
            37.5
          ]
        ],
        "debtOverview": {
          "debt": true,
          "debtBalance": 93000,
          "beforeRetirement": true,
          "avgDtiInRetirement": 0,
          "percentageOfDebtOverGrossIncome": 0.3444
        },
        "clientProfile": {
          "clientName": "Timothy",
          "coClientName": "Melanie"
        },
        "creditCardDebt": {
          "ccPayoffDate": "2039-09-01T00:00:00.000Z",
          "retirementDate": "2048-03-01T00:00:00.000Z",
          "ccMonthlyPayment": 300,
          "creditCardBalance": 18000,
          "yearsInRetirement": "Not applicable",
          "maxCcPaymentNormal": 650.74,
          "minCcPaymentNormal": 457.08,
          "yearsToCcPayoffDate": 12,
          "ccPaymentEqualToInterestRate": 270
        },
        "vehiclePayment": {
          "vehiclesPri": 0.0178,
          "doTheyHaveAnyVehicle": true,
          "vehiclesMonthlyPayments": 400
        },
        "housingExpenses": {
          "rentVsOwn": "Own",
          "housingRatio": 0.1083,
          "rentalPayment": 0,
          "housingExpenses": 2437.5,
          "mortgagePayment": 2000,
          "otherHousingExpenses": 437.5,
          "housingRatioFirstThreshold": 0.28,
          "housingRatioSecondThreshold": 0.32
        },
        "savingsAndCashflow": {
          "annualCashFlow": 36960.75,
          "annualSavingsRate": 0.2278,
          "annualSavingsAmount": 61500
        },
        "debtToIncomeAndMonthlyObligations": {
          "dti": 0.151,
          "debtOnlyDti": 0.1316,
          "grossIncome": 270000,
          "dtiFirstThreshold": 0.36,
          "dtiThirdThreshold": 0.5,
          "dtiSecondThreshold": 0.43,
          "monthlyGrossIncome": 22500,
          "monthlyDebtPayments": 2960,
          "totalMonthlyObligations": 3397.5,
          "percentageOfDebtOverGrossIncome": 0.3444
        }
      },
      "cashflowStatement": {
        "inflows": {
          "items": [
            {
              "name": "Earned income",
              "items": [
                {
                  "name": "Salary and wages",
                  "joint": 0,
                  "total": 270000,
                  "client": 150000,
                  "coClient": 120000
                }
              ],
              "joint": 0,
              "total": 270000,
              "client": 150000,
              "coClient": 120000
            }
          ],
          "joint": 0,
          "total": 270000,
          "client": 150000,
          "coClient": 120000
        },
        "outflows": {
          "items": [
            {
              "name": "Taxes",
              "items": [
                {
                  "name": "Federal Income Tax",
                  "joint": 36267.98,
                  "total": 36267.98,
                  "client": 0,
                  "coClient": 0
                },
                {
                  "name": "FICA tax",
                  "joint": 180,
                  "total": 20835,
                  "client": 11475,
                  "coClient": 9180
                },
                {
                  "name": "State Income Tax",
                  "joint": 15662.27,
                  "total": 15662.27,
                  "client": 0,
                  "coClient": 0
                }
              ],
              "joint": 52110.25,
              "total": 72765.25,
              "client": 11475,
              "coClient": 9180
            },
            {
              "name": "Expenses",
              "items": [
                {
                  "name": "Living Expenses",
                  "joint": 0,
                  "total": 72000,
                  "client": 72000,
                  "coClient": 0
                },
                {
                  "name": "Insurance payments",
                  "joint": 0,
                  "total": 4,
                  "client": 2,
                  "coClient": 2
                }
              ],
              "joint": 0,
              "total": 72004,
              "client": 72002,
              "coClient": 2
            },
            {
              "name": "Savings",
              "items": [
                {
                  "name": "401k - Traditional savings",
                  "joint": 0,
                  "total": 25000,
                  "client": 14000,
                  "coClient": 11000
                },
                {
                  "name": "Brokerage account savings",
                  "joint": 0,
                  "total": 15000,
                  "client": 0,
                  "coClient": 15000
                },
                {
                  "name": "Cash savings",
                  "joint": 0,
                  "total": 7500,
                  "client": 0,
                  "coClient": 7500
                }
              ],
              "joint": 0,
              "total": 47500,
              "client": 14000,
              "coClient": 33500
            },
            {
              "name": "Housing Expenses",
              "items": [
                {
                  "name": "Mortgage",
                  "joint": 0,
                  "total": 24000,
                  "client": 24000,
                  "coClient": 0
                },
                {
                  "name": "Property Taxes",
                  "joint": 0,
                  "total": 3500,
                  "client": 3500,
                  "coClient": 0
                },
                {
                  "name": "Home Insurance",
                  "joint": 0,
                  "total": 1750,
                  "client": 1750,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "total": 29250,
              "client": 29250,
              "coClient": 0
            },
            {
              "name": "Debt Payments",
              "items": [
                {
                  "name": "Car loan payments",
                  "joint": 0,
                  "total": 4800,
                  "client": 4800,
                  "coClient": 0
                },
                {
                  "name": "Credit card payments",
                  "joint": 0,
                  "total": 3600,
                  "client": 3600,
                  "coClient": 0
                },
                {
                  "name": "Student loan payments",
                  "joint": 0,
                  "total": 3120,
                  "client": 3120,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "total": 11520,
              "client": 11520,
              "coClient": 0
            }
          ],
          "joint": 52110.25,
          "total": 233039.25,
          "client": 138247,
          "coClient": 42682
        },
        "freeCashflow": {
          "joint": -52110.25,
          "total": 36960.75,
          "client": 11753,
          "coClient": 77318
        }
      },
      "netWorthStatement": {
        "assets": {
          "name": "Assets",
          "type": "MAIN",
          "items": [
            {
              "name": "Cash account",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Cash account",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 150000,
                  "client": 0,
                  "coClient": 150000,
                  "annualSavings": 7500,
                  "clientSavings": 7500,
                  "annualMatching": 0,
                  "portfolioTypeName": "Checking account"
                }
              ],
              "joint": 0,
              "order": 1,
              "total": 150000,
              "client": 0,
              "coClient": 150000,
              "totalDebts": 0
            },
            {
              "name": "Investment account",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Taxable",
                  "type": "INDIVIDUAL",
                  "items": [
                    {
                      "name": "Brokerage account",
                      "type": "PORTFOLIO",
                      "joint": 0,
                      "total": 40000,
                      "client": 0,
                      "coClient": 40000,
                      "annualSavings": 15000,
                      "clientSavings": 15000,
                      "annualMatching": 0,
                      "portfolioTypeName": "Brokerage account"
                    }
                  ],
                  "joint": 0,
                  "total": 40000,
                  "client": 0,
                  "coClient": 40000
                },
                {
                  "name": "Tax-free",
                  "type": "INDIVIDUAL",
                  "items": [
                    {
                      "name": "IRA - Roth Timothy",
                      "type": "PORTFOLIO",
                      "joint": 0,
                      "total": 25000,
                      "client": 25000,
                      "coClient": 0,
                      "annualSavings": 0,
                      "clientSavings": 0,
                      "annualMatching": 0,
                      "portfolioTypeName": "401k - Roth"
                    },
                    {
                      "name": "IRA - Roth Melanie",
                      "type": "PORTFOLIO",
                      "joint": 0,
                      "total": 20000,
                      "client": 0,
                      "coClient": 20000,
                      "annualSavings": 0,
                      "clientSavings": 0,
                      "annualMatching": 0,
                      "portfolioTypeName": "401k - Roth"
                    }
                  ],
                  "joint": 0,
                  "total": 45000,
                  "client": 25000,
                  "coClient": 20000
                },
                {
                  "name": "Tax-deferred",
                  "type": "INDIVIDUAL",
                  "items": [
                    {
                      "name": "401(k) - Timothy",
                      "type": "PORTFOLIO",
                      "joint": 0,
                      "total": 70000,
                      "client": 70000,
                      "coClient": 0,
                      "annualSavings": 22000,
                      "clientSavings": 14000,
                      "annualMatching": 8000,
                      "portfolioTypeName": "401k - Traditional"
                    },
                    {
                      "name": "401k - Melanie",
                      "type": "PORTFOLIO",
                      "joint": 0,
                      "total": 55000,
                      "client": 0,
                      "coClient": 55000,
                      "annualSavings": 17000,
                      "clientSavings": 11000,
                      "annualMatching": 6000,
                      "portfolioTypeName": "401k - Traditional"
                    }
                  ],
                  "joint": 0,
                  "total": 125000,
                  "client": 70000,
                  "coClient": 55000
                }
              ],
              "joint": 0,
              "order": 2,
              "total": 210000,
              "client": 95000,
              "coClient": 115000,
              "totalDebts": 0
            },
            {
              "name": "Stock compensation",
              "type": "CATEGORY",
              "joint": 0,
              "order": 3,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Annuity",
              "type": "CATEGORY",
              "joint": 0,
              "order": 4,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Insurance (Cash value)",
              "type": "CATEGORY",
              "joint": 0,
              "order": 5,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Business",
              "type": "CATEGORY",
              "joint": 0,
              "order": 6,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Real estate",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Primary home",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 350000,
                  "client": 350000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 7,
              "total": 350000,
              "client": 350000,
              "coClient": 0,
              "totalDebts": 50000
            },
            {
              "name": "Vehicle",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Tesla",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 30000,
                  "client": 30000,
                  "coClient": 0
                },
                {
                  "name": "Ford",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 28500,
                  "client": 28500,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 8,
              "total": 58500,
              "client": 58500,
              "coClient": 0,
              "totalDebts": 10000
            },
            {
              "name": "Other asset",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Jewelry",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 20000,
                  "client": 20000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 9,
              "total": 20000,
              "client": 20000,
              "coClient": 0,
              "totalDebts": 0
            }
          ],
          "joint": 0,
          "total": 788500,
          "client": 523500,
          "coClient": 265000,
          "totalDebts": 60000
        },
        "netWorth": {
          "joint": 0,
          "total": 695500,
          "client": 430500,
          "coClient": 265000
        },
        "liabilities": {
          "name": "Liabilities",
          "type": "MAIN",
          "items": [
            {
              "name": "Credit card",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Chase CC",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 18000,
                  "client": 18000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 1,
              "total": 18000,
              "client": 18000,
              "coClient": 0
            },
            {
              "name": "Student loan",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Melanie's student loan",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 15000,
                  "client": 15000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 2,
              "total": 15000,
              "client": 15000,
              "coClient": 0
            },
            {
              "name": "Business loan",
              "type": "CATEGORY",
              "joint": 0,
              "order": 3,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true
            },
            {
              "name": "Personal loan",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Tesla loan",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 10000,
                  "client": 10000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 4,
              "total": 10000,
              "client": 10000,
              "coClient": 0
            },
            {
              "name": "Investment loan",
              "type": "CATEGORY",
              "joint": 0,
              "order": 5,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true
            },
            {
              "name": "Real estate debt",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Primary home mortgage",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 50000,
                  "client": 50000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 6,
              "total": 50000,
              "client": 50000,
              "coClient": 0
            },
            {
              "name": "Other debt",
              "type": "CATEGORY",
              "joint": 0,
              "order": 7,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true
            }
          ],
          "joint": 0,
          "total": 93000,
          "client": 93000,
          "coClient": 0
        }
      },
      "savingsAndExpenses": {
        "goals": {
          "clientRetirementAge": 62,
          "coClientRetirementAge": 60,
          "shortTermGoalsCashNeeds": 6000,
          "doTheyHaveEducationFundingGoals": true,
          "totalEducationGoalRequiredAmount": 22500
        },
        "annualSavings": {
          "currentAnnualSavingsAtHSA": 0,
          "currentAnnualSavingsAtHSARate": 0,
          "currentAnnualSavingsAt529Accounts": 0,
          "requiredRetirementExtraAnnualSavings": 0,
          "currentAnnualSavingsAt529AccountsRate": 0,
          "currentAnnualSavingsAtTaxableAccounts": 15000,
          "gapInRetirementAccountsAtRetirementAge": 0,
          "requiredAnnualSavingsAtTaxableAccounts": 15000,
          "requiredExtraAnnualSavingsForEducation": 4609.22,
          "currentAnnualSavingsAtRetirementAccounts": 39000,
          "requiredRetirementExtraAnnualSavingsRate": 0,
          "currentAnnualSavingsAtTaxableAccountsRate": 0.0556,
          "requiredAnnualSavingsAtTaxableAccountsRate": 0.0556,
          "requiredExtraAnnualSavingsForEducationRate": 0.0171,
          "currentAnnualSavingsAtRetirementAccountsRate": 0.1444
        },
        "clientProfile": {
          "clientAge": 40,
          "clientName": "Timothy",
          "coClientAge": 38,
          "coClientName": "Melanie",
          "numberOfChildren": 2,
          "stateOfResidence": "California",
          "clientRiskProfile": "(4) Growth",
          "coClientRiskProfile": "(3) Moderate",
          "maximumAgeOfChildren": 6,
          "minimumAgeOfChildren": 3
        },
        "otherExpenses": {
          "lifeInsuranceGap": 1100000,
          "umbrellaInsuranceGap": 1000000
        },
        "liquidityContext": {
          "shortTermNeeds": 6000,
          "emergencyFundInCash": 150800,
          "emergencyFundInMonths": "+12",
          "maxEmergencyFundTargetInCash": 84577.5,
          "minEmergencyFundTargetInCash": 75180,
          "maxEmergencyFundTargetInMonths": 9,
          "minEmergencyFundTargetInMonths": 8,
          "gapWithRecommendedMinEmergencyFund": "Not applicable",
          "excessWithRecommendedMaxEmergencyFund": 66222.5,
          "maxEmergencyFundTargetAndShortTermNeeds": 90577.5,
          "minEmergencyFundTargetAndShortTermNeeds": 81180,
          "gapWithRecommendedMinEmergencyFundAndShortTermNeeds": "Not applicable",
          "excessWithRecommendedMaxEmergencyFundAndShortTermNeeds": 60222.5
        },
        "advantagedSavings": {
          "hsaMaxContributions": 8750,
          "hsaClientCanContribute": true,
          "hsaClientContributions": 0,
          "client401kCanContribute": "Yes",
          "client401kContributions": 14000,
          "hsaCoClientCanContribute": true,
          "hsaCoClientContributions": 0,
          "coClient401kCanContribute": "Yes",
          "coClient401kContributions": 11000,
          "iraClientMaxContributions": 7500,
          "rothIraClientCanContribute": true,
          "rothIraClientContributions": 0,
          "iraCoClientMaxContributions": 7500,
          "rothIraCoClientCanContribute": true,
          "rothIraCoClientContributions": 0,
          "rothIraClientMaxContributions": 5250.1,
          "rothIraCoClientMaxContributions": 5250.1,
          "traditionalIraClientContributions": 0,
          "traditionalIraCoClientContributions": 0,
          "client401kContributionsMaxEmployerMatch": 9000,
          "coClient401kContributionsMaxEmployerMatch": 7200,
          "traditionalIraClientCanDeductContributions": false,
          "client401kContributionsCurrentEmployerMatch": 8000,
          "traditionalIraCoClientCanDeductContributions": false,
          "coClient401kContributionsCurrentEmployerMatch": 6000,
          "traditionalIraClientMaxDeductibleContributions": 0,
          "traditionalIraCoClientMaxDeductibleContributions": 0
        },
        "incomeAndCashflow": {
          "incomeSummary": [
            [
              "Category",
              "Value",
              "Percentage"
            ],
            [
              "Earned income - Client",
              150000,
              0.5556
            ],
            [
              "Earned income - Co-Client",
              120000,
              0.4444
            ],
            [
              "Total",
              270000,
              1
            ]
          ],
          "annualCashflow": 36960.75,
          "outflowSummary": [
            [
              "Category",
              "Value",
              "Percentage"
            ],
            [
              "Taxes",
              72765.25,
              0.2695
            ],
            [
              "Debt Payments",
              11520,
              0.0427
            ],
            [
              "Housing Expenses",
              29250,
              0.1083
            ],
            [
              "Savings",
              61500,
              0.2278
            ],
            [
              "Expenses",
              72004,
              0.2667
            ],
            [
              "Total",
              247039.25,
              0.915
            ]
          ],
          "annualCashflowPercentage": 0.1369,
          "householdIncomePercentile": 0.9
        },
        "housingInformation": {
          "rentVsOwn": "Own",
          "rentalPayment": 0,
          "housingExpenses": 2437.5,
          "mortgagePayment": 2000,
          "otherHousingExpenses": 437.5
        },
        "debtRatiosAndHealth": {
          "dti": 0.151,
          "housingRatio": 0.1083,
          "housingExpenses": 2437.5,
          "dtiFirstThreshold": 0.36,
          "dtiThirdThreshold": 0.5,
          "dtiSecondThreshold": 0.43,
          "totalMonthlyObligations": 3397.5,
          "housingRatioFirstThreshold": 0.28,
          "housingRatioSecondThreshold": 0.32,
          "percentageOfDebtOverGrossIncome": 0.3444
        },
        "shortTermGoalsNeeded": [
          {
            "date": "2027-01-01T00:00:00.000Z",
            "amount": 6000,
            "description": "Go on vacation",
            "paymentFrequency": "ANNUAL"
          }
        ]
      },
      "assetsAndInvestments": {
        "withdrawals": {
          "rmdStartAge": 75,
          "rmdStartYear": 2061,
          "coClientRmdStartAge": 75,
          "coClientRmdStartYear": 2063,
          "averageWithdrawalsDuringRmds": 0,
          "yearsPayingMoreRmdsThanRequiredWithoutSavings": 0,
          "yearsPayingMoreRmdsThanRequiredWithCurrentSavings": 7
        },
        "listOfAssets": [
          [
            "Asset type",
            "Number of assets",
            "Asset value",
            "% of total assets",
            "Equity value",
            "% of Net worth"
          ],
          [
            "Cash account",
            1,
            150000,
            0.1902,
            150000,
            0.2059
          ],
          [
            "Investment account",
            5,
            210000,
            0.2663,
            210000,
            0.2883
          ],
          [
            "Real estate",
            1,
            350000,
            0.4439,
            300000,
            0.4118
          ],
          [
            "Vehicle",
            2,
            58500,
            0.0742,
            48500,
            0.0666
          ],
          [
            "Other asset",
            1,
            20000,
            0.0254,
            20000,
            0.0275
          ]
        ],
        "clientProfile": {
          "clientAge": 40,
          "clientName": "Timothy",
          "coClientAge": 38,
          "coClientName": "Melanie",
          "clientRiskProfile": "(4) Growth",
          "clientRetirementAge": 62,
          "coClientRiskProfile": "(3) Moderate",
          "coClientRetirementAge": 60
        },
        "contributions": {
          "IRAContributions": [
            [
              "IRA contributions (Traditional + Roth)",
              "Client",
              "Co-Client"
            ],
            [
              "Max IRA contribution (Traditional + Roth)",
              7500,
              7500
            ],
            [
              "IRA catch-up (age 50+)",
              "Not applicable",
              "Not applicable"
            ],
            [
              "Total possible IRA contribution",
              7500,
              7500
            ],
            [
              "Roth IRA eligible amount (estimate)",
              5250.1,
              5250.1
            ]
          ],
          "hsaContributions": {
            "catchUpForClient": "Not applicable",
            "maxContributions": 8750,
            "catchUpForCoClient": "Not applicable",
            "totalPossibleContribution": 8750
          },
          "employerPlanContributions": [
            [
              "Employer plan contributions (401k, 403b, etc)",
              "Client",
              "Co-Client"
            ],
            [
              "Max employee contribution",
              24500,
              24500
            ],
            [
              "Catch up (age 50+)",
              "Not applicable",
              "Not applicable"
            ],
            [
              "Super catch up (age 60-63)",
              "Not applicable",
              "Not applicable"
            ],
            [
              "Total possible employee contribution",
              24500,
              24500
            ]
          ]
        },
        "educationGoal": {
          "hasAnEducationGoal": true
        },
        "listOfAccounts": [
          [
            "Account",
            "Client",
            "Number",
            "Balance",
            "Annual contribution"
          ],
          [
            "401k - Roth",
            "Melanie",
            1,
            20000,
            0
          ],
          [
            "401k - Roth",
            "Timothy",
            1,
            25000,
            0
          ],
          [
            "401k - Traditional",
            "Melanie",
            1,
            55000,
            17000
          ],
          [
            "401k - Traditional",
            "Timothy",
            1,
            70000,
            22000
          ],
          [
            "Brokerage account",
            "Melanie",
            1,
            40000,
            15000
          ],
          [
            "Cash/savings",
            "Melanie",
            1,
            150000,
            7500
          ]
        ],
        "matchGapAnalysis": [
          {
            "holder": "client",
            "accountName": "401(k) - Timothy",
            "accountType": "401K",
            "grossSalary": 150000,
            "matchStructure": "FIXED_AMOUNT",
            "alertSuppressed": false,
            "matchPolicySource": "configured",
            "currentAnnualMatch": 8000,
            "fullMatchThreshold": 0,
            "activeContributions": true,
            "matchPolicyConfigured": true,
            "uncapturedAnnualMatch": 0,
            "maxPossibleAnnualMatch": 8000,
            "matchMaximizationStatus": "MAXIMIZED",
            "lifetimeUncapturedMatchEstimate": 0,
            "additionalContributionToMaximize": 0
          },
          {
            "holder": "coClient",
            "accountName": "401k - Melanie",
            "accountType": "401K",
            "grossSalary": 120000,
            "matchStructure": "FIXED_AMOUNT",
            "alertSuppressed": false,
            "matchPolicySource": "configured",
            "currentAnnualMatch": 6000,
            "fullMatchThreshold": 0,
            "activeContributions": true,
            "matchPolicyConfigured": true,
            "uncapturedAnnualMatch": 0,
            "maxPossibleAnnualMatch": 6000,
            "matchMaximizationStatus": "MAXIMIZED",
            "lifetimeUncapturedMatchEstimate": 0,
            "additionalContributionToMaximize": 0
          }
        ],
        "incomeAndTaxation": {
          "taxRates": [
            [
              "Tax rate",
              "Current",
              "Expected at retirement"
            ],
            [
              "Federal ordinary tax rate",
              0.24,
              0.2352
            ],
            [
              "State tax rate",
              0.093,
              0.093
            ],
            [
              "NIIT tax rate",
              0,
              0
            ],
            [
              "Effective ordinary tax rate",
              0.333,
              0.3282
            ]
          ],
          "taxableIncome": {
            "totalTaxableIncome": 212799.92
          },
          "totalGrossIncome": 270000,
          "clientGrossIncome": 150000,
          "coClientGrossIncome": 120000
        },
        "educationGoalNeeds": {
          "current529Balance": 0,
          "educationGoalAmount": 22500,
          "target529Contributions": 4609.22,
          "current529Contributions": 0
        },
        "retirementGlidePath": {
          "retirementGlidePathForClient": "98% equity and 2% fixed income",
          "retirementGlideEquityForClient": 0.9798,
          "retirementGlidePathForCoClient": "98% equity and 2% fixed income",
          "retirementGlideEquityForCoClient": 0.9798,
          "retirementGlideFixedIncomeForClient": 0.0202,
          "retirementGlideFixedIncomeForCoClient": 0.0202
        },
        "totalAssetsAndEquity": {
          "totalAssets": 788500,
          "totalEquity": 728500
        },
        "realEstateAndMortgage": {
          "mortgageBalance": 50000,
          "realEstateEquity": 0.8571,
          "realEstateEquityThreshold1": 0.2,
          "realEstateEquityThreshold2": 0.5
        },
        "listOfRealEstateAssets": [
          [
            "Real estate",
            "Value",
            "Debt amount",
            "Debt %",
            "Equity amount",
            "Equity %"
          ],
          [
            "Primary home",
            350000,
            50000,
            0.1429,
            300000,
            0.8571
          ]
        ],
        "percentageOfCashThreshold": 0.5,
        "listOfChildrenAndEducationGoals": [
          [
            "Student",
            "Age",
            "Education goal timeframe",
            "Years to uni",
            "Education goal ($)",
            "Target equity allocation in 529 account",
            "Target fixed income in 529 account"
          ],
          [
            "Liam",
            6,
            "2038 - 2042",
            11,
            11250,
            0.7999,
            0.2001
          ],
          [
            "Josh",
            3,
            "2041 - 2045",
            14,
            11250,
            0.9798,
            0.0202
          ]
        ]
      },
      "retirementAndOtherGoals": {
        "otherIncome": [
          [
            "Income source",
            "Total value",
            "Yearly average value"
          ],
          [
            "Earned income",
            12240.69,
            394.86
          ],
          [
            "Total other income",
            12240.69,
            394.86
          ]
        ],
        "withdrawals": {
          "withdrawalRatio": 0.0102,
          "supplementalTotalWithdrawals": 641317.73,
          "supplementalAnnualWithdrawals": 20687.67
        },
        "clientProfile": {
          "clientAge": 40,
          "clientName": "Timothy",
          "coClientAge": 38,
          "coClientName": "Melanie",
          "endOfPlanAge": 91,
          "clientRiskProfile": "(4) Growth",
          "clientRetirementAge": 62,
          "coClientRiskProfile": "(3) Moderate",
          "coClientRetirementAge": 60
        },
        "assetDepletion": {
          "netWorthAtEndOfPlan": 3359399.98,
          "requiredRetirementAge": "Not applicable",
          "liquidAssetsAtEndOfPlan": 2371900.89,
          "shortfallInNumberOfYears": "Not applicable",
          "ageWhenTheyRunOutOfNetWorth": "Not applicable",
          "ageWhenTheyRunOutOfLiquidAssets": "Not applicable"
        },
        "guaranteedIncome": [
          [
            "Income source",
            "Total value",
            "Yearly average value"
          ],
          [
            "Social security",
            1833702.02,
            59151.68
          ],
          [
            "Annuity income",
            3469028.55,
            111904.15
          ],
          [
            "Pension / defined benefit",
            0,
            0
          ],
          [
            "Total guaranteed income",
            5302730.58,
            171055.83
          ]
        ],
        "incomeVsIncomeNeeds": {
          "allIncomesVsIncomeNeeded": 0.7948,
          "otherIncomeVsIncomeNeeded": 0.0018,
          "guaranteedIncomeVsIncomeNeeded": 0.7929,
          "allIncomesVsIncomeNeededExLtcCosts": 0.9303,
          "otherIncomeVsIncomeNeededExLtcCosts": 0.0021,
          "guaranteedIncomeVsIncomeNeededExLtcCosts": 0.9281
        },
        "otherGoalsAndLegacy": {
          "legacyGoal": false,
          "legacyGoalGap": "Not applicable",
          "legacyGoalAmount": "Not applicable",
          "achievesLegacyGoals": "Not applicable",
          "otherGoalsAfterRetirement": true,
          "otherGoalsAfterRetirementAmount": 673481.06
        },
        "netWorthAtRetirement": {
          "netWorthAtRetirementAge": 2820966.62,
          "liquidAssetsAtRetirementAge": 2010341.81,
          "nonLiquidAssetsAtRetirementAge": 810624.8
        },
        "incomeNeedsAndWithdrawals": {
          "totalLtcCosts": 974057.64,
          "annualLtcCosts": 243514.41,
          "totalIncomeNeeded": 6687466.39,
          "ltcCostsAreEstimated": true,
          "annualTotalIncomeNeeded": 215724.72,
          "totalIncomeNeededExLtcCosts": 5713408.75,
          "annualTotalIncomeNeededExLtcCosts": 184303.51
        }
      },
      "taxDragAnalysis": {
        "householdRollup": [
          [
            "Metric",
            "Value",
            "Notes"
          ],
          [
            "Total annual tax cost (Table 2)",
            498.23,
            "All taxable-account rows, including money-market positions."
          ],
          [
            "Money-market drag routed to Cash sub-task",
            0,
            "Money-market positions stay visible here but are carved out of the in-scope Tax Drag total."
          ],
          [
            "In-scope tax cost (Table 2 ex-MM)",
            498.23,
            "Standalone Tax Drag total after routing money-market drag to Cash."
          ],
          [
            "Total annual tax cost saved (Table 3)",
            667.35,
            "Permanent annual tax saved if those holdings were taxable today."
          ],
          [
            "Total annual tax cost deferred (Table 4)",
            946.28,
            "Deferred, not eliminated; future withdrawals remain taxable on exit."
          ],
          [
            "NIIT contribution to Table 2",
            0,
            "Taxable net-investment components multiplied by the current NIIT rate."
          ]
        ],
        "accountTypeInputs": [
          [
            "#",
            "Account name",
            "Account type",
            "Tax treatment"
          ],
          [
            "1",
            "Cash account",
            "Checking account",
            "Taxable"
          ],
          [
            "2",
            "401k - Melanie",
            "401k - Traditional",
            "Tax deferred"
          ],
          [
            "3",
            "Brokerage account",
            "Brokerage account",
            "Taxable"
          ],
          [
            "4",
            "IRA - Roth Melanie",
            "401k - Roth",
            "Tax free"
          ],
          [
            "5",
            "401(k) - Timothy",
            "401k - Traditional",
            "Tax deferred"
          ],
          [
            "6",
            "IRA - Roth Timothy",
            "401k - Roth",
            "Tax free"
          ]
        ],
        "effectiveTaxMargin": [
          [
            "Component",
            "Rate",
            "Source / Trigger",
            "Applies to"
          ],
          [
            "Federal ordinary",
            "24%",
            "FH metrics — currentTaxBracket",
            "Ordinary income, ST cap gains, ST cap gain distributions, ordinary interest, non-qualified dividends"
          ],
          [
            "Federal LTCG",
            "15%",
            "PW-computed federal LTCG (2026 thresholds; taxable-income proxy)",
            "Qualified dividends, LT cap gains, LT cap gain distributions"
          ],
          [
            "State (CA)",
            "9.3%",
            "FH metrics — stateTaxRate (CA)",
            "All investment income (state rules)"
          ],
          [
            "NIIT",
            "0%",
            "FH metrics — niitRate",
            "All net investment income"
          ],
          [
            "Total taxable income",
            "$212,800",
            "FH metrics — taxableIncome.totalTaxableIncome",
            "Debug input for LTCG and NIIT lookups"
          ],
          [
            "MAGI proxy",
            "$212,800",
            "Current tax-margin logic — reuse taxableIncome.totalTaxableIncome as MAGI proxy",
            "Debug input for NIIT and current LTCG threshold lookup"
          ],
          [
            "State input",
            "CA — California",
            "PW params — state.code / state.name",
            "Debug input for state marginal-rate lookup"
          ],
          [
            "Expected retirement ordinary",
            "23.52%",
            "FH metrics — expectedTaxBracketInRetirement",
            "Future withdrawals from tax-deferred accounts"
          ],
          [
            "Effective ordinary rate",
            "33.3%",
            "24% + 9.3% + 0%",
            "Today's ordinary-rate income"
          ],
          [
            "Effective LTCG rate",
            "24.3%",
            "15% + 9.3% + 0%",
            "Today's LTCG-rate income"
          ]
        ],
        "fundHoldingsInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Morningstar category",
            "Balance",
            "Shares",
            "Estimated shares",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Interest income ($/share)",
            "Tax-free income ($/share)",
            "LT cap gain ($/share)",
            "ST cap gain ($/share)",
            "Ordinary-rate share (non-qual div + interest + ST cap gain) / total distribution",
            "Tax cost ratio",
            "Turnover",
            "PCGE"
          ],
          [
            "1",
            "401k - Melanie",
            "Cash (USD)",
            "Money Market-Taxable",
            1100,
            1100,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "2",
            "IRA - Roth Timothy",
            "FCNTX",
            "Large Growth",
            11760,
            449.71,
            "-",
            "$0",
            "$0",
            "$0",
            "$0",
            "$1.265",
            "$0",
            "0%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "3",
            "IRA - Roth Timothy",
            "UPRO",
            "Trading--Leveraged Equity",
            12740,
            98.81,
            "-",
            "$0",
            "$0.973",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "4",
            "401(k) - Timothy",
            "Cash (USD)",
            "Money Market-Taxable",
            1400,
            1400,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "5",
            "401k - Melanie",
            "LQD",
            "Corporate Bond",
            14700,
            140.8,
            "-",
            "$0",
            "$4.938",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "6",
            "Brokerage account",
            "VWO",
            "Diversified Emerging Markets",
            14700,
            265.53,
            "-",
            "$0.168",
            "$1.329",
            "$0",
            "$0",
            "$0",
            "$0",
            "88.77%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "7",
            "Brokerage account",
            "SCHD",
            "Large Value",
            14700,
            417.85,
            "-",
            "$0",
            "$1.048",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "8",
            "Cash account",
            "Cash (USD)",
            "Money Market-Taxable",
            150000,
            150000,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "9",
            "401k - Melanie",
            "VEA",
            "Foreign Large Blend",
            39200,
            578.43,
            "-",
            "$0",
            "$2.009",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "10",
            "IRA - Roth Melanie",
            "Cash (USD)",
            "Money Market-Taxable",
            400,
            400,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "11",
            "IRA - Roth Timothy",
            "Cash (USD)",
            "Money Market-Taxable",
            500,
            500,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "12",
            "401(k) - Timothy",
            "VTI",
            "Large Blend",
            58800,
            162.49,
            "-",
            "$0.86",
            "$2.897",
            "$0",
            "$0",
            "$0",
            "$0",
            "77.11%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "13",
            "Brokerage account",
            "Cash (USD)",
            "Money Market-Taxable",
            800,
            800,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "14",
            "IRA - Roth Melanie",
            "FIGSX",
            "Foreign Large Growth",
            9800,
            507.77,
            "-",
            "$0.28",
            "$0.049",
            "$0",
            "$0",
            "$1.328",
            "$0",
            "2.98%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "15",
            "Brokerage account",
            "JNK",
            "High Yield Bond",
            9800,
            105.83,
            "-",
            "$0",
            "$6.358",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "16",
            "401(k) - Timothy",
            "SCHP",
            "Inflation-Protected Bond",
            9800,
            382.96,
            "-",
            "$0",
            "$1.075",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "17",
            "IRA - Roth Melanie",
            "VWELX",
            "Moderate Allocation",
            9800,
            212.63,
            "-",
            "$0.386",
            "$0.623",
            "$0",
            "$0",
            "$3.4",
            "$0.715",
            "26.12%",
            "[pending]",
            "[pending]",
            "[pending]"
          ]
        ],
        "stockHoldingsInputs": [
          [
            "#",
            "Account",
            "Name",
            "Ticker",
            "Sector",
            "Industry",
            "Country",
            "Balance",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Dividend yield TTM"
          ]
        ],
        "taxFreeAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable)",
            "Annual tax cost saved"
          ],
          [
            "1",
            "IRA - Roth Timothy",
            "FCNTX",
            11760,
            "LT cap gain distribution",
            568.89,
            "24.3%",
            138.24
          ],
          [
            "2",
            "IRA - Roth Timothy",
            "UPRO",
            12740,
            "Non-qualified dividend",
            96.18,
            "33.3%",
            32.03
          ],
          [
            "3",
            "IRA - Roth Melanie",
            "Cash (USD)",
            400,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "4",
            "IRA - Roth Timothy",
            "Cash (USD)",
            500,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "5a",
            "IRA - Roth Melanie",
            "FIGSX",
            9800,
            "Qualified dividend",
            141.98,
            "24.3%",
            34.5
          ],
          [
            "5b",
            "IRA - Roth Melanie",
            "FIGSX",
            9800,
            "Non-qualified dividend",
            25.07,
            "33.3%",
            8.3492
          ],
          [
            "5c",
            "IRA - Roth Melanie",
            "FIGSX",
            9800,
            "LT cap gain distribution",
            674.32,
            "24.3%",
            163.86
          ],
          [
            "5d",
            "IRA - Roth Melanie",
            "FIGSX",
            9800,
            "Subtotal",
            841.38,
            "-",
            206.71
          ],
          [
            "6a",
            "IRA - Roth Melanie",
            "VWELX",
            9800,
            "Qualified dividend",
            82.13,
            "24.3%",
            19.96
          ],
          [
            "6b",
            "IRA - Roth Melanie",
            "VWELX",
            9800,
            "Non-qualified dividend",
            132.44,
            "33.3%",
            44.1
          ],
          [
            "6c",
            "IRA - Roth Melanie",
            "VWELX",
            9800,
            "LT cap gain distribution",
            722.86,
            "24.3%",
            175.66
          ],
          [
            "6d",
            "IRA - Roth Melanie",
            "VWELX",
            9800,
            "ST cap gain distribution",
            152.12,
            "33.3%",
            50.65
          ],
          [
            "6e",
            "IRA - Roth Melanie",
            "VWELX",
            9800,
            "Subtotal",
            1089.54,
            "-",
            290.37
          ],
          [
            "Total",
            "Total tax-free",
            "-",
            45000,
            "-",
            2595.99,
            "-",
            667.35
          ]
        ],
        "taxableAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate",
            "Annual tax cost"
          ],
          [
            "1a",
            "Brokerage account",
            "VWO",
            14700,
            "Qualified dividend",
            44.66,
            "24.3%",
            10.85
          ],
          [
            "1b",
            "Brokerage account",
            "VWO",
            14700,
            "Non-qualified dividend",
            352.93,
            "33.3%",
            117.52
          ],
          [
            "1c",
            "Brokerage account",
            "VWO",
            14700,
            "Subtotal",
            397.59,
            "-",
            128.38
          ],
          [
            "2",
            "Brokerage account",
            "SCHD",
            14700,
            "Non-qualified dividend",
            437.74,
            "33.3%",
            145.77
          ],
          [
            "3",
            "Cash account",
            "Cash (USD)",
            150000,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "4",
            "Brokerage account",
            "Cash (USD)",
            800,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "5",
            "Brokerage account",
            "JNK",
            9800,
            "Non-qualified dividend",
            672.94,
            "33.3%",
            224.09
          ],
          [
            "Total",
            "Total taxable",
            "-",
            190000,
            "-",
            1508.27,
            "-",
            498.23
          ]
        ],
        "costBasisBlockingNotes": [
          [
            "Account",
            "Blocking note"
          ],
          [
            "Brokerage account",
            "Implementation of Brokerage account cannot be responsibly sequenced without tax-lot data."
          ]
        ],
        "taxableCostBasisInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Balance (market value)",
            "Cost basis",
            "Unrealized gain",
            "Holding period",
            "Notes"
          ],
          [
            "1",
            "Brokerage account",
            "VWO",
            14700,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "2",
            "Brokerage account",
            "SCHD",
            14700,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "3",
            "Cash account",
            "Cash (USD)",
            150000,
            150000,
            0,
            "N/A",
            "Money market — NAV $1.00, no embedded gain by design."
          ],
          [
            "4",
            "Brokerage account",
            "Cash (USD)",
            800,
            800,
            0,
            "N/A",
            "Money market — NAV $1.00, no embedded gain by design."
          ],
          [
            "5",
            "Brokerage account",
            "JNK",
            9800,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "Total",
            "Total taxable",
            "-",
            190000,
            "[missing cost basis]",
            "[missing cost basis]",
            "-",
            "Totals stay blocked until missing tax-lot inputs are filled."
          ]
        ],
        "taxDeferredAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable today)",
            "Annual tax cost deferred"
          ],
          [
            "1",
            "401k - Melanie",
            "Cash (USD)",
            1100,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "2",
            "401(k) - Timothy",
            "Cash (USD)",
            1400,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "3",
            "401k - Melanie",
            "LQD",
            14700,
            "Non-qualified dividend",
            695.21,
            "33.3%",
            231.51
          ],
          [
            "4",
            "401k - Melanie",
            "VEA",
            39200,
            "Non-qualified dividend",
            1162.29,
            "33.3%",
            387.04
          ],
          [
            "5a",
            "401(k) - Timothy",
            "VTI",
            58800,
            "Qualified dividend",
            139.71,
            "24.3%",
            33.95
          ],
          [
            "5b",
            "401(k) - Timothy",
            "VTI",
            58800,
            "Non-qualified dividend",
            470.7,
            "33.3%",
            156.74
          ],
          [
            "5c",
            "401(k) - Timothy",
            "VTI",
            58800,
            "Subtotal",
            610.41,
            "-",
            190.69
          ],
          [
            "6",
            "401(k) - Timothy",
            "SCHP",
            9800,
            "Non-qualified dividend",
            411.53,
            "33.3%",
            137.04
          ],
          [
            "Total",
            "Total tax-deferred",
            "-",
            125000,
            "-",
            2879.44,
            "-",
            946.28
          ]
        ],
        "componentTaxTreatmentMatrix": [
          [
            "Component",
            "Federal rate type",
            "Effective household rate today",
            "Taxable accounts",
            "Tax-free accounts",
            "Tax-deferred accounts",
            "Notes"
          ],
          [
            "Qualified dividend",
            "LTCG",
            "24.3%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for US common stock and treaty-country foreign names; funds keep the precomputed Morningstar qualified split."
          ],
          [
            "Non-qualified dividend",
            "ORDINARY",
            "33.3%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for REIT and non-treaty foreign names, while MLP distributions are treated as ROC; funds keep the precomputed Morningstar non-qualified split."
          ],
          [
            "Interest income",
            "ORDINARY",
            "33.3%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Money-market and bond-style fund income is treated as ordinary-rate income."
          ],
          [
            "Tax-free income",
            "Tax-exempt federal",
            "0%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Current phase assumes a 0% effective rate because state-specific muni exposure is not available in the data path."
          ],
          [
            "LT cap gain distribution",
            "LTCG",
            "24.3%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed long-term capital gains use the LTCG household rate."
          ],
          [
            "ST cap gain distribution",
            "ORDINARY",
            "33.3%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed short-term capital gains use the ordinary household rate."
          ]
        ]
      },
      "realEstate": {
        "realEstateEquity": 300000,
        "realEstateEquityThreshold1": 0.2,
        "realEstateEquityThreshold2": 0.5,
        "percentageOfRealEstateEquity": 0.8571
      },
      "savingsRate": null,
      "educationGoalNeeds": {
        "current529Balance": 0,
        "educationGoalAmount": 22500,
        "target529Contributions": 4609.22,
        "current529Contributions": 0
      }
    },
    "savingsWaterfall": [
      {
        "step": 1,
        "bucket": "Build minimum emergency threshold (3 months)",
        "current": 150800,
        "target": 28193,
        "status": "Filled",
        "delta": 122608,
        "flag": "",
        "notes": ""
      },
      {
        "step": 2,
        "bucket": "Address essential insurance gaps",
        "current": 250000,
        "target": 2350000,
        "status": "Partially filled",
        "delta": -2100000,
        "flag": "",
        "notes": ""
      },
      {
        "step": 3,
        "bucket": "Set aside cash for near-term goals",
        "current": 122608,
        "target": 6000,
        "status": "Filled",
        "delta": 116608,
        "flag": "",
        "notes": ""
      },
      {
        "step": 4,
        "bucket": "Maximize employer match — primary plan",
        "current": "N/A",
        "target": "",
        "status": ""
      },
      {
        "step": 5,
        "bucket": "Maximize employer match — secondary plan",
        "current": "N/A",
        "target": "",
        "status": ""
      },
      {
        "step": 6,
        "bucket": "Maximize HSA match",
        "current": "N/A",
        "target": "",
        "status": ""
      },
      {
        "step": 7,
        "bucket": "Maximize ESPP (Employee Stock Purchase Plan)",
        "current": "N/A",
        "target": "",
        "status": ""
      },
      {
        "step": 8,
        "bucket": "Pay high-interest debt (>7%)",
        "current": 18000,
        "target": 0,
        "status": "Empty",
        "delta": 18000,
        "flag": "",
        "notes": ""
      },
      {
        "step": 9,
        "bucket": "Build toward maximum emergency threshold (6 months)",
        "current": 144800,
        "target": 56385,
        "status": "Filled",
        "delta": 88415,
        "flag": "",
        "notes": ""
      },
      {
        "step": 10,
        "bucket": "Contribute to Roth IRA",
        "current": 0,
        "target": 10500,
        "status": "Empty",
        "delta": -10500,
        "flag": "",
        "notes": ""
      },
      {
        "step": 11,
        "bucket": "Maximize HSA",
        "current": 0,
        "target": 8750,
        "status": "Empty",
        "delta": -8750,
        "flag": "",
        "notes": ""
      },
      {
        "step": 12,
        "bucket": "Contribute to 529 accounts",
        "current": 0,
        "target": 4609,
        "status": "Empty",
        "delta": -4609,
        "flag": "",
        "notes": ""
      },
      {
        "step": 13,
        "bucket": "Maximize 401k / employer plans",
        "current": 25000,
        "target": 49000,
        "status": "Partially filled",
        "delta": -24000,
        "flag": "",
        "notes": ""
      },
      {
        "step": 14,
        "bucket": "Invest in taxable brokerage",
        "current": 15000,
        "target": "N/A",
        "status": "",
        "delta": ""
      },
      {
        "step": 15,
        "bucket": "Pay low-interest debt (personal, auto)",
        "current": 10000,
        "target": 0,
        "status": "Partially filled",
        "delta": 10000,
        "flag": "",
        "notes": ""
      },
      {
        "step": 16,
        "bucket": "Make extra mortgage payments",
        "current": 50000,
        "target": "N/A",
        "status": "",
        "delta": ""
      }
    ],
    "shocks": [
      {
        "assetClassesAffected": [
          "US Treasuries",
          "US equities",
          "USD",
          "rate-sensitive sectors"
        ],
        "dateLabel": "2023-07-26",
        "description": "The Fed raised rates 25bp to 5.25–5.50%, the 11th and final hike in the cycle — the highest level in 22 years. The Fed held here for 14 months before cutting in September 2024.",
        "duration": "Extended",
        "endDate": "2024-09-17",
        "impactDirection": "Rates-driven",
        "name": "Fed final hike to 5.25–5.50%",
        "portfolioImpact": "Mixed",
        "severity": "High",
        "startDate": "2023-07-23",
        "type": "Fed/Macro",
        "drawdown": {
          "severity": "major",
          "eventDate": "2023-07-26",
          "household": {
            "drawdownPct": -0.042,
            "recoveryDays": 15,
            "returnDuringPct": 0.1689
          },
          "windowEnd": "2024-09-17",
          "eventTitle": "Fed final hike to 5.25–5.50%",
          "windowStart": "2023-07-23",
          "divergencePp": -0.0062,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0358,
            "recoveryDays": 15,
            "returnDuringPct": 0.184
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "US Treasuries",
          "small caps",
          "USD",
          "rate-sensitive sectors"
        ],
        "dateLabel": "2023-12-13",
        "description": "Fed held rates steady but the dot plot signaled 75bp of cuts in 2024, marking a decisive pivot. S&P 500 surged to new highs; Russell 2000 +4%. Long-end yields fell sharply. Catalyzed a broad year-end rally across equities and bonds.",
        "duration": "Extended",
        "endDate": "2024-03-31",
        "impactDirection": "Risk-on equity",
        "name": "Fed pivot — December 2023 dot plot",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2023-12-10",
        "type": "Fed/Macro",
        "drawdown": {
          "severity": "major",
          "eventDate": "2023-12-13",
          "household": {
            "drawdownPct": -0.0117,
            "recoveryDays": 6,
            "returnDuringPct": 0.069
          },
          "windowEnd": "2024-03-31",
          "eventTitle": "Fed pivot — December 2023 dot plot",
          "windowStart": "2023-12-10",
          "divergencePp": -0.0004,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0113,
            "recoveryDays": 14,
            "returnDuringPct": 0.0713
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "Japanese equities",
          "EM",
          "global equities",
          "USD/JPY"
        ],
        "dateLabel": "2024-08-05",
        "description": "Yen carry trade unwind and US recession fears triggered a global rout. Japan's TOPIX fell 12.3% — worst since 1987 Black Monday. VIX spiked above 65 intraday. S&P 500 fell ~3% at the open but recovered most losses by Friday. The episode lasted one week.",
        "duration": "Immediate (days)",
        "endDate": "2024-08-09",
        "impactDirection": "Risk-off equity",
        "name": "Global selloff — VIX spikes above 60",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2024-07-31",
        "type": "Market",
        "drawdown": {
          "severity": "major",
          "eventDate": "2024-08-05",
          "household": {
            "drawdownPct": -0.0338,
            "returnDuringPct": -0.0171
          },
          "windowEnd": "2024-08-09",
          "eventTitle": "Global selloff — VIX spikes above 60",
          "windowStart": "2024-07-31",
          "divergencePp": -0.0059,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0279,
            "returnDuringPct": -0.0142
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "US Treasuries",
          "USD",
          "EM",
          "rate-sensitive sectors"
        ],
        "dateLabel": "2024-09-18",
        "description": "First Fed rate cut in four years, and an outsized 50bp move, formally marking the start of the easing cycle. Signaled the Fed's confidence that inflation was heading sustainably toward 2% and opened the door to subsequent cuts.",
        "duration": "Extended",
        "endDate": "2024-12-18",
        "impactDirection": "Risk-on equity",
        "name": "Fed first rate cut — 50bp",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2024-09-15",
        "type": "Fed/Macro",
        "drawdown": {
          "severity": "major",
          "eventDate": "2024-09-18",
          "household": {
            "drawdownPct": -0.0235,
            "returnDuringPct": 0.004
          },
          "windowEnd": "2024-12-18",
          "eventTitle": "Fed first rate cut — 50bp",
          "windowStart": "2024-09-15",
          "divergencePp": -0.0037,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0198,
            "returnDuringPct": 0.0235
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "small caps",
          "financials",
          "USD",
          "crypto"
        ],
        "dateLabel": "2024-11-05",
        "description": "Trump defeated Kamala Harris decisively. S&P 500 surged 2.5%, Dow +3.6%, Russell 2000 +5.8%. The \"Trump trade\" lifted banks, small caps, and crypto on expectations of deregulation and tax cuts. USD strengthened sharply.",
        "duration": "Short",
        "endDate": "2024-11-19",
        "impactDirection": "Risk-on equity",
        "name": "Trump election win",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2024-11-05",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2024-11-05",
          "household": {
            "drawdownPct": -0.0146,
            "returnDuringPct": 0.0029
          },
          "windowEnd": "2024-11-19",
          "eventTitle": "Trump election win",
          "windowStart": "2024-11-05",
          "divergencePp": -0.0033,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0114,
            "returnDuringPct": 0.0124
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities (tech/semis)",
          "Nvidia",
          "AI-linked names"
        ],
        "dateLabel": "2025-01-27",
        "description": "Chinese startup DeepSeek released an open-source AI model rivaling GPT-4 at a fraction of the cost, questioning the US AI capex thesis. Nvidia lost $589B in market value — the largest single-day loss for any stock in history. Nasdaq fell 3.1%, S&P 500 fell 1.5%.",
        "duration": "Immediate (days)",
        "endDate": "2025-01-30",
        "impactDirection": "Sector-specific",
        "name": "DeepSeek AI shock",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2025-01-27",
        "type": "Tech/AI",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-01-27",
          "household": {
            "drawdownPct": -0.0016,
            "recoveryDays": 0,
            "returnDuringPct": 0.0053
          },
          "windowEnd": "2025-01-30",
          "eventTitle": "DeepSeek AI shock",
          "windowStart": "2025-01-27",
          "divergencePp": 0.0004,
          "sameRiskBenchmark": {
            "drawdownPct": -0.002,
            "recoveryDays": 0,
            "returnDuringPct": 0.005
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "EM",
          "USD",
          "US Treasuries"
        ],
        "dateLabel": "2025-04-02",
        "description": "Trump announced sweeping reciprocal tariffs (10% baseline, 34% on China, 20% on EU, 46% on Vietnam) — the highest US tariff level since 1909. S&P 500 lost 10% in two days — the worst two-day loss in history ($6.6T erased). Long-end yields spiked on bond vigilante concerns.",
        "duration": "Short",
        "endDate": "2025-04-09",
        "impactDirection": "Risk-off equity",
        "name": "Liberation Day tariffs announced",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2025-04-02",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-04-02",
          "household": {
            "drawdownPct": -0.0711,
            "returnDuringPct": -0.0253
          },
          "windowEnd": "2025-04-09",
          "eventTitle": "Liberation Day tariffs announced",
          "windowStart": "2025-04-02",
          "divergencePp": -0.0095,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0615,
            "returnDuringPct": -0.0174
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "US Treasuries",
          "USD"
        ],
        "dateLabel": "2025-04-09",
        "description": "After the S&P 500 fell 10% in two days post-Liberation Day, Trump announced a 90-day pause on reciprocal tariffs above 10% for all countries except China (raised to 125%). S&P 500 surged 9.52% — its largest single-day gain since 2008. Nasdaq jumped 12.16%. Record 30B shares traded.",
        "duration": "Short",
        "endDate": "2025-04-22",
        "impactDirection": "Risk-on equity",
        "name": "90-day tariff pause rally",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2025-04-09",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-04-09",
          "household": {
            "drawdownPct": -0.0156,
            "returnDuringPct": -0.0021
          },
          "windowEnd": "2025-04-22",
          "eventTitle": "90-day tariff pause rally",
          "windowStart": "2025-04-09",
          "divergencePp": 0.0087,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0243,
            "returnDuringPct": -0.0123
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "EM",
          "USD",
          "tech",
          "retail"
        ],
        "dateLabel": "2025-05-12",
        "description": "After two days of talks in Geneva, the US and China agreed to reduce reciprocal tariffs from 125% to 10% for 90 days. S&P 500 surged 3.3%, Nasdaq +4.4%. Apple and Amazon led gains as the deal eased supply-chain fears for import-dependent tech and retail sectors.",
        "duration": "Short",
        "endDate": "2025-05-19",
        "impactDirection": "Risk-on equity",
        "name": "US-China Geneva tariff truce",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2025-05-11",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-05-12",
          "household": {
            "drawdownPct": -0.0009,
            "recoveryDays": 0,
            "returnDuringPct": 0.0101
          },
          "windowEnd": "2025-05-19",
          "eventTitle": "US-China Geneva tariff truce",
          "windowStart": "2025-05-11",
          "divergencePp": -0.0009,
          "sameRiskBenchmark": {
            "drawdownPct": 0,
            "recoveryDays": 0,
            "returnDuringPct": 0.0096
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "USD",
          "imports-sensitive sectors"
        ],
        "dateLabel": "2026-02-01",
        "description": "The Supreme Court affirmed that the Trump administration's use of emergency powers to impose the April 2025 reciprocal tariffs was unlawful, formally unwinding the tariff regime's legal basis. (Exact date to verify on next run.)",
        "duration": "Extended",
        "endDate": "2026-02-28",
        "impactDirection": "Risk-on equity",
        "name": "Supreme Court strikes down Liberation Day tariffs",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2026-02-01",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2026-02-01",
          "household": {
            "drawdownPct": -0.0086,
            "returnDuringPct": 0.0077
          },
          "windowEnd": "2026-02-28",
          "eventTitle": "Supreme Court strikes down Liberation Day tariffs",
          "windowStart": "2026-02-01",
          "divergencePp": 0.0022,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0109,
            "returnDuringPct": -0.0018
          }
        }
      },
      {
        "assetClassesAffected": [
          "Crude oil",
          "US equities",
          "international equities",
          "defense stocks",
          "US Treasuries"
        ],
        "dateLabel": "2026-02-28",
        "description": "US and Israel launched coordinated airstrikes on Iranian military and nuclear sites, with nearly 900 strikes in the first 12 hours. Iranian leadership was decapitated. Brent crude surged 10–13% immediately; global equity markets sold off sharply on escalation and energy-supply fears.",
        "duration": "Extended",
        "endDate": "2026-03-04",
        "impactDirection": "Risk-off equity",
        "name": "Operation Epic Fury — US-Israel strikes on Iran",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2026-02-28",
        "type": "Geopolitical",
        "drawdown": {
          "severity": "major",
          "eventDate": "2026-02-28",
          "household": {
            "drawdownPct": -0.0099,
            "returnDuringPct": -0.0064
          },
          "windowEnd": "2026-03-04",
          "eventTitle": "Operation Epic Fury — US-Israel strikes on Iran",
          "windowStart": "2026-02-28",
          "divergencePp": -0.0052,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0047,
            "returnDuringPct": -0.0013
          }
        }
      }
    ],
    "performanceSummary": {
      "maxDrawdown3y": -0.0915,
      "maxDrawdownRecoveryDays": 37,
      "benchmark": {
        "sharpe3y": 1.3341,
        "blendCash": 0.4444,
        "blendEquity": 0.4513,
        "volatility3y": 0.0684,
        "maxDrawdown3y": -0.088,
        "blendFixedIncome": 0.1043,
        "return1yAnnualized": 0.0716,
        "return3yAnnualized": 0.1271,
        "return3yCumulative": 0.4324
      },
      "assetAllocation": {
        "currentEF": {
          "equity": 0.4513,
          "fixedIncome": 0.5487
        },
        "currentEFC": {
          "cash": 0.4444,
          "equity": 0.4513,
          "fixedIncome": 0.1043
        },
        "targetEF": {
          "equity": 0.4022,
          "fixedIncome": 0.5978
        },
        "targetEFC": {
          "cash": 0.4305,
          "equity": 0.4022,
          "fixedIncome": 0.1679
        }
      },
      "concentration": {
        "topSectorPct": 0.3134,
        "topSectorName": "Technology",
        "isMaterialConcentration": true
      },
      "positions": [
        {
          "account": "IRA - Roth Timothy",
          "ticker": "UPRO",
          "name": "ProShares UltraPro S&P500",
          "type": "ETF",
          "category": "Trading--Leveraged Equity",
          "value": 12740,
          "weight_in_account": 0.5096,
          "expense_ratio": 0.0088
        },
        {
          "account": "401(k) - Timothy",
          "ticker": "VTI",
          "name": "Vanguard Morningstar Total Stock Market ETF",
          "type": "ETF",
          "category": "Large Blend",
          "value": 58800,
          "weight_in_account": 0.84,
          "expense_ratio": 0.0003
        },
        {
          "account": "Brokerage account",
          "ticker": "JNK",
          "name": "SPDR Bloomberg High Yield Bond ETF",
          "type": "ETF",
          "category": "High Yield Bond",
          "value": 9800,
          "weight_in_account": 0.245,
          "expense_ratio": 0.004
        }
      ],
      "taxDragAnalysis": {
        "householdRollup": [
          [
            "Metric",
            "Value",
            "Notes"
          ],
          [
            "Total annual tax cost (Table 2)",
            498.23,
            "All taxable-account rows, including money-market positions."
          ],
          [
            "Money-market drag routed to Cash sub-task",
            0,
            "Money-market positions stay visible here but are carved out of the in-scope Tax Drag total."
          ],
          [
            "In-scope tax cost (Table 2 ex-MM)",
            498.23,
            "Standalone Tax Drag total after routing money-market drag to Cash."
          ],
          [
            "Total annual tax cost saved (Table 3)",
            667.35,
            "Permanent annual tax saved if those holdings were taxable today."
          ],
          [
            "Total annual tax cost deferred (Table 4)",
            946.28,
            "Deferred, not eliminated; future withdrawals remain taxable on exit."
          ],
          [
            "NIIT contribution to Table 2",
            0,
            "Taxable net-investment components multiplied by the current NIIT rate."
          ]
        ],
        "accountTypeInputs": [
          [
            "#",
            "Account name",
            "Account type",
            "Tax treatment"
          ],
          [
            "1",
            "Cash account",
            "Checking account",
            "Taxable"
          ],
          [
            "2",
            "401k - Melanie",
            "401k - Traditional",
            "Tax deferred"
          ],
          [
            "3",
            "Brokerage account",
            "Brokerage account",
            "Taxable"
          ],
          [
            "4",
            "IRA - Roth Melanie",
            "401k - Roth",
            "Tax free"
          ],
          [
            "5",
            "401(k) - Timothy",
            "401k - Traditional",
            "Tax deferred"
          ],
          [
            "6",
            "IRA - Roth Timothy",
            "401k - Roth",
            "Tax free"
          ]
        ],
        "effectiveTaxMargin": [
          [
            "Component",
            "Rate",
            "Source / Trigger",
            "Applies to"
          ],
          [
            "Federal ordinary",
            "24%",
            "FH metrics — currentTaxBracket",
            "Ordinary income, ST cap gains, ST cap gain distributions, ordinary interest, non-qualified dividends"
          ],
          [
            "Federal LTCG",
            "15%",
            "PW-computed federal LTCG (2026 thresholds; taxable-income proxy)",
            "Qualified dividends, LT cap gains, LT cap gain distributions"
          ],
          [
            "State (CA)",
            "9.3%",
            "FH metrics — stateTaxRate (CA)",
            "All investment income (state rules)"
          ],
          [
            "NIIT",
            "0%",
            "FH metrics — niitRate",
            "All net investment income"
          ],
          [
            "Total taxable income",
            "$212,800",
            "FH metrics — taxableIncome.totalTaxableIncome",
            "Debug input for LTCG and NIIT lookups"
          ],
          [
            "MAGI proxy",
            "$212,800",
            "Current tax-margin logic — reuse taxableIncome.totalTaxableIncome as MAGI proxy",
            "Debug input for NIIT and current LTCG threshold lookup"
          ],
          [
            "State input",
            "CA — California",
            "PW params — state.code / state.name",
            "Debug input for state marginal-rate lookup"
          ],
          [
            "Expected retirement ordinary",
            "23.52%",
            "FH metrics — expectedTaxBracketInRetirement",
            "Future withdrawals from tax-deferred accounts"
          ],
          [
            "Effective ordinary rate",
            "33.3%",
            "24% + 9.3% + 0%",
            "Today's ordinary-rate income"
          ],
          [
            "Effective LTCG rate",
            "24.3%",
            "15% + 9.3% + 0%",
            "Today's LTCG-rate income"
          ]
        ],
        "fundHoldingsInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Morningstar category",
            "Balance",
            "Shares",
            "Estimated shares",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Interest income ($/share)",
            "Tax-free income ($/share)",
            "LT cap gain ($/share)",
            "ST cap gain ($/share)",
            "Ordinary-rate share (non-qual div + interest + ST cap gain) / total distribution",
            "Tax cost ratio",
            "Turnover",
            "PCGE"
          ],
          [
            "1",
            "401k - Melanie",
            "Cash (USD)",
            "Money Market-Taxable",
            1100,
            1100,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "2",
            "IRA - Roth Timothy",
            "FCNTX",
            "Large Growth",
            11760,
            449.71,
            "-",
            "$0",
            "$0",
            "$0",
            "$0",
            "$1.265",
            "$0",
            "0%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "3",
            "IRA - Roth Timothy",
            "UPRO",
            "Trading--Leveraged Equity",
            12740,
            98.81,
            "-",
            "$0",
            "$0.973",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "4",
            "401(k) - Timothy",
            "Cash (USD)",
            "Money Market-Taxable",
            1400,
            1400,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "5",
            "401k - Melanie",
            "LQD",
            "Corporate Bond",
            14700,
            140.8,
            "-",
            "$0",
            "$4.938",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "6",
            "Brokerage account",
            "VWO",
            "Diversified Emerging Markets",
            14700,
            265.53,
            "-",
            "$0.168",
            "$1.329",
            "$0",
            "$0",
            "$0",
            "$0",
            "88.77%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "7",
            "Brokerage account",
            "SCHD",
            "Large Value",
            14700,
            417.85,
            "-",
            "$0",
            "$1.048",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "8",
            "Cash account",
            "Cash (USD)",
            "Money Market-Taxable",
            150000,
            150000,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "9",
            "401k - Melanie",
            "VEA",
            "Foreign Large Blend",
            39200,
            578.43,
            "-",
            "$0",
            "$2.009",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "10",
            "IRA - Roth Melanie",
            "Cash (USD)",
            "Money Market-Taxable",
            400,
            400,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "11",
            "IRA - Roth Timothy",
            "Cash (USD)",
            "Money Market-Taxable",
            500,
            500,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "12",
            "401(k) - Timothy",
            "VTI",
            "Large Blend",
            58800,
            162.49,
            "-",
            "$0.86",
            "$2.897",
            "$0",
            "$0",
            "$0",
            "$0",
            "77.11%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "13",
            "Brokerage account",
            "Cash (USD)",
            "Money Market-Taxable",
            800,
            800,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "14",
            "IRA - Roth Melanie",
            "FIGSX",
            "Foreign Large Growth",
            9800,
            507.77,
            "-",
            "$0.28",
            "$0.049",
            "$0",
            "$0",
            "$1.328",
            "$0",
            "2.98%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "15",
            "Brokerage account",
            "JNK",
            "High Yield Bond",
            9800,
            105.83,
            "-",
            "$0",
            "$6.358",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "16",
            "401(k) - Timothy",
            "SCHP",
            "Inflation-Protected Bond",
            9800,
            382.96,
            "-",
            "$0",
            "$1.075",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "17",
            "IRA - Roth Melanie",
            "VWELX",
            "Moderate Allocation",
            9800,
            212.63,
            "-",
            "$0.386",
            "$0.623",
            "$0",
            "$0",
            "$3.4",
            "$0.715",
            "26.12%",
            "[pending]",
            "[pending]",
            "[pending]"
          ]
        ],
        "stockHoldingsInputs": [
          [
            "#",
            "Account",
            "Name",
            "Ticker",
            "Sector",
            "Industry",
            "Country",
            "Balance",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Dividend yield TTM"
          ]
        ],
        "taxFreeAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable)",
            "Annual tax cost saved"
          ],
          [
            "1",
            "IRA - Roth Timothy",
            "FCNTX",
            11760,
            "LT cap gain distribution",
            568.89,
            "24.3%",
            138.24
          ],
          [
            "2",
            "IRA - Roth Timothy",
            "UPRO",
            12740,
            "Non-qualified dividend",
            96.18,
            "33.3%",
            32.03
          ],
          [
            "3",
            "IRA - Roth Melanie",
            "Cash (USD)",
            400,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "4",
            "IRA - Roth Timothy",
            "Cash (USD)",
            500,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "5a",
            "IRA - Roth Melanie",
            "FIGSX",
            9800,
            "Qualified dividend",
            141.98,
            "24.3%",
            34.5
          ],
          [
            "5b",
            "IRA - Roth Melanie",
            "FIGSX",
            9800,
            "Non-qualified dividend",
            25.07,
            "33.3%",
            8.3492
          ],
          [
            "5c",
            "IRA - Roth Melanie",
            "FIGSX",
            9800,
            "LT cap gain distribution",
            674.32,
            "24.3%",
            163.86
          ],
          [
            "5d",
            "IRA - Roth Melanie",
            "FIGSX",
            9800,
            "Subtotal",
            841.38,
            "-",
            206.71
          ],
          [
            "6a",
            "IRA - Roth Melanie",
            "VWELX",
            9800,
            "Qualified dividend",
            82.13,
            "24.3%",
            19.96
          ],
          [
            "6b",
            "IRA - Roth Melanie",
            "VWELX",
            9800,
            "Non-qualified dividend",
            132.44,
            "33.3%",
            44.1
          ],
          [
            "6c",
            "IRA - Roth Melanie",
            "VWELX",
            9800,
            "LT cap gain distribution",
            722.86,
            "24.3%",
            175.66
          ],
          [
            "6d",
            "IRA - Roth Melanie",
            "VWELX",
            9800,
            "ST cap gain distribution",
            152.12,
            "33.3%",
            50.65
          ],
          [
            "6e",
            "IRA - Roth Melanie",
            "VWELX",
            9800,
            "Subtotal",
            1089.54,
            "-",
            290.37
          ],
          [
            "Total",
            "Total tax-free",
            "-",
            45000,
            "-",
            2595.99,
            "-",
            667.35
          ]
        ],
        "taxableAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate",
            "Annual tax cost"
          ],
          [
            "1a",
            "Brokerage account",
            "VWO",
            14700,
            "Qualified dividend",
            44.66,
            "24.3%",
            10.85
          ],
          [
            "1b",
            "Brokerage account",
            "VWO",
            14700,
            "Non-qualified dividend",
            352.93,
            "33.3%",
            117.52
          ],
          [
            "1c",
            "Brokerage account",
            "VWO",
            14700,
            "Subtotal",
            397.59,
            "-",
            128.38
          ],
          [
            "2",
            "Brokerage account",
            "SCHD",
            14700,
            "Non-qualified dividend",
            437.74,
            "33.3%",
            145.77
          ],
          [
            "3",
            "Cash account",
            "Cash (USD)",
            150000,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "4",
            "Brokerage account",
            "Cash (USD)",
            800,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "5",
            "Brokerage account",
            "JNK",
            9800,
            "Non-qualified dividend",
            672.94,
            "33.3%",
            224.09
          ],
          [
            "Total",
            "Total taxable",
            "-",
            190000,
            "-",
            1508.27,
            "-",
            498.23
          ]
        ],
        "costBasisBlockingNotes": [
          [
            "Account",
            "Blocking note"
          ],
          [
            "Brokerage account",
            "Implementation of Brokerage account cannot be responsibly sequenced without tax-lot data."
          ]
        ],
        "taxableCostBasisInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Balance (market value)",
            "Cost basis",
            "Unrealized gain",
            "Holding period",
            "Notes"
          ],
          [
            "1",
            "Brokerage account",
            "VWO",
            14700,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "2",
            "Brokerage account",
            "SCHD",
            14700,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "3",
            "Cash account",
            "Cash (USD)",
            150000,
            150000,
            0,
            "N/A",
            "Money market — NAV $1.00, no embedded gain by design."
          ],
          [
            "4",
            "Brokerage account",
            "Cash (USD)",
            800,
            800,
            0,
            "N/A",
            "Money market — NAV $1.00, no embedded gain by design."
          ],
          [
            "5",
            "Brokerage account",
            "JNK",
            9800,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "Total",
            "Total taxable",
            "-",
            190000,
            "[missing cost basis]",
            "[missing cost basis]",
            "-",
            "Totals stay blocked until missing tax-lot inputs are filled."
          ]
        ],
        "taxDeferredAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable today)",
            "Annual tax cost deferred"
          ],
          [
            "1",
            "401k - Melanie",
            "Cash (USD)",
            1100,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "2",
            "401(k) - Timothy",
            "Cash (USD)",
            1400,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "3",
            "401k - Melanie",
            "LQD",
            14700,
            "Non-qualified dividend",
            695.21,
            "33.3%",
            231.51
          ],
          [
            "4",
            "401k - Melanie",
            "VEA",
            39200,
            "Non-qualified dividend",
            1162.29,
            "33.3%",
            387.04
          ],
          [
            "5a",
            "401(k) - Timothy",
            "VTI",
            58800,
            "Qualified dividend",
            139.71,
            "24.3%",
            33.95
          ],
          [
            "5b",
            "401(k) - Timothy",
            "VTI",
            58800,
            "Non-qualified dividend",
            470.7,
            "33.3%",
            156.74
          ],
          [
            "5c",
            "401(k) - Timothy",
            "VTI",
            58800,
            "Subtotal",
            610.41,
            "-",
            190.69
          ],
          [
            "6",
            "401(k) - Timothy",
            "SCHP",
            9800,
            "Non-qualified dividend",
            411.53,
            "33.3%",
            137.04
          ],
          [
            "Total",
            "Total tax-deferred",
            "-",
            125000,
            "-",
            2879.44,
            "-",
            946.28
          ]
        ],
        "componentTaxTreatmentMatrix": [
          [
            "Component",
            "Federal rate type",
            "Effective household rate today",
            "Taxable accounts",
            "Tax-free accounts",
            "Tax-deferred accounts",
            "Notes"
          ],
          [
            "Qualified dividend",
            "LTCG",
            "24.3%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for US common stock and treaty-country foreign names; funds keep the precomputed Morningstar qualified split."
          ],
          [
            "Non-qualified dividend",
            "ORDINARY",
            "33.3%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for REIT and non-treaty foreign names, while MLP distributions are treated as ROC; funds keep the precomputed Morningstar non-qualified split."
          ],
          [
            "Interest income",
            "ORDINARY",
            "33.3%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Money-market and bond-style fund income is treated as ordinary-rate income."
          ],
          [
            "Tax-free income",
            "Tax-exempt federal",
            "0%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Current phase assumes a 0% effective rate because state-specific muni exposure is not available in the data path."
          ],
          [
            "LT cap gain distribution",
            "LTCG",
            "24.3%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed long-term capital gains use the LTCG household rate."
          ],
          [
            "ST cap gain distribution",
            "ORDINARY",
            "33.3%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed short-term capital gains use the ordinary household rate."
          ]
        ]
      }
    }
  },
  "daniel-emily-johnson": {
    "meta": {
      "slug": "daniel-emily-johnson",
      "household": "Daniel & Emily",
      "city": "Denver",
      "state": "CO",
      "tax_filing_status": "MARRIED_JOINTLY",
      "isCouple": true,
      "owners": [
        {
          "key": "A",
          "name": "Daniel",
          "role": "client",
          "age": 44,
          "retirement_age": 62,
          "risk_profile": "Growth"
        },
        {
          "key": "B",
          "name": "Emily",
          "role": "co-client",
          "age": 42,
          "retirement_age": 60,
          "risk_profile": "Moderate"
        }
      ]
    },
    "score": {
      "published_score": 52,
      "scale": "0 to 100",
      "band": "vulnerable",
      "colour": "red",
      "message": "With a score of 52, your financial health is below average, affecting not just your financial life but your overall well-being. Let's work together to take immediate steps toward organizing and clarifying your financial situation. Let me help you take control of your finances and improve the quality of your life.",
      "pillars": [
        {
          "pillar": "Savings and cash flow",
          "score": 54,
          "points_shown_in_app": "16/30"
        },
        {
          "pillar": "Debt",
          "score": 76,
          "points_shown_in_app": "15/20"
        },
        {
          "pillar": "Investments",
          "score": 51,
          "points_shown_in_app": "8/15"
        },
        {
          "pillar": "Liquidity and emergency fund",
          "score": 85,
          "points_shown_in_app": "13/15"
        },
        {
          "pillar": "Insurance and protection",
          "score": 0,
          "points_shown_in_app": "0/20"
        }
      ],
      "caps_applied": [],
      "top_moves": [
        {
          "title": "Raise mortality coverage",
          "action": "Add $1,166,000 of life cover to reach the next mortality-coverage anchor",
          "effort": "low",
          "target_amount": 1616000,
          "score_before": 52,
          "score_after": 57,
          "lifts_a_cap": false
        },
        {
          "title": "Add umbrella cover",
          "action": "Add $1M of umbrella to raise the liability shield",
          "effort": "low",
          "target_amount": 1000000,
          "score_before": 52,
          "score_after": 56,
          "lifts_a_cap": false
        },
        {
          "title": "Raise annual savings",
          "action": "Redirect $15,032/year of free cash flow into savings to raise retirement-directed savings toward the next band",
          "effort": "medium",
          "target_amount": 41032.01,
          "score_before": 52,
          "score_after": 55,
          "lifts_a_cap": false
        }
      ],
      "combined_moves": [
        {
          "moves": [
            "Raise mortality coverage",
            "Add umbrella cover"
          ],
          "score_after": 60,
          "note": "Together they raise the published score more than either move alone."
        },
        {
          "moves": [
            "Raise mortality coverage",
            "Raise annual savings"
          ],
          "score_after": 60,
          "note": "Together they raise the published score more than either move alone."
        },
        {
          "moves": [
            "Raise mortality coverage",
            "Add umbrella cover",
            "Raise annual savings"
          ],
          "score_after": 60,
          "note": "Together they raise the published score more than either move alone."
        },
        {
          "moves": [
            "Add umbrella cover",
            "Raise annual savings"
          ],
          "score_after": 59,
          "note": "Together they raise the published score more than either move alone."
        }
      ]
    },
    "persona": {
      "D0": "EMERGING. Investable assets are $330,000, which is under the $500K line. That covers the two 401(k)s ($150,000 and $100,000), the 529 college account ($30,000) and the taxable brokerage account ($50,000). It excludes the home and the $14,000 in checking and savings. Net worth is $511,000: $1,129,000 of assets (including a $750,000 home) minus $618,000 of debt. Only $190,000 of the home is equity.\r\n\r\nHousehold income is $280,000 ($160,000 Daniel, $120,000 Emily), about the 90th percentile in Colorado. High income against modest investable assets defines the profile.",
      "D1": "MID ACCUMULATION. Daniel is 44 and Emily is 42. Both work. Daniel plans to retire at 62 and Emily at 60, both in 2044, 17 years away. Their children are Oliver (11) and Sophia (9). College starts for Oliver in August 2033 and for Sophia in August 2035. The plan runs to age 91. No change of stage is expected within 24 months.",
      "D2": "MODERATE. Income is two salaries, with no equity compensation, business, rental property or single stock. They file jointly. Accounts are two traditional 401(k)s, a 529, a taxable brokerage account, checking and savings. They own one home and one car, and carry four debts (mortgage, credit card, car loan, student loan). Both have a whole life policy and disability cover.",
      "D3": "SIGNIFICANT GAPS. Not a crisis: bills are paid and free cash flow is positive at $15,032 a year. The score is 52 out of 100, in the \"vulnerable\" band, with no cap applied. By area: savings and cash flow 16 of 30, debt 15 of 20, investments 8 of 15, liquidity 13 of 15, insurance and protection 0 of 20.\r\n\r\n- **Retirement:** nothing goes into either 401(k) today, although each of them could put in up to $24,500 a year. The retirement gap is $1,427,456 in today's dollars, and closing it would take about $34,165 more saving a year, more than twice their free cash flow. Retirement spending is projected at $124,071 a year. Income (nearly all Social Security) covers about 49% of it, and savings must pay about $62,932 a year, an average draw of 5.5%. The money lasts to age 91 with $260,272 left, a modest cushion.\r\n- **Cash:** accessible cash is $19,000 (checking $5,000, savings $9,000 and $5,000 of money market inside the brokerage account). That covers about 1.4 months of essential expenses, against a recommended 8 to 9 months ($106,860 to $120,217.50). With the $4,500 vacation due in January 2027, the cash target is $111,360 to $124,717.50 and the gap is $92,360.\r\n- **Life insurance:** Daniel has $250,000 against a recommended $1,600,000 to $2,400,000 (a shortfall of $1,350,000). Emily has $200,000 against $1,200,000 to $1,800,000 (a shortfall of $1,000,000).\r\n- **Umbrella:** there is no umbrella policy, against a recommended $1,000,000.\r\n- **Debt:** total debt is $618,000, with monthly payments of $5,420. Debt payments take 23.23% of gross income, and housing plus debt together take 27.25%, below the 36%, 43% and 50% levels lenders commonly use. The costly item is the Chase Sapphire card: $18,000 at 24.9%, paid at $450 a month, projected to clear in January 2034. At today's balance, $373.50 of each payment is interest.\r\n- **College:** the 529 holds $30,000 and receives $8,000 a year. College costs $15,000 a year per child ($60,000 each). A gap of $106,552 remains beyond the 529, and about $1,927.57 more saving in the first year is needed, rising each year.",
      "D4a": "- **D4a stated:** Daniel is Growth (4) and Emily is Moderate (3). The household reading is MODERATE, with a split between the two.\r",
      "D4b": "- **D4b revealed:** MODERATE. Across $344,000 of cash and investments the mix is 54.35% stocks, 35.99% bonds and 9.66% cash. The household target mix is about 66.3% stocks, so they hold less than the target. Over three years it returned 13.7% a year, with a worst fall of 10.0%. Daniel's 401(k) holds about 59.9% stocks, one risk step below the Growth profile he states (the Growth benchmark is 80.0% stocks). Emily's holds about 53.1%, near the Moderate benchmark of 60.0%. Technology is 35.6% of the stock holdings, flagged as concentrated, though there are no individual stocks.\r",
      "D4c": "- **D4c inferred:** AGGRESSIVE. This reads overall exposure, not the funds. Cash covers 1.4 months, life cover is far below the recommended range, there is no umbrella policy, a 24.9% card is carried, nothing goes into the 401(k)s, and two salaries equal 54.79% of net worth.\r\n\r\nAlignment: MISALIGNED. The household says Moderate and the portfolio is moderate, but the thin cushion and open protection gaps expose the family to more risk than a Moderate household would accept. This looks like drift rather than a considered choice (see T3).",
      "D4": "- **D4a stated:** Daniel is Growth (4) and Emily is Moderate (3). The household reading is MODERATE, with a split between the two.\r\n- **D4b revealed:** MODERATE. Across $344,000 of cash and investments the mix is 54.35% stocks, 35.99% bonds and 9.66% cash. The household target mix is about 66.3% stocks, so they hold less than the target. Over three years it returned 13.7% a year, with a worst fall of 10.0%. Daniel's 401(k) holds about 59.9% stocks, one risk step below the Growth profile he states (the Growth benchmark is 80.0% stocks). Emily's holds about 53.1%, near the Moderate benchmark of 60.0%. Technology is 35.6% of the stock holdings, flagged as concentrated, though there are no individual stocks.\r\n- **D4c inferred:** AGGRESSIVE. This reads overall exposure, not the funds. Cash covers 1.4 months, life cover is far below the recommended range, there is no umbrella policy, a 24.9% card is carried, nothing goes into the 401(k)s, and two salaries equal 54.79% of net worth.\r\n\r\nAlignment: MISALIGNED. The household says Moderate and the portfolio is moderate, but the thin cushion and open protection gaps expose the family to more risk than a Moderate household would accept. This looks like drift rather than a considered choice (see T3).",
      "D5": "DUAL. This is inferred from the plan's structure, not from anything they said. They appear to split roles: Emily holds the checking, savings, 529 and brokerage accounts and makes all $26,000 a year of saving, while Daniel's name is on the credit card and the student loan. Protection and cash gaps persist, which suggests defaults rather than active management. Confidence is low.",
      "D6": "PROTECTION. This is a provisional reading from structure, and confidence is low. The largest score levers are protection moves, and with two children and two incomes at risk, protecting the family is the likely motivation. Protection is still the weakest area, so the anchor is not yet backed by action.",
      "transitionAlerts": "None detected within 12 to 24 months. The nearest events are the $4,500 vacation in January 2027, college in August 2033 and August 2035, and retirement in 2044.",
      "subjectiveConcerns": "None recorded. The plan holds no interview notes or free text from Daniel and Emily, so what worries them is not stated. Their stated goals are retirement at 62 and 60, a $4,500 vacation every year, and $60,000 of college per child.",
      "objectiveConcerns": [
        {
          "id": "O1",
          "detail": "- **O1: Retirement (SIGNIFICANT).** The gap is $1,427,456 and about $34,165 a year more is needed, while free cash flow is $15,032 a year. Nothing goes into either 401(k). No employer match is recorded; the plan estimates about $6,400 for Daniel and $4,800 for Emily, unconfirmed. Contributing the full $49,000 would cut tax by about $11,760 a year at their 24% marginal rate."
        },
        {
          "id": "O2",
          "detail": "- **O2: Life insurance (SIGNIFICANT).** Shortfalls of $1,350,000 for Daniel and $1,000,000 for Emily. Adding $1,166,000 of cover is worth 5 points of score (52 to 57)."
        },
        {
          "id": "O3",
          "detail": "- **O3: No umbrella cover (MODERATE).** A $1,000,000 gap. Adding it is worth 4 points (52 to 56). With life cover, the two together lift it to 60."
        },
        {
          "id": "O4",
          "detail": "- **O4: Cash reserve (SIGNIFICANT).** Accessible cash of $19,000 against a target of $111,360 to $124,717.50, a gap of $92,360."
        },
        {
          "id": "O5",
          "detail": "- **O5: Debt load and the 24.9% card (MODERATE).** Debt-only DTI is 23.23%, monthly debt payments are $5,420, and the $18,000 card is the most expensive debt by a wide margin. The mortgage is $560,000 at 6.5% ($4,100 a month), the Toyota Highlander loan $28,000 at 7.9% ($620) and Daniel's student loan $12,000 at 5.2% ($250)."
        },
        {
          "id": "O6",
          "detail": "- **O6: Income dependence (MINOR).** Annual salary is 54.79% of net worth, so the household relies heavily on two paychecks. Worth keeping in view, with no action needed today."
        },
        {
          "id": "O7",
          "detail": "- **O7: Thin margin (MODERATE).** Free cash flow of $15,032 a year is 5.37% of income, small next to the needs above. Raising annual savings alone lifts the score from 52 to 55."
        },
        {
          "id": "O8",
          "detail": "- **O8: College funding (MODERATE).** A $106,552 gap remains after the $30,000 already in the 529, even though $8,000 a year goes in."
        }
      ],
      "tensions": [
        {
          "id": "T1",
          "detail": "- **T1 (HIGH):** O1 and O4, together with O2 and O3, compete for the same $15,032 of yearly free cash flow. Retirement needs about $34,165 a year and the cash gap is $92,360. They must weigh the trade-off together."
        },
        {
          "id": "T2",
          "detail": "- **T2 (MEDIUM):** O2, O3 and D4c. The protection gaps stay open while the household carries high exposure and a thin cushion, and closing them costs cash flow that O1 and O4 also need."
        },
        {
          "id": "T3",
          "detail": "- **T3 (LOW):** D4a against D4c. They state a Moderate orientation and hold a moderate portfolio, but their overall exposure is closer to aggressive, which suggests drift. Any plan also has to work for both a Growth and a Moderate partner."
        },
        {
          "id": "T4",
          "detail": "- **T4 (MEDIUM):** O5 against the current saving pattern. The household saves $26,000 a year ($12,000 to brokerage, $8,000 to the 529 and $6,000 to cash) while carrying an $18,000 balance at 24.9% and sending $0 to the 401(k)s."
        },
        {
          "id": "T5",
          "detail": "- **T5 (MEDIUM):** O8 against O1. The 529 receives $8,000 a year while retirement receives nothing, though retirement is the larger gap."
        }
      ]
    },
    "projections": {
      "yearly": [
        {
          "year": 2026,
          "age_client": 44,
          "age_co_client": 42,
          "net_worth": 522431,
          "net_worth_todays_dollars": 521128,
          "total_debts": 614435,
          "investable_assets": 350354,
          "net_worth_needed": 522431
        },
        {
          "year": 2027,
          "age_client": 45,
          "age_co_client": 43,
          "net_worth": 612940,
          "net_worth_todays_dollars": 593364,
          "total_debts": 592082,
          "investable_assets": 399708,
          "net_worth_needed": 612940
        },
        {
          "year": 2028,
          "age_client": 46,
          "age_co_client": 44,
          "net_worth": 710736,
          "net_worth_todays_dollars": 667727,
          "total_debts": 567956,
          "investable_assets": 453403,
          "net_worth_needed": 710736
        },
        {
          "year": 2029,
          "age_client": 47,
          "age_co_client": 45,
          "net_worth": 816300,
          "net_worth_todays_dollars": 744265,
          "total_debts": 541868,
          "investable_assets": 511766,
          "net_worth_needed": 816300
        },
        {
          "year": 2030,
          "age_client": 48,
          "age_co_client": 46,
          "net_worth": 930179,
          "net_worth_todays_dollars": 823061,
          "total_debts": 513601,
          "investable_assets": 575155,
          "net_worth_needed": 930179
        },
        {
          "year": 2031,
          "age_client": 49,
          "age_co_client": 47,
          "net_worth": 1045717,
          "net_worth_todays_dollars": 897980,
          "total_debts": 490171,
          "investable_assets": 643949,
          "net_worth_needed": 1045717
        },
        {
          "year": 2032,
          "age_client": 50,
          "age_co_client": 48,
          "net_worth": 1167703,
          "net_worth_todays_dollars": 973134,
          "total_debts": 468055,
          "investable_assets": 719432,
          "net_worth_needed": 1167703
        },
        {
          "year": 2033,
          "age_client": 51,
          "age_co_client": 49,
          "net_worth": 1281217,
          "net_worth_todays_dollars": 1036216,
          "total_debts": 443675,
          "investable_assets": 783116,
          "net_worth_needed": 1281217
        },
        {
          "year": 2034,
          "age_client": 52,
          "age_co_client": 50,
          "net_worth": 1399114,
          "net_worth_todays_dollars": 1098166,
          "total_debts": 422564,
          "investable_assets": 853392,
          "net_worth_needed": 1399114
        },
        {
          "year": 2035,
          "age_client": 53,
          "age_co_client": 51,
          "net_worth": 1501657,
          "net_worth_todays_dollars": 1143861,
          "total_debts": 400172,
          "investable_assets": 905977,
          "net_worth_needed": 1501657
        },
        {
          "year": 2036,
          "age_client": 54,
          "age_co_client": 52,
          "net_worth": 1609987,
          "net_worth_todays_dollars": 1190179,
          "total_debts": 376280,
          "investable_assets": 961789,
          "net_worth_needed": 1609987
        },
        {
          "year": 2037,
          "age_client": 55,
          "age_co_client": 53,
          "net_worth": 1750437,
          "net_worth_todays_dollars": 1255809,
          "total_debts": 350787,
          "investable_assets": 1047054,
          "net_worth_needed": 1750437
        },
        {
          "year": 2038,
          "age_client": 56,
          "age_co_client": 54,
          "net_worth": 1900037,
          "net_worth_todays_dollars": 1322899,
          "total_debts": 323588,
          "investable_assets": 1138687,
          "net_worth_needed": 1900037
        },
        {
          "year": 2039,
          "age_client": 57,
          "age_co_client": 55,
          "net_worth": 2083384,
          "net_worth_todays_dollars": 1407737,
          "total_debts": 294566,
          "investable_assets": 1261157,
          "net_worth_needed": 2083384
        },
        {
          "year": 2040,
          "age_client": 58,
          "age_co_client": 56,
          "net_worth": 2279585,
          "net_worth_todays_dollars": 1494842,
          "total_debts": 263601,
          "investable_assets": 1393434,
          "net_worth_needed": 2279585
        },
        {
          "year": 2041,
          "age_client": 59,
          "age_co_client": 57,
          "net_worth": 2489458,
          "net_worth_todays_dollars": 1584279,
          "total_debts": 230563,
          "investable_assets": 1536258,
          "net_worth_needed": 2489458
        },
        {
          "year": 2042,
          "age_client": 60,
          "age_co_client": 58,
          "net_worth": 2714718,
          "net_worth_todays_dollars": 1676637,
          "total_debts": 195311,
          "investable_assets": 1690421,
          "net_worth_needed": 2714718
        },
        {
          "year": 2043,
          "age_client": 61,
          "age_co_client": 59,
          "net_worth": 2955621,
          "net_worth_todays_dollars": 1771538,
          "total_debts": 157699,
          "investable_assets": 1856776,
          "net_worth_needed": 2955621
        },
        {
          "year": 2044,
          "age_client": 62,
          "age_co_client": 60,
          "net_worth": 3111209,
          "net_worth_todays_dollars": 1809749,
          "total_debts": 117568,
          "investable_assets": 1934173,
          "net_worth_needed": 3111209
        },
        {
          "year": 2045,
          "age_client": 63,
          "age_co_client": 61,
          "net_worth": 3094647,
          "net_worth_todays_dollars": 1746980,
          "total_debts": 74749,
          "investable_assets": 1835576,
          "net_worth_needed": 3094647
        },
        {
          "year": 2046,
          "age_client": 64,
          "age_co_client": 62,
          "net_worth": 3068954,
          "net_worth_todays_dollars": 1681336,
          "total_debts": 29063,
          "investable_assets": 1723787,
          "net_worth_needed": 3068954
        },
        {
          "year": 2047,
          "age_client": 65,
          "age_co_client": 63,
          "net_worth": 3030391,
          "net_worth_todays_dollars": 1611203,
          "total_debts": 0,
          "investable_assets": 1614522,
          "net_worth_needed": 3030391
        },
        {
          "year": 2048,
          "age_client": 66,
          "age_co_client": 64,
          "net_worth": 2959079,
          "net_worth_todays_dollars": 1526847,
          "total_debts": 0,
          "investable_assets": 1500305,
          "net_worth_needed": 2959079
        },
        {
          "year": 2049,
          "age_client": 67,
          "age_co_client": 65,
          "net_worth": 2878630,
          "net_worth_todays_dollars": 1441492,
          "total_debts": 0,
          "investable_assets": 1375646,
          "net_worth_needed": 2878630
        },
        {
          "year": 2050,
          "age_client": 68,
          "age_co_client": 66,
          "net_worth": 2833527,
          "net_worth_todays_dollars": 1377023,
          "total_debts": 0,
          "investable_assets": 1284987,
          "net_worth_needed": 2833527
        },
        {
          "year": 2051,
          "age_client": 69,
          "age_co_client": 67,
          "net_worth": 2830670,
          "net_worth_todays_dollars": 1335028,
          "total_debts": 0,
          "investable_assets": 1235189,
          "net_worth_needed": 2830670
        },
        {
          "year": 2052,
          "age_client": 70,
          "age_co_client": 68,
          "net_worth": 2851394,
          "net_worth_todays_dollars": 1305106,
          "total_debts": 0,
          "investable_assets": 1207545,
          "net_worth_needed": 2851394
        },
        {
          "year": 2053,
          "age_client": 71,
          "age_co_client": 69,
          "net_worth": 2869569,
          "net_worth_todays_dollars": 1274655,
          "total_debts": 0,
          "investable_assets": 1175881,
          "net_worth_needed": 2869569
        },
        {
          "year": 2054,
          "age_client": 72,
          "age_co_client": 70,
          "net_worth": 2882266,
          "net_worth_todays_dollars": 1242503,
          "total_debts": 0,
          "investable_assets": 1137222,
          "net_worth_needed": 2882266
        },
        {
          "year": 2055,
          "age_client": 73,
          "age_co_client": 71,
          "net_worth": 2888157,
          "net_worth_todays_dollars": 1208292,
          "total_debts": 0,
          "investable_assets": 1090196,
          "net_worth_needed": 2888157
        },
        {
          "year": 2056,
          "age_client": 74,
          "age_co_client": 72,
          "net_worth": 2887962,
          "net_worth_todays_dollars": 1172546,
          "total_debts": 0,
          "investable_assets": 1035474,
          "net_worth_needed": 2887962
        },
        {
          "year": 2057,
          "age_client": 75,
          "age_co_client": 73,
          "net_worth": 2905666,
          "net_worth_todays_dollars": 1144910,
          "total_debts": 0,
          "investable_assets": 996992,
          "net_worth_needed": 2905666
        },
        {
          "year": 2058,
          "age_client": 76,
          "age_co_client": 74,
          "net_worth": 2939460,
          "net_worth_todays_dollars": 1124037,
          "total_debts": 0,
          "investable_assets": 972892,
          "net_worth_needed": 2939460
        },
        {
          "year": 2059,
          "age_client": 77,
          "age_co_client": 75,
          "net_worth": 2976627,
          "net_worth_todays_dollars": 1104651,
          "total_debts": 0,
          "investable_assets": 950404,
          "net_worth_needed": 2976627
        },
        {
          "year": 2060,
          "age_client": 78,
          "age_co_client": 76,
          "net_worth": 3017473,
          "net_worth_todays_dollars": 1086755,
          "total_debts": 0,
          "investable_assets": 929780,
          "net_worth_needed": 3017473
        },
        {
          "year": 2061,
          "age_client": 79,
          "age_co_client": 77,
          "net_worth": 3062328,
          "net_worth_todays_dollars": 1070353,
          "total_debts": 0,
          "investable_assets": 911295,
          "net_worth_needed": 3062328
        },
        {
          "year": 2062,
          "age_client": 80,
          "age_co_client": 78,
          "net_worth": 3111550,
          "net_worth_todays_dollars": 1055455,
          "total_debts": 0,
          "investable_assets": 895251,
          "net_worth_needed": 3111550
        },
        {
          "year": 2063,
          "age_client": 81,
          "age_co_client": 79,
          "net_worth": 3165527,
          "net_worth_todays_dollars": 1042069,
          "total_debts": 0,
          "investable_assets": 881977,
          "net_worth_needed": 3165527
        },
        {
          "year": 2064,
          "age_client": 82,
          "age_co_client": 80,
          "net_worth": 3224681,
          "net_worth_todays_dollars": 1030207,
          "total_debts": 0,
          "investable_assets": 871834,
          "net_worth_needed": 3224681
        },
        {
          "year": 2065,
          "age_client": 83,
          "age_co_client": 81,
          "net_worth": 3289465,
          "net_worth_todays_dollars": 1019883,
          "total_debts": 0,
          "investable_assets": 865214,
          "net_worth_needed": 3289465
        },
        {
          "year": 2066,
          "age_client": 84,
          "age_co_client": 82,
          "net_worth": 3360374,
          "net_worth_todays_dollars": 1011114,
          "total_debts": 0,
          "investable_assets": 862546,
          "net_worth_needed": 3360374
        },
        {
          "year": 2067,
          "age_client": 85,
          "age_co_client": 83,
          "net_worth": 3437938,
          "net_worth_todays_dollars": 1003918,
          "total_debts": 0,
          "investable_assets": 864297,
          "net_worth_needed": 3437938
        },
        {
          "year": 2068,
          "age_client": 86,
          "age_co_client": 84,
          "net_worth": 3522737,
          "net_worth_todays_dollars": 998315,
          "total_debts": 0,
          "investable_assets": 870975,
          "net_worth_needed": 3522737
        },
        {
          "year": 2069,
          "age_client": 87,
          "age_co_client": 85,
          "net_worth": 3615393,
          "net_worth_todays_dollars": 994330,
          "total_debts": 0,
          "investable_assets": 883135,
          "net_worth_needed": 3615393
        },
        {
          "year": 2070,
          "age_client": 88,
          "age_co_client": 86,
          "net_worth": 3716581,
          "net_worth_todays_dollars": 991987,
          "total_debts": 0,
          "investable_assets": 901378,
          "net_worth_needed": 3716581
        },
        {
          "year": 2071,
          "age_client": 89,
          "age_co_client": 87,
          "net_worth": 3827030,
          "net_worth_todays_dollars": 991315,
          "total_debts": 0,
          "investable_assets": 926360,
          "net_worth_needed": 3827030
        },
        {
          "year": 2072,
          "age_client": 90,
          "age_co_client": 88,
          "net_worth": 3947529,
          "net_worth_todays_dollars": 992344,
          "total_debts": 0,
          "investable_assets": 958792,
          "net_worth_needed": 3947529
        },
        {
          "year": 2073,
          "age_client": null,
          "age_co_client": 89,
          "net_worth": 4084580,
          "net_worth_todays_dollars": 996488,
          "total_debts": 0,
          "investable_assets": 1005098,
          "net_worth_needed": 4084580
        },
        {
          "year": 2074,
          "age_client": null,
          "age_co_client": 90,
          "net_worth": 4252040,
          "net_worth_todays_dollars": 1006722,
          "total_debts": 0,
          "investable_assets": 1079052,
          "net_worth_needed": 4252040
        },
        {
          "year": 2075,
          "age_client": null,
          "age_co_client": 90,
          "net_worth": 4325892,
          "net_worth_todays_dollars": 1011500,
          "total_debts": 0,
          "investable_assets": 1113108,
          "net_worth_needed": 4325892
        }
      ],
      "firstNegativeInvestableYear": null,
      "firstNegativeNetWorthYear": null,
      "peakInvestable": 1934173,
      "endOfPlan": {
        "year": 2075,
        "age_client": null,
        "age_co_client": 90,
        "net_worth": 4325892,
        "net_worth_todays_dollars": 1011500,
        "total_debts": 0,
        "investable_assets": 1113108,
        "net_worth_needed": 4325892
      }
    },
    "goals": {
      "goalsSummary": [
        {
          "goalType": "RETIREMENT",
          "value": "Both Daniel and Emily want to retire in 2044 at ages 62 and 60."
        },
        {
          "amount": 4500,
          "goalType": "VACATION",
          "value": "Going on a $4,500 vacation every year."
        },
        {
          "amount": 60000,
          "goalType": "COLLEGE",
          "value": "Finance education for 2 children ($60,000 in total for each child)."
        }
      ],
      "chartGoals": [
        {
          "date": "2027-01-01T00:00:00.000Z",
          "goalType": "VACATION",
          "name": "Take a vacation",
          "termDate": "2044-09-01T00:00:00.000Z"
        },
        {
          "date": "2033-08-01T00:00:00.000Z",
          "goalType": "COLLEGE",
          "name": "College Oliver",
          "termDate": "2037-01-01T00:00:00.000Z"
        },
        {
          "date": "2035-08-01T00:00:00.000Z",
          "goalType": "COLLEGE",
          "name": "College Sophia",
          "termDate": "2039-01-01T00:00:00.000Z"
        },
        {
          "date": "2044-05-01T00:00:00.000Z",
          "goalType": "RETIREMENT",
          "name": "Emily's Retirement"
        },
        {
          "date": "2044-09-01T00:00:00.000Z",
          "goalType": "RETIREMENT",
          "name": "Daniel's Retirement"
        }
      ]
    },
    "facts": {
      "facts": {
        "cash": {
          "monthsCovered": {
            "unit": "months",
            "basis": "n/a",
            "label": "Months of essential expenses accessible cash covers",
            "value": "1.4",
            "period": "today, before near-term goals",
            "replaces": [
              "ratios.emergencyFund.emergencyFundMonths (capped at \"+12\")",
              "savingsAndExpenses.liquidityContext.emergencyFundInMonths",
              "protection.emergencyFund.emergencyFundCoverageEvaluation.monthsCovered"
            ],
            "notToBeConfusedWith": [
              "the recommended number of months"
            ]
          },
          "nearTermGoals": [
            {
              "note": "A goal payment, not a down payment unless the goal is a purchase.",
              "unit": "USD",
              "basis": "as entered",
              "label": "Take a vacation: cash to hold for its next payment",
              "value": 4500,
              "period": "next payment January 2027, then every year",
              "replaces": [
                "extraCashOutflows[].downpayment (holds any goal payment)"
              ]
            }
          ],
          "accessibleCash": {
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Accessible cash (bank accounts plus taxable money market)",
            "value": 19000,
            "period": "balance today",
            "notToBeConfusedWith": [
              "bank cash alone (excludes money market)",
              "cash inside retirement accounts, which is not accessible"
            ]
          },
          "totalCashNeeded": {
            "max": 124717.5,
            "min": 111360,
            "note": "Never call this the emergency reserve.",
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Cash target: emergency reserve plus near-term goals",
            "period": "target balance today",
            "replaces": [
              "ratios.emergencyFund.adjustedRecommendedMin/MaxAmount",
              "savingsAndExpenses.liquidityContext.min/maxEmergencyFundTargetAndShortTermNeeds",
              "cashNeeds.cashTarget"
            ],
            "notToBeConfusedWith": [
              "emergencyReserve"
            ]
          },
          "emergencyReserve": {
            "max": 120217.5,
            "min": 106860,
            "note": "Excludes near-term goals. This alone is the emergency reserve.",
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Recommended emergency reserve (8–9 months of essential expenses)",
            "period": "target balance today",
            "replaces": [
              "ratios.emergencyFund.min/maxRecommendedEmergencyFund",
              "savingsAndExpenses.liquidityContext.min/maxEmergencyFundTargetInCash",
              "protection.emergencyFund.recommendedEmergencyFundLevels.minimum/maximumAmountRecommended",
              "cashNeeds.emergencyFund"
            ],
            "notToBeConfusedWith": [
              "totalCashNeeded"
            ]
          },
          "monthsCoveredAfterNearTermGoals": {
            "unit": "months",
            "basis": "n/a",
            "label": "Months of essential expenses covered after setting aside near-term goals",
            "value": "1.1",
            "period": "today",
            "replaces": [
              "ratios.emergencyFund.adjustedMonthsCoveredAfterShortTermCashNeeds"
            ]
          }
        },
        "rules": [
          "These facts are the only figures to quote for these concepts. Quote the label's meaning with the number; never relabel a fact as another one.",
          "Each fact names the facts it must not be confused with. Never call one by the other's name.",
          "Keep the unit: a USD/yr figure is always said per year, a lump sum never is.",
          "Do not add, subtract or compare two facts unless a fact says how they relate.",
          "Never quote a date that is before the plan date.",
          "Write a date as month and year (August 2039), never as an ISO date (2039-08-01).",
          "Write a ratio or rate as a percentage (55%), never as a decimal (0.551).",
          "A fact's `replaces` lists key-metric fields that hold the same or a confusable figure under a misleading name. When you see one of those fields in your other inputs, quote the fact with its label instead. Field names are never labels."
        ],
        "education": {
          "fundingGap": {
            "note": "Not the amount to invest today and not the goal. It is larger than the total cost because college costs are inflated to the years they are paid.",
            "unit": "USD",
            "basis": "engine estimate: inflated college costs valued at college start, restated in today's dollars",
            "label": "College funding still needed beyond current 529 balances",
            "value": 106552.38,
            "period": "one lump sum for all college years",
            "notToBeConfusedWith": [
              "totalCostAllGoals",
              "combinedAnnualCost"
            ]
          },
          "totalCostPerGoal": [
            {
              "unit": "USD",
              "basis": "today's dollars at the plan date, before education inflation",
              "label": "College Oliver: total college cost, whole program",
              "value": 60000,
              "period": "4 years of college",
              "notToBeConfusedWith": [
                "annualCostPerGoal"
              ]
            },
            {
              "unit": "USD",
              "basis": "today's dollars at the plan date, before education inflation",
              "label": "College Sophia: total college cost, whole program",
              "value": 60000,
              "period": "4 years of college",
              "notToBeConfusedWith": [
                "annualCostPerGoal"
              ]
            }
          ],
          "annualCostPerGoal": [
            {
              "unit": "USD/yr",
              "basis": "today's dollars at the plan date",
              "label": "College Oliver: yearly college cost",
              "value": 15000,
              "period": "each year of college, 2033–2036 (4 payments); college starts August 2033, about 7 years from now",
              "replaces": [
                "listOfChildrenAndEducationGoals column \"Years to uni\" (rounded down)",
                "listOfChildrenAndEducationGoals column \"Education goal ($)\" (a yearly cost)",
                "protection.lifeInsurance.educationGoal column \"Total cost\" (a yearly cost)"
              ],
              "notToBeConfusedWith": [
                "totalCostPerGoal",
                "fundingGap"
              ]
            },
            {
              "unit": "USD/yr",
              "basis": "today's dollars at the plan date",
              "label": "College Sophia: yearly college cost",
              "value": 15000,
              "period": "each year of college, 2035–2038 (4 payments); college starts August 2035, about 9 years from now",
              "replaces": [
                "listOfChildrenAndEducationGoals column \"Years to uni\" (rounded down)",
                "listOfChildrenAndEducationGoals column \"Education goal ($)\" (a yearly cost)",
                "protection.lifeInsurance.educationGoal column \"Total cost\" (a yearly cost)"
              ],
              "notToBeConfusedWith": [
                "totalCostPerGoal",
                "fundingGap"
              ]
            }
          ],
          "extraYearlySaving": {
            "unit": "USD/yr",
            "basis": "engine estimate",
            "label": "Extra yearly saving needed for college (first year)",
            "value": 1927.57,
            "period": "per year from now until each child starts college, rising each year",
            "notToBeConfusedWith": [
              "annualCostPerGoal"
            ]
          },
          "totalCostAllGoals": {
            "note": "This is the education goal when one total is needed.",
            "unit": "USD",
            "basis": "today's dollars at the plan date, before education inflation",
            "label": "Total college cost, all children, whole programs",
            "value": 120000,
            "period": "all college years",
            "notToBeConfusedWith": [
              "fundingGap",
              "combinedAnnualCost"
            ]
          },
          "combinedAnnualCost": {
            "note": "Not the education goal and not a yearly household bill. Prefer per-child yearly costs; for one total use totalCostAllGoals.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Sum of each child's yearly college cost",
            "value": 30000,
            "period": "one year per child added together; their college years do not overlap",
            "replaces": [
              "assetsAndInvestments.educationGoalNeeds.educationGoalAmount",
              "savingsAndExpenses.goals.totalEducationGoalRequiredAmount",
              "ratios.educationSavings.totalEducationGoalsAmount"
            ]
          }
        },
        "retirement": {
          "spendingGap": {
            "note": "Savings, cash and required IRA withdrawals included, pay this each year on average. It is what the plan asks of savings.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Yearly retirement spending that income does not cover, paid from savings",
            "value": 62932.2,
            "period": "average over the 31 years of retirement",
            "notToBeConfusedWith": [
              "averagePortfolioDraw"
            ]
          },
          "spendingNeed": {
            "note": "Includes taxes, debt payments and goals after retirement; do not add those on top. annualTotalIncomeNeeded adds an estimated long-term care cost: do not quote it.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Yearly retirement spending need (excluding estimated long-term care)",
            "value": 124070.59,
            "period": "average over the 31 years of retirement",
            "replaces": [
              "retirementAndOtherGoals.incomeNeedsAndWithdrawals.annualTotalIncomeNeeded (adds estimated long-term care)"
            ]
          },
          "guaranteedIncome": {
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Guaranteed income in retirement (Social Security, annuities, pensions)",
            "value": 59465.61,
            "period": "average over the 31 years of retirement; years before a benefit starts count as zero"
          },
          "incomeShareOfNeed": {
            "unit": "percent",
            "basis": "today's dollars at the plan date",
            "label": "Share of the yearly retirement spending need that income covers (guaranteed and other income)",
            "value": "49%",
            "period": "average over the 31 years of retirement",
            "replaces": [
              "retirementAndOtherGoals.incomeVsIncomeNeeds.allIncomesVsIncomeNeededExLtcCosts",
              "ratios.guaranteedIncomeRatio.allIncomesVsIncomeNeededExLtcCosts"
            ]
          },
          "netCashFlowThisYear": {
            "note": "Income minus outflows for the plan year.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Net cash flow this year",
            "value": 15032.01,
            "period": "the plan year",
            "notToBeConfusedWith": [
              "averagePortfolioDraw",
              "withdrawalRateThisYear",
              "savingsCapacity"
            ]
          },
          "averagePortfolioDraw": {
            "note": "Counts only the months when spending exceeds every inflow. Required IRA withdrawals and other inflows drawn from savings are not in it, so savings pay more than this. Draws are concentrated in fewer years and are larger in those years. It is not the spending gap: never present it as filling that gap, and never use it to say the plan leans little on savings.",
            "unit": "USD/yr",
            "basis": "today's dollars at the plan date",
            "label": "Average yearly draw from savings in retirement",
            "value": 62932.2,
            "period": "average over the 31 years of retirement, counting years with no draw as zero",
            "replaces": [
              "retirementAndOtherGoals.withdrawals.supplementalAnnualWithdrawals"
            ],
            "notToBeConfusedWith": [
              "spendingGap"
            ]
          },
          "savingsLeftAtPlanEnd": {
            "unit": "USD",
            "basis": "today's dollars at the plan date",
            "label": "Savings and investments left at the end of the plan",
            "value": 260272.08,
            "period": "end of plan",
            "replaces": [
              "assetDepletion.liquidAssetsAtEndOfPlan",
              "capacity.liquidAssetsAtEndOfPlan"
            ]
          },
          "withdrawalRateAverage": {
            "note": "A lifetime average. Do not compare it with the 4% sustainable rate.",
            "unit": "percent",
            "basis": "today's dollars at the plan date",
            "label": "Average yearly draw as a share of savings at the start of retirement",
            "value": "5.5%",
            "period": "average over the 31 years of retirement",
            "replaces": [
              "retirementAndOtherGoals.withdrawals.withdrawalRatio"
            ],
            "notToBeConfusedWith": [
              "withdrawalRateThisYear"
            ]
          }
        }
      },
      "ratios": {
        "umbrella": {
          "claim": "No coverage",
          "color": "R",
          "currentCoverage": 0,
          "recommendedCoverage": 1000000
        },
        "currentDPD": {
          "debtLastPayment": "2047-08-01T00:00:00.000Z",
          "beforeRetirement": false,
          "yearsInRetirement": 3,
          "avgDTIInRetirement": 0.2725,
          "howMuchInRetirement": "Less than 5 years",
          "avgDTIInRetirementLevel": ">10%"
        },
        "vehiclePRI": {
          "vehiclesPri": 0.0266,
          "monthlyGrossIncome": 23333.33,
          "doTheyHaveAnyVehicle": true,
          "vehiclesMonthlyPayments": 620,
          "doTheyHaveAnyVehicleLoan": true,
          "vehiclesPriFirstThreshold": 0.1,
          "vehiclesPriSecondThreshold": 0.15
        },
        "debtToIncome": {
          "ratio": 0.2725,
          "debtOnlyDti": 0.2323,
          "grossIncome": 280000,
          "rentalPayment": 0,
          "mortgagesPayments": 49200,
          "monthlyDebtPayments": 5420,
          "otherHousingExpenses": 11250,
          "totalMonthlyObligations": 6357.5,
          "debtPaymentExcludingMortgages": 15840
        },
        "housingRatio": {
          "ratio": 0.2159,
          "grossIncome": 280000,
          "rentalPayment": 0,
          "housingExpenses": 60450,
          "mortgagePayment": 49200,
          "otherHousingExpenses": 11250
        },
        "indebtedness": {
          "debt": true,
          "housing": "own",
          "debtBalance": 618000,
          "monthlyDebtPayment": 5420,
          "totalMonthlyObligations": 6357.5
        },
        "savingsLevel": {
          "ratio": 0.0929,
          "grossIncome": 280000,
          "savingAmount": 26000
        },
        "emergencyFund": {
          "claim": "Vulnerable",
          "color": "R",
          "nrOfEarners": 2,
          "emergencyFund": 19000,
          "incomeDisparity": "Low",
          "monthlyExpenses": 13357.5,
          "totalCashAmount": 14000,
          "inaccessibleCash": 12000,
          "excessOverBaseMax": "Not applicable",
          "extraCashOutflows": [
            {
              "amount": 0,
              "description": "Take a vacation",
              "downpayment": 4500
            }
          ],
          "shortfallToBaseMin": 87860,
          "emergencyFundMonths": "1",
          "highestEarningsLevel": "High",
          "shortTermGoalsNeeded": [
            {
              "date": "2027-01-01T00:00:00.000Z",
              "amount": 4500,
              "description": "Take a vacation",
              "paymentFrequency": "ANNUAL"
            }
          ],
          "excessOverAdjustedMax": "Not applicable",
          "maxRecommendedEFMonths": 9,
          "minRecommendedEFMonths": 8,
          "shortfallToAdjustedMin": 92360,
          "totalMoneyMarketAmount": 5000,
          "deltaToMaxEmergencyFund": "Not applicable",
          "moneyMarketFundAccounts": [
            {
              "accountName": "Taxable Brokerage",
              "accountType": "Brokerage account",
              "cashBalance": 5000
            }
          ],
          "extraEmergencyFundNeeded": 4500,
          "maxRecommendedEmergencyFund": 120217.5,
          "maximumEmergencyFundPlusStg": 124717.5,
          "minRecommendedEmergencyFund": 106860,
          "adjustedRecommendedMaxAmount": 124717.5,
          "adjustedRecommendedMinAmount": 111360,
          "deltaToMaxEmergencyFundPlusStg": "Not applicable",
          "extraCashAboveMaxEmergencyFund": "Not applicable",
          "extraCashAboveMinEmergencyFund": "Not applicable",
          "cashReservesAfterShortTermCashNeeds": 14500,
          "extraCashAboveMaxEmergencyFundPlusStg": "Not applicable",
          "adjustedMonthsCoveredAfterShortTermCashNeeds": 1
        },
        "lifeInsurance": {
          "scenario": {
            "kids": true,
            "earners": 2,
            "spouses": 2,
            "scenario": 11,
            "debtBurden": "High",
            "incomeDisparity": "Low"
          },
          "clientEarner": {
            "overInsured": 18,
            "isHighEarner": true,
            "underInsured": 0,
            "adequatelyInsured": 10,
            "slightlyOverInsured": 15,
            "slightlyUnderInsured": 5
          },
          "clientCoverage": 250000,
          "coClientEarner": {
            "overInsured": 18,
            "isHighEarner": false,
            "underInsured": 0,
            "adequatelyInsured": 10,
            "slightlyOverInsured": 15,
            "slightlyUnderInsured": 5
          },
          "coClientCoverage": 200000,
          "clientCoverageKey": "Under insured",
          "clientEarnedIncome": 160000,
          "clientCoverageColor": "R",
          "coClientCoverageKey": "Under insured",
          "coClientEarnedIncome": 120000,
          "coClientCoverageColor": "R",
          "clientReplacementValue": 0,
          "clientCoverageOverIncome": 1.5625,
          "coClientReplacementValue": 0,
          "coClientCoverageOverIncome": 1.6667,
          "recommendedClientMaxCoverage": 2400000,
          "recommendedClientMinCoverage": 1600000,
          "recommendedCoClientMaxCoverage": 1800000,
          "recommendedCoClientMinCoverage": 1200000,
          "lifeInsuranceCoverageGapsAndExcess": {
            "clientExcess": 0,
            "coClientExcess": 0,
            "clientShortfall": 1350000,
            "coClientShortfall": 1000000
          }
        },
        "creditCardDebt": {
          "balance": 18000,
          "hasDebt": true,
          "ccPayoffDate": "2034-01-01T00:00:00.000Z",
          "monthlyPayment": 450,
          "retirementDate": "2044-05-01T00:00:00.000Z",
          "yearsInRetirement": "Not applicable",
          "maxCCPaymentNormal": 714.73,
          "minCCPaymentNormal": 527.27,
          "yearsToCcPayoffDate": 7,
          "paymentsEqualToInterest": 373.5,
          "percentageOfCCOverGrossIncome": 0.0643
        },
        "educationSavings": {
          "totalGAP": 106552.38,
          "goalsSummary": [
            {
              "date": "2033-08-01T00:00:00.000Z",
              "weight": 0.5407,
              "kidsAge": 11,
              "goalName": "College Oliver",
              "termDate": "2037-01-01T00:00:00.000Z",
              "totalGAP": 50742.14,
              "goalAmount": 15000,
              "yearsToStart": 6.75,
              "accountBalance": 16221.18,
              "accountSavings": 4325.65,
              "requiredSavings": 5621.29,
              "requiredExtraSavings": 1295.64,
              "goalRequiredAmountAtToday": 66963.32,
              "expectedCapitalizationAmount": 282.8
            },
            {
              "date": "2035-08-01T00:00:00.000Z",
              "weight": 0.4593,
              "kidsAge": 9,
              "goalName": "College Sophia",
              "termDate": "2039-01-01T00:00:00.000Z",
              "totalGAP": 55810.24,
              "goalAmount": 15000,
              "yearsToStart": 8.75,
              "accountBalance": 13778.82,
              "accountSavings": 3674.35,
              "requiredSavings": 4306.29,
              "requiredExtraSavings": 631.93,
              "goalRequiredAmountAtToday": 69589.06,
              "expectedCapitalizationAmount": 240.22
            }
          ],
          "savingsIncrease": 0.03,
          "expectedPerformance": 0.073,
          "totalRequiredSavings": 9927.57,
          "current529AccountsBalance": 30000,
          "totalEducationGoalsAmount": 30000,
          "totalRequiredExtraSavings": 1927.57,
          "annualSavingsGoingTo529Accounts": 8000,
          "doTheyHaveEducationFundingGoals": true,
          "totalEducationGoalRequiredAmountAtToday": 136552.38
        },
        "incomePercentile": {
          "state": "CO",
          "hasSpouse": true,
          "percentile": 0.9,
          "grossIncome": 280000
        },
        "realEstateEquity": {
          "ratio": 0.2533,
          "realEstateAssets": 750000,
          "realEstateEquity": 190000,
          "realEstateMortgages": 560000,
          "realEstateEquityThreshold1": 0.2,
          "realEstateEquityThreshold2": 0.5
        },
        "retirementSavings": {
          "generalInflation": 0.03,
          "yearsToRetirement": 17,
          "averagePerformance": 0.0758,
          "requiredExtraSavings": 34164.77,
          "planningGapAtRetirementAge": 4143863.42,
          "supplementalTotalWithdrawals": 5009033.85,
          "planningGapAtRetirementAgeInTodaysDollars": 1427455.89,
          "balanceInRetirementAccountsAtRetirementAge": 865170.44,
          "supplementalTotalWithdrawalsInTodaysDollars": 1950898.23,
          "balanceInRetirementAccountsAtRetirementAgeInTodaysDollars": 523442.34
        },
        "withdrawalRateRatio": {
          "withdrawalRate": 0.0833,
          "withdrawalRateToday": 0.01,
          "annualWithdrawalsToday": 3450.77,
          "annualWithdrawalsOnAverage": 161581.74,
          "withdrawalRateAtTodaysValue": 0.0549,
          "totalWithdrawalsDuringRetirement": 5009033.85,
          "investableAssetsAtFirstInRetireYrs": 1940092.95,
          "investableAssetsAt2050YrsAtTodaysValue": 1145560.64,
          "annualWithdrawalsOnAverageAtTodaysValue": 62932.2,
          "totalWithdrawalsDuringRetirementAtTodaysValue": 1950898.23
        },
        "investableAssetLevel": {
          "basis": "income",
          "ratio": 1.2286,
          "cashBalance": 14000,
          "grossIncome": 280000,
          "annualExpenses": 160290,
          "investableAssets": 330000,
          "portfolioSustainabilityMultiple": 1.2286
        },
        "guaranteedIncomeRatio": {
          "inflowsSummary": {
            "name": "All inflows",
            "total": 5571796.34,
            "guaranteedIncome": {
              "name": "Guaranteed income",
              "total": 5483644.49,
              "ANNUITY_INCOME": {
                "name": "Annuity income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "SOCIAL_SECURITY": {
                "name": "Social security",
                "total": 5483644.49,
                "totalAtTodaysValue": 1843433.78,
                "yearlyAverageTotal": 176891.76,
                "yearlyAverageTotalAtTodaysValue": 59465.61
              },
              "totalAtTodaysValue": 1843433.78,
              "yearlyAverageTotal": 176891.76,
              "PENSION_AND_DEFINED_BENEFIT": {
                "name": "Pension / defined benefit",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "yearlyAverageTotalAtTodaysValue": 59465.61
            },
            "otherIncomeSources": {
              "name": "Other income sources",
              "total": 88151.85,
              "STOCK_COMP": {
                "name": "Stock compensation",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "OTHER_INFLOW": {
                "name": "Other income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "DEFERRED_COMP": {
                "name": "Deferred compensation",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "EARNED_INCOME": {
                "name": "Earned income",
                "total": 88151.85,
                "totalAtTodaysValue": 51856.37,
                "yearlyAverageTotal": 2843.61,
                "yearlyAverageTotalAtTodaysValue": 1672.79
              },
              "RENTAL_INCOME": {
                "name": "Rental income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "ROYALTY_AND_IP": {
                "name": "Royalty & IP",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "SUPPORT_TRANSFER": {
                "name": "Support & transfer",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "GOVERNMENT_BENEFIT": {
                "name": "Government benefit",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "totalAtTodaysValue": 51856.37,
              "yearlyAverageTotal": 2843.61,
              "BUSINESS_PASSIVE_INCOME": {
                "name": "Business passive income",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "PROPERTY_LIQUIDATION_EVENT": {
                "name": "Property liquidation event",
                "total": 0,
                "totalAtTodaysValue": 0,
                "yearlyAverageTotal": 0,
                "yearlyAverageTotalAtTodaysValue": 0
              },
              "yearlyAverageTotalAtTodaysValue": 1672.79
            },
            "totalAtTodaysValue": 1895290.15,
            "yearlyAverageTotal": 179735.37,
            "yearlyAverageTotalAtTodaysValue": 61138.39
          },
          "outflowsSummary": {
            "name": "Outflows",
            "total": 14276828.65,
            "ltcCosts": {
              "name": "LTC Costs",
              "total": 3695998.45,
              "totalAtTodaysValue": 937589.97,
              "yearlyAverageTotal": 119225.76,
              "yearlyAverageTotalAtTodaysValue": 234397.49
            },
            "excludingLtcCosts": {
              "name": "Excluding LTC Costs",
              "total": 10580830.19,
              "totalAtTodaysValue": 3846188.37,
              "yearlyAverageTotal": 341317.1,
              "yearlyAverageTotalAtTodaysValue": 124070.59
            },
            "totalAtTodaysValue": 4783778.34,
            "yearlyAverageTotal": 460542.86,
            "yearlyAverageTotalAtTodaysValue": 154315.43
          },
          "ltcCostsAreEstimated": true,
          "allIncomesVsIncomeNeeded": 0.3962,
          "otherIncomeVsIncomeNeeded": 0.0108,
          "guaranteedIncomeVsIncomeNeeded": 0.3854,
          "allIncomesVsIncomeNeededExLtcCosts": 0.4928,
          "otherIncomeVsIncomeNeededExLtcCosts": 0.0135,
          "guaranteedIncomeVsIncomeNeededExLtcCosts": 0.4793
        }
      },
      "protection": {
        "emergencyFund": {
          "clientProfile": {
            "kids": [
              {
                "age": 11,
                "name": "Oliver"
              },
              {
                "age": 9,
                "name": "Sophia"
              }
            ],
            "clientAge": 44,
            "clientName": "Daniel",
            "coClientAge": 42,
            "coClientName": "Emily",
            "numberOfChildren": 2,
            "clientRiskProfile": "(4) Growth",
            "clientIncomeAtRisk": 160000,
            "coClientRiskProfile": "(3) Moderate",
            "coClientIncomeAtRisk": 120000
          },
          "cashAccountList": [
            {
              "name": "Checking account",
              "type": "Checking account",
              "owner": "Emily",
              "value": 5000
            },
            {
              "name": "Savings account",
              "type": "Savings account",
              "owner": "Emily",
              "value": 9000
            }
          ],
          "extraCashOutflows": [
            {
              "amount": 0,
              "description": "Take a vacation",
              "downpayment": 4500
            }
          ],
          "realEstateDetails": [
            [
              "Real estate",
              "Market value",
              "Mortgage balance",
              "Equity",
              "HELOC"
            ],
            [
              "Primary home",
              750000,
              560000,
              0.2533,
              0
            ]
          ],
          "cashAndExpensesOverview": {
            "cashReserves": 19000,
            "livingExpenses": 7000,
            "housingExpenses": 5037.5,
            "monthlyExpenses": 13357.5,
            "totalCashAmount": 19000,
            "otherDebtPayment": 1320,
            "totalMoneyMarketAmount": 5000,
            "cashReservesAfterShortTermCashNeeds": 14500
          },
          "otherAccountsContributions": [
            [
              "Account",
              "Holder",
              "Current contribution"
            ],
            [
              "Checking account",
              "Emily",
              0
            ],
            [
              "Savings account",
              "Emily",
              6000
            ],
            [
              "Taxable Brokerage",
              "Emily",
              12000
            ]
          ],
          "retirementAndEducationGaps": {
            "educationGap": 106552.38,
            "retirementGap": 1427455.89
          },
          "recommendedEmergencyFundLevels": {
            "maximumAmountRecommended": 120217.5,
            "maximumMonthsRecommended": 9,
            "minimumAmountRecommended": 106860,
            "minimumMonthsRecommended": 8,
            "extraEmergencyFundNeededByShortTermCashNeeds": 4500,
            "maximumAmountAdjustedAfterShortTermCashNeeds": 124717.5,
            "minimumAmountAdjustedAfterShortTermCashNeeds": 111360
          },
          "emergencyFundCoverageEvaluation": {
            "monthsCovered": 1,
            "emergencyFundExcess": "Not applicable",
            "emergencyFundShortfall": 87860,
            "adjustedMonthsCoveredAfterShortTermCashNeeds": 1,
            "adjustedEmergencyFundExcessAfterShortTermCashNeeds": "Not applicable",
            "adjustedEmergencyFundShortfallAfterShortTermCashNeeds": 92360
          },
          "taxAdvantagedAccountsContributions": [
            [
              "Account",
              "Holder",
              "Current contribution",
              "Max contribution"
            ],
            [
              "401(k) - Daniel",
              "Daniel",
              0,
              24500
            ],
            [
              "401(k) - Emily",
              "Emily",
              0,
              24500
            ],
            [
              "529 College Savings",
              "Emily",
              8000,
              0
            ]
          ]
        },
        "lifeInsurance": {
          "legacyGoal": {
            "amount": "Not applicable",
            "hasLegacyGoal": false
          },
          "educationGoal": [
            [
              "Kid name",
              "Total cost",
              "Inception Year"
            ],
            [
              "Oliver",
              15000,
              "2033"
            ],
            [
              "Sophia",
              15000,
              "2035"
            ]
          ],
          "clientDemographics": {
            "kids": [
              {
                "age": 11,
                "name": "Oliver"
              },
              {
                "age": 9,
                "name": "Sophia"
              }
            ],
            "clientAge": 44,
            "clientName": "Daniel",
            "coClientAge": 42,
            "coClientName": "Emily",
            "numberOfChildren": 2,
            "clientRiskProfile": "(4) Growth",
            "clientIncomeAtRisk": 160000,
            "coClientRiskProfile": "(3) Moderate",
            "coClientIncomeAtRisk": 120000
          },
          "lifeInsuranceCoverageBasics": {
            "hasLifeInsuranceClient": true,
            "hasLifeInsuranceCoClient": true,
            "lifeInsuranceAmountClient": 250000,
            "lifeInsuranceAmountCoClient": 200000
          },
          "lifeInsuranceCoverageGapsAndExcess": {
            "clientExcess": 0,
            "coClientExcess": 0,
            "clientShortfall": 1350000,
            "coClientShortfall": 1000000
          },
          "lifeInsuranceCoverageRecommendations": {
            "clientMaxRecommendedCoverage": 2400000,
            "clientMinRecommendedCoverage": 1600000,
            "coClientMaxRecommendedCoverage": 1800000,
            "coClientMinRecommendedCoverage": 1200000
          }
        },
        "umbrellaInsurance": {
          "assetExposed": {
            "netWorth": 511000,
            "totalLiquidAssets": 344000,
            "assetExposedSummary": [
              [
                "Asset",
                "Number",
                "Value",
                "Equity"
              ],
              [
                "Real estate",
                1,
                750000,
                190000
              ],
              [
                "Vehicle",
                1,
                35000,
                7000
              ],
              [
                "Total",
                2,
                785000,
                197000
              ]
            ]
          },
          "umbrellaCoverage": {
            "claim": "No coverage",
            "hasUmbrellaPolicy": false,
            "umbrellaCoverageAmount": "Not applicable"
          },
          "clientDemographics": {
            "kids": [
              {
                "age": 11,
                "name": "Oliver"
              },
              {
                "age": 9,
                "name": "Sophia"
              }
            ],
            "clientAge": 44,
            "clientName": "Daniel",
            "coClientAge": 42,
            "coClientName": "Emily",
            "numberOfChildren": 2,
            "clientRiskProfile": "(4) Growth",
            "clientIncomeAtRisk": 160000,
            "coClientRiskProfile": "(3) Moderate",
            "coClientIncomeAtRisk": 120000
          },
          "assetInsuranceStatus": [
            {
              "assetName": "Primary home",
              "assetType": "Real Estate",
              "isInsured": false,
              "equityAmount": 190000
            },
            {
              "assetName": "Toyota Highlander",
              "assetType": "Vehicle",
              "isInsured": false,
              "equityAmount": 7000
            }
          ],
          "coverageRecommendationsAndAnalysis": {
            "umbrellaCoverageGap": 1000000,
            "umbrellaCoverageExcess": "Not applicable",
            "umbrellaMinRecommendedCoverage": 1000000
          }
        }
      },
      "debtManagement": {
        "realEstate": {
          "realEstateEquity": 190000,
          "realEstateEquityThreshold1": 0.2,
          "realEstateEquityThreshold2": 0.5,
          "percentageOfRealEstateEquity": 0.2533
        },
        "listOfDebts": [
          [
            "Name",
            "Type",
            "Balance",
            "Interest rate",
            "Monthly payments",
            "Interest paid"
          ],
          [
            "Primary home mortgage",
            "Mortgage",
            560000,
            0.065,
            4100,
            3033.33
          ],
          [
            "Toyota Highlander loan",
            "Vehicle loan",
            28000,
            0.079,
            620,
            184.33
          ],
          [
            "Chase Sapphire",
            "Credit card",
            18000,
            0.249,
            450,
            373.5
          ],
          [
            "Student loan - Daniel",
            "Student loan",
            12000,
            0.052,
            250,
            52
          ]
        ],
        "debtOverview": {
          "debt": true,
          "debtBalance": 618000,
          "beforeRetirement": false,
          "avgDtiInRetirement": 0.2725,
          "percentageOfDebtOverGrossIncome": 2.2071
        },
        "clientProfile": {
          "clientName": "Daniel",
          "coClientName": "Emily"
        },
        "creditCardDebt": {
          "ccPayoffDate": "2034-01-01T00:00:00.000Z",
          "retirementDate": "2044-05-01T00:00:00.000Z",
          "ccMonthlyPayment": 450,
          "creditCardBalance": 18000,
          "yearsInRetirement": "Not applicable",
          "maxCcPaymentNormal": 714.73,
          "minCcPaymentNormal": 527.27,
          "yearsToCcPayoffDate": 7,
          "ccPaymentEqualToInterestRate": 373.5
        },
        "vehiclePayment": {
          "vehiclesPri": 0.0266,
          "doTheyHaveAnyVehicle": true,
          "vehiclesMonthlyPayments": 620
        },
        "housingExpenses": {
          "rentVsOwn": "Own",
          "housingRatio": 0.2159,
          "rentalPayment": 0,
          "housingExpenses": 5037.5,
          "mortgagePayment": 4100,
          "otherHousingExpenses": 937.5,
          "housingRatioFirstThreshold": 0.28,
          "housingRatioSecondThreshold": 0.32
        },
        "savingsAndCashflow": {
          "annualCashFlow": 15032.01,
          "annualSavingsRate": 0.0929,
          "annualSavingsAmount": 26000
        },
        "debtToIncomeAndMonthlyObligations": {
          "dti": 0.2725,
          "debtOnlyDti": 0.2323,
          "grossIncome": 280000,
          "dtiFirstThreshold": 0.36,
          "dtiThirdThreshold": 0.5,
          "dtiSecondThreshold": 0.43,
          "monthlyGrossIncome": 23333.33,
          "monthlyDebtPayments": 5420,
          "totalMonthlyObligations": 6357.5,
          "percentageOfDebtOverGrossIncome": 2.2071
        }
      },
      "cashflowStatement": {
        "inflows": {
          "items": [
            {
              "name": "Earned income",
              "items": [
                {
                  "name": "Salary and wages",
                  "joint": 0,
                  "total": 280000,
                  "client": 160000,
                  "coClient": 120000
                }
              ],
              "joint": 0,
              "total": 280000,
              "client": 160000,
              "coClient": 120000
            }
          ],
          "joint": 0,
          "total": 280000,
          "client": 160000,
          "coClient": 120000
        },
        "outflows": {
          "items": [
            {
              "name": "Expenses",
              "items": [
                {
                  "name": "Living Expenses",
                  "joint": 0,
                  "total": 84000,
                  "client": 84000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "total": 84000,
              "client": 84000,
              "coClient": 0
            },
            {
              "name": "Taxes",
              "items": [
                {
                  "name": "Federal Income Tax",
                  "joint": 44667.99,
                  "total": 44667.99,
                  "client": 0,
                  "coClient": 0
                },
                {
                  "name": "FICA tax",
                  "joint": 270,
                  "total": 21690,
                  "client": 12240,
                  "coClient": 9180
                },
                {
                  "name": "State Income Tax",
                  "joint": 12320,
                  "total": 12320,
                  "client": 0,
                  "coClient": 0
                }
              ],
              "joint": 57257.99,
              "total": 78677.99,
              "client": 12240,
              "coClient": 9180
            },
            {
              "name": "Housing Expenses",
              "items": [
                {
                  "name": "Mortgage",
                  "joint": 49200,
                  "total": 49200,
                  "client": 0,
                  "coClient": 0
                },
                {
                  "name": "Property Taxes",
                  "joint": 7500,
                  "total": 7500,
                  "client": 0,
                  "coClient": 0
                },
                {
                  "name": "Home Insurance",
                  "joint": 3750,
                  "total": 3750,
                  "client": 0,
                  "coClient": 0
                }
              ],
              "joint": 60450,
              "total": 60450,
              "client": 0,
              "coClient": 0
            },
            {
              "name": "Savings",
              "items": [
                {
                  "name": "Brokerage account savings",
                  "joint": 0,
                  "total": 12000,
                  "client": 0,
                  "coClient": 12000
                },
                {
                  "name": "529 - College Savings Plan savings",
                  "joint": 0,
                  "total": 8000,
                  "client": 0,
                  "coClient": 8000
                },
                {
                  "name": "Cash savings",
                  "joint": 0,
                  "total": 6000,
                  "client": 0,
                  "coClient": 6000
                }
              ],
              "joint": 0,
              "total": 26000,
              "client": 0,
              "coClient": 26000
            },
            {
              "name": "Debt Payments",
              "items": [
                {
                  "name": "Car loan payments",
                  "joint": 7440,
                  "total": 7440,
                  "client": 0,
                  "coClient": 0
                },
                {
                  "name": "Credit card payments",
                  "joint": 0,
                  "total": 5400,
                  "client": 5400,
                  "coClient": 0
                },
                {
                  "name": "Student loan payments",
                  "joint": 0,
                  "total": 3000,
                  "client": 3000,
                  "coClient": 0
                }
              ],
              "joint": 7440,
              "total": 15840,
              "client": 8400,
              "coClient": 0
            }
          ],
          "joint": 125147.99,
          "total": 264967.99,
          "client": 104640,
          "coClient": 35180
        },
        "freeCashflow": {
          "joint": -125147.99,
          "total": 15032.01,
          "client": 55360,
          "coClient": 84820
        }
      },
      "netWorthStatement": {
        "assets": {
          "name": "Assets",
          "type": "MAIN",
          "items": [
            {
              "name": "Cash account",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Savings account",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 9000,
                  "client": 0,
                  "coClient": 9000,
                  "annualSavings": 6000,
                  "clientSavings": 6000,
                  "annualMatching": 0,
                  "portfolioTypeName": "Savings account"
                },
                {
                  "name": "Checking account",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 5000,
                  "client": 0,
                  "coClient": 5000,
                  "annualSavings": 0,
                  "clientSavings": 0,
                  "annualMatching": 0,
                  "portfolioTypeName": "Checking account"
                }
              ],
              "joint": 0,
              "order": 1,
              "total": 14000,
              "client": 0,
              "coClient": 14000,
              "totalDebts": 0
            },
            {
              "name": "Investment account",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Taxable",
                  "type": "INDIVIDUAL",
                  "items": [
                    {
                      "name": "Taxable Brokerage",
                      "type": "PORTFOLIO",
                      "joint": 0,
                      "total": 50000,
                      "client": 0,
                      "coClient": 50000,
                      "annualSavings": 12000,
                      "clientSavings": 12000,
                      "annualMatching": 0,
                      "portfolioTypeName": "Brokerage account"
                    }
                  ],
                  "joint": 0,
                  "total": 50000,
                  "client": 0,
                  "coClient": 50000
                },
                {
                  "name": "Tax-free",
                  "type": "INDIVIDUAL",
                  "items": [
                    {
                      "name": "529 College Savings",
                      "type": "PORTFOLIO",
                      "joint": 0,
                      "total": 30000,
                      "client": 0,
                      "coClient": 30000,
                      "annualSavings": 8000,
                      "clientSavings": 8000,
                      "annualMatching": 0,
                      "portfolioTypeName": "529 - College Savings Plan"
                    }
                  ],
                  "joint": 0,
                  "total": 30000,
                  "client": 0,
                  "coClient": 30000
                },
                {
                  "name": "Tax-deferred",
                  "type": "INDIVIDUAL",
                  "items": [
                    {
                      "name": "401(k) - Daniel",
                      "type": "PORTFOLIO",
                      "joint": 0,
                      "total": 150000,
                      "client": 150000,
                      "coClient": 0,
                      "annualSavings": 0,
                      "clientSavings": 0,
                      "annualMatching": 0,
                      "portfolioTypeName": "401k - Traditional"
                    },
                    {
                      "name": "401(k) - Emily",
                      "type": "PORTFOLIO",
                      "joint": 0,
                      "total": 100000,
                      "client": 0,
                      "coClient": 100000,
                      "annualSavings": 0,
                      "clientSavings": 0,
                      "annualMatching": 0,
                      "portfolioTypeName": "401k - Traditional"
                    }
                  ],
                  "joint": 0,
                  "total": 250000,
                  "client": 150000,
                  "coClient": 100000
                }
              ],
              "joint": 0,
              "order": 2,
              "total": 330000,
              "client": 150000,
              "coClient": 180000,
              "totalDebts": 0
            },
            {
              "name": "Stock compensation",
              "type": "CATEGORY",
              "joint": 0,
              "order": 3,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Annuity",
              "type": "CATEGORY",
              "joint": 0,
              "order": 4,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Insurance (Cash value)",
              "type": "CATEGORY",
              "joint": 0,
              "order": 5,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Business",
              "type": "CATEGORY",
              "joint": 0,
              "order": 6,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true,
              "totalDebts": 0
            },
            {
              "name": "Real estate",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Primary home",
                  "type": "INDIVIDUAL",
                  "joint": 750000,
                  "total": 750000,
                  "client": 0,
                  "coClient": 0
                }
              ],
              "joint": 750000,
              "order": 7,
              "total": 750000,
              "client": 0,
              "coClient": 0,
              "totalDebts": 560000
            },
            {
              "name": "Vehicle",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Toyota Highlander",
                  "type": "INDIVIDUAL",
                  "joint": 35000,
                  "total": 35000,
                  "client": 0,
                  "coClient": 0
                }
              ],
              "joint": 35000,
              "order": 8,
              "total": 35000,
              "client": 0,
              "coClient": 0,
              "totalDebts": 28000
            },
            {
              "name": "Other asset",
              "type": "CATEGORY",
              "joint": 0,
              "order": 9,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "totalDebts": 0
            }
          ],
          "joint": 785000,
          "total": 1129000,
          "client": 150000,
          "coClient": 194000,
          "totalDebts": 588000
        },
        "netWorth": {
          "joint": 197000,
          "total": 511000,
          "client": 120000,
          "coClient": 194000
        },
        "liabilities": {
          "name": "Liabilities",
          "type": "MAIN",
          "items": [
            {
              "name": "Credit card",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Chase Sapphire",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 18000,
                  "client": 18000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 1,
              "total": 18000,
              "client": 18000,
              "coClient": 0
            },
            {
              "name": "Student loan",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Student loan - Daniel",
                  "type": "INDIVIDUAL",
                  "joint": 0,
                  "total": 12000,
                  "client": 12000,
                  "coClient": 0
                }
              ],
              "joint": 0,
              "order": 2,
              "total": 12000,
              "client": 12000,
              "coClient": 0
            },
            {
              "name": "Business loan",
              "type": "CATEGORY",
              "joint": 0,
              "order": 3,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true
            },
            {
              "name": "Personal loan",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Toyota Highlander loan",
                  "type": "INDIVIDUAL",
                  "joint": 28000,
                  "total": 28000,
                  "client": 0,
                  "coClient": 0
                }
              ],
              "joint": 28000,
              "order": 4,
              "total": 28000,
              "client": 0,
              "coClient": 0
            },
            {
              "name": "Investment loan",
              "type": "CATEGORY",
              "joint": 0,
              "order": 5,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true
            },
            {
              "name": "Real estate debt",
              "type": "CATEGORY",
              "items": [
                {
                  "name": "Primary home mortgage",
                  "type": "INDIVIDUAL",
                  "joint": 560000,
                  "total": 560000,
                  "client": 0,
                  "coClient": 0
                }
              ],
              "joint": 560000,
              "order": 6,
              "total": 560000,
              "client": 0,
              "coClient": 0
            },
            {
              "name": "Other debt",
              "type": "CATEGORY",
              "joint": 0,
              "order": 7,
              "total": 0,
              "client": 0,
              "coClient": 0,
              "_isHidden": true
            }
          ],
          "joint": 588000,
          "total": 618000,
          "client": 30000,
          "coClient": 0
        }
      },
      "savingsAndExpenses": {
        "goals": {
          "clientRetirementAge": 62,
          "coClientRetirementAge": 60,
          "shortTermGoalsCashNeeds": 4500,
          "doTheyHaveEducationFundingGoals": true,
          "totalEducationGoalRequiredAmount": 30000
        },
        "annualSavings": {
          "currentAnnualSavingsAtHSA": 0,
          "currentAnnualSavingsAtHSARate": 0,
          "currentAnnualSavingsAt529Accounts": 8000,
          "requiredRetirementExtraAnnualSavings": 34164.77,
          "currentAnnualSavingsAt529AccountsRate": 0.0286,
          "currentAnnualSavingsAtTaxableAccounts": 12000,
          "gapInRetirementAccountsAtRetirementAge": 1427455.89,
          "requiredAnnualSavingsAtTaxableAccounts": 12000,
          "requiredExtraAnnualSavingsForEducation": 1927.57,
          "currentAnnualSavingsAtRetirementAccounts": 0,
          "requiredRetirementExtraAnnualSavingsRate": 0.122,
          "currentAnnualSavingsAtTaxableAccountsRate": 0.0429,
          "requiredAnnualSavingsAtTaxableAccountsRate": 0.0429,
          "requiredExtraAnnualSavingsForEducationRate": 0.0069,
          "currentAnnualSavingsAtRetirementAccountsRate": 0
        },
        "clientProfile": {
          "clientAge": 44,
          "clientName": "Daniel",
          "coClientAge": 42,
          "coClientName": "Emily",
          "numberOfChildren": 2,
          "stateOfResidence": "Colorado",
          "clientRiskProfile": "(4) Growth",
          "coClientRiskProfile": "(3) Moderate",
          "maximumAgeOfChildren": 11,
          "minimumAgeOfChildren": 9
        },
        "otherExpenses": {
          "lifeInsuranceGap": 2350000,
          "umbrellaInsuranceGap": 1000000
        },
        "liquidityContext": {
          "shortTermNeeds": 4500,
          "emergencyFundInCash": 19000,
          "emergencyFundInMonths": "1",
          "maxEmergencyFundTargetInCash": 120217.5,
          "minEmergencyFundTargetInCash": 106860,
          "maxEmergencyFundTargetInMonths": 9,
          "minEmergencyFundTargetInMonths": 8,
          "gapWithRecommendedMinEmergencyFund": 87860,
          "excessWithRecommendedMaxEmergencyFund": "Not applicable",
          "maxEmergencyFundTargetAndShortTermNeeds": 124717.5,
          "minEmergencyFundTargetAndShortTermNeeds": 111360,
          "gapWithRecommendedMinEmergencyFundAndShortTermNeeds": 92360,
          "excessWithRecommendedMaxEmergencyFundAndShortTermNeeds": "Not applicable"
        },
        "advantagedSavings": {
          "hsaMaxContributions": 8750,
          "hsaClientCanContribute": true,
          "hsaClientContributions": 0,
          "client401kCanContribute": "Yes",
          "client401kContributions": 0,
          "hsaCoClientCanContribute": true,
          "hsaCoClientContributions": 0,
          "coClient401kCanContribute": "Yes",
          "coClient401kContributions": 0,
          "iraClientMaxContributions": 7500,
          "rothIraClientCanContribute": false,
          "rothIraClientContributions": 0,
          "iraCoClientMaxContributions": 7500,
          "rothIraCoClientCanContribute": false,
          "rothIraCoClientContributions": 0,
          "rothIraClientMaxContributions": 0,
          "rothIraCoClientMaxContributions": 0,
          "traditionalIraClientContributions": 0,
          "traditionalIraCoClientContributions": 0,
          "client401kContributionsMaxEmployerMatch": 9600,
          "coClient401kContributionsMaxEmployerMatch": 7200,
          "traditionalIraClientCanDeductContributions": false,
          "client401kContributionsCurrentEmployerMatch": 0,
          "traditionalIraCoClientCanDeductContributions": false,
          "coClient401kContributionsCurrentEmployerMatch": 0,
          "traditionalIraClientMaxDeductibleContributions": 0,
          "traditionalIraCoClientMaxDeductibleContributions": 0
        },
        "incomeAndCashflow": {
          "incomeSummary": [
            [
              "Category",
              "Value",
              "Percentage"
            ],
            [
              "Earned income - Client",
              160000,
              0.5714
            ],
            [
              "Earned income - Co-Client",
              120000,
              0.4286
            ],
            [
              "Total",
              280000,
              1
            ]
          ],
          "annualCashflow": 15032.01,
          "outflowSummary": [
            [
              "Category",
              "Value",
              "Percentage"
            ],
            [
              "Taxes",
              78677.99,
              0.281
            ],
            [
              "Debt Payments",
              15840,
              0.0566
            ],
            [
              "Housing Expenses",
              60450,
              0.2159
            ],
            [
              "Savings",
              26000,
              0.0929
            ],
            [
              "Expenses",
              84000,
              0.3
            ],
            [
              "Total",
              264967.99,
              0.9463
            ]
          ],
          "annualCashflowPercentage": 0.0537,
          "householdIncomePercentile": 0.9
        },
        "housingInformation": {
          "rentVsOwn": "Own",
          "rentalPayment": 0,
          "housingExpenses": 5037.5,
          "mortgagePayment": 4100,
          "otherHousingExpenses": 937.5
        },
        "debtRatiosAndHealth": {
          "dti": 0.2725,
          "housingRatio": 0.2159,
          "housingExpenses": 5037.5,
          "dtiFirstThreshold": 0.36,
          "dtiThirdThreshold": 0.5,
          "dtiSecondThreshold": 0.43,
          "totalMonthlyObligations": 6357.5,
          "housingRatioFirstThreshold": 0.28,
          "housingRatioSecondThreshold": 0.32,
          "percentageOfDebtOverGrossIncome": 2.2071
        },
        "shortTermGoalsNeeded": [
          {
            "date": "2027-01-01T00:00:00.000Z",
            "amount": 4500,
            "description": "Take a vacation",
            "paymentFrequency": "ANNUAL"
          }
        ]
      },
      "assetsAndInvestments": {
        "withdrawals": {
          "rmdStartAge": 75,
          "rmdStartYear": 2057,
          "coClientRmdStartAge": 75,
          "coClientRmdStartYear": 2059,
          "averageWithdrawalsDuringRmds": 45345.54,
          "yearsPayingMoreRmdsThanRequiredWithoutSavings": 0,
          "yearsPayingMoreRmdsThanRequiredWithCurrentSavings": 0
        },
        "listOfAssets": [
          [
            "Asset type",
            "Number of assets",
            "Asset value",
            "% of total assets",
            "Equity value",
            "% of Net worth"
          ],
          [
            "Cash account",
            2,
            14000,
            0.0124,
            14000,
            0.0259
          ],
          [
            "Investment account",
            4,
            330000,
            0.2923,
            330000,
            0.61
          ],
          [
            "Real estate",
            1,
            750000,
            0.6643,
            190000,
            0.3512
          ],
          [
            "Vehicle",
            1,
            35000,
            0.031,
            7000,
            0.0129
          ],
          [
            "Other asset",
            0,
            0,
            0,
            0,
            0
          ]
        ],
        "clientProfile": {
          "clientAge": 44,
          "clientName": "Daniel",
          "coClientAge": 42,
          "coClientName": "Emily",
          "clientRiskProfile": "(4) Growth",
          "clientRetirementAge": 62,
          "coClientRiskProfile": "(3) Moderate",
          "coClientRetirementAge": 60
        },
        "contributions": {
          "IRAContributions": [
            [
              "IRA contributions (Traditional + Roth)",
              "Client",
              "Co-Client"
            ],
            [
              "Max IRA contribution (Traditional + Roth)",
              7500,
              7500
            ],
            [
              "IRA catch-up (age 50+)",
              "Not applicable",
              "Not applicable"
            ],
            [
              "Total possible IRA contribution",
              7500,
              7500
            ],
            [
              "Roth IRA eligible amount (estimate)",
              "Not applicable",
              "Not applicable"
            ]
          ],
          "hsaContributions": {
            "catchUpForClient": "Not applicable",
            "maxContributions": 8750,
            "catchUpForCoClient": "Not applicable",
            "totalPossibleContribution": 8750
          },
          "employerPlanContributions": [
            [
              "Employer plan contributions (401k, 403b, etc)",
              "Client",
              "Co-Client"
            ],
            [
              "Max employee contribution",
              24500,
              24500
            ],
            [
              "Catch up (age 50+)",
              "Not applicable",
              "Not applicable"
            ],
            [
              "Super catch up (age 60-63)",
              "Not applicable",
              "Not applicable"
            ],
            [
              "Total possible employee contribution",
              24500,
              24500
            ]
          ]
        },
        "educationGoal": {
          "hasAnEducationGoal": true
        },
        "listOfAccounts": [
          [
            "Account",
            "Client",
            "Number",
            "Balance",
            "Annual contribution"
          ],
          [
            "401k - Traditional",
            "Daniel",
            1,
            150000,
            0
          ],
          [
            "401k - Traditional",
            "Emily",
            1,
            100000,
            0
          ],
          [
            "529 - College Savings Plan",
            "Emily",
            1,
            30000,
            8000
          ],
          [
            "Brokerage account",
            "Emily",
            1,
            50000,
            12000
          ],
          [
            "Cash/savings",
            "Emily",
            2,
            14000,
            6000
          ]
        ],
        "matchGapAnalysis": [
          {
            "holder": "client",
            "accountName": "401(k) - Daniel",
            "accountType": "401K",
            "grossSalary": 160000,
            "alertSuppressed": false,
            "currentAnnualMatch": 0,
            "fullMatchThreshold": 0,
            "activeContributions": false,
            "matchPolicyConfigured": false,
            "matchMaximizationStatus": "NOT_APPLICABLE"
          },
          {
            "holder": "coClient",
            "accountName": "401(k) - Emily",
            "accountType": "401K",
            "grossSalary": 120000,
            "alertSuppressed": false,
            "currentAnnualMatch": 0,
            "fullMatchThreshold": 0,
            "activeContributions": false,
            "matchPolicyConfigured": false,
            "matchMaximizationStatus": "NOT_APPLICABLE"
          }
        ],
        "incomeAndTaxation": {
          "taxRates": [
            [
              "Tax rate",
              "Current",
              "Expected at retirement"
            ],
            [
              "Federal ordinary tax rate",
              0.24,
              0.22
            ],
            [
              "State tax rate",
              0.044,
              0.044
            ],
            [
              "NIIT tax rate",
              0.038,
              0.038
            ],
            [
              "Effective ordinary tax rate",
              0.322,
              0.302
            ]
          ],
          "taxableIncome": {
            "totalTaxableIncome": 247799.96
          },
          "totalGrossIncome": 280000,
          "clientGrossIncome": 160000,
          "coClientGrossIncome": 120000
        },
        "educationGoalNeeds": {
          "current529Balance": 30000,
          "educationGoalAmount": 30000,
          "target529Contributions": 9927.57,
          "current529Contributions": 8000
        },
        "retirementGlidePath": {
          "retirementGlidePathForClient": "80% equity and 20% fixed income",
          "retirementGlideEquityForClient": 0.7999,
          "retirementGlidePathForCoClient": "80% equity and 20% fixed income",
          "retirementGlideEquityForCoClient": 0.7999,
          "retirementGlideFixedIncomeForClient": 0.2001,
          "retirementGlideFixedIncomeForCoClient": 0.2001
        },
        "totalAssetsAndEquity": {
          "totalAssets": 1129000,
          "totalEquity": 541000
        },
        "realEstateAndMortgage": {
          "mortgageBalance": 560000,
          "realEstateEquity": 0.2533,
          "realEstateEquityThreshold1": 0.2,
          "realEstateEquityThreshold2": 0.5
        },
        "listOfRealEstateAssets": [
          [
            "Real estate",
            "Value",
            "Debt amount",
            "Debt %",
            "Equity amount",
            "Equity %"
          ],
          [
            "Primary home",
            750000,
            560000,
            0.7467,
            190000,
            0.2533
          ]
        ],
        "percentageOfCashThreshold": 0.5,
        "listOfChildrenAndEducationGoals": [
          [
            "Student",
            "Age",
            "Education goal timeframe",
            "Years to uni",
            "Education goal ($)",
            "Target equity allocation in 529 account",
            "Target fixed income in 529 account"
          ],
          [
            "Oliver",
            11,
            "2033 - 2037",
            6,
            15000,
            0.5999,
            0.4001
          ],
          [
            "Sophia",
            9,
            "2035 - 2039",
            8,
            15000,
            0.7999,
            0.2001
          ]
        ]
      },
      "retirementAndOtherGoals": {
        "otherIncome": [
          [
            "Income source",
            "Total value",
            "Yearly average value"
          ],
          [
            "Earned income",
            51856.37,
            1672.79
          ],
          [
            "Total other income",
            51856.37,
            1672.79
          ]
        ],
        "withdrawals": {
          "withdrawalRatio": 0.0549,
          "supplementalTotalWithdrawals": 1950898.23,
          "supplementalAnnualWithdrawals": 62932.2
        },
        "clientProfile": {
          "clientAge": 44,
          "clientName": "Daniel",
          "coClientAge": 42,
          "coClientName": "Emily",
          "endOfPlanAge": 91,
          "clientRiskProfile": "(4) Growth",
          "clientRetirementAge": 62,
          "coClientRiskProfile": "(3) Moderate",
          "coClientRetirementAge": 60
        },
        "assetDepletion": {
          "netWorthAtEndOfPlan": 1011499.66,
          "requiredRetirementAge": "Not applicable",
          "liquidAssetsAtEndOfPlan": 260272.08,
          "shortfallInNumberOfYears": "Not applicable",
          "ageWhenTheyRunOutOfNetWorth": "Not applicable",
          "ageWhenTheyRunOutOfLiquidAssets": "Not applicable"
        },
        "guaranteedIncome": [
          [
            "Income source",
            "Total value",
            "Yearly average value"
          ],
          [
            "Social security",
            1843433.78,
            59465.61
          ],
          [
            "Annuity income",
            0,
            0
          ],
          [
            "Pension / defined benefit",
            0,
            0
          ],
          [
            "Total guaranteed income",
            1843433.78,
            59465.61
          ]
        ],
        "incomeVsIncomeNeeds": {
          "allIncomesVsIncomeNeeded": 0.3962,
          "otherIncomeVsIncomeNeeded": 0.0108,
          "guaranteedIncomeVsIncomeNeeded": 0.3854,
          "allIncomesVsIncomeNeededExLtcCosts": 0.4928,
          "otherIncomeVsIncomeNeededExLtcCosts": 0.0135,
          "guaranteedIncomeVsIncomeNeededExLtcCosts": 0.4793
        },
        "otherGoalsAndLegacy": {
          "legacyGoal": false,
          "legacyGoalGap": "Not applicable",
          "legacyGoalAmount": "Not applicable",
          "achievesLegacyGoals": "Not applicable",
          "otherGoalsAfterRetirement": false,
          "otherGoalsAfterRetirementAmount": 0
        },
        "netWorthAtRetirement": {
          "netWorthAtRetirementAge": 1812256.43,
          "liquidAssetsAtRetirementAge": 1142786.39,
          "nonLiquidAssetsAtRetirementAge": 669470.04
        },
        "incomeNeedsAndWithdrawals": {
          "totalLtcCosts": 937589.97,
          "annualLtcCosts": 234397.49,
          "totalIncomeNeeded": 4783778.34,
          "ltcCostsAreEstimated": true,
          "annualTotalIncomeNeeded": 154315.43,
          "totalIncomeNeededExLtcCosts": 3846188.37,
          "annualTotalIncomeNeededExLtcCosts": 124070.59
        }
      },
      "taxDragAnalysis": {
        "householdRollup": [
          [
            "Metric",
            "Value",
            "Notes"
          ],
          [
            "Total annual tax cost (Table 2)",
            658.65,
            "All taxable-account rows, including money-market positions."
          ],
          [
            "Money-market drag routed to Cash sub-task",
            0,
            "Money-market positions stay visible here but are carved out of the in-scope Tax Drag total."
          ],
          [
            "In-scope tax cost (Table 2 ex-MM)",
            658.65,
            "Standalone Tax Drag total after routing money-market drag to Cash."
          ],
          [
            "Total annual tax cost saved (Table 3)",
            210.89,
            "Permanent annual tax saved if those holdings were taxable today."
          ],
          [
            "Total annual tax cost deferred (Table 4)",
            3655.28,
            "Deferred, not eliminated; future withdrawals remain taxable on exit."
          ],
          [
            "NIIT contribution to Table 2",
            77.73,
            "Taxable net-investment components multiplied by the current NIIT rate."
          ]
        ],
        "accountTypeInputs": [
          [
            "#",
            "Account name",
            "Account type",
            "Tax treatment"
          ],
          [
            "1",
            "Checking account",
            "Checking account",
            "Taxable"
          ],
          [
            "2",
            "Savings account",
            "Savings account",
            "Taxable"
          ],
          [
            "3",
            "401(k) - Daniel",
            "401k - Traditional",
            "Tax deferred"
          ],
          [
            "4",
            "401(k) - Emily",
            "401k - Traditional",
            "Tax deferred"
          ],
          [
            "5",
            "529 College Savings",
            "529 - College Savings Plan",
            "Tax free"
          ],
          [
            "6",
            "Taxable Brokerage",
            "Brokerage account",
            "Taxable"
          ]
        ],
        "effectiveTaxMargin": [
          [
            "Component",
            "Rate",
            "Source / Trigger",
            "Applies to"
          ],
          [
            "Federal ordinary",
            "24%",
            "FH metrics — currentTaxBracket",
            "Ordinary income, ST cap gains, ST cap gain distributions, ordinary interest, non-qualified dividends"
          ],
          [
            "Federal LTCG",
            "15%",
            "PW-computed federal LTCG (2026 thresholds; taxable-income proxy)",
            "Qualified dividends, LT cap gains, LT cap gain distributions"
          ],
          [
            "State (CO)",
            "4.4%",
            "FH metrics — stateTaxRate (CO)",
            "All investment income (state rules)"
          ],
          [
            "NIIT",
            "3.8%",
            "Triggered: income $247,800 > $250K MFJ",
            "All net investment income"
          ],
          [
            "Total taxable income",
            "$247,800",
            "FH metrics — taxableIncome.totalTaxableIncome",
            "Debug input for LTCG and NIIT lookups"
          ],
          [
            "MAGI proxy",
            "$247,800",
            "Current tax-margin logic — reuse taxableIncome.totalTaxableIncome as MAGI proxy",
            "Debug input for NIIT and current LTCG threshold lookup"
          ],
          [
            "State input",
            "CO — Colorado",
            "PW params — state.code / state.name",
            "Debug input for state marginal-rate lookup"
          ],
          [
            "Expected retirement ordinary",
            "22%",
            "FH metrics — expectedTaxBracketInRetirement",
            "Future withdrawals from tax-deferred accounts"
          ],
          [
            "Effective ordinary rate",
            "32.2%",
            "24% + 4.4% + 3.8%",
            "Today's ordinary-rate income"
          ],
          [
            "Effective LTCG rate",
            "23.2%",
            "15% + 4.4% + 3.8%",
            "Today's LTCG-rate income"
          ]
        ],
        "fundHoldingsInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Morningstar category",
            "Balance",
            "Shares",
            "Estimated shares",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Interest income ($/share)",
            "Tax-free income ($/share)",
            "LT cap gain ($/share)",
            "ST cap gain ($/share)",
            "Ordinary-rate share (non-qual div + interest + ST cap gain) / total distribution",
            "Tax cost ratio",
            "Turnover",
            "PCGE"
          ],
          [
            "1",
            "Taxable Brokerage",
            "SCHP",
            "Inflation-Protected Bond",
            10000,
            390.78,
            "-",
            "$0",
            "$1.075",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "2",
            "Taxable Brokerage",
            "JNK",
            "High Yield Bond",
            15000,
            161.99,
            "-",
            "$0",
            "$6.358",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "3",
            "401(k) - Emily",
            "FSTDX",
            "Inflation-Protected Bond",
            18000,
            2465.75,
            "-",
            "$0",
            "$0.332",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "4",
            "401(k) - Emily",
            "Cash (USD)",
            "Money Market-Taxable",
            2000,
            2000,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "5",
            "Taxable Brokerage",
            "SCHD",
            "Large Value",
            20000,
            568.5,
            "-",
            "$0",
            "$1.048",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "6",
            "529 College Savings",
            "VWO",
            "Diversified Emerging Markets",
            25000,
            451.59,
            "-",
            "$0.168",
            "$1.329",
            "$0",
            "$0",
            "$0",
            "$0",
            "88.77%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "7",
            "401(k) - Daniel",
            "Cash (USD)",
            "Money Market-Taxable",
            5000,
            5000,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "8",
            "529 College Savings",
            "Cash (USD)",
            "Money Market-Taxable",
            5000,
            5000,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "9",
            "Taxable Brokerage",
            "Cash (USD)",
            "Money Market-Taxable",
            5000,
            5000,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "10",
            "401(k) - Daniel",
            "LQD",
            "Corporate Bond",
            55000,
            526.79,
            "-",
            "$0",
            "$4.938",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "11",
            "401(k) - Emily",
            "VWELX",
            "Moderate Allocation",
            80000,
            1735.73,
            "-",
            "$0.386",
            "$0.623",
            "$0",
            "$0",
            "$3.4",
            "$0.715",
            "26.12%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "12",
            "401(k) - Daniel",
            "VTI",
            "Large Blend",
            90000,
            248.71,
            "-",
            "$0.86",
            "$2.897",
            "$0",
            "$0",
            "$0",
            "$0",
            "77.11%",
            "[pending]",
            "[pending]",
            "[pending]"
          ]
        ],
        "stockHoldingsInputs": [
          [
            "#",
            "Account",
            "Name",
            "Ticker",
            "Sector",
            "Industry",
            "Country",
            "Balance",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Dividend yield TTM"
          ]
        ],
        "taxFreeAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable)",
            "Annual tax cost saved"
          ],
          [
            "1a",
            "529 College Savings",
            "VWO",
            25000,
            "Qualified dividend",
            75.95,
            "23.2%",
            17.62
          ],
          [
            "1b",
            "529 College Savings",
            "VWO",
            25000,
            "Non-qualified dividend",
            600.21,
            "32.2%",
            193.27
          ],
          [
            "1c",
            "529 College Savings",
            "VWO",
            25000,
            "Subtotal",
            676.17,
            "-",
            210.89
          ],
          [
            "2",
            "529 College Savings",
            "Cash (USD)",
            5000,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "Total",
            "Total tax-free",
            "-",
            30000,
            "-",
            676.17,
            "-",
            210.89
          ]
        ],
        "taxableAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate",
            "Annual tax cost"
          ],
          [
            "1",
            "Taxable Brokerage",
            "SCHP",
            10000,
            "Non-qualified dividend",
            419.93,
            "32.2%",
            135.22
          ],
          [
            "2",
            "Taxable Brokerage",
            "JNK",
            15000,
            "Non-qualified dividend",
            1030.01,
            "32.2%",
            331.66
          ],
          [
            "3",
            "Taxable Brokerage",
            "SCHD",
            20000,
            "Non-qualified dividend",
            595.57,
            "32.2%",
            191.77
          ],
          [
            "4",
            "Taxable Brokerage",
            "Cash (USD)",
            5000,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "Total",
            "Total taxable",
            "-",
            50000,
            "-",
            2045.51,
            "-",
            658.65
          ]
        ],
        "costBasisBlockingNotes": [
          [
            "Account",
            "Blocking note"
          ],
          [
            "Taxable Brokerage",
            "Implementation of Taxable Brokerage cannot be responsibly sequenced without tax-lot data."
          ]
        ],
        "taxableCostBasisInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Balance (market value)",
            "Cost basis",
            "Unrealized gain",
            "Holding period",
            "Notes"
          ],
          [
            "1",
            "Taxable Brokerage",
            "SCHP",
            10000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "2",
            "Taxable Brokerage",
            "JNK",
            15000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "3",
            "Taxable Brokerage",
            "SCHD",
            20000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "4",
            "Taxable Brokerage",
            "Cash (USD)",
            5000,
            5000,
            0,
            "N/A",
            "Money market — NAV $1.00, no embedded gain by design."
          ],
          [
            "Total",
            "Total taxable",
            "-",
            50000,
            "[missing cost basis]",
            "[missing cost basis]",
            "-",
            "Totals stay blocked until missing tax-lot inputs are filled."
          ]
        ],
        "taxDeferredAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable today)",
            "Annual tax cost deferred"
          ],
          [
            "1",
            "401(k) - Emily",
            "FSTDX",
            18000,
            "Non-qualified dividend",
            818.63,
            "32.2%",
            263.6
          ],
          [
            "2",
            "401(k) - Emily",
            "Cash (USD)",
            2000,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "3",
            "401(k) - Daniel",
            "Cash (USD)",
            5000,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "4",
            "401(k) - Daniel",
            "LQD",
            55000,
            "Non-qualified dividend",
            2601.14,
            "32.2%",
            837.57
          ],
          [
            "5a",
            "401(k) - Emily",
            "VWELX",
            80000,
            "Qualified dividend",
            670.43,
            "23.2%",
            155.54
          ],
          [
            "5b",
            "401(k) - Emily",
            "VWELX",
            80000,
            "Non-qualified dividend",
            1081.1,
            "32.2%",
            348.12
          ],
          [
            "5c",
            "401(k) - Emily",
            "VWELX",
            80000,
            "LT cap gain distribution",
            5900.92,
            "23.2%",
            1369.01
          ],
          [
            "5d",
            "401(k) - Emily",
            "VWELX",
            80000,
            "ST cap gain distribution",
            1241.77,
            "32.2%",
            399.85
          ],
          [
            "5e",
            "401(k) - Emily",
            "VWELX",
            80000,
            "Subtotal",
            8894.22,
            "-",
            2272.52
          ],
          [
            "6a",
            "401(k) - Daniel",
            "VTI",
            90000,
            "Qualified dividend",
            213.84,
            "23.2%",
            49.61
          ],
          [
            "6b",
            "401(k) - Daniel",
            "VTI",
            90000,
            "Non-qualified dividend",
            720.46,
            "32.2%",
            231.99
          ],
          [
            "6c",
            "401(k) - Daniel",
            "VTI",
            90000,
            "Subtotal",
            934.3,
            "-",
            281.6
          ],
          [
            "Total",
            "Total tax-deferred",
            "-",
            250000,
            "-",
            13248.29,
            "-",
            3655.28
          ]
        ],
        "componentTaxTreatmentMatrix": [
          [
            "Component",
            "Federal rate type",
            "Effective household rate today",
            "Taxable accounts",
            "Tax-free accounts",
            "Tax-deferred accounts",
            "Notes"
          ],
          [
            "Qualified dividend",
            "LTCG",
            "23.2%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for US common stock and treaty-country foreign names; funds keep the precomputed Morningstar qualified split."
          ],
          [
            "Non-qualified dividend",
            "ORDINARY",
            "32.2%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for REIT and non-treaty foreign names, while MLP distributions are treated as ROC; funds keep the precomputed Morningstar non-qualified split."
          ],
          [
            "Interest income",
            "ORDINARY",
            "32.2%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Money-market and bond-style fund income is treated as ordinary-rate income."
          ],
          [
            "Tax-free income",
            "Tax-exempt federal",
            "0%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Current phase assumes a 0% effective rate because state-specific muni exposure is not available in the data path."
          ],
          [
            "LT cap gain distribution",
            "LTCG",
            "23.2%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed long-term capital gains use the LTCG household rate."
          ],
          [
            "ST cap gain distribution",
            "ORDINARY",
            "32.2%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed short-term capital gains use the ordinary household rate."
          ]
        ]
      },
      "realEstate": {
        "realEstateEquity": 190000,
        "realEstateEquityThreshold1": 0.2,
        "realEstateEquityThreshold2": 0.5,
        "percentageOfRealEstateEquity": 0.2533
      },
      "savingsRate": null,
      "educationGoalNeeds": {
        "current529Balance": 30000,
        "educationGoalAmount": 30000,
        "target529Contributions": 9927.57,
        "current529Contributions": 8000
      }
    },
    "savingsWaterfall": [
      {
        "step": 1,
        "bucket": "Build minimum emergency threshold (3 months)",
        "current": 19000,
        "target": 40073,
        "status": "Partially filled",
        "delta": -21072,
        "flag": "",
        "notes": ""
      },
      {
        "step": 2,
        "bucket": "Address essential insurance gaps",
        "current": 450000,
        "target": 3800000,
        "status": "Partially filled",
        "delta": -3350000,
        "flag": "",
        "notes": ""
      },
      {
        "step": 3,
        "bucket": "Set aside cash for near-term goals",
        "current": 0,
        "target": 4500,
        "status": "Empty",
        "delta": -4500,
        "flag": "",
        "notes": ""
      },
      {
        "step": 4,
        "bucket": "Maximize employer match — primary plan",
        "current": 0,
        "target": 6400,
        "status": "Empty",
        "delta": -6400,
        "flag": "Estimated",
        "notes": ""
      },
      {
        "step": 5,
        "bucket": "Maximize employer match — secondary plan",
        "current": 0,
        "target": 4800,
        "status": "Empty",
        "delta": -4800,
        "flag": "Estimated",
        "notes": ""
      },
      {
        "step": 6,
        "bucket": "Maximize HSA match",
        "current": "N/A",
        "target": "",
        "status": ""
      },
      {
        "step": 7,
        "bucket": "Maximize ESPP (Employee Stock Purchase Plan)",
        "current": "N/A",
        "target": "",
        "status": ""
      },
      {
        "step": 8,
        "bucket": "Pay high-interest debt (>7%)",
        "current": 46000,
        "target": 0,
        "status": "Empty",
        "delta": 46000,
        "flag": "",
        "notes": ""
      },
      {
        "step": 9,
        "bucket": "Build toward maximum emergency threshold (6 months)",
        "current": 14500,
        "target": 80145,
        "status": "Empty",
        "delta": -65645,
        "flag": "",
        "notes": ""
      },
      {
        "step": 10,
        "bucket": "Contribute to Roth IRA",
        "current": 0,
        "target": "N/A",
        "status": "",
        "delta": ""
      },
      {
        "step": 11,
        "bucket": "Maximize HSA",
        "current": 0,
        "target": 8750,
        "status": "Empty",
        "delta": -8750,
        "flag": "",
        "notes": ""
      },
      {
        "step": 12,
        "bucket": "Contribute to 529 accounts",
        "current": 8000,
        "target": 1928,
        "status": "Filled",
        "delta": 6072,
        "flag": "",
        "notes": ""
      },
      {
        "step": 13,
        "bucket": "Maximize 401k / employer plans",
        "current": 0,
        "target": 49000,
        "status": "Empty",
        "delta": -49000,
        "flag": "",
        "notes": ""
      },
      {
        "step": 14,
        "bucket": "Invest in taxable brokerage",
        "current": 12000,
        "target": "N/A",
        "status": "",
        "delta": ""
      },
      {
        "step": 15,
        "bucket": "Pay low-interest debt (personal, auto)",
        "current": 0,
        "target": "N/A",
        "status": "",
        "delta": ""
      },
      {
        "step": 16,
        "bucket": "Make extra mortgage payments",
        "current": 560000,
        "target": "N/A",
        "status": "",
        "delta": ""
      }
    ],
    "shocks": [
      {
        "assetClassesAffected": [
          "US Treasuries",
          "US equities",
          "USD",
          "rate-sensitive sectors"
        ],
        "dateLabel": "2023-07-26",
        "description": "The Fed raised rates 25bp to 5.25–5.50%, the 11th and final hike in the cycle — the highest level in 22 years. The Fed held here for 14 months before cutting in September 2024.",
        "duration": "Extended",
        "endDate": "2024-09-17",
        "impactDirection": "Rates-driven",
        "name": "Fed final hike to 5.25–5.50%",
        "portfolioImpact": "Mixed",
        "severity": "High",
        "startDate": "2023-07-23",
        "type": "Fed/Macro",
        "drawdown": {
          "severity": "major",
          "eventDate": "2023-07-26",
          "household": {
            "drawdownPct": -0.0385,
            "recoveryDays": 11,
            "returnDuringPct": 0.217
          },
          "windowEnd": "2024-09-17",
          "eventTitle": "Fed final hike to 5.25–5.50%",
          "windowStart": "2023-07-23",
          "divergencePp": 0.0026,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0411,
            "recoveryDays": 11,
            "returnDuringPct": 0.2354
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "US Treasuries",
          "small caps",
          "USD",
          "rate-sensitive sectors"
        ],
        "dateLabel": "2023-12-13",
        "description": "Fed held rates steady but the dot plot signaled 75bp of cuts in 2024, marking a decisive pivot. S&P 500 surged to new highs; Russell 2000 +4%. Long-end yields fell sharply. Catalyzed a broad year-end rally across equities and bonds.",
        "duration": "Extended",
        "endDate": "2024-03-31",
        "impactDirection": "Risk-on equity",
        "name": "Fed pivot — December 2023 dot plot",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2023-12-10",
        "type": "Fed/Macro",
        "drawdown": {
          "severity": "major",
          "eventDate": "2023-12-13",
          "household": {
            "drawdownPct": -0.0151,
            "recoveryDays": 7,
            "returnDuringPct": 0.0749
          },
          "windowEnd": "2024-03-31",
          "eventTitle": "Fed pivot — December 2023 dot plot",
          "windowStart": "2023-12-10",
          "divergencePp": 0.0018,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0169,
            "recoveryDays": 17,
            "returnDuringPct": 0.0837
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "Japanese equities",
          "EM",
          "global equities",
          "USD/JPY"
        ],
        "dateLabel": "2024-08-05",
        "description": "Yen carry trade unwind and US recession fears triggered a global rout. Japan's TOPIX fell 12.3% — worst since 1987 Black Monday. VIX spiked above 65 intraday. S&P 500 fell ~3% at the open but recovered most losses by Friday. The episode lasted one week.",
        "duration": "Immediate (days)",
        "endDate": "2024-08-09",
        "impactDirection": "Risk-off equity",
        "name": "Global selloff — VIX spikes above 60",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2024-07-31",
        "type": "Market",
        "drawdown": {
          "severity": "major",
          "eventDate": "2024-08-05",
          "household": {
            "drawdownPct": -0.0309,
            "returnDuringPct": -0.0155
          },
          "windowEnd": "2024-08-09",
          "eventTitle": "Global selloff — VIX spikes above 60",
          "windowStart": "2024-07-31",
          "divergencePp": 0.0013,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0323,
            "returnDuringPct": -0.0161
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "US Treasuries",
          "USD",
          "EM",
          "rate-sensitive sectors"
        ],
        "dateLabel": "2024-09-18",
        "description": "First Fed rate cut in four years, and an outsized 50bp move, formally marking the start of the easing cycle. Signaled the Fed's confidence that inflation was heading sustainably toward 2% and opened the door to subsequent cuts.",
        "duration": "Extended",
        "endDate": "2024-12-18",
        "impactDirection": "Risk-on equity",
        "name": "Fed first rate cut — 50bp",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2024-09-15",
        "type": "Fed/Macro",
        "drawdown": {
          "severity": "major",
          "eventDate": "2024-09-18",
          "household": {
            "drawdownPct": -0.0282,
            "returnDuringPct": 0.007
          },
          "windowEnd": "2024-12-18",
          "eventTitle": "Fed first rate cut — 50bp",
          "windowStart": "2024-09-15",
          "divergencePp": 0.0007,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0289,
            "returnDuringPct": 0.0141
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "small caps",
          "financials",
          "USD",
          "crypto"
        ],
        "dateLabel": "2024-11-05",
        "description": "Trump defeated Kamala Harris decisively. S&P 500 surged 2.5%, Dow +3.6%, Russell 2000 +5.8%. The \"Trump trade\" lifted banks, small caps, and crypto on expectations of deregulation and tax cuts. USD strengthened sharply.",
        "duration": "Short",
        "endDate": "2024-11-19",
        "impactDirection": "Risk-on equity",
        "name": "Trump election win",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2024-11-05",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2024-11-05",
          "household": {
            "drawdownPct": -0.0175,
            "returnDuringPct": 0.0073
          },
          "windowEnd": "2024-11-19",
          "eventTitle": "Trump election win",
          "windowStart": "2024-11-05",
          "divergencePp": -0.0018,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0156,
            "returnDuringPct": 0.0131
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities (tech/semis)",
          "Nvidia",
          "AI-linked names"
        ],
        "dateLabel": "2025-01-27",
        "description": "Chinese startup DeepSeek released an open-source AI model rivaling GPT-4 at a fraction of the cost, questioning the US AI capex thesis. Nvidia lost $589B in market value — the largest single-day loss for any stock in history. Nasdaq fell 3.1%, S&P 500 fell 1.5%.",
        "duration": "Immediate (days)",
        "endDate": "2025-01-30",
        "impactDirection": "Sector-specific",
        "name": "DeepSeek AI shock",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2025-01-27",
        "type": "Tech/AI",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-01-27",
          "household": {
            "drawdownPct": -0.0025,
            "recoveryDays": 0,
            "returnDuringPct": 0.0048
          },
          "windowEnd": "2025-01-30",
          "eventTitle": "DeepSeek AI shock",
          "windowStart": "2025-01-27",
          "divergencePp": 0.0001,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0026,
            "recoveryDays": 0,
            "returnDuringPct": 0.006
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "EM",
          "USD",
          "US Treasuries"
        ],
        "dateLabel": "2025-04-02",
        "description": "Trump announced sweeping reciprocal tariffs (10% baseline, 34% on China, 20% on EU, 46% on Vietnam) — the highest US tariff level since 1909. S&P 500 lost 10% in two days — the worst two-day loss in history ($6.6T erased). Long-end yields spiked on bond vigilante concerns.",
        "duration": "Short",
        "endDate": "2025-04-09",
        "impactDirection": "Risk-off equity",
        "name": "Liberation Day tariffs announced",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2025-04-02",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-04-02",
          "household": {
            "drawdownPct": -0.0808,
            "returnDuringPct": -0.0319
          },
          "windowEnd": "2025-04-09",
          "eventTitle": "Liberation Day tariffs announced",
          "windowStart": "2025-04-02",
          "divergencePp": -0.0031,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0777,
            "returnDuringPct": -0.0242
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "US Treasuries",
          "USD"
        ],
        "dateLabel": "2025-04-09",
        "description": "After the S&P 500 fell 10% in two days post-Liberation Day, Trump announced a 90-day pause on reciprocal tariffs above 10% for all countries except China (raised to 125%). S&P 500 surged 9.52% — its largest single-day gain since 2008. Nasdaq jumped 12.16%. Record 30B shares traded.",
        "duration": "Short",
        "endDate": "2025-04-22",
        "impactDirection": "Risk-on equity",
        "name": "90-day tariff pause rally",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2025-04-09",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-04-09",
          "household": {
            "drawdownPct": -0.0232,
            "returnDuringPct": -0.0092
          },
          "windowEnd": "2025-04-22",
          "eventTitle": "90-day tariff pause rally",
          "windowStart": "2025-04-09",
          "divergencePp": 0.0079,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0311,
            "returnDuringPct": -0.0161
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "EM",
          "USD",
          "tech",
          "retail"
        ],
        "dateLabel": "2025-05-12",
        "description": "After two days of talks in Geneva, the US and China agreed to reduce reciprocal tariffs from 125% to 10% for 90 days. S&P 500 surged 3.3%, Nasdaq +4.4%. Apple and Amazon led gains as the deal eased supply-chain fears for import-dependent tech and retail sectors.",
        "duration": "Short",
        "endDate": "2025-05-19",
        "impactDirection": "Risk-on equity",
        "name": "US-China Geneva tariff truce",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2025-05-11",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2025-05-12",
          "household": {
            "drawdownPct": -0.0009,
            "recoveryDays": 0,
            "returnDuringPct": 0.0111
          },
          "windowEnd": "2025-05-19",
          "eventTitle": "US-China Geneva tariff truce",
          "windowStart": "2025-05-11",
          "divergencePp": -0.0001,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0007,
            "recoveryDays": 0,
            "returnDuringPct": 0.0116
          }
        }
      },
      {
        "assetClassesAffected": [
          "US equities",
          "international equities",
          "USD",
          "imports-sensitive sectors"
        ],
        "dateLabel": "2026-02-01",
        "description": "The Supreme Court affirmed that the Trump administration's use of emergency powers to impose the April 2025 reciprocal tariffs was unlawful, formally unwinding the tariff regime's legal basis. (Exact date to verify on next run.)",
        "duration": "Extended",
        "endDate": "2026-02-28",
        "impactDirection": "Risk-on equity",
        "name": "Supreme Court strikes down Liberation Day tariffs",
        "portfolioImpact": "Positive",
        "severity": "High",
        "startDate": "2026-02-01",
        "type": "Policy",
        "drawdown": {
          "severity": "major",
          "eventDate": "2026-02-01",
          "household": {
            "drawdownPct": -0.0084,
            "returnDuringPct": 0.0056
          },
          "windowEnd": "2026-02-28",
          "eventTitle": "Supreme Court strikes down Liberation Day tariffs",
          "windowStart": "2026-02-01",
          "divergencePp": 0.0039,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0123,
            "returnDuringPct": 0.0007
          }
        }
      },
      {
        "assetClassesAffected": [
          "Crude oil",
          "US equities",
          "international equities",
          "defense stocks",
          "US Treasuries"
        ],
        "dateLabel": "2026-02-28",
        "description": "US and Israel launched coordinated airstrikes on Iranian military and nuclear sites, with nearly 900 strikes in the first 12 hours. Iranian leadership was decapitated. Brent crude surged 10–13% immediately; global equity markets sold off sharply on escalation and energy-supply fears.",
        "duration": "Extended",
        "endDate": "2026-03-04",
        "impactDirection": "Risk-off equity",
        "name": "Operation Epic Fury — US-Israel strikes on Iran",
        "portfolioImpact": "Negative",
        "severity": "High",
        "startDate": "2026-02-28",
        "type": "Geopolitical",
        "drawdown": {
          "severity": "major",
          "eventDate": "2026-02-28",
          "household": {
            "drawdownPct": -0.0074,
            "returnDuringPct": -0.0042
          },
          "windowEnd": "2026-03-04",
          "eventTitle": "Operation Epic Fury — US-Israel strikes on Iran",
          "windowStart": "2026-02-28",
          "divergencePp": -0.0015,
          "sameRiskBenchmark": {
            "drawdownPct": -0.0059,
            "returnDuringPct": -0.0021
          }
        }
      }
    ],
    "performanceSummary": {
      "maxDrawdown3y": -0.0997,
      "maxDrawdownRecoveryDays": 61,
      "benchmark": {
        "sharpe3y": 1.2824,
        "blendCash": 0.0966,
        "blendEquity": 0.5435,
        "volatility3y": 0.0857,
        "maxDrawdown3y": -0.1055,
        "blendFixedIncome": 0.3599,
        "return1yAnnualized": 0.0689,
        "return3yAnnualized": 0.1458,
        "return3yCumulative": 0.5049
      },
      "assetAllocation": {
        "currentEF": {
          "equity": 0.5435,
          "fixedIncome": 0.4565
        },
        "currentEFC": {
          "cash": 0.0966,
          "equity": 0.5435,
          "fixedIncome": 0.3599
        },
        "targetEF": {
          "equity": 0.663,
          "fixedIncome": 0.337
        },
        "targetEFC": {
          "cash": 0.0624,
          "equity": 0.663,
          "fixedIncome": 0.2747
        }
      },
      "concentration": {
        "topSectorPct": 0.3224,
        "topSectorName": "Technology",
        "isMaterialConcentration": true
      },
      "positions": [
        {
          "account": "Taxable Brokerage",
          "ticker": "JNK",
          "name": "SPDR Bloomberg High Yield Bond ETF",
          "type": "ETF",
          "category": "High Yield Bond",
          "value": 15000,
          "weight_in_account": 0.3,
          "expense_ratio": 0.004
        },
        {
          "account": "401(k) - Daniel",
          "ticker": "VTI",
          "name": "Vanguard Morningstar Total Stock Market ETF",
          "type": "ETF",
          "category": "Large Blend",
          "value": 90000,
          "weight_in_account": 0.6,
          "expense_ratio": 0.0003
        }
      ],
      "taxDragAnalysis": {
        "householdRollup": [
          [
            "Metric",
            "Value",
            "Notes"
          ],
          [
            "Total annual tax cost (Table 2)",
            658.65,
            "All taxable-account rows, including money-market positions."
          ],
          [
            "Money-market drag routed to Cash sub-task",
            0,
            "Money-market positions stay visible here but are carved out of the in-scope Tax Drag total."
          ],
          [
            "In-scope tax cost (Table 2 ex-MM)",
            658.65,
            "Standalone Tax Drag total after routing money-market drag to Cash."
          ],
          [
            "Total annual tax cost saved (Table 3)",
            210.89,
            "Permanent annual tax saved if those holdings were taxable today."
          ],
          [
            "Total annual tax cost deferred (Table 4)",
            3655.28,
            "Deferred, not eliminated; future withdrawals remain taxable on exit."
          ],
          [
            "NIIT contribution to Table 2",
            77.73,
            "Taxable net-investment components multiplied by the current NIIT rate."
          ]
        ],
        "accountTypeInputs": [
          [
            "#",
            "Account name",
            "Account type",
            "Tax treatment"
          ],
          [
            "1",
            "Checking account",
            "Checking account",
            "Taxable"
          ],
          [
            "2",
            "Savings account",
            "Savings account",
            "Taxable"
          ],
          [
            "3",
            "401(k) - Daniel",
            "401k - Traditional",
            "Tax deferred"
          ],
          [
            "4",
            "401(k) - Emily",
            "401k - Traditional",
            "Tax deferred"
          ],
          [
            "5",
            "529 College Savings",
            "529 - College Savings Plan",
            "Tax free"
          ],
          [
            "6",
            "Taxable Brokerage",
            "Brokerage account",
            "Taxable"
          ]
        ],
        "effectiveTaxMargin": [
          [
            "Component",
            "Rate",
            "Source / Trigger",
            "Applies to"
          ],
          [
            "Federal ordinary",
            "24%",
            "FH metrics — currentTaxBracket",
            "Ordinary income, ST cap gains, ST cap gain distributions, ordinary interest, non-qualified dividends"
          ],
          [
            "Federal LTCG",
            "15%",
            "PW-computed federal LTCG (2026 thresholds; taxable-income proxy)",
            "Qualified dividends, LT cap gains, LT cap gain distributions"
          ],
          [
            "State (CO)",
            "4.4%",
            "FH metrics — stateTaxRate (CO)",
            "All investment income (state rules)"
          ],
          [
            "NIIT",
            "3.8%",
            "Triggered: income $247,800 > $250K MFJ",
            "All net investment income"
          ],
          [
            "Total taxable income",
            "$247,800",
            "FH metrics — taxableIncome.totalTaxableIncome",
            "Debug input for LTCG and NIIT lookups"
          ],
          [
            "MAGI proxy",
            "$247,800",
            "Current tax-margin logic — reuse taxableIncome.totalTaxableIncome as MAGI proxy",
            "Debug input for NIIT and current LTCG threshold lookup"
          ],
          [
            "State input",
            "CO — Colorado",
            "PW params — state.code / state.name",
            "Debug input for state marginal-rate lookup"
          ],
          [
            "Expected retirement ordinary",
            "22%",
            "FH metrics — expectedTaxBracketInRetirement",
            "Future withdrawals from tax-deferred accounts"
          ],
          [
            "Effective ordinary rate",
            "32.2%",
            "24% + 4.4% + 3.8%",
            "Today's ordinary-rate income"
          ],
          [
            "Effective LTCG rate",
            "23.2%",
            "15% + 4.4% + 3.8%",
            "Today's LTCG-rate income"
          ]
        ],
        "fundHoldingsInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Morningstar category",
            "Balance",
            "Shares",
            "Estimated shares",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Interest income ($/share)",
            "Tax-free income ($/share)",
            "LT cap gain ($/share)",
            "ST cap gain ($/share)",
            "Ordinary-rate share (non-qual div + interest + ST cap gain) / total distribution",
            "Tax cost ratio",
            "Turnover",
            "PCGE"
          ],
          [
            "1",
            "Taxable Brokerage",
            "SCHP",
            "Inflation-Protected Bond",
            10000,
            390.78,
            "-",
            "$0",
            "$1.075",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "2",
            "Taxable Brokerage",
            "JNK",
            "High Yield Bond",
            15000,
            161.99,
            "-",
            "$0",
            "$6.358",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "3",
            "401(k) - Emily",
            "FSTDX",
            "Inflation-Protected Bond",
            18000,
            2465.75,
            "-",
            "$0",
            "$0.332",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "4",
            "401(k) - Emily",
            "Cash (USD)",
            "Money Market-Taxable",
            2000,
            2000,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "5",
            "Taxable Brokerage",
            "SCHD",
            "Large Value",
            20000,
            568.5,
            "-",
            "$0",
            "$1.048",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "6",
            "529 College Savings",
            "VWO",
            "Diversified Emerging Markets",
            25000,
            451.59,
            "-",
            "$0.168",
            "$1.329",
            "$0",
            "$0",
            "$0",
            "$0",
            "88.77%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "7",
            "401(k) - Daniel",
            "Cash (USD)",
            "Money Market-Taxable",
            5000,
            5000,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "8",
            "529 College Savings",
            "Cash (USD)",
            "Money Market-Taxable",
            5000,
            5000,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "9",
            "Taxable Brokerage",
            "Cash (USD)",
            "Money Market-Taxable",
            5000,
            5000,
            "-",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "10",
            "401(k) - Daniel",
            "LQD",
            "Corporate Bond",
            55000,
            526.79,
            "-",
            "$0",
            "$4.938",
            "$0",
            "$0",
            "$0",
            "$0",
            "100%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "11",
            "401(k) - Emily",
            "VWELX",
            "Moderate Allocation",
            80000,
            1735.73,
            "-",
            "$0.386",
            "$0.623",
            "$0",
            "$0",
            "$3.4",
            "$0.715",
            "26.12%",
            "[pending]",
            "[pending]",
            "[pending]"
          ],
          [
            "12",
            "401(k) - Daniel",
            "VTI",
            "Large Blend",
            90000,
            248.71,
            "-",
            "$0.86",
            "$2.897",
            "$0",
            "$0",
            "$0",
            "$0",
            "77.11%",
            "[pending]",
            "[pending]",
            "[pending]"
          ]
        ],
        "stockHoldingsInputs": [
          [
            "#",
            "Account",
            "Name",
            "Ticker",
            "Sector",
            "Industry",
            "Country",
            "Balance",
            "Qualified div ($/share)",
            "Non-qualified div ($/share)",
            "Dividend yield TTM"
          ]
        ],
        "taxFreeAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable)",
            "Annual tax cost saved"
          ],
          [
            "1a",
            "529 College Savings",
            "VWO",
            25000,
            "Qualified dividend",
            75.95,
            "23.2%",
            17.62
          ],
          [
            "1b",
            "529 College Savings",
            "VWO",
            25000,
            "Non-qualified dividend",
            600.21,
            "32.2%",
            193.27
          ],
          [
            "1c",
            "529 College Savings",
            "VWO",
            25000,
            "Subtotal",
            676.17,
            "-",
            210.89
          ],
          [
            "2",
            "529 College Savings",
            "Cash (USD)",
            5000,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "Total",
            "Total tax-free",
            "-",
            30000,
            "-",
            676.17,
            "-",
            210.89
          ]
        ],
        "taxableAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate",
            "Annual tax cost"
          ],
          [
            "1",
            "Taxable Brokerage",
            "SCHP",
            10000,
            "Non-qualified dividend",
            419.93,
            "32.2%",
            135.22
          ],
          [
            "2",
            "Taxable Brokerage",
            "JNK",
            15000,
            "Non-qualified dividend",
            1030.01,
            "32.2%",
            331.66
          ],
          [
            "3",
            "Taxable Brokerage",
            "SCHD",
            20000,
            "Non-qualified dividend",
            595.57,
            "32.2%",
            191.77
          ],
          [
            "4",
            "Taxable Brokerage",
            "Cash (USD)",
            5000,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "Total",
            "Total taxable",
            "-",
            50000,
            "-",
            2045.51,
            "-",
            658.65
          ]
        ],
        "costBasisBlockingNotes": [
          [
            "Account",
            "Blocking note"
          ],
          [
            "Taxable Brokerage",
            "Implementation of Taxable Brokerage cannot be responsibly sequenced without tax-lot data."
          ]
        ],
        "taxableCostBasisInputs": [
          [
            "#",
            "Account",
            "Holding",
            "Balance (market value)",
            "Cost basis",
            "Unrealized gain",
            "Holding period",
            "Notes"
          ],
          [
            "1",
            "Taxable Brokerage",
            "SCHP",
            10000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "2",
            "Taxable Brokerage",
            "JNK",
            15000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "3",
            "Taxable Brokerage",
            "SCHD",
            20000,
            "[missing cost basis]",
            "[missing cost basis]",
            "[missing purchase date]",
            "Approximation blocked until purchaseAmount / purchaseDate are filled."
          ],
          [
            "4",
            "Taxable Brokerage",
            "Cash (USD)",
            5000,
            5000,
            0,
            "N/A",
            "Money market — NAV $1.00, no embedded gain by design."
          ],
          [
            "Total",
            "Total taxable",
            "-",
            50000,
            "[missing cost basis]",
            "[missing cost basis]",
            "-",
            "Totals stay blocked until missing tax-lot inputs are filled."
          ]
        ],
        "taxDeferredAccountDetails": [
          [
            "#",
            "Account",
            "Holding",
            "Balance",
            "Component",
            "Component distribution ($)",
            "Applicable rate (if taxable today)",
            "Annual tax cost deferred"
          ],
          [
            "1",
            "401(k) - Emily",
            "FSTDX",
            18000,
            "Non-qualified dividend",
            818.63,
            "32.2%",
            263.6
          ],
          [
            "2",
            "401(k) - Emily",
            "Cash (USD)",
            2000,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "3",
            "401(k) - Daniel",
            "Cash (USD)",
            5000,
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]",
            "[missing historical load]"
          ],
          [
            "4",
            "401(k) - Daniel",
            "LQD",
            55000,
            "Non-qualified dividend",
            2601.14,
            "32.2%",
            837.57
          ],
          [
            "5a",
            "401(k) - Emily",
            "VWELX",
            80000,
            "Qualified dividend",
            670.43,
            "23.2%",
            155.54
          ],
          [
            "5b",
            "401(k) - Emily",
            "VWELX",
            80000,
            "Non-qualified dividend",
            1081.1,
            "32.2%",
            348.12
          ],
          [
            "5c",
            "401(k) - Emily",
            "VWELX",
            80000,
            "LT cap gain distribution",
            5900.92,
            "23.2%",
            1369.01
          ],
          [
            "5d",
            "401(k) - Emily",
            "VWELX",
            80000,
            "ST cap gain distribution",
            1241.77,
            "32.2%",
            399.85
          ],
          [
            "5e",
            "401(k) - Emily",
            "VWELX",
            80000,
            "Subtotal",
            8894.22,
            "-",
            2272.52
          ],
          [
            "6a",
            "401(k) - Daniel",
            "VTI",
            90000,
            "Qualified dividend",
            213.84,
            "23.2%",
            49.61
          ],
          [
            "6b",
            "401(k) - Daniel",
            "VTI",
            90000,
            "Non-qualified dividend",
            720.46,
            "32.2%",
            231.99
          ],
          [
            "6c",
            "401(k) - Daniel",
            "VTI",
            90000,
            "Subtotal",
            934.3,
            "-",
            281.6
          ],
          [
            "Total",
            "Total tax-deferred",
            "-",
            250000,
            "-",
            13248.29,
            "-",
            3655.28
          ]
        ],
        "componentTaxTreatmentMatrix": [
          [
            "Component",
            "Federal rate type",
            "Effective household rate today",
            "Taxable accounts",
            "Tax-free accounts",
            "Tax-deferred accounts",
            "Notes"
          ],
          [
            "Qualified dividend",
            "LTCG",
            "23.2%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for US common stock and treaty-country foreign names; funds keep the precomputed Morningstar qualified split."
          ],
          [
            "Non-qualified dividend",
            "ORDINARY",
            "32.2%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Stocks route TTM dividend amount here for REIT and non-treaty foreign names, while MLP distributions are treated as ROC; funds keep the precomputed Morningstar non-qualified split."
          ],
          [
            "Interest income",
            "ORDINARY",
            "32.2%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Money-market and bond-style fund income is treated as ordinary-rate income."
          ],
          [
            "Tax-free income",
            "Tax-exempt federal",
            "0%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Current phase assumes a 0% effective rate because state-specific muni exposure is not available in the data path."
          ],
          [
            "LT cap gain distribution",
            "LTCG",
            "23.2%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed long-term capital gains use the LTCG household rate."
          ],
          [
            "ST cap gain distribution",
            "ORDINARY",
            "32.2%",
            "Annual tax cost today",
            "Annual tax cost saved (permanent)",
            "Annual tax cost deferred",
            "Fund-distributed short-term capital gains use the ordinary household rate."
          ]
        ]
      }
    }
  }
};
  function listCases() { return CASE_IDS.map(id => CASES_DATA[id]); }
  function getCaseData(id) { return CASES_DATA[id] || null; }
  async function loadCaseData(id) { const fallback=getCaseData(id); if(typeof location!=='undefined' && /^http/.test(location.protocol) && typeof fetch==='function'){ let timer; const ctl=typeof AbortController!=='undefined'?new AbortController():null; try { const timeout=new Promise((_,reject)=>{timer=setTimeout(()=>{if(ctl)ctl.abort();reject(new Error('timeout'));},1500);}); const req=fetch('/api/cases/'+encodeURIComponent(id),ctl?{signal:ctl.signal}:undefined).then(r=>{if(!r.ok)throw new Error('request failed');return r.json();}); return await Promise.race([req,timeout]); } catch(_){return fallback;} finally{clearTimeout(timer);} } return fallback; }
  return { CASE_IDS, CASES_DATA, listCases, getCaseData, loadCaseData };
});
