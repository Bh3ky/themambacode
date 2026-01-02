## Halftone Algorithm 

A halftone image replaces continuous shades (gray values) with patterns (dots, lines, curves) that _trick the eye_ into seeing brightness.

> Dark areas → dense / large marks
>
> Light areas → sparse / small marks

Everything flows from this principle.

### Defining the artistic intent
---


For this project:
- Input: portrait image
- Output: black background + white halftone marks
- Perception goal: strong silhouette, minimal noise, poster-grade clarity

This dictates:
- High contrast
- Aggressive thresholding
- Controlled dot density

### Image normalisation 
---

**Goal**

Create a stable grayscale image that behaves predictably.

**Why it matters**

Halftoning is extremely sensitive to lighting inconsistencies.

**Operations**
1. Convert to grayscale
2. Normalize brightness
3. Boost contrast
4. Optional background suppression

**Conceptually**:
- Want pixel intensities ∈ [0, 1]
- Dark pixels ≈ 0
- Bright pixels ≈ 1

After this step, the image is a brightness map.

### Decidng the halftone "sampling grid"
---

This is where most quality differences come from.

**Key idea**

Do not place dots per pixel and sample the image at a lower spatial resolution.

**Why**
- Prevents noise
- Creates rhythm
- Gives intentional structure

**Parameters**
- `cell_size` → distance between samples (e.g. 6–20 pixels)
- Smaller = more detail, noisier
- Larger = bolder, more graphic

Think of the image as divided into invisible squares:
```code
+---+---+---+
|   |   |   |
+---+---+---+
|   |   |   |
+---+---+---+
```
Each cell -> one haltfone element


### Map brightness -> dot size
---


This is the core halftone equation.

**For each cell**:
1.	Compute average brightness b ∈ [0,1]
2.	Convert brightness into a radius

**Intuition**
- Dark area → big dot
- Light area → small or no dot

**Sample mapping

```code
radius = max_radius * (1 - b)
```

### Dot placement strategy
---
**Default (grid-based)**
- Dot center = center of cell
- Clean, geometric, poster-like

**Optional variations**
- Jitter centers slightly → organic feel
- Rotate grid → dynamic tension

This step determines whether your image feels:
- Mechanical
- Organic
- Brutalist
- Elegant

### Thresholding (visual discipline)
---
Not all dots deserve to exist.

**Rule**

If brightness is above a cutoff:
- Skip dot entirely

**Why**
- Cleans highlights
- Creates negative space
- Prevents visual clutter

Example:
```code
if b > 0.85:
    skip
```



### Contrast sculpting (poster look)

Your reference images do not preserve all midtones.

They:
- Sacrifice subtlety
- Favor clarity

Strategy

Apply a non-linear curve:
- Gamma correction
- Sigmoid mapping
- Hard threshold for background

Conceptually:
```code
b' = b ^ gamma
```

Gamma > 1 -> darker image -> stronger dots


### Style 1: Classic dot halftone (baseline)
---
This is your baseline style.

Algorithm summary:
1.	Loop over grid
2.	Measure brightness
3.	Compute radius
4.	Draw circle

This is the foundation for everything else.

### Style 2: Radial/circular halftone (poster aesthetic)
---


**Idea**

Dots arranged in concentric rings around a center.

**Why it works**
- Guides the eye
- Adds motion
- Feels intentional and designed

**Mechanism**
1.	Pick image center (cx, cy)
2.	For each sample point:
	- Compute distance r
	- Place dots at angular intervals
3.	Dot size still controlled by brightness

This is how you get that hypnotic poster feel.


### Style 3: Flow-field / fingerprint halftone (advanced)
---
Idea

Instead of a grid, dots follow curved vector paths.

Conceptual pipeline
	1.	Generate a vector field:
	•	Perlin noise
	•	Curl noise
	•	Edge direction gradients
	2.	Trace streamlines
	3.	Place dots along curves
	4.	Dot density ∝ brightness

Result:
	•	Organic
	•	Identity-like
	•	Almost biometric

This is high-level generative design.


STEP 11 — Edge preservation (important)

Faces fail when edges collapse.

Solution
	•	Detect edges (Canny / Sobel)
	•	Increase dot density near edges
	•	Preserve silhouette

This keeps:
	•	Jawline
	•	Nose
	•	Eyes readable

⸻

STEP 12 — Background discipline

Your images:
	•	Have pure black backgrounds
	•	No mid-gray noise

Strategy:
	•	Hard threshold background
	•	Fade dots near edges
	•	Let negative space breathe

⸻

STEP 13 — Typography integration (design-aware)

Important principle:

Text is not an afterthought.

Rules:
	•	Quotes live in negative space
	•	Never overlap dense halftone
	•	Scale text relative to image size

This informs layout decisions earlier.

⸻

STEP 14 — Parameterization (this makes it powerful)

Expose creative knobs:
	•	cell_size
	•	max_radius
	•	gamma
	•	threshold
	•	style

This lets you:
	•	Create presets
	•	Automate daily output
	•	Maintain brand consistency

⸻

STEP 15 — Determinism & repeatability

This matters for consistency.
	•	Fix random seeds
	•	Same input → same output
	•	Essential for a recognizable aesthetic

⸻

Mental model summary

Think of the algorithm as:

Brightness → Structure → Discipline

You’re not “filtering” an image —
You’re reconstructing it using intent.


