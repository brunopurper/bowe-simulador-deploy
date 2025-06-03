// Função para aprovar proposta (Placeholder - uses backend form)
function aprovarProposta() {
    // This function is now handled by the form submission to the backend.
    // Kept here for potential future client-side enhancements if needed.
    // Original logic:
    // if (confirm("Confirma a aprovação desta proposta?")) {
    //     // Aqui você faria a requisição para o backend
    //     alert("Proposta aprovada com sucesso!");
    // }
    console.log("Approval handled by backend form.");
}

// Função para recusar proposta (Placeholder - uses backend form)
function recusarProposta() {
    // This function is now handled by the form submission to the backend.
    // Kept here for potential future client-side enhancements if needed.
    // Original logic:
    // if (confirm("Confirma a recusa desta proposta?")) {
    //     // Aqui você faria a requisição para o backend
    //     alert("Proposta recusada.");
    // }
    console.log("Rejection handled by backend form.");
}

// Função para compartilhar no WhatsApp (Placeholder - uses backend link)
function compartilharWhatsApp() {
    // This function is now handled by the link to the backend share page.
    // Kept here for potential future client-side enhancements if needed.
    // Original logic:
    // const url = window.location.href; // Might need adjustment if base URL changes
    // const texto = `Confira esta proposta de energia da Bowe: ${url}`;
    // const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(texto)}`;
    // window.open(whatsappUrl, "._blank");
    console.log("WhatsApp share handled by backend link.");
}

// Função para compartilhar por email (Placeholder - uses backend link)
function compartilharEmail() {
    // This function is now handled by the link to the backend share page.
    // Kept here for potential future client-side enhancements if needed.
    // Original logic:
    // const url = window.location.href;
    // const assunto = "Proposta de Energia - Bowe";
    // const corpo = `Olá,\n\nConfira esta proposta de energia da Bowe:\n${url}\n\nAtenciosamente,\nEquipe Bowe`;
    // const emailUrl = `mailto:?subject=${encodeURIComponent(assunto)}&body=${encodeURIComponent(corpo)}`;
    // window.location.href = emailUrl;
    console.log("Email share handled by backend link.");
}

// Função para copiar link (Placeholder - uses backend link)
function copiarLink() {
    // This function is now handled by the link to the backend share page.
    // Kept here for potential future client-side enhancements if needed.
    // Original logic:
    // const url = window.location.href;
    // navigator.clipboard.writeText(url).then(() => {
    //     // Feedback visual
    //     const btn = event.target.closest(".btn");
    //     const originalText = btn.innerHTML;
    //     btn.innerHTML = ".<i class=\"fas fa-check\"></i> Copiado!";
    //     btn.style.background = "linear-gradient(135deg, #28a745 0%, #20c997 100%)";
    //     btn.style.color = "white";
        
    //     setTimeout(() => {
    //         btn.innerHTML = originalText;
    //         btn.style.background = "";
    //         btn.style.color = "";
    //     }, 2000);
    // }).catch(() => {
    //     alert("Erro ao copiar link. Tente novamente.");
    // });
    console.log("Copy link handled by backend link.");
}

// --- PDF Export Function Removed --- 
// The PDF export is handled by the backend using WeasyPrint.
// function exportarPDF() { ... } // Removed

// Adicionar efeitos de hover nos cards (Optional)
document.addEventListener("DOMContentLoaded", function() {
    const calcCards = document.querySelectorAll(".calc-card");
    calcCards.forEach(card => {
        card.addEventListener("mouseenter", function() {
            // Optional: Add hover effect if desired
            // this.style.transform = "translateY(-5px) scale(1.02)";
        });
        
        card.addEventListener("mouseleave", function() {
            // Optional: Reset hover effect
            // this.style.transform = "translateY(0) scale(1)";
        });
    });
});

