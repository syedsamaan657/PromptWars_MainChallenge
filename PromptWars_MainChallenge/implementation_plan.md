# Implementation Plan - Pan-Indian ChefAI with Warm-Cozy Techno Aesthetics

This update transitions the ChefAI cooking scheduler and budget planner to support Pan-Indian cuisines (North Indian, South Indian, etc.), switch all currency references to INR (₹), and overhaul the visual layout to combine warm, cozy food-themed colors (saffron, terracotta, warm cream) with glowing techno-neon accents.

## User Review Required

> [!IMPORTANT]
> - All recipes will be rewritten to focus on Pan-Indian breakfast, lunch, and dinner options, covering Vegetarian, Vegan, Keto, Gluten-Free, and Standard diets.
> - Currency formatting will switch from USD ($) to INR (₹) across the forms, recipe details, grocery costs, and budget feasibility cards.
> - Color tokens in `style.css` will be re-calibrated.

We recommend maintaining the active workspace in `C:\Users\samaan\.gemini\antigravity-ide\scratch\cooking-todo-app`.

## Proposed Changes

### [cooking-todo-app]

#### [MODIFY] [style.css](file:///C:/Users/samaan/.gemini/antigravity-ide/scratch/cooking-todo-app/style.css)
- Change CSS variables:
  - Background base colors to warm terracotta-tinted darks (`hsl(20, 20%, 6%)` to `hsl(30, 16%, 8%)`).
  - Cozy tones: Saffron/Turmeric gold (`hsl(38, 95%, 55%)`), Cardamom/Coriander green (`hsl(100, 45%, 45%)`), Terracotta Red (`hsl(12, 70%, 50%)`).
  - Techno accents: Glowing neon Cyan/Blue (`hsl(185, 95%, 48%)`) or Electric Purple for active selections and UI highlights.
- Keep the premium glassmorphism borders and update shadows.

#### [MODIFY] [index.html](file:///C:/Users/samaan/.gemini/antigravity-ide/scratch/cooking-todo-app/index.html)
- Change input currency indicator from `$` to `₹`.
- Change default daily budget value from `30` to `500` INR (an appropriate range for single-day home cooking in India).

#### [MODIFY] [app.js](file:///C:/Users/samaan/.gemini/antigravity-ide/scratch/cooking-todo-app/app.js)
- Update currency display references from `$` to `₹`.
- Replace the entire `RECIPE_POOL` database with rich Indian recipes:
  - South Indian: Idli Sambar, Lemon Rice, Coconut Fish Curry.
  - North Indian: Aloo Paratha, Paneer Butter Masala, Chole Bhature.
  - West/Street: Poha, Egg Bhurji Pav.
- Implement appropriate Indian substitutions:
  - Swap Paneer (Dairy) with Tofu (Vegan/Dairy-free).
  - Swap Ghee (Dairy) with Mustard/Coconut Oil (Vegan/Dairy-free).
  - Swap Rice with Cauliflower Rice (Keto/Low carb).
  - Swap premium paneer/veggies for low-cost alternatives (e.g. potato, chickpeas) to save budget.
- Calibrate individual ingredient costs in INR (e.g. ₹20 - ₹250).

## Verification Plan

### Manual Verification
- Open the application in the browser at `http://localhost:8000/index.html`.
- Run a generation with a default budget of ₹500 and verify:
  - All output recipes are Pan-Indian dishes.
  - All ingredient prices are in ₹.
  - The budget summary calculations work with ₹.
- Test vegan, keto, and standard restrictions to verify the selection matches Indian cuisine.
- Run a substitution swap (e.g. Paneer to Tofu) and verify cost adjustments recalculate correctly in INR.
