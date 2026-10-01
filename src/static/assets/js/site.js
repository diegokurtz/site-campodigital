// Campo Digital: comportamento mínimo (menu móvel, abas da demonstração, revelação ao rolar)
(function () {
  document.documentElement.classList.remove('sem-js');

  // menu móvel
  var botao = document.querySelector('.menu-botao');
  var menu = document.getElementById('menu');
  if (botao && menu) {
    botao.addEventListener('click', function () {
      var aberto = menu.classList.toggle('aberto');
      botao.setAttribute('aria-expanded', aberto ? 'true' : 'false');
      botao.textContent = aberto ? 'Fechar' : 'Menu';
    });
  }

  // abas da demonstração (padrão WAI-ARIA tabs)
  document.querySelectorAll('[data-abas]').forEach(function (grupo) {
    var abas = Array.prototype.slice.call(grupo.querySelectorAll('[role="tab"]'));
    function ativar(aba, foco) {
      abas.forEach(function (a) {
        var sel = a === aba;
        a.setAttribute('aria-selected', sel ? 'true' : 'false');
        a.tabIndex = sel ? 0 : -1;
        var p = document.getElementById(a.getAttribute('aria-controls'));
        if (p) p.hidden = !sel;
      });
      if (foco) aba.focus();
    }
    abas.forEach(function (aba, i) {
      aba.addEventListener('click', function () { ativar(aba); });
      aba.addEventListener('keydown', function (e) {
        var k = e.key, n = null;
        if (k === 'ArrowDown' || k === 'ArrowRight') n = abas[(i + 1) % abas.length];
        if (k === 'ArrowUp' || k === 'ArrowLeft') n = abas[(i - 1 + abas.length) % abas.length];
        if (n) { e.preventDefault(); ativar(n, true); }
      });
    });
  });

  // revelação suave
  var els = document.querySelectorAll('.revela');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('visivel'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('visivel'); });
  }
})();
