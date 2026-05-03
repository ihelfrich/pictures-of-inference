# Table of Contents

A draft. The structure is committed; the chapter list is open to revision.

---

## Front Matter

**Preface.** Why this book exists. What it expects of you. How to read it (the layered structure, the four core datasets, the recurring characters).

**A Field Guide to the Book.** A two-page map. Where to enter, what to skip, what to come back to. Different reading paths for different readers.

---

## Part One. How to See

The literacy book. Reading the world through quantitative eyes. By the end of Part One, the reader can pick up a published paper and follow its argument. They cannot yet produce serious analysis. They can read it.

**1. Numbers on the page.** Where data comes from. The fundamental rectangle: rows are units, columns are measurements. Variable types. The first questions to ask of any dataset. The four datasets we will live with for the rest of the book are introduced here.

**2. Probability as area.** Probability before formulas. The sample space, events as regions, probability as the fraction of area covered. Conditional probability as zooming in. Bayes' theorem developed visually before any algebra. The disease-test paradox.

**3. Shapes of data.** Distributions you will see again and again — Bernoulli, binomial, Poisson, normal, exponential, log-normal, $t$. Each one as a *story* about what kind of process produces it, not as a formula to memorize.

**4. The grammar of graphics.** Wilkinson's framework taught explicitly. Aesthetics, geometries, scales, facets. Why position beats length beats angle beats area beats color. The visual vocabulary the rest of the book will use.

**5. Center, spread, shape.** The descriptive statistics that survive contact with reality. Mean and median. Variance and IQR. Why robustness matters. The five-number summary. When to report which.

**6. Lying with charts.** A critical-reading chapter. Truncated axes, dual-axis chicanery, area-when-length-was-needed, log scales hiding effect sizes, cherry-picked windows. Real published examples dissected.

**7. Underused visualizations.** Slope graphs, Cleveland dot plots, mosaic plots, hex bins, ridge plots, alluvial diagrams, calendar heatmaps. Each one anchored to the question it answers better than its conventional alternative.

**8. Visualizing uncertainty.** Confidence bands. Coefficient plots. Hypothetical outcome plots. Fan charts. Why error bars are usually the wrong choice and what to use instead. Modern best practices that have not yet reached most introductory books.

**9. Reading equations.** A whole chapter on parsing. What does $\E[Y \mid X]$ say? How do you read $\hat\beta = (\bm{X}^\top\bm{X})^{-1}\bm{X}^\top\bm{y}$ aloud? Translation drills, English-to-math and math-to-English. The skill the rest of the book depends on.

**10. Reading tables.** A table is a chart with words. The conventions of regression tables, summary statistics, balance tables. What every cell is doing. How journal tables are structured and why.

**11. The empirical paper, walked through.** A complete published paper, read end to end, with the reader looking over the shoulder. Every claim located, every number explained, every figure interpreted. The capstone of Part One.

---

## Part Two. How to Speak

The production book. By the end of Part Two, the reader is a competent applied analyst. They can run a real analysis from raw data to defensible conclusion and communicate the result to a non-statistical audience.

**12. From sample to population.** Sampling distributions. Standard errors. The Central Limit Theorem developed slowly. Why $\sqrt{n}$ instead of $n$.

**13. The confidence interval, properly understood.** What 95% confidence actually means. Why the natural interpretation is wrong. Why most practitioners use it anyway. The Bayesian alternative previewed.

**14. Hypothesis testing.** The five-part structure. The $p$-value, what it is and what it isn't. Type I and Type II errors. Power. The replication crisis as context.

**15. The sin of multiple comparisons.** Why running twenty tests gives one false positive. Bonferroni, FDR, family-wise vs. comparison-wise error rates. The garden of forking paths.

**16. Simple regression.** A line through points, properly understood. The OLS objective. The normal equations. The slope as correlation rescaled. The intercept's interpretation, including when it has none.

**17. Regression as a way of thinking.** Conditional expectation as the target. Regression as projection. Residuals as the part you have not explained. The leap from arithmetic to analysis.

**18. Multiple regression.** Holding things constant — what it means and what it doesn't. The Frisch-Waugh-Lovell theorem. Omitted variable bias. Why "controlling for" is not "causally identifying."

**19. Diagnostics and criticism.** What can go wrong with a regression. Residual plots. Heteroskedasticity. Influential observations. Functional form. The discipline of looking before believing.

**20. Categorical variables and interactions.** Dummies. Reference categories. Interaction terms. ANOVA as regression. Why the categorical-continuous distinction is a notational convenience, not a deep difference.

**21. Logistic regression and the GLM family.** Binary outcomes, count outcomes, the link function as a design decision. MLE introduced as a method, deferred for theory.

**22. Communicating results.** The results section of a paper. The policy memo. The newspaper op-ed. How to translate $\hat\beta = 0.47$ $(0.12)$ into something a senator will understand without lying.

**23. The applied workflow.** A full project from raw data to final write-up. Code organization, version control, documentation, reproducibility. Real datasets, real choices, real outputs.

---

## Part Three. How to Think

The theoretical book. The mathematical apparatus underneath the techniques. By the end of Part Three, the reader understands not just how to use these tools but why they work. Calculus and linear algebra are taught here in service of statistical understanding, not as separate subjects.

**24. The line of best fit, geometrically.** Vectors, dot products, projection. Regression as the shadow of $\bm{y}$ on the column space of $\bm{X}$. The Pythagorean decomposition that gives us $R^2$. Linear algebra introduced for what it actually does.

