// ANIMAÇÃO PARA OS BALÕES DA SEÇÃO SOBRE

function InitAnimaScrollHome() {
  const baloes = document.querySelectorAll('.js-scroll');

  if (baloes.length) {
    const windMetade = window.innerHeight * 0.7;

    function animaScroll() {
      baloes.forEach((balao) => {
        const balaoTop = balao.getBoundingClientRect().top;
        if (balaoTop < windMetade) {
          balao.classList.add('ativo');
        }
      });
    }

    window.addEventListener('scroll', animaScroll);
  }
}

InitAnimaScrollHome();

// ANIMAÇÃO PARA SEÇÃO INSTRUÇÃO

function animaScrollInstrucao() {
  const instrucoes = document.querySelectorAll('.anima-scroll');

  if (instrucoes.length) {
    const alturaAnimada = window.innerHeight * 1;

    function animaInstrucao() {
      instrucoes.forEach((instrucao) => {
        const instrucaoTop = instrucao.getBoundingClientRect().top;
        if (instrucaoTop < alturaAnimada) {
          instrucao.classList.add('ativo');
        }
      });
    }
    window.addEventListener('scroll', animaInstrucao);
  }
}

animaScrollInstrucao();

// ANIMAÇÃO PARA IMAGEM MEGAFONE INSTRUÇÃO

function animaImgInstrucao() {
  const img = document.querySelectorAll('.img-instrucao');

  if (img.length) {
    const altAnimada = window.innerHeight * 1.1;

    function animaImg() {
      img.forEach((imagem) => {
        const imgTop = imagem.getBoundingClientRect().top;
        if (imgTop < altAnimada) {
          imagem.classList.add('ativo');
        }
      });
    }
    window.addEventListener('scroll', animaImg);
  }
}
animaImgInstrucao();

// FUNÇÃO PARA MOSTRAR NOME DO ARQ. SELECIONADO
function mostraTxtArq() {
  const procurar = document.querySelector('#csv_file');
  if (procurar) {
    procurar.addEventListener('change', function () {
      document.querySelector('.txt').textContent = this.files[0].name;
    });
  }
}

mostraTxtArq();

// FUNÇÃO PARA DESABILITAR BOTÃO APÓS O CLIQUE

function btnDesabilitado() {
  var submitButton = document.getElementById('disparar'); // Seleciona o botão de envio

  if (submitButton) {
    document
      .getElementById('formulario')
      .addEventListener('submit', function (event) {
        event.preventDefault();

        // Desabilita o botão
        submitButton.disabled = true;
        submitButton.style.backgroundColor = '#ccc';
        submitButton.style.color = '#000000';
        submitButton.textContent = 'ENVIANDO! O bot está iniciando...';
        submitButton.style.cursor = 'progress';
        submitButton.classList.add('disabled');
        setTimeout(function () {
          // Após o envio ser concluído, atualize o texto do botão
          submitButton.textContent = 'Disparar mensagens';
        }, 90000);
      });
  }
}

btnDesabilitado();

// function btnDesabilitado() {
//   var submitButton = document.getElementById('disparar'); // Seleciona o botão de envio

//   if (submitButton) {
//     document
//       .getElementById('formulario')
//       .addEventListener('submit', function (event) {
//         event.preventDefault();

//         // Desabilita o botão
//         submitButton.disabled = true;
//         submitButton.style.backgroundColor = '#ccc'; // Altera a cor de fundo para cinza
//         submitButton.style.color = '#000000';
//         submitButton.textContent = 'ENVIANDO! O bot está iniciando...'; // Altera o texto para "Enviando..."
//         submitButton.style.cursor = 'progress'; // Altera o cursor para "carregando"
//         submitButton.classList.add('disabled'); // Adiciona a classe "disabled" para remover o efeito de hover
//       });
//   }
// }

btnDesabilitado();

// FUNÇÃO PARA DEIXAR O MENU ATIVO

function menuAtivo() {
  const itemMenu = document.querySelectorAll('.menu-item ul li a');
  const paginaAtual = window.location.pathname; // Obtém o caminho da URL da página atual

  function ativaClasse() {
    itemMenu.forEach((item) => {
      item.classList.remove('ativo'); // Remove a classe 'ativo' de todos os elementos do menu
    });
    this.classList.add('ativo'); // Adiciona a classe 'ativo' apenas ao elemento clicado
  }

  // Itera sobre os itens do menu e verifica se o atributo 'href' corresponde à página atual
  itemMenu.forEach((item) => {
    if (item.getAttribute('href') === paginaAtual) {
      item.classList.add('ativo'); // Adiciona a classe 'ativo' ao elemento correspondente à página atual
    }
    item.addEventListener('click', ativaClasse);
  });
}
menuAtivo();

function scrollSuave() {
  const linkInterno = document.querySelectorAll('.js-menu a[href^="#"]');

  function scrollToSection(event) {
    event.preventDefault();
    const href = event.currentTarget.getAttribute('href');
    const section = document.querySelector(href);
    const topo = section.offsetTop - 80;

    window.scrollTo({
      top: topo,
      behavior: 'smooth',
    });
  }

  linkInterno.forEach((link) => {
    link.addEventListener('click', scrollToSection);
  });
}

scrollSuave();
