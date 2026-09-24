# Reading the severity scores — a plain-language guide

`severity_leaderboard.md` reports POD, FAR, CSI, PSS and BSS. This page explains
what each one asks, using worked examples small enough to check by hand.

The method behind the thresholds is in [`SEVERITY.md`](SEVERITY.md). This page is
only about interpreting the columns.

## Everything comes from one table

For each neighborhood-week the rate either crossed the threshold or it did not,
and the forecast either said it would or it did not. Four possibilities:

|  | forecast said **yes** | forecast said **no** |
| --- | --- | --- |
| it **did** cross | **hit** | **miss** |
| it **did not** cross | **false alarm** | **correct negative** |

Every score below is a different way of dividing those four numbers. There is no
extra information anywhere — only different opinions about which mistakes matter.

**The key fact about this data: correct negatives massively outnumber everything
else.** Of 627 neighborhood-weeks in 2025-26, only 51 crossed IT50. So roughly
550 weeks are quiet weeks that nobody was ever going to call. Any score that
counts those as successes will look wonderful for no reason. That single fact
drives every recommendation here.

## A worked example

Twenty weeks. Four of them (weeks 8-11) really did cross the threshold. Five
forecasters:

| forecaster | hits | misses | false alarms | correct neg | POD | FAR | CSI | PSS | accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Cautious** — never alerts | 0 | 4 | 0 | 16 | 0.00 | — | 0.00 | 0.00 | **0.80** |
| **Panicky** — alerts every week | 4 | 0 | 16 | 0 | **1.00** | 0.80 | 0.20 | 0.00 | 0.20 |
| **Trigger-happy** — 7 alerts | 4 | 0 | 3 | 13 | **1.00** | 0.43 | 0.57 | **0.81** | 0.85 |
| **Careful** — 3 alerts | 3 | 1 | 0 | 16 | 0.75 | **0.00** | **0.75** | 0.75 | 0.95 |
| **Perfect** | 4 | 0 | 0 | 16 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 |

Read the two rows in the middle carefully. **Trigger-happy wins on PSS.
Careful wins on CSI, on FAR, and on accuracy.** They are not the same forecaster
and no single number settles which is better.

This disagreement used to show up in the real results too, between an
over-alerting graph arm and the LSTM. It no longer does — `gnn_st` currently
leads PSS, CSI and BSS at once — but the metrics have not changed, only the
models. The disagreement returns the moment an arm starts over-alerting, which
is why both columns stay in the tables.

Note also that **Cautious scores 80% accuracy while being useless.** In the real
data, where crossings are rarer, that becomes 91.9%.

---

## POD — "of the bad weeks, how many did it catch?"

```
POD = hits / (hits + misses)
```

Also called *recall*, *hit rate*, or *sensitivity*. The denominator is every week
that really crossed, so POD only ever looks at the left column of the table.

- Cautious: `0/4 = 0.00`
- Careful: `3/4 = 0.75`
- Panicky: `4/4 = 1.00`

**The trap:** Panicky gets a perfect POD by alerting every single week. POD
cannot be a target on its own — you can always raise it by alerting more freely.
It only means something next to FAR.

**When to lead with it:** when missing an event is far more costly than a false
alarm. If a missed surge means an unstaffed ED and a false alarm means a wasted
meeting, POD is what you care about.

## FAR — "when it cried wolf, how often was there no wolf?"

```
FAR = false alarms / (hits + false alarms)
```

The share of *alerts* that turned out wrong. This is the only score on the page
where **lower is better**.

- Careful: `0/3 = 0.00` — every alert it raised was real
- Trigger-happy: `3/7 = 0.43`
- Panicky: `16/20 = 0.80`
- Cautious: `0/0` → **undefined**, printed blank

That blank matters. Cautious raised no alerts, so "how often were its alerts
wrong?" has no answer. The code returns `NaN`, not 0 — a 0 would read as a
perfect score for a forecaster that never did anything.

**FAR is not the false positive rate.** FAR divides by the alerts you raised; the
false positive rate divides by all the quiet weeks. On this data those differ by
a factor of ten. `severity_long.csv` has both — `FAR` and `FPR`.

## CSI — "of everything that mattered, how much did it get right?"

```
CSI = hits / (hits + misses + false alarms)
```

Also called the *threat score* or *Jaccard index*. The denominator is every week
that was either a real crossing or a claimed one — so **correct negatives are
excluded entirely**.

- Careful: `3/(3+1+0) = 0.75`
- Trigger-happy: `4/(4+0+3) = 0.57`
- Panicky: `4/(4+0+16) = 0.20`

That exclusion is the whole point. Because it never counts the ~550 quiet weeks,
CSI cannot be inflated by the base rate. **In a rare-event problem, CSI is the
most trustworthy single number**, and it is the one I would read first.

Its limitation is that it is not a skill score: there is no reference level, so
"CSI = 0.5" is not intrinsically good or bad. You can only compare CSI between
models on the same events.

## PSS — "how much better than guessing?"

```
PSS = POD − FPR,   where FPR = false alarms / (false alarms + correct negatives)
```

Also called the *True Skill Statistic* or *Youden's J*. It takes credit for
catching events and subtracts a penalty for alerting on quiet weeks.

