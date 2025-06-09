// formulario.js
document.addEventListener("DOMContentLoaded", function() {
    $('#telefone').mask('(00) 00000-0000');
    $('#cpf').mask('000.000.000-00', {reverse: true});
    $('#rg').mask('00.000.000-0');

    $('#documento').on('change', function() {
        $('#documento-name').text(this.files[0] ? this.files[0].name : 'Nenhum arquivo selecionado');
    });
    $('#conta_luz').on('change', function() {
        $('#conta_luz-name').text(this.files[0] ? this.files[0].name : 'Nenhum arquivo selecionado');
    });

    function validarEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function validarCPF(cpf) {
        cpf = cpf.replace(/\D/g, '');
        if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;

        let soma = 0;
        for (let i = 0; i < 9; i++) soma += parseInt(cpf.charAt(i)) * (10 - i);
        let resto = (soma * 10) % 11;
        if (resto === 10 || resto === 11) resto = 0;
        if (resto !== parseInt(cpf.charAt(9))) return false;

        soma = 0;
        for (let i = 0; i < 10; i++) soma += parseInt(cpf.charAt(i)) * (11 - i);
        resto = (soma * 10) % 11;
        if (resto === 10 || resto === 11) resto = 0;
        if (resto !== parseInt(cpf.charAt(10))) return false;

        return true;
    }

    function validarRG(rg) {
    rg = rg.replace(/\D/g, '');
    // Deve ter entre 7 e 9 dígitos
    if (rg.length < 7 || rg.length > 9) {
        return false;
    }
    // Verifica se todos os dígitos são iguais (não pode)
    return !/^(\d)\1+$/.test(rg);
}


    function mostrarErro(mensagem) {
        $('.modal-erro').remove();
        $('body').append(`
            <div class="modal-erro" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 9999;">
                <div style="background: #fff; padding: 20px; border-radius: 8px; max-width: 400px; text-align: center;">
                    <h3 style="color: #e74c3c; margin-bottom: 10px;">Erro!</h3>
                    <p style="margin-bottom: 20px;">${mensagem}</p>
                    <button id="fecharModal" style="background: #e74c3c; color: #fff; border: none;
                        padding: 8px 16px; border-radius: 4px; cursor: pointer;">Fechar</button>
                </div>
            </div>
        `);
        $('#fecharModal').click(function() { $('.modal-erro').remove(); });
    }

    $('#clienteForm').submit(function(e) {
        e.preventDefault();

        const nome = $('#nome_completo').val().trim();
        if (!nome) { mostrarErro('Por favor, preencha o campo "Nome Completo".'); return; }

        const telefone = $('#telefone').val().replace(/\D/g, '');
        if (!telefone) { mostrarErro('Por favor, preencha o campo "Telefone".'); return; }
        else if (telefone.length !== 11) { mostrarErro('O campo "Telefone" está inválido.'); return; }

        const email = $('#email').val().trim();
        if (!email) { mostrarErro('Por favor, preencha o campo "E-mail".'); return; }
        else if (!validarEmail(email)) { mostrarErro('O campo "E-mail" está inválido.'); return; }

        const estadoCivil = $('#estado_civil').val();
        if (!estadoCivil) { mostrarErro('Por favor, selecione o campo "Estado Civil".'); return; }

        const cpf = $('#cpf').val().replace(/\D/g, '');
        if (!cpf) { mostrarErro('Por favor, preencha o campo "CPF".'); return; }
        else if (!validarCPF(cpf)) { mostrarErro('O campo "CPF" está inválido.'); return; }

        const rg = $('#rg').val().replace(/\D/g, '');
        if (!rg) { mostrarErro('Por favor, preencha o campo "RG".'); return; }
        else if (!validarRG(rg)) { mostrarErro('O campo "RG" está inválido.'); return; }

        const naturalidade = $('#naturalidade').val().trim();
        if (!naturalidade) { mostrarErro('Por favor, preencha o campo "Naturalidade".'); return; }

        const docFile = $('#documento')[0].files[0];
        if (!docFile) { mostrarErro('Por favor, envie o documento com foto e CPF.'); return; }

        const contaFile = $('#conta_luz')[0].files[0];
        if (!contaFile) { mostrarErro('Por favor, envie a conta de luz atualizada.'); return; }

        this.submit();
    });
});
