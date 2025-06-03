# Bowe Simulador - New Layout Integration Todo

- [ ] 1. **Backup Project:** Create a zip backup of the `bowe-simulador-simplificado-v2` directory.
- [ ] 2. **Extract New Assets:**
    - [ ] Create `/src/static/css/new_layout.css` from the `<style>` block in `pasted_content.txt`.
    - [ ] Create `/src/static/js/new_layout_interactions.js` from the `<script>` block in `pasted_content.txt`.
    - [ ] **Important:** Remove `jspdf`, `html2canvas` CDN links and the `exportarPDF` JavaScript function. Keep other interaction functions for now (Approve/Reject/Share alerts).
- [ ] 3. **Update `base.html`:**
    - [ ] Comment out/remove Bootstrap CSS link.
    - [ ] Comment out/remove `style.css` and `custom.css` links.
    - [ ] Add `<link rel="stylesheet" href="{{ url_for('static', filename='css/new_layout.css') }}">`.
    - [ ] Keep FontAwesome CSS link.
    - [ ] Decide and potentially remove Bootstrap JS link.
    - [ ] Add `<script src="{{ url_for('static', filename='js/new_layout_interactions.js') }}"></script>` (if keeping JS interactions).
- [ ] 4. **Refactor `proposta.html`:**
    - [ ] Replace the content within `{% block content %}` with the HTML structure from `pasted_content.txt`'s `<body>`.
    - [ ] Systematically replace all static placeholder values (names, numbers, amounts) with the correct Jinja variables (e.g., `{{ proposta.nome_indicado }}`).
    - [ ] Adapt action buttons:
        - [ ] Ensure Approve/Reject buttons use existing `<form>` pointing to `proposta.resposta`, styled with new CSS classes. Remove `onclick`.
        - [ ] Ensure Share button is a link (`<a>`) pointing to `proposta.compartilhar`, styled with new CSS. Remove JS share functions for now.
        - [ ] Ensure **Export PDF** button is a link (`<a>`) pointing to `proposta.exportar_pdf`, styled with new CSS. Remove `onclick`.
- [ ] 5. **Refine `new_layout.css`:**
    - [ ] Verify selectors match the refactored `proposta.html`.
    - [ ] Remove or comment out the `@media print` block.
    - [ ] Test rendering with WeasyPrint (consider simplifying complex styles if PDF issues arise).
- [ ] 6. **Implement & Test:**
    - [ ] Run the Flask application.
    - [ ] Test proposal page rendering in browser (visuals, dynamic data).
    - [ ] Test Approve/Reject functionality.
    - [ ] Test Share link functionality.
    - [ ] Test **Export PDF** button (verify backend WeasyPrint generation, check PDF layout and quality).
    - [ ] Test responsiveness.
- [ ] 7. **Final Adjustments:** Make necessary CSS/HTML tweaks based on testing.
- [ ] 8. **Package & Deliver:** Zip the updated project and report results to the user.

**Key Constraint:** Preserve existing backend logic and WeasyPrint PDF generation. Do NOT use the client-side JS PDF generation from the new layout.