- Careful: `0.75 − 0/16 = 0.75`
- Trigger-happy: `1.00 − 3/16 = 0.81`
- Panicky: `1.00 − 16/16 = 0.00`
- Cautious: `0.00 − 0/16 = 0.00`

**Why it leads the tables:** it is 0 for both degenerate forecasters. You cannot
buy a PSS by never alerting, and you cannot buy one by always alerting. Nothing
else on this page has that property, which is what makes it safe as a default
ranking.

**Its blind spot, in the real data:** that penalty term is divided by the number
of quiet weeks, and there are ~576 of them. So

| model | false alarms | penalty (FPR) | POD | PSS |
| --- | --- | --- | --- | --- |
| a retired over-alerting graph arm | 56 | `56/576 = 0.097` | 0.863 | 0.766 |
| `lstm` | 9 | `9/576 = 0.016` | 0.745 | 0.729 |
| `gnn_st` (current) | 10 | `10/576 = 0.017` | 0.784 | 0.767 |

**Fifty-six false alarms cost only 0.097.** PSS is very nearly POD with a small
haircut, because it prices false alarms against how many quiet weeks exist rather
than against how many alerts you raised. An operational user feels the 56, not
the 0.097. **That is why PSS should never be read without CSI or FAR beside it.**

The third row makes the point from the other direction: `gnn_st` scores
essentially the *same* PSS as the retired arm (0.767 against 0.766) while raising
10 false alarms instead of 56. PSS could not tell those two apart. CSI could —
0.656 against 0.411.

## BSS — "were the stated probabilities honest?"

The only score here that is not about yes/no. Each forecast also carries a
probability, derived from its 95% interval — "62% chance this week crosses
IT50". The Brier score is the mean squared error of those probabilities:

```
Brier = mean( (probability − outcome)² ),   outcome is 1 or 0
```

Lower is better, but the raw number is hard to read at a low base rate, so it is
compared against always predicting the base rate:

```
BSS = 1 − (model Brier / climatology Brier)
```

On the same 20 weeks as above (base rate 0.20):

| probability forecast | Brier | BSS |
| --- | --- | --- |
| honest — 0.90 on the four real weeks, 0.05 elsewhere | 0.0040 | **+0.975** |
| climatology — 0.20 every week | 0.1600 | 0.000 |
| over-confident — 0.90 on seven weeks, 0.05 elsewhere | 0.1251 | +0.218 |

**Zero means no better than reciting the base rate every week. Negative means
worse than that** — the model's confidence is actively misleading. In the current
results `seasonal_naive` scores **−0.545** and `dualtopo` **−0.057**: both would
have been better off saying nothing. Retired arms reached −2.827.

BSS rewards two different things at once — picking the right weeks
(*resolution*) and stating probabilities that match reality (*calibration*). A
model can catch every event and still score badly by being over-confident about
it. `severity_reliability.png` separates the two: it plots stated probability
against observed frequency, and anything below the diagonal is over-confident.

---

## Which should I read?

**Start with CSI and BSS.** CSI ignores the quiet weeks that dominate this data;
BSS checks whether the confidence is real. Together they are hard to fool.

**Use PSS as the ranking** — it is the one that cannot be gamed by degenerate
behaviour, which is why the leaderboard sorts on it by default.

**Check FAR before believing a high PSS.** If FAR is above ~0.5, the model is
wrong more often than right whenever it speaks, however good its PSS looks.

**Never quote accuracy.** At an 8% base rate it is 92% for a model that does
nothing.

**Check `n_events` first of all.** Any row with fewer than five observed events
is flagged `underpowered` in `severity_long.csv`. IT98 in this window has two
events across 627 weeks; its scores are arithmetic, not evidence.

## Cheat sheet

| column | question | direction | ignores correct negatives? | gameable by "never alert"? |
| --- | --- | --- | --- | --- |
| `POD` | of real crossings, how many caught? | higher | yes | scores 0 |
| `FAR` | of alerts raised, how many wrong? | **lower** | yes | undefined |
| `precision` | `1 − FAR` | higher | yes | undefined |
| `FPR` | of quiet weeks, how many alerted? | **lower** | no | scores 0 |
| `CSI` | of all relevant weeks, how many right? | higher | yes | scores 0 |
| `F1` | harmonic mean of POD and precision | higher | yes | scores 0 |
| `PSS` | skill over chance, both errors priced | higher | no | scores 0 |
| `HSS` / `MCC` | skill over chance, chance-corrected | higher | no | scores 0 |
| `accuracy` | of all weeks, how many right? | higher | no | **scores 0.92** |
| `frequency_bias` | alerts raised ÷ events that happened | **near 1** | yes | scores 0 |
| `brier` | squared error of the probabilities | **lower** | no | — |
| `BSS` | skill over always predicting the base rate | higher | no | — |
| `exact_band` | right one of the four bands | higher | no | **scores 0.92** |
| `kappa_quadratic` | band agreement, chance-corrected | higher | no | scores 0 |
| `mean_band_error` | signed band bias, `+` = over-calls | **near 0** | no | negative |

A blank cell in the leaderboard is always "not measurable", never zero. Zero
would say the model has no skill; blank says the question has no answer for that
row — usually because it raised no alerts, or nothing crossed.
