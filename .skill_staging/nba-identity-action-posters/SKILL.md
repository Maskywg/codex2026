---
name: nba-identity-action-posters
description: Generate NBA one-on-one matchup posters that use ESPN or user-provided headshots as facial identity references, then create dynamic full-body action scenes with reliable local typography. Use for NBA duel posters, center dunk/block posters, bench mob hardcore play posters, or any workflow where player faces must be checked against ESPN before generation.
---

# NBA Identity Action Posters

Use this skill when creating NBA matchup posters where player likeness matters.

## Non-negotiables

- Always verify each player's face with ESPN player headshots or user-provided reference images before generating.
- Do not paste headshots directly into the final poster unless the user explicitly asks for a collage/headshot style.
- Use the headshots only as identity references for face shape, hairstyle, beard, expression, and build.
- Generate a dynamic full-body basketball action scene first, then add title typography locally with Pillow.
- If the face is wrong, regenerate the action image with stricter identity notes before composing final typography.

## Workflow

1. Confirm the exact matchup pairings, title, teams, and scene type.
2. Collect identity references:
   - Prefer user-provided PNG/JPG files when available.
   - Otherwise download ESPN headshots from `https://a.espncdn.com/i/headshots/nba/players/full/{espn_player_id}.png`.
   - If unsure of the ESPN ID, check ESPN NBA player pages before using an image.
3. Create a temporary identity reference board with both headshots and concise traits:
   - Face shape
   - Hair style
   - Beard/facial hair
   - Notable expression/build cues
4. Use image edit/generation from the reference board to create a new full-body action image:
   - Prompt must say: "Use the portraits only for facial identity and hairstyle. Do not copy the reference board layout."
   - Prompt must describe both players' identity traits.
   - Prompt must request full-body basketball action, arena, sweat, motion, realistic sports photography.
   - Prompt must ban readable text, logos, watermark, and generated lettering.
5. Compose the poster locally:
   - Use the generated action image as the visual.
   - Add title, player names, team labels, and color bars with Pillow.
   - Do not ask the image model to render the final poster text.
6. Review the final image:
   - Confirm it is not a pasted-headshot collage.
   - Confirm both faces broadly match the reference.
   - Confirm title and names are readable and not cropped.
7. Copy finished PNGs to the user's requested Google Drive folder if available locally.

## Scene Guidance

For **main star matchups**:
- One-on-one isolation, attacker dribbling, defender in low stance, eye contact.

For **center matchups**:
- Theme must be dunk vs block.
- Show one center attacking the rim for a powerful dunk while the other contests or blocks at the summit.
- Include rim, backboard, vertical contact, arena lights, sweat, and paint-area collision.

For **bench mob / bench enforcer matchups**:
- Theme must be hardcore play, loose ball, scramble, or floor dive.
- Show players fighting for possession, diving, ripping the ball away, or colliding on a 50-50 ball.
- Tone should feel gritty, physical, high-effort, and chaotic.

## Prompt Skeleton

```text
Create a new ultra-realistic full-body NBA playoff [scene type] photograph using the two portrait references only for facial identity and hairstyle. Do not copy the reference board layout.

Left player should resemble [NAME]: [face/hair/beard/build traits], [team uniform colors].
Right player should resemble [NAME]: [face/hair/beard/build traits], [team uniform colors].

[Action scene description]. Hardwood court, packed NBA arena, dramatic stadium lighting, sweat, motion blur, cinematic sports photography.
No readable text, no official logos, no watermark, leave darker lower area for later typography.
```

## Naming

Use output filenames that preserve the phase:

- Raw identity action: `{slug}_identity_action_YYYYMMDD_HHMMSS.png`
- Final poster: `{slug}_identity_action.png`
