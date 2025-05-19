document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".contactForm");
    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        // Simula envio de emails
        const nome = form.nome.value;
        const email = form.email.value;
        const mensagem = form.mensagem.value;

        // Exibe uma simples mensagem de envio com sucesso
        let notificacao = document.getElementById("notificacao");
        if (!notificacao) {
            notificacao = document.createElement("div");
            notificacao.id = "notificacao";
            notificacao.style.background = "#2a2040";
            notificacao.style.color = "#ffd86b";
            notificacao.style.padding = "1rem";
            notificacao.style.borderRadius = "8px";
            notificacao.style.textAlign = "center";
            notificacao.style.margin = "1rem 0";
            form.parentNode.insertBefore(notificacao, form);
        }

        notificacao.textContent = "Email enviado com sucesso! (Simulação)";
        notificacao.style.display = "block";

        setTimeout(() => {
            notificacao.style.display = "none";
        }, 2500);

        form.reset();
    });
});