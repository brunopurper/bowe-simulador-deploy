# Design Improvements for Bowe Proposal Layout

Based on the review of `proposta.html`, here are the planned improvements for a more harmonious layout:

1.  **Header & Branding:**
    *   Adjust the alignment of the logo and company details (`col-md-6 text-end`) for better balance with the proposal title section, especially on medium screens. Consider vertical stacking on smaller screens using Bootstrap classes.
    *   Refine the main card header (`bg-success text-white`): Maybe use a lighter shade of green or just a top/bottom border with the green color for a less heavy look.

2.  **Color Palette & Consistency:**
    *   Review the usage of `text-success`, `text-warning`, `text-primary`. Ensure they are used meaningfully and consistently.
    *   Standardize background colors. `bg-light` for info cards is acceptable, but ensure consistency in padding and margins.

3.  **Typography & Readability:**
    *   Ensure consistent font sizes and weights for headings (h3, h4, h5) and body text.
    *   Check line spacing and paragraph margins for optimal readability.

4.  **Spacing & Alignment:**
    *   Refine vertical alignment in sections combining icons and text (e.g., "TIPO DE LIGAÇÃO", "MODELO DE CONTRATO"). Use Flexbox utilities (`d-flex align-items-center`) consistently.
    *   Review all margin (`m*`) and padding (`p*`) utilities (`mt-4`, `mb-3`, `p-3`, etc.) for consistent rhythm and adequate white space.

5.  **Element Styling:**
    *   **Cards:** Apply a subtle `box-shadow` (if not already present via `shadow` class) and potentially a consistent `border-radius` for a softer look.
    *   **Tables:** Ensure table headers (`bg-dark text-white`) have sufficient padding. Verify `table-striped` appearance fits the overall theme.
    *   **Buttons:** Maintain consistency in button styling (size, padding, border-radius). The large action buttons (`btn-lg`) are okay for emphasis.
    *   **Icons:** Ensure FontAwesome icons render correctly. Consider adding a subtle background shape or increasing size slightly for key icons if needed for visual hierarchy.

6.  **Responsiveness:**
    *   Explicitly test and refine the layout for various screen sizes (mobile, tablet, desktop) using browser developer tools during implementation.

7.  **PDF Export Button:**
    *   **Placement:** Add the button logically alongside the "COMPARTILHAR" button at the bottom, or potentially near the top right of the main card.
    *   **Styling:** Style it consistently with other buttons (e.g., `btn btn-info` or `btn btn-secondary`) and include a relevant FontAwesome icon like `fas fa-file-pdf`.

8.  **Implementation Strategy:**
    *   Create a new CSS file `/home/ubuntu/bowe-simulador-simplificado/src/static/css/custom.css`.
    *   Link this `custom.css` file in `/home/ubuntu/bowe-simulador-simplificado/src/templates/base.html` *after* the Bootstrap CSS link to allow overriding styles.
    *   Implement the visual refinements primarily through `custom.css` to keep HTML changes minimal and maintainable.
    *   Modify `proposta.html` for structural changes and to add the new button.
