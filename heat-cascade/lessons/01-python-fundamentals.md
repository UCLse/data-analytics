# 01. Python fundamentals through a heat example

[Course home](../README.md) | **Indicative time:** 2 hours

**Research question:** How can a small Python calculation describe heat exposure without claiming to measure real risk?

**Dataset boundary:** Every supplied observation and parameter is synthetic. The exercises teach analytical practice; their results do not establish Heat Cascade research findings.

## 1. Learning outcomes and vocabulary

- Store numbers and text in variables, then inspect their types.
- Use a list, a dictionary and a short loop.
- Write a reusable function and explain its assumptions.

| Term | Meaning in this workshop |
| --- | --- |
| `variable` | A name attached to a value. |
| `string` | Text enclosed in quotation marks. |
| `list` | An ordered collection, written inside square brackets. |
| `function` | A named operation that can receive inputs and return a result. |

## 2. Guided analysis

Read the purpose, paste one Python block into a new code cell, then run it with **Shift+Enter**. Compare the output before moving to the next step. Code cells within this lesson share variables and must run in order.

### 2.1. Store and inspect values

**Why this step matters:** Named values make a calculation readable and easier to revise.

```python
neighbourhood = "Ashfield"
surface_temp_c = 35.0
canopy_pct = 9.0
print(neighbourhood, surface_temp_c, canopy_pct)
print(type(neighbourhood).__name__, type(surface_temp_c).__name__)
```

**Expected result:** `Ashfield 35.0 9.0`, followed by `str float`.

**Read the result:** The equals sign assigns a value. It does not test equality. Quotation marks distinguish text from variable names.

### 2.2. Calculate an illustrative excess

**Why this step matters:** A boundary value makes the assumptions behind a calculation explicit.

```python
teaching_boundary_c = 30.0
excess_c = surface_temp_c - teaching_boundary_c
above_boundary = surface_temp_c > teaching_boundary_c
print("Illustrative excess:", excess_c)
print("Above boundary:", above_boundary)
```

**Expected result:** `Illustrative excess: 5.0` and `Above boundary: True`.

**Read the result:** The 30 C boundary is invented for this exercise. A land-surface temperature is not a clinical threshold or a measurement of personal exposure.

### 2.3. Use collections and a loop

**Why this step matters:** Several values can be processed without copying a calculation repeatedly.

```python
temperatures_c = [29.0, 35.0, 38.0]
area = {"name": "Ashfield", "canopy_pct": 9.0}
print(area["name"])
for temperature in temperatures_c:
    excess = max(temperature - teaching_boundary_c, 0)
    print(temperature, excess)
```

**Expected result:** `Ashfield`, then `29.0 0`, `35.0 5.0` and `38.0 8.0`.

**Read the result:** The indented lines belong to the loop. `max` sets negative excess to zero. Dictionary keys retrieve named attributes.

### 2.4. Write a function

**Why this step matters:** A function keeps the calculation consistent when the boundary changes.

```python
def illustrative_excess(temperature_c, boundary_c=30.0):
    return max(temperature_c - boundary_c, 0)

print(illustrative_excess(35.0))
print(illustrative_excess(35.0, boundary_c=32.0))
```

**Expected result:** `5.0` and `3.0`.

**Read the result:** `return` supplies the result to the calling code. A default parameter can be overridden using its name.

## 3. Independent practice

Calculate the excess for `[28.0, 32.0, 37.0]` using a 31 C teaching boundary. Explain how the choice of boundary changes the answer.

<details>
<summary>Hint</summary>

Reuse the function inside a loop and pass `boundary_c=31.0`. Keep four spaces before the line inside the loop.

</details>

## 4. Interpretation and checkpoint

Explain the difference between `=` and `>`. Identify the input, boundary and output of the function. State why the output cannot be called a validated heat-risk score.

Save the personal notebook in `student_work` and place the written response underneath the relevant output. Commit and push the checkpoint to the student's own fork, then verify it on GitHub. A correct result requires both reproducible code and a defensible interpretation. The [troubleshooting guide](../docs/troubleshooting.md) explains common errors.

The [worked script](../solutions/01-python-fundamentals.py) repeats every guided code cell. The [practice answers](../instructor/practice-answers.md) support self-checking after an independent attempt.

[Previous workshop](00-setup.md) | [Next workshop](02-reading-data.md)

---

Course author and research lead: **Sayara Beg**, Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences. [UCL profile](https://profiles.ucl.ac.uk/106848-sayara-beg). Reused or adapted material must preserve this author credit.
