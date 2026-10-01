// Formulário de calibração de indicadores: 1 toque por item, resposta enviada pelo WhatsApp.
// Nada é enviado ao servidor; o rascunho fica só no navegador de quem responde.
(function () {
  var cfgEl = document.getElementById('cfg-indicadores');
  if (!cfgEl) return;
  var C = JSON.parse(cfgEl.textContent);
  var ALL = [].concat.apply([], C.blocos.map(function (b) { return b.itens; }));
  var TOTAL = ALL.length;
  var LBL = { e: 'Essencial', u: 'Útil', n: 'Não uso' };
  var S = { v: {} };
  try { var r = localStorage.getItem(C.chave); if (r) S = Object.assign(S, JSON.parse(r)); } catch (e) {}
  function salvar() { try { localStorage.setItem(C.chave, JSON.stringify(S)); } catch (e) {} }
  function esc(t) { var d = document.createElement('div'); d.textContent = t; return d.innerHTML; }

  var host = document.getElementById('blocos');
  C.blocos.forEach(function (b) {
    var sec = document.createElement('section'); sec.className = 'bloco';
    var h = document.createElement('h2'); h.textContent = b.nome; sec.appendChild(h);
    b.itens.forEach(function (it) {
      var row = document.createElement('div'); row.className = 'item';
      if (S.v[it.id]) row.dataset.v = S.v[it.id];
      row.innerHTML = '<div class="txt"><span class="nome">' + esc(it.n) + '</span><span class="desc">' + esc(it.d) + '</span></div>' +
        '<span class="seg" role="group" aria-label="' + esc(it.n) + '">' + ['e', 'u', 'n'].map(function (v) {
          return '<button type="button" data-v="' + v + '" aria-pressed="' + (S.v[it.id] === v) + '">' + LBL[v] + '</button>';
        }).join('') + '</span>';
      row.querySelectorAll('button').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var v = S.v[it.id] === btn.dataset.v ? undefined : btn.dataset.v;
          if (v) { S.v[it.id] = v; row.dataset.v = v; } else { delete S.v[it.id]; delete row.dataset.v; }
          row.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', String(x.dataset.v === v)); });
          salvar(); atualizar();
        });
      });
      sec.appendChild(row);
    });
    host.appendChild(sec);
  });

  var tbox = document.getElementById('p-teste');
  ['Sim', 'Talvez', 'Agora não'].forEach(function (o, i) {
    var l = document.createElement('label'); l.className = 'chip';
    var inp = document.createElement('input'); inp.type = 'radio'; inp.name = 'teste'; inp.value = o;
    if (S.teste === o) inp.checked = true;
    inp.addEventListener('change', function () { S.teste = o; salvar(); atualizar(); });
    l.appendChild(inp); l.appendChild(document.createTextNode(o)); tbox.appendChild(l);
  });
  ['p-nome', 'p-emp', 'p-falta'].forEach(function (id) {
    var el = document.getElementById(id);
    if (S[id]) el.value = S[id];
    el.addEventListener('input', function () { S[id] = el.value; salvar(); atualizar(); });
  });
  function val(id) { return (S[id] || '').trim(); }

  function texto() {
    var L = ['*' + C.titulo + '*'];
    L.push([val('p-nome'), val('p-emp')].filter(Boolean).join(' · ') || '(sem identificação)');
    ['e', 'u', 'n'].forEach(function (v) {
      var its = ALL.filter(function (i) { return S.v[i.id] === v; });
      if (its.length) { L.push('', '*' + LBL[v].toUpperCase() + '*'); its.forEach(function (i) { L.push('• ' + i.n); }); }
    });
    if (val('p-falta')) L.push('', '*Faltou:* ' + val('p-falta'));
    if (S.teste) L.push('', '*Teste 30 dias:* ' + S.teste);
    return L.join('\n');
  }
  function atualizar() {
    var n = Object.keys(S.v).length;
    document.getElementById('progtxt').textContent = n + ' de ' + TOTAL + ' marcados';
    document.getElementById('preench').style.width = (n / TOTAL * 100) + '%';
    var wa = document.getElementById('wa-envio');
    wa.href = 'https://wa.me/' + C.whatsapp + '?text=' + encodeURIComponent(texto());
    wa.setAttribute('aria-disabled', String(n === 0));
  }
  document.getElementById('copiar').addEventListener('click', function (e) {
    var b = e.currentTarget;
    function fim(t) { b.textContent = t; setTimeout(function () { b.textContent = 'copiar respostas'; }, 2600); }
    if (navigator.clipboard) navigator.clipboard.writeText(texto()).then(function () { fim('respostas copiadas'); }, function () { fim('não deu para copiar, use o botão Enviar'); });
    else fim('não deu para copiar, use o botão Enviar');
  });
  atualizar();
})();