**25. Functions and rates.** Calculus as the mathematics of change. Derivatives as instantaneous rates. The intuition before the formalism. Why this matters: every estimator is the solution to an optimization problem.

**26. Optimization.** First-order conditions. Second-order conditions. Constrained optimization. The maximum-likelihood method developed properly. Lagrange multipliers as the language of constrained problems.

**27. Maximum likelihood.** The principle. The likelihood function. Why log-likelihoods. Score equations. The information matrix. MLE as a unifying framework that contains OLS as a special case.

**28. The geometry of estimators.** What it means for an estimator to be unbiased, consistent, efficient. The bias-variance trade-off as a real curve, not a slogan. Why no estimator is best in every sense.

**29. Asymptotic theory.** Convergence in probability. Convergence in distribution. The law of large numbers, made precise. The Central Limit Theorem, made precise. Delta method. Why "large $n$" makes everything easier.

**30. Inference, properly.** What does $p < 0.05$ really mean? The frequentist worldview, formalized. Likelihood ratio, Wald, and score tests as different ways to ask the same question.

**31. The Bayesian alternative.** Probability as degree of belief. Prior, likelihood, posterior. Conjugacy. MCMC as the modern enabler. When Bayes and frequentism agree numerically and what to do when they don't.

**32. Causal inference, formalized.** Potential outcomes. The fundamental problem. Identification under randomization. Identification under conditional independence. Pearl's DAGs. The languages and their (largely overstated) tensions.

**33. Identification.** What it means for a parameter to be identified. Local identification vs. global identification. When the data alone determine the answer and when they do not.

**34. Standard errors, the long story.** Heteroskedasticity-robust. Cluster-robust. Bootstrap. Why naive standard errors are usually wrong and what to do about it. A topic that deserves a whole chapter and rarely gets one.

---

## Part Four. How to Discover

The research book. Modern methods at the frontier of empirical economics. Computational, design-based, and high-dimensional approaches. By the end of Part Four, the reader can engage with current research and contribute to it.

**35. The instrumental-variables framework.** From the basic IV intuition to the LATE theorem. Compliance, monotonicity, exclusion. Modern critiques and modern responses.

**36. Difference-in-differences, modern edition.** The two-period base case. The two-way fixed-effects critique. Goodman-Bacon. Callaway-Sant'Anna. The methods that have replaced naive DiD in the last decade.

**37. Regression discontinuity.** Sharp and fuzzy designs. Local linear regression. The continuity assumption. McCrary tests for manipulation. Modern bandwidth-selection methods.

**38. Synthetic control.** The Abadie method. Inference for synthetic control. Generalized synthetic control. When you cannot find a comparison group, build one.

**39. Panel data, advanced.** Fixed effects beyond the within estimator. Dynamic panel methods. Arellano-Bond. The incidental-parameters problem. When panel data buys you something and when it doesn't.

**40. Machine learning for causal inference.** Double/debiased machine learning. Causal forests. Heterogeneous treatment effects. The Chernozhukov-Hansen-Spindler agenda. How modern computational methods have changed empirical practice.

**41. High-dimensional econometrics.** Lasso and ridge in causal settings. Post-selection inference. The honest-confidence-interval problem. Why "use the lasso" is harder than it sounds.

**42. Time-series econometrics.** Stationarity and cointegration. ARMA, ARCH, GARCH. Vector autoregressions. Spurious regression. Structural breaks.

**43. Nonparametric and semiparametric methods.** Kernel regression. Local polynomial methods. Sieve estimation. Series methods. When you do not want to commit to a functional form.

**44. Simulation-based inference.** When the likelihood is intractable. Approximate Bayesian computation. Indirect inference. Modern computational methods for problems that classical methods cannot solve.

**45. Structural estimation.** Reduced-form vs. structural. The Lucas critique in practice. Estimating economic models that mean something. The trade-off between flexibility and interpretability.

**46. Theoretical econometrics: a tour.** The mathematical foundations of the field. Empirical processes. M-estimation. Z-estimation. The general theorems that specific methods are special cases of. A reader's guide to *Econometrica*.

**47. Doing original research.** A meta-chapter. How research questions are chosen. How they are refined into estimable forms. How papers are structured, reviewed, revised, published. The political economy of academic research, honestly described.

---

## Back Matter

**Mathematical appendix.** Reference material on probability, calculus, linear algebra, real analysis. For the reader who needs to look something up.

**Computational appendix.** Quick references for R, Stata, Python. The basic setup, the most common patterns, where to learn more.

**Datasets.** Documentation of the four core datasets. Sources, processing decisions, codebooks, exercise prompts.

**Bibliography.** Real and complete.

**Index.**

---

## A note on what is missing

This table of contents is a draft and several things deserve consideration.

- **Survey methods.** Sample design, weights, complex surveys. Important for the public-policy reader. A chapter on this should probably appear in Part Two.
- **Survival analysis.** Important in many applied contexts. Could be a Part Three chapter or a Part Four module.
- **Multilevel and hierarchical models.** A natural fit somewhere in Parts Three or Four.
- **Spatial econometrics.** Given your background, this should probably be present somewhere in Part Four.
- **Network and graph data.** Increasingly important. Could be its own chapter or a section.
- **Measurement and data quality.** A topic that almost no textbook covers and that almost every working analyst eventually wishes they had been taught.

We'll revisit these as we make progress. Some will become full chapters; some will be modules within larger chapters; some will be cut.
