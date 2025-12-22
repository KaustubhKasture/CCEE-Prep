import os
from agents.mcq_agent import generate_questions as base_generate

AA_INSTRUCTION = """
You are an expert in Analytics/Statistical programming.

Generate questions ONLY about Analytics/Statistics:
- Data Analytics life cycle, Model Planning, 
- Sample Spaces and Events
- Joint, Conditional and Marginal Probabilities
- Baye's Theorem
- Random Variable, Concepts of Correlation, Covariance, Outliers
- Probability Distribution and Data
- Continous Distribution (Uniform, Exponential and Normal)
- Discrete Distribution (Binomial, Poisson, Geometric)
- Descriptive Statistical Measures
- Summary Statistics - Central Tendency and Dispersion
        -mean
        -median
        -mode
        -quartiles
        -percentiles
        -range
        -interquantile range
        -standard deviation
        -variance
        -coefficient of variation
- Sampling and Estimation
- Sample and Population, univariate  and bivariate sampling, resampling
- Central Limit Theorem
- Statistical Inference Terminology
        -types of error
        -tails of test
        -confidence intervals
- Hypothesis Testing
- Parametric Testing: ANOVA, t-test
- Non-parametric Test: chi-square, U-test
- Predictive Modeling
- Identifying Information Attribute
- Induction and Prediction
- Supervised Segmentation
- Visualising Segmentation
- Trees as set of Rules
- Probability Estimation
- Simulaiton and Risk Analysis, Optimisation
- Decision Analytics
- Evaluating Classifiers
- Explicit Evidence Combination with Bayes Rule
- Probabilistic Reasoning
- Factor Analysis
- Directional Data Analytics

Do NOT include questions about Java or other languages.
Use small code snippets when useful.
"""

async def generate_analytics_questions(
    difficulty: str,
    num_questions: int,
    api_key: str | None = None,
    fallback_api_key: str | None = None,
    fallback_model: str = "gpt-3.5-turbo"
) -> str:
    return await base_generate(
        subject="Analytics",
        difficulty=difficulty,
        num_questions=num_questions,
        api_key=api_key,
        fallback_api_key=fallback_api_key,
        fallback_model=fallback_model,
        extra_instruction=AA_INSTRUCTION,
    )

import asyncio

async def _test():
    text = await generate_analytics_questions(
        difficulty="easy",
        num_questions=5,
        api_key=None,
    )
    print(text)

if __name__ == "__main__" and os.getenv("ENV") == "local":
    asyncio.run(_test())
